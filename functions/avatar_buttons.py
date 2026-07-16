import bpy
from .. import glob_vars

rbx_anim_error = None
unhide_store = []


# ---------------------------------------------------------------------------
# Action F-Curve helpers (Blender 4.5+).
# Blender 4.4 introduced "slotted" actions (layers -> strips -> channelbags ->
# fcurves) and Blender 5.0 removed the legacy `Action.fcurves` accessor. These
# helpers walk/edit F-Curves the same way whether the action is slotted (all
# supported 4.5+ builds) or, as a fallback, exposes the legacy attribute.
# ---------------------------------------------------------------------------

def _iter_action_fcurves(action):
    """Yield every F-Curve of an action, slotted or legacy."""
    if action is None:
        return
    layers = getattr(action, "layers", None)
    if layers is not None and len(layers) > 0:
        for layer in layers:
            for strip in layer.strips:
                if getattr(strip, "type", None) != 'KEYFRAME':
                    continue
                cbags = getattr(strip, "channelbags", None)
                if not cbags:
                    continue
                for cbag in cbags:
                    for fc in cbag.fcurves:
                        yield fc
        return
    legacy = getattr(action, "fcurves", None)
    if legacy is not None:
        for fc in legacy:
            yield fc


def _remove_action_fcurve(action, fc):
    """Remove a single F-Curve from an action, slotted or legacy."""
    layers = getattr(action, "layers", None)
    if layers is not None and len(layers) > 0:
        for layer in layers:
            for strip in layer.strips:
                cbags = getattr(strip, "channelbags", None)
                if not cbags:
                    continue
                for cbag in cbags:
                    try:
                        cbag.fcurves.remove(fc)
                        return
                    except (RuntimeError, ReferenceError):
                        continue  # belongs to a different channelbag
        return
    legacy = getattr(action, "fcurves", None)
    if legacy is not None:
        try:
            legacy.remove(fc)
        except Exception:
            pass


def _prune_object_level_fcurves(action):
    """Keep only pose-bone and custom-property curves; drop object-level
    transforms (location/rotation/scale of the armature object itself) so the
    FACS animation doesn't move the target rig around."""
    to_remove = [
        fc for fc in _iter_action_fcurves(action)
        if not (fc.data_path.startswith("pose.bones") or fc.data_path.startswith('["'))
    ]
    for fc in to_remove:
        _remove_action_fcurve(action, fc)



######### Avatar Buttons ########### 
class RBX_BUTTON_AVA(bpy.types.Operator):
    bl_label = "RBX_BUTTON_AVA"
    bl_idname = "object.rbx_button_ava"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_ava : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        global rbx_anim_error
        global unhide_store
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_ava = self.rbx_ava

        ava_list = [
                    'Blocky_ava',
                    'Round_male',
                    'Anime_ava'
                    ]

        if rbx_ava == 'avatar':     
            for x in range(len(ava_list)):
                if rbx_prefs.rbx_ava_enum == 'OP' + str(x+1):
                    ava_spwn = ava_list[x]   
            
            colls_before = set(bpy.data.collections)
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename =ava_spwn)
            
            # Clean up .000 suffixes from the newly spawned collection and its objects
            new_colls = set(bpy.data.collections) - colls_before
            for coll in new_colls:
                if '.' in coll.name:
                    coll.name = coll.name.split('.')[0]
                for obj in coll.objects:
                    if '.' in obj.name:
                        obj.name = obj.name.split('.')[0]
            
            bpy.context.view_layer.update()
            
        if rbx_ava == 'clear':
            selected = bpy.context.selected_objects
            active = bpy.context.view_layer.objects.active
            prop_lst = []
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            
            for item in selected:
                bpy.data.objects[item.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[item.name]
                
                props = bpy.data.objects[item.name].items()
       
                for x in props:
                    prop_lst.append(x[0])
                for prop in prop_lst:
                    bpy.ops.wm.properties_remove(data_path='object', property_name=prop)
                prop_lst.clear()
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                
            for item in selected:
                bpy.data.objects[item.name].select_set(True)
                bpy.context.view_layer.objects.active = active
                
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'add_facs':
            selected = bpy.context.selected_objects
            
            if len(selected) != 1:
                self.report({'ERROR'}, "Select exactly 1 Head Mesh")
                return {'FINISHED'}
            
            obj = selected[0]
            if 'Head' not in obj.name:
                self.report({'ERROR'}, "Head Mesh should be selected")
                return {'FINISHED'}
            
            facs_properties = [
                ('Frame0', 'Neutral'),
                ('Frame1', 'Corrugator'),
                ('Frame2', 'ChinRaiserUpperLip'),
                ('Frame3', 'ChinRaiser'),
                ('Frame4', 'EyesLookDown'),
                ('Frame5', 'EyesLookLeft'),
                ('Frame6', 'EyesLookRight'),
                ('Frame7', 'EyesLookUp'),
                ('Frame8', 'Funneler'),
                ('Frame9', 'FlatPucker'),
                ('Frame10', 'JawDrop'),
                ('Frame11', 'JawLeft'),
                ('Frame12', 'JawRight'),
                ('Frame13', 'LowerLipSuck'),
                ('Frame14', 'LipPresser'),
                ('Frame15', 'LipsTogether'),
                ('Frame16', 'MouthLeft'),
                ('Frame17', 'MouthRight'),
                ('Frame18', 'Pucker'),
                ('Frame19', 'UpperLipSuck'),
                ('Frame20', 'LeftBrowLowerer'),
                ('Frame21', 'LeftCheekPuff'),
                ('Frame22', 'LeftCheekRaiser'),
                ('Frame23', 'LeftDimpler'),
                ('Frame24', 'LeftEyeClosed'),
                ('Frame25', 'LeftEyeUpperLidRaiser'),
                ('Frame26', 'LeftInnerBrowRaiser'),
                ('Frame27', 'LeftLipCornerDown'),
                ('Frame28', 'LeftLipCornerPuller'),
                ('Frame29', 'LeftLowerLipDepressor'),
                ('Frame30', 'LeftLipStretcher'),
                ('Frame31', 'LeftNoseWrinkler'),
                ('Frame32', 'LeftOuterBrowRaiser'),
                ('Frame33', 'LeftUpperLipRaiser'),
                ('Frame34', 'RightBrowLowerer'),
                ('Frame35', 'RightCheekPuff'),
                ('Frame36', 'RightCheekRaiser'),
                ('Frame37', 'RightDimpler'),
                ('Frame38', 'RightEyeClosed'),
                ('Frame39', 'RightEyeUpperLidRaiser'),
                ('Frame40', 'RightInnerBrowRaiser'),
                ('Frame41', 'RightLipCornerDown'),
                ('Frame42', 'RightLipCornerPuller'),
                ('Frame43', 'RightLowerLipDepressor'),
                ('Frame44', 'RightLipStretcher'),
                ('Frame45', 'RightNoseWrinkler'),
                ('Frame46', 'RightOuterBrowRaiser'),
                ('Frame47', 'RightUpperLipRaiser'),
                ('Frame100', 'TongueDown'),
                ('Frame101', 'TongueOut'),
                ('Frame102', 'TongueUp'),
                ('Frame110', 'JawDrop_TongueDown'),
                ('Frame111', 'JawDrop_TongueOut'),
                ('Frame112', 'JawDrop_TongueUp'),
                ('Frame113', 'TongueDown_TongueOut'),
                ('Frame114', 'TongueOut_TongueUp'),
                ('Frame130', 'JawDrop_TongueDown_TongueOut'),
                ('Frame131', 'JawDrop_TongueOut_TongueUp'),
                ('Frame200', 'Funneler_JawDrop'),
                ('Frame201', 'Funneler_Pucker'),
                ('Frame202', 'JawDrop_LowerLipSuck'),
                ('Frame203', 'JawDrop_Pucker'),
                ('Frame204', 'LipsTogether_Pucker'),
                ('Frame205', 'EyesLookDown_EyesLookLeft'),
                ('Frame206', 'EyesLookDown_EyesLookRight'),
                ('Frame207', 'EyesLookLeft_EyesLookUp'),
                ('Frame208', 'EyesLookRight_EyesLookUp'),
                ('Frame209', 'LeftCheekRaiser_LeftEyeClosed'),
                ('Frame210', 'LeftEyeClosed_EyesLookDown'),
                ('Frame211', 'LeftEyeClosed_EyesLookLeft'),
                ('Frame212', 'LeftEyeClosed_EyesLookRight'),
                ('Frame213', 'LeftEyeClosed_EyesLookUp'),
                ('Frame214', 'EyesLookUp_LeftEyeUpperLidRaiser'),
                ('Frame215', 'JawDrop_LeftLipCornerPuller'),
                ('Frame216', 'JawDrop_LeftLowerLipDepressor'),
                ('Frame217', 'JawDrop_LeftLipStretcher'),
                ('Frame218', 'JawDrop_LeftUpperLipRaiser'),
                ('Frame219', 'LeftLipCornerPuller_LeftLowerLipDepressor'),
                ('Frame220', 'LeftLipCornerPuller_LeftLipStretcher'),
                ('Frame221', 'LeftLipCornerPuller_Pucker'),
                ('Frame222', 'LeftLipCornerPuller_LeftUpperLipRaiser'),
                ('Frame223', 'LeftLowerLipDepressor_Pucker'),
                ('Frame224', 'LeftLipStretcher_LeftUpperLipRaiser'),
                ('Frame225', 'Pucker_LeftUpperLipRaiser'),
                ('Frame226', 'RightCheekRaiser_RightEyeClosed'),
                ('Frame227', 'RightEyeClosed_EyesLookDown'),
                ('Frame228', 'RightEyeClosed_EyesLookLeft'),
                ('Frame229', 'RightEyeClosed_EyesLookRight'),
                ('Frame230', 'RightEyeClosed_EyesLookUp'),
                ('Frame231', 'EyesLookUp_RightEyeUpperLidRaiser'),
                ('Frame232', 'JawDrop_RightLipCornerPuller'),
                ('Frame233', 'JawDrop_RightLowerLipDepressor'),
                ('Frame234', 'JawDrop_RightLipStretcher'),
                ('Frame235', 'JawDrop_RightUpperLipRaiser'),
                ('Frame236', 'RightLipCornerPuller_RightLowerLipDepressor'),
                ('Frame237', 'RightLipCornerPuller_RightLipStretcher'),
                ('Frame238', 'RightLipCornerPuller_Pucker'),
                ('Frame239', 'RightLipCornerPuller_RightUpperLipRaiser'),
                ('Frame240', 'RightLowerLipDepressor_Pucker'),
                ('Frame241', 'RightLipStretcher_RightUpperLipRaiser'),
                ('Frame242', 'Pucker_RightUpperLipRaiser'),
                ('Frame243', 'LeftBrowLowerer_LeftEyeClosed'),
                ('Frame244', 'RightBrowLowerer_RightEyeClosed'),
                ('Frame245', 'LeftLipCornerDown_LeftLowerLipDepressor'),
                ('Frame246', 'RightLipCornerDown_RightLowerLipDepressor'),
                ('Frame247', 'LeftInnerBrowRaiser_LeftOuterBrowRaiser'),
                ('Frame248', 'RightInnerBrowRaiser_RightOuterBrowRaiser'),
                ('Frame300', 'Funneler_JawDrop_Pucker'),
                ('Frame301', 'JawDrop_LeftLowerLipDepressor_Pucker'),
                ('Frame302', 'JawDrop_Pucker_LeftUpperLipRaiser'),
                ('Frame303', 'JawDrop_RightLowerLipDepressor_Pucker'),
                ('Frame304', 'JawDrop_Pucker_RightUpperLipRaiser'),
                ('dropoff', 4.0),
                ('smoothness', 0.0),
                ('RootFaceJoint', 'DynamicHead'),
            ]
            
            for prop_name, prop_value in facs_properties:
                obj[prop_name] = prop_value
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'add_facs_anim':
            selected = context.selected_objects

            if len(selected) != 1 or selected[0].type != 'ARMATURE':
                self.report({'ERROR'}, "Select exactly 1 Armature")
                return {'FINISHED'}

            target_rig = selected[0]
            objs_before = set(bpy.data.objects)
            colls_before = set(bpy.data.collections)
            acts_before = set(bpy.data.actions)

            # Append the template armature (carries the FACS preview animation)
            ava_spwn = 'Blocky_ava'
            try:
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + "/Collection/", filename = ava_spwn)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to append template: {e}")
                return {'FINISHED'}

            # Snapshot exactly what the append brought in so we can always remove it,
            # even on an error. (new_action, created later, is NOT in these sets.)
            appended_objs = set(bpy.data.objects) - objs_before
            appended_colls = set(bpy.data.collections) - colls_before
            appended_acts = set(bpy.data.actions) - acts_before

            def _cleanup_appended():
                try:
                    bpy.ops.object.select_all(action='DESELECT')
                except Exception:
                    pass
                for o in list(appended_objs):
                    try:
                        bpy.data.objects.remove(o, do_unlink=True)
                    except Exception:
                        pass
                for c in list(appended_colls):
                    try:
                        bpy.data.collections.remove(c)
                    except Exception:
                        pass
                for a in list(appended_acts):
                    try:
                        bpy.data.actions.remove(a)
                    except Exception:
                        pass

            def _reselect_target():
                try:
                    target_rig.select_set(True)
                    context.view_layer.objects.active = target_rig
                except Exception:
                    pass

            try:
                # Find the appended armature that carries the FACS animation
                template_rig = None
                for obj in appended_objs:
                    if obj.type == 'ARMATURE' and obj.animation_data and obj.animation_data.action:
                        template_rig = obj
                        break

                if not (template_rig and template_rig.animation_data.action):
                    _cleanup_appended()
                    _reselect_target()
                    self.report({'ERROR'}, "Could not find FACS animation in template")
                    return {'FINISHED'}

                template_action = template_rig.animation_data.action

                # Which bones does the template animation drive?
                anim_bones = set()
                for fc in _iter_action_fcurves(template_action):
                    if fc.data_path.startswith("pose.bones"):
                        try:
                            # Bone name, whether single- or double-quoted
                            bone_name = fc.data_path.split('[')[1].split(']')[0].strip('\'"')
                            anim_bones.add(bone_name)
                        except Exception:
                            pass

                # The template holds a full R15 body; FACS only needs the face
                # joints, so ignore standard body/root parts when checking gaps.
                ignored_parts = {
                    "LeftUpperArm", "LeftLowerArm", "LeftHand",
                    "RightUpperArm", "RightLowerArm", "RightHand",
                    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
                    "RightUpperLeg", "RightLowerLeg", "RightFoot",
                    "UpperTorso", "LowerTorso", "Head", "HumanoidRootPart",
                    "HumanoidRootNode", "Root",
                }

                facs_bones = {b for b in anim_bones if b not in ignored_parts}
                missing_bones = {b for b in facs_bones if b not in target_rig.pose.bones}

                # Validate: the selected armature must actually carry FACS joints.
                # Surface this as a UI error/banner instead of a Python traceback.
                if facs_bones and missing_bones == facs_bones:
                    glob_vars.rbx_facs_anim_error = "Selected armature has no FACS bones. Wrong rig or bone names."
                    _cleanup_appended()
                    _reselect_target()
                    self.report({'ERROR'}, "No matching FACS bones on the selected armature.")
                    return {'FINISHED'}

                # Copy the template action (correctly reproduces the slotted
                # structure on any Blender 4.5+), then drop object-level curves so
                # only the pose/custom-prop data is applied to the target rig.
                new_action = template_action.copy()
                new_action.name = "FACS_Animation"
                _prune_object_level_fcurves(new_action)

                # Assign the action (and its slot) to the target rig
                if not target_rig.animation_data:
                    target_rig.animation_data_create()
                else:
                    for track in list(target_rig.animation_data.nla_tracks):
                        target_rig.animation_data.nla_tracks.remove(track)

                target_rig.animation_data.action = new_action
                # Bind the action slot so the animation actually evaluates
                # (slotted actions, Blender 4.4+).
                slots = getattr(new_action, "slots", None)
                if slots and len(slots) > 0:
                    try:
                        target_rig.animation_data.action_slot = slots[0]
                    except Exception:
                        pass

                if missing_bones:
                    glob_vars.rbx_facs_anim_error = "Some FACS bones are missing in the face armature."
                    self.report({'WARNING'}, "FACS applied, but some face bones are missing.")
                else:
                    glob_vars.rbx_facs_anim_error = None
                    self.report({'INFO'}, "FACS Animation applied!")

            except Exception as e:
                _cleanup_appended()
                _reselect_target()
                self.report({'ERROR'}, f"Add FACS failed: {e}")
                return {'FINISHED'}

            # Success: remove the appended template, keep the new action, reselect.
            _cleanup_appended()
            _reselect_target()
            context.view_layer.update()


        if rbx_ava == 'rename':
            objects = bpy.context.selected_objects
        
            for item in objects:
                if '.' in item.name:
                     new_name = item.name.split('.')[0]
                     item.name = new_name
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'hide':
            objects = bpy.context.selected_objects
            
            for item in objects:
                if '_Att' in item.name:
                    item.hide_viewport = True
                    unhide_store.append(item)
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'unhide':
           for item in unhide_store:
               item.hide_viewport = False

           unhide_store.clear()
           bpy.context.view_layer.update()
                   
            
        if rbx_ava == 'export':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', path_mode='COPY', embed_textures=True, use_selection=True, object_types={'MESH', 'OTHER', 'EMPTY', 'ARMATURE'}, use_custom_props=True, add_leaf_bones=False, bake_anim=True, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=False, bake_anim_simplify_factor=0)


        return {'FINISHED'}         