###
# Copyright 2018 Den_S/@DennisRBLX
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###
#
# Rbx Animations Blender Addon
# Written by Den_S/@DennisRBLX
# Refer to https://devforum.roblox.com/t/blender-rig-exporter-animation-importer/34729 for usage instructions
#
# For your information:
#   Armature is assumed to have the identity matrix(!!!)
#   When creating a rig, bones are first created in a way they were in the original rig data,
#     the resulting matrices are stored as base matrices.
#   Then, bone tails are moved to be in a more intuitive position (helps IK etc too)
#   This transformation is thus undone when exporting
#   Blender also uses a Z-up/-Y-forward coord system, so this results in more transformations
#   Transform <=> Original **world space** CFrame, should match the associate mesh base matrix, Transform1 <=> C1
#   The meshes are imported in a certain order. Mesh names are restored using attached metadata.
#   Rig data is also encoded in this metdata.
#
# Communication:
#   To blender: A bunch of extra meshes whose names encode metadata (they are numbered, the contents are together encoded in base32)
#   From blender: Base64-encoded string (after compression)
#

import bpy, math, re, json, bpy_extras
from itertools import chain
from mathutils import Vector, Matrix
import zlib
import base64
from bpy_extras.io_utils import ImportHelper
from bpy.props import *

transform_to_blender = bpy_extras.io_utils.axis_conversion(from_forward='Z', from_up='Y', to_forward='-Y', to_up='Z').to_4x4() # transformation matrix from Y-up to Z-up
identity_cf = [0,0,0,1,0,0,0,1,0,0,0,1] # identity CF components matrix
cf_round = False # round cframes before exporting? (reduce size)
cf_round_fac = 4 # round to how many decimals?

# y-up cf -> y-up mat
def cf_to_mat(cf):
    mat = Matrix.Translation((cf[0], cf[1], cf[2]))
    mat[0][0:3] = (cf[3], cf[4], cf[5])
    mat[1][0:3] = (cf[6], cf[7], cf[8])
    mat[2][0:3] = (cf[9], cf[10], cf[11])
    return mat

# y-up mat -> y-up cf
def mat_to_cf(mat):
    r_mat = [mat[0][3], mat[1][3], mat[2][3],
        mat[0][0], mat[0][1], mat[0][2],
        mat[1][0], mat[1][1], mat[1][2],
        mat[2][0], mat[2][1], mat[2][2]
    ]
    return r_mat

# links the passed object to the bone with the transformation equal to the current(!) transformation between the bone and object
def link_object_to_bone_rigid(obj, ao, bone):
    # remove existing
    for constraint in [c for c in obj.constraints if c.type == 'CHILD_OF']:
        obj.constraints.remove(constraint)

    # create new
    constraint = obj.constraints.new(type = 'CHILD_OF')
    constraint.target = ao
    constraint.subtarget = bone.name
    constraint.inverse_matrix = (ao.matrix_world @ bone.matrix).inverted()

# serializes the current bone state to a dict
def serialize_animation_state(ao):
    state = {}
    for bone in ao.pose.bones:
        if 'is_transformable' in bone.bone:
            # original matrices, straight from the import cfs
            # this is always the true baseline
            orig_mat = Matrix(bone.bone['transform'])
            orig_mat_tr1 = Matrix(bone.bone['transform1'])
            parent_orig_mat = Matrix(bone.parent.bone['transform'])
            parent_orig_mat_tr1 = Matrix(bone.parent.bone['transform1'])

            # get the bone neutral transform
            extr_transform = Matrix(bone.bone['nicetransform']).inverted()
            parent_extr_transform = Matrix(bone.parent.bone['nicetransform']).inverted()
            
            # z-up -> y-up transform matrix
            back_trans = transform_to_blender.inverted()

            # get the real bone transform
            cur_obj_transform = back_trans @ (bone.matrix @ extr_transform)
            parent_obj_transform = back_trans @ (bone.parent.matrix @ parent_extr_transform)
            
            # compute neutrals after applying C1/transform1
            orig_base_mat = back_trans @ (orig_mat @ orig_mat_tr1)
            parent_orig_base_mat = back_trans @ (parent_orig_mat @ parent_orig_mat_tr1)
            
            # compute y-up bone transform (transformation between C0 and C1)
            orig_transform = parent_orig_base_mat.inverted() @ orig_base_mat
            cur_transform = parent_obj_transform.inverted() @ cur_obj_transform
            bone_transform = orig_transform.inverted() @ cur_transform

            statel = mat_to_cf(bone_transform)
            if cf_round:
                statel = list(map(lambda x: round(x, cf_round_fac), statel)) # compresses result
            
            # flatten, compresses the resulting json too
            for i in range(len(statel)):
                if int(statel[i]) ==  statel[i]:
                    statel[i] = int(statel[i])
            
            # only store if not identity, compresses the resulting json
            if statel != identity_cf:
                state[bone.name] = statel
    
    return state

# removes all IK stuff from a bone
def remove_ik_config(ao, tail_bone):
    to_clear = []
    for constraint in [c for c in tail_bone.constraints if c.type == 'IK']:
        if constraint.target and constraint.subtarget:
            to_clear.append((constraint.target, constraint.subtarget))
        if constraint.pole_target and constraint.pole_subtarget:
            to_clear.append((constraint.pole_target, constraint.pole_subtarget))
            
        tail_bone.constraints.remove(constraint)
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    for util_bone in to_clear:
        util_bone[0].data.edit_bones.remove(util_bone[0].data.edit_bones[util_bone[1]])
    
    bpy.ops.object.mode_set(mode='POSE')

# created IK bones and constraints for a given chain
def create_ik_config(ao, tail_bone, chain_count, create_pose_bone, lock_tail):
    lock_tail = False # not implemented
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    amt = ao.data
    ik_target_bone = tail_bone if not lock_tail else tail_bone.parent
    
    ik_target_bone_name = ik_target_bone.name
    ik_name = "{}-IKTarget".format(ik_target_bone_name)
    ik_name_pole = "{}-IKPole".format(ik_target_bone_name)
    
    ik_bone = amt.edit_bones.new(ik_name)
    ik_bone.head = ik_target_bone.tail
    ik_bone.tail = (Matrix.Translation(ik_bone.head) @ ik_target_bone.matrix.to_3x3().to_4x4()) @ Vector((0, 0, -.5))
    ik_bone.bbone_x *= 1.5
    ik_bone.bbone_z *= 1.5
    
    ik_pole = None
    if create_pose_bone:
        pos_low = tail_bone.tail
        pos_high = tail_bone.parent_recursive[chain_count-2].head
        pos_avg = (pos_low + pos_high) * .5
        dist = (pos_low - pos_high).length
        
        basal_bone = tail_bone
        for i in range(1, chain_count):
            if basal_bone.parent:
                basal_bone = basal_bone.parent
        
        basal_mat = basal_bone.bone.matrix_local

        ik_pole = amt.edit_bones.new(ik_name_pole)
        ik_pole.head = basal_mat @ Vector((0, 0, dist * -.25))
        ik_pole.tail = basal_mat @ Vector((0, 0, dist * -.25 - .3))
        ik_pole.bbone_x *= .5
        ik_pole.bbone_z *= .5

    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = ao.pose.bones[ik_target_bone_name]
    constraint = pose_bone.constraints.new(type = 'IK')
    constraint.target = ao
    constraint.subtarget = ik_name
    if create_pose_bone:
        constraint.pole_target = ao
        constraint.pole_subtarget = ik_name_pole
        constraint.pole_angle = math.pi * -.5
    constraint.chain_count = chain_count

# loads a (child) rig bone
def load_rigbone(ao, rigging_type, rigsubdef, parent_bone):
    amt = ao.data
    bone = amt.edit_bones.new(rigsubdef['jname'])
    
    mat = cf_to_mat(rigsubdef['transform'])
    bone["transform"] = mat
    bone_dir = (transform_to_blender @ mat).to_3x3().to_4x4() @ Vector((0, 0, 1))
    
    if 'jointtransform0' not in rigsubdef:
        # Rig root
        bone.head = (transform_to_blender @ mat).to_translation()
        bone.tail = (transform_to_blender @ mat) @ Vector((0, .01, 0))
        bone["transform0"] = Matrix()
        bone["transform1"] = Matrix()
        bone['nicetransform'] = Matrix()
        bone.align_roll(bone_dir)
        bone.hide_select = True
        pre_mat = bone.matrix
        o_trans = transform_to_blender @ mat
    else:
        mat0 = cf_to_mat(rigsubdef['jointtransform0'])
        mat1 = cf_to_mat(rigsubdef['jointtransform1'])
        bone["transform0"] = mat0
        bone["transform1"] = mat1
        bone["is_transformable"] = True
        
        bone.parent = parent_bone
        o_trans = transform_to_blender @ (mat @ mat1)
        bone.head = o_trans.to_translation()
        real_tail = o_trans @ Vector((0, .25, 0))
        
        neutral_pos = (transform_to_blender @ mat).to_translation()
        bone.tail = real_tail
        bone.align_roll(bone_dir)
        
        # store neutral matrix
        pre_mat = bone.matrix
        
        if rigging_type != 'RAW': # If so, apply some transform
            if len(rigsubdef['children']) == 1:
                nextmat = cf_to_mat(rigsubdef['children'][0]['transform'])
                nextmat1 = cf_to_mat(rigsubdef['children'][0]['jointtransform1'])
                next_joint_pos = (transform_to_blender @ (nextmat @ nextmat1)).to_translation()
                    
                if rigging_type == 'CONNECT': # Instantly connect
                    bone.tail = next_joint_pos
                else:
                    axis = 'y'
                    if rigging_type == 'LOCAL_AXIS_EXTEND': # Allow non-Y too
                        invtrf = pre_mat.inverted() * next_joint_pos
                        bestdist = abs(invtrf.y)
                        for paxis in ['x', 'z']:
                            dist = abs(getattr(invtrf, paxis))
                            if dist > bestdist:
                                bestdist = dist
                                axis = paxis
                    
                    next_connect_to_parent = True
                    
                    ppd_nr_dir = real_tail - bone.head
                    ppd_nr_dir.normalize()
                    proj = ppd_nr_dir.dot(next_joint_pos - bone.head)
                    vis_world_root = ppd_nr_dir * proj
                    bone.tail = bone.head + vis_world_root
                
            else:
                bone.tail = bone.head + (bone.head - neutral_pos) * -2
        
            if (bone.tail - bone.head).length < .01:
                # just reset, no "nice" config can be found
                bone.tail = real_tail
                bone.align_roll(bone_dir)
    
    # fix roll
    bone.align_roll(bone_dir)
    
    post_mat = bone.matrix
    
    # this value stores the transform between the "proper" matrix and the "nice" matrix where bones are oriented in a more friendly way
    bone['nicetransform'] = o_trans.inverted() @ post_mat

    # link objects to bone
    for aux in rigsubdef['aux']:
        if aux and aux in bpy.data.objects:
            obj = bpy.data.objects[aux]
            link_object_to_bone_rigid(obj, ao, bone)
    
    # handle child bones
    for child in rigsubdef['children']:
        load_rigbone(ao, rigging_type, child, bone)

# renames parts to whatever the metadata defines, mostly just for user-friendlyness (not required)
def autoname_parts(partnames, basename):
    indexmatcher = re.compile(basename + '(\d+)1(\.\d+)?', re.IGNORECASE)
    for object in bpy.data.objects:
        match = indexmatcher.match(object.name.lower())
        if match:
            index = int(match.group(1))
            object.name = partnames[index - 1]

# removes existing rig if it exists, then builds a new one using the stored metadata
def create_rig(rigging_type):
    bpy.ops.object.mode_set(mode='OBJECT')
    if '__Rig' in bpy.data.objects:
        bpy.data.objects['__Rig'].select_set(True)
        bpy.ops.object.delete()
        
    meta_loaded = json.loads(bpy.data.objects['__RigMeta']['RigMeta'])
    
    bpy.ops.object.add(type='ARMATURE', enter_editmode=True, location=(0,0,0))
    ao = bpy.context.object
    ao.show_in_front = True
    ao.name = '__Rig'
    amt = ao.data
    amt.name = '__RigArm'
    amt.show_axes = True
    amt.show_names = True
    
    bpy.ops.object.mode_set(mode='EDIT')
    load_rigbone(ao, rigging_type, meta_loaded['rig'], None)
    
    bpy.ops.object.mode_set(mode='OBJECT')


# export the entire animation to the clipboard (serialized), returns animation time
def serialize():
    ao = bpy.data.objects['__Rig']
    ctx = bpy.context
    bake_jump = ctx.scene.frame_step
    
    collected = []
    frames = ctx.scene.frame_end+1 - ctx.scene.frame_start
    cur_frame = ctx.scene.frame_current
    for i in range(ctx.scene.frame_start, ctx.scene.frame_end+1, bake_jump):
        ctx.scene.frame_set(i)
        bpy.context.evaluated_depsgraph_get().update()
    
        state = serialize_animation_state(ao)
        collected.append({'t': (i - ctx.scene.frame_start) / ctx.scene.render.fps, 'kf': state})
    
    ctx.scene.frame_set(cur_frame)
    
    result = {
        't': (frames-1) / ctx.scene.render.fps,
        'kfs': collected
    }
    
    return result

def copy_anim_state_bone(target, source, bone):
    # get transform mat of the bone in the source ao
    bpy.context.view_layer.objects.active = source
    t_mat = source.pose.bones[bone.name].matrix

    bpy.context.view_layer.objects.active = target
        
    # root bone transform is ignored, this is carried to child bones (keeps HRP static)
    if bone.parent:
        # apply transform w.r.t. the current parent bone transform
        r_mat = bone.bone.matrix_local
        p_mat = bone.parent.matrix
        p_r_mat = bone.parent.bone.matrix_local
        bone.matrix_basis = (p_r_mat.inverted() @ r_mat).inverted() @ (p_mat.inverted() @ t_mat)

    # update properties (hacky :p)
    bpy.ops.anim.keyframe_insert()
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)

    # now apply on children (which use the parents transform)
    for ch in bone.children:
        copy_anim_state_bone(target, source, ch)
    
def copy_anim_state(target, source):
    # to pose mode
    bpy.context.view_layer.objects.active = source
    bpy.ops.object.mode_set(mode='POSE')

    bpy.context.view_layer.objects.active = target
    bpy.ops.object.mode_set(mode='POSE')

    root = target.pose.bones['HumanoidRootPart']
 
    for i in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end+1):
        bpy.context.scene.frame_set(i)
        copy_anim_state_bone(target, source, root)
        bpy.ops.anim.keyframe_insert()

def prepare_for_kf_map():
    # clear anim data from target rig
    bpy.data.objects['__Rig'].animation_data_clear()
    
    # select all pose bones in the target rig (simply generate kfs for everything)
    bpy.context.view_layer.objects.active = bpy.data.objects['__Rig']
    bpy.ops.object.mode_set(mode='POSE')
    for bone in bpy.data.objects['__Rig'].pose.bones:
        bone.bone.select = not not bone.parent

def get_mapping_error_bones(target, source):
    return [bone.name for bone in target.data.bones if bone.name not in [bone2.name for bone2 in source.data.bones]]
    
# apply ao transforms to the root PoseBone
# + clear ao animation tracks (root only, not Pose anim data) + reset ao transform to identity
def apply_ao_transform(ao):
    bpy.context.view_layer.objects.active = ao
    bpy.ops.object.mode_set(mode='POSE')
    
    # select only root bones
    for bone in ao.pose.bones:
        bone.bone.select = not bone.parent
    
    for root in [bone for bone in ao.pose.bones if not bone.parent]:
        # collect initial root matrices (if they do not exist yet, this will prevent interpolation from keyframes that are being set in the next loop)
        root_matrix_at = {}
        for i in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end+1):
            bpy.context.scene.frame_set(i)
            root_matrix_at[i] = root.matrix.copy()
        
        # apply world space transform to root bone
        for i in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end+1):
            bpy.context.scene.frame_set(i)
            root.matrix = ao.matrix_world @ root_matrix_at[i]
            bpy.ops.anim.keyframe_insert()

    # clear non-pose fcurves
    fcurves = ao.animation_data.action.fcurves
    for c in [c for c in fcurves if not c.data_path.startswith('pose')]:
        fcurves.remove(c)
        
    # reset ao transform
    ao.matrix_basis = Matrix.Identity(4)
    bpy.context.evaluated_depsgraph_get().update()

## UI/OPERATOR STUFF ##

class OBJECT_OT_ImportModel(bpy.types.Operator, ImportHelper):
    bl_label = "Import rig data (.obj)"
    bl_idname = "object.rbxanims_importmodel"
    bl_description = "Import rig data (.obj)"

    filename_ext = ".obj"
    filter_glob: bpy.props.StringProperty(default="*.obj", options={'HIDDEN'})
    filepath: bpy.props.StringProperty(name="File Path", maxlen=1024, default="")
 
    def execute(self, context):
        # clear objects first
        for obj in bpy.data.objects:
            obj.select_set(obj.type == 'MESH' or obj.type == 'ARMATURE' or obj.name.startswith('__RigMeta'))
        bpy.ops.object.delete()
        
        bpy.ops.import_scene.obj(filepath=self.properties.filepath, use_split_groups=True)
        
        # Extract meta...
        encodedmeta = ''
        partial = {}
        for obj in bpy.data.objects:
            match = re.search(r'^Meta(\d+)q1(.*?)q1\d*(\.\d+)?$', obj.name)
            if match:
                partial[int(match.group(1))] = match.group(2)
            
            obj.select_set(not not match)
        bpy.ops.object.delete() # delete meta objects
        
        for i in range(1, len(partial)+1):
            encodedmeta += partial[i]
        encodedmeta = encodedmeta.replace('0', '=')
        meta = base64.b32decode(encodedmeta, True).decode('utf-8')
        
        # store meta in an empty
        bpy.ops.object.add(type='EMPTY', location=(0,0,0))
        ob = bpy.context.object
        ob.name = '__RigMeta'
        ob['RigMeta'] = meta
        
        meta_loaded = json.loads(meta)
        autoname_parts(meta_loaded['parts'], meta_loaded['rigName'])
        
        return {'FINISHED'}    
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

class OBJECT_OT_GenRig(bpy.types.Operator):
    bl_label = "Generate rig"
    bl_idname = "object.rbxanims_genrig"
    bl_description = "Generate rig"

    pr_rigging_type: bpy.props.EnumProperty(items=[
        ('RAW', 'Nodes only', ''), 
        ('LOCAL_AXIS_EXTEND', 'Local axis aligned bones', ''),
        ('LOCAL_YAXIS_EXTEND', 'Local Y-axis aligned bones', ''),
        ('CONNECT', 'Connect', '')
    ], name="Rigging type");
 
    @classmethod
    def poll(cls, context):
        meta_obj = bpy.data.objects.get('__RigMeta')
        return meta_obj and 'RigMeta' in meta_obj
 
    def execute(self, context):
        create_rig(self.pr_rigging_type)
        self.report({'INFO'}, "Rig rebuilt.")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.pr_rigging_type = 'LOCAL_YAXIS_EXTEND'
        
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class OBJECT_OT_GenIK(bpy.types.Operator):
    bl_label = "Generate IK"
    bl_idname = "object.rbxanims_genik"
    bl_description = "Generate IK"
    
    pr_chain_count: bpy.props.IntProperty(name = "Chain count (0 = to root)", min=0)
    pr_create_pose_bone: bpy.props.BoolProperty(name = "Create pose bone")
    pr_lock_tail_bone: bpy.props.BoolProperty(name = "Lock final bone orientation")
    
    @classmethod
    def poll(cls, context):
        premise = context.active_object and context.active_object.mode == 'POSE'
        premise = premise and context.active_object and context.active_object.type == 'ARMATURE'
        return context.active_object and context.active_object.mode == 'POSE' and len([x for x in context.active_object.pose.bones if x.bone.select]) > 0

    def execute(self, context):
        
        to_apply = [b for b in context.active_object.pose.bones if b.bone.select]
        
        for bone in to_apply:
            create_ik_config(context.active_object, bone, self.pr_chain_count, self.pr_create_pose_bone, self.pr_lock_tail_bone)

        return {'FINISHED'}

    def invoke(self, context, event):
        to_apply = [b for b in context.active_object.pose.bones if b.bone.select]
        if len(to_apply) == 0:
            return {'FINISHED'}
        
        rec_chain_len = 1
        no_loop_mech = set()
        itr = to_apply[0].bone
        while itr and itr.parent and len(itr.parent.children) == 1 and itr not in no_loop_mech:
            rec_chain_len += 1
            no_loop_mech.add(itr)
            itr = itr.parent
        
        self.pr_chain_count = rec_chain_len
        self.pr_create_pose_bone = False
        self.pr_lock_tail_bone = False
        
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
class OBJECT_OT_RemoveIK(bpy.types.Operator):
    bl_label = "Remove IK"
    bl_idname = "object.rbxanims_removeik"
    bl_description = "Remove IK"

    @classmethod
    def poll(cls, context):
        premise = context.active_object and context.active_object.mode == 'POSE'
        premise = premise and context.active_object
        return context.active_object and context.active_object.mode == 'POSE' and len([x for x in context.active_object.pose.bones if x.bone.select]) > 0

    def execute(self, context):
        to_apply = [b for b in context.active_object.pose.bones if b.bone.select]
        
        for bone in to_apply:
            remove_ik_config(context.active_object, bone)
            
        return {'FINISHED'}

class OBJECT_OT_ImportFbxAnimation(bpy.types.Operator, ImportHelper):
    bl_label = "Import animation data (.fbx)"
    bl_idname = "object.rbxanims_importfbxanimation"
    bl_description = "Import animation data (.fbx) --- FBX file should contain an armature, which will be mapped onto the generated rig by bone names."

    filename_ext = ".fbx"
    filter_glob: bpy.props.StringProperty(default="*.fbx", options={'HIDDEN'})
    filepath: bpy.props.StringProperty(name="File Path", maxlen=1024, default="")
    
    @classmethod
    def poll(cls, context):
        return bpy.data.objects.get('__Rig')
 
    def execute(self, context):
        # check active keying set
        if not bpy.context.scene.keying_sets.active:
            self.report({'ERROR'}, 'There is no active keying set, this is required.')
            return {'FINISHED'}
        
        # import and keep track of what is imported
        objnames_before_import = [x.name for x in bpy.data.objects]
        bpy.ops.import_scene.fbx(filepath=self.properties.filepath)
        objnames_imported = [x.name for x in bpy.data.objects if x.name not in objnames_before_import]
        
        def clear_imported():
            bpy.ops.object.mode_set(mode='OBJECT')
            for obj in bpy.data.objects:
                obj.select_set(obj.name in objnames_imported)
            bpy.ops.object.delete()
        
        # check that there's only 1 armature
        armatures_imported = [x for x in bpy.data.objects if x.type == 'ARMATURE' and x.name in objnames_imported]
        if len(armatures_imported) != 1:
            self.report({'ERROR'}, 'Imported file contains {:d} armatures, expected 1.'.format(len(armatures_imported)))
            clear_imported()
            return {'FINISHED'}
        
        ao_imp = armatures_imported[0]
        
        err_mappings = get_mapping_error_bones(bpy.data.objects['__Rig'], ao_imp)
        if len(err_mappings) > 0:
            self.report({'ERROR'}, 'Cannot map rig, the following bones are missing from the source rig: {}.'.format(', '.join(err_mappings)))
            clear_imported()
            return {'FINISHED'}
        
        print(dir(bpy.context.scene))
        bpy.context.view_layer.objects.active = ao_imp
        
        # check that the ao contains anim data
        if not ao_imp.animation_data or not ao_imp.animation_data.action or not ao_imp.animation_data.action.fcurves:
            self.report({'ERROR'}, 'Imported armature contains no animation data.')
            clear_imported()
            return {'FINISHED'}
        
        # get keyframes + boundary timestamps
        fcurves = ao_imp.animation_data.action.fcurves
        kp_frames = []
        for key in fcurves:
            kp_frames += [kp.co.x for kp in key.keyframe_points]
        if len(kp_frames) <= 0:
            self.report({'ERROR'}, 'Imported armature contains no keyframes.')
            clear_imported()
            return {'FINISHED'}
        
        # set frame range
        bpy.context.scene.frame_start = math.floor(min(kp_frames))
        bpy.context.scene.frame_end = math.ceil(max(kp_frames))
        
        # for the imported rig, apply ao transforms
        apply_ao_transform(ao_imp)
        
        prepare_for_kf_map()
        
        # actually copy state
        copy_anim_state(bpy.data.objects['__Rig'], ao_imp)
        
        clear_imported()
        return {'FINISHED'}    
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}    

class OBJECT_OT_ApplyTransform(bpy.types.Operator):
    bl_label = "Apply armature object transform to the root bone for each keyframe"
    bl_idname = "object.rbxanims_applytransform"
    bl_description = "Apply armature object transform to the root bone for each keyframe -- Must set a proper frame range first!"

    @classmethod
    def poll(cls, context):
        grig = bpy.data.objects.get('__Rig')
        return grig and bpy.context.active_object and bpy.context.active_object.animation_data
 
    def execute(self, context):
        if not bpy.context.scene.keying_sets.active:
            self.report({'ERROR'}, 'There is no active keying set, this is required.')
            return {'FINISHED'}
        
        apply_ao_transform(bpy.context.view_layer.objects.active)

        return {'FINISHED'} 

class OBJECT_OT_MapKeyframes(bpy.types.Operator):
    bl_label = "Map keyframes by bone name"
    bl_idname = "object.rbxanims_mapkeyframes"
    bl_description = "Map keyframes by bone name --- From a selected armature, maps data (using a new keyframe per frame) onto the generated rig by name. Set frame ranges first!"

    @classmethod
    def poll(cls, context):
        grig = bpy.data.objects.get('__Rig')
        return grig and bpy.context.active_object and bpy.context.active_object != grig
 
    def execute(self, context):
        if not bpy.context.scene.keying_sets.active:
            self.report({'ERROR'}, 'There is no active keying set, this is required.')
            return {'FINISHED'}
        
        ao_imp = bpy.context.scene.objects.active
        
        err_mappings = get_mapping_error_bones(bpy.data.objects['__Rig'], ao_imp)
        if len(err_mappings) > 0:
            self.report({'ERROR'}, 'Cannot map rig, the following bones are missing from the source rig: {}.'.format(', '.join(err_mappings)))
            return {'FINISHED'}
        
        prepare_for_kf_map()
        
        copy_anim_state(bpy.data.objects['__Rig'], ao_imp)

        return {'FINISHED'} 

class OBJECT_OT_Bake(bpy.types.Operator):
    bl_label = "Bake"
    bl_idname = "object.rbxanims_bake"
    bl_description = "Bake animation for export"
 
    def execute(self, context):
        serialized = serialize()
        encoded = json.dumps(serialized, separators=(',',':'))
        bpy.context.window_manager.clipboard = (base64.b64encode(zlib.compress(encoded.encode(), 9))).decode('utf-8')
        self.report({'INFO'}, 'Baked animation data exported to the system clipboard ({:d} keyframes, {:.2f} seconds).'.format(len(serialized['kfs']), serialized['t']))
        return {'FINISHED'}

class OBJECT_PT_RbxAnimations(bpy.types.Panel):
    bl_label = "Rbx Animations"
    bl_idname = "OBJECT_PT_RbxAnimations"
    bl_category = "Rbx Animations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return bpy.data.objects.get('__RigMeta')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        obj = context.object

        layout.label(text="Rigging:")
        layout.operator("object.rbxanims_genrig", text="Rebuild rig")
        layout.label(text="Quick inverse kinematics:")
        layout.operator("object.rbxanims_genik", text="Create IK constraints")
        layout.operator("object.rbxanims_removeik", text="Remove IK constraints")
        layout.label(text="Animation import:")
        layout.operator("object.rbxanims_importfbxanimation", text="Import FBX")
        layout.operator("object.rbxanims_mapkeyframes", text="Map keyframes by bone name")
        layout.operator("object.rbxanims_applytransform", text="Apply armature transform")
        layout.label(text="Export:")
        layout.operator("object.rbxanims_bake", text="Export animation", icon='RENDER_ANIMATION')

def file_import_extend(self, context):
    self.layout.operator("object.rbxanims_importmodel", text="[Rbx Animations] Rig import (.obj)")

bl_info = {"name": "Rbx Animations", "category": "Animation", "blender": (2, 80, 0)}

module_classes = [
    OBJECT_OT_ImportModel,
    OBJECT_OT_GenRig,
    OBJECT_OT_GenIK,
    OBJECT_OT_RemoveIK,
    OBJECT_OT_ImportFbxAnimation,
    OBJECT_OT_ApplyTransform,
    OBJECT_OT_MapKeyframes,
    OBJECT_OT_Bake,
    OBJECT_PT_RbxAnimations,
]

register_classes, unregister_classes = bpy.utils.register_classes_factory(module_classes)

def register():
    register_classes()
    bpy.types.TOPBAR_MT_file_import.append(file_import_extend)

def unregister():
    unregister_classes()
    bpy.types.TOPBAR_MT_file_import.remove(file_import_extend)
    
if __name__ == "__main__":
    register()
x1.00