import bpy
import os
from RBX_Toolbox import glob_vars
import mathutils


ANIM_COLLECTION_NAME = "LC_Animation_Test"


def _update_frame_scrub(self, context):
    """Map the 0-100 scrub slider to the animation's frame range."""
    scene = context.scene
    f_start = scene.frame_start
    f_end = scene.frame_end
    total = max(f_end - f_start, 1)
    frame = f_start + int((self.rbx_lc_anim_scrub / 100.0) * total)
    scene.frame_set(frame)


class _LC_Anim_V2_Globals:
    """Shared state for LC Animation V2 operators."""
    animationIsPlaying = False
    currentAnim = ""
    currentSpeed = 1.0
    importedAction = None
    originalStart = None
    originalEnd = None
    originalFps = None
    spawned_armature_name = None  # track spawned rig


# ───────────────────────────── helpers ──────────────────────────────

def _get_anims_dir():
    """Return absolute path to the anims/ folder shipped with the addon."""
    return os.path.join(glob_vars.addon_path, glob_vars.rbx_anims_fldr)


def _validate_armature(obj):
    """Return True if *obj* is an Armature containing the standard R15 bone set."""
    if obj is None or obj.type != 'ARMATURE':
        return False
    bone_list = [
        "Root", "HumanoidRootNode", "LowerTorso", "UpperTorso", "Head",
        "LeftUpperArm", "LeftLowerArm", "LeftHand",
        "RightUpperArm", "RightLowerArm", "RightHand",
        "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
        "RightUpperLeg", "RightLowerLeg", "RightFoot",
    ]
    found = sum(1 for b in obj.data.bones if b.name in bone_list)
    return found == len(bone_list)


def _check_bone_direction(armature_obj):
    """
    Determine whether bones point downward (Blender-style rig).
    Returns True when the lower-limb bones have their tails ABOVE their heads
    (i.e. bones face down).  Mirrors CalisthenicsTool's ``checkRigType_2``.
    """
    check_bones = ["LeftLowerArm", "RightLowerArm", "LeftLowerLeg", "RightLowerLeg"]
    up_count = 0
    for pb in armature_obj.pose.bones:
        if pb.name in check_bones:
            rotx, _, _ = armature_obj.rotation_euler
            if rotx != 0.0:
                tail_h, head_h = pb.tail[1], pb.head[1]
            else:
                tail_h, head_h = pb.tail[2], pb.head[2]
            if tail_h > head_h:
                up_count += 1
    return up_count != 4        # True → bones face down


def _get_anim_fbx_path(anim_type, bones_face_down):
    """
    Map an animation type string to the correct FBX file inside *anims/*.
    anim_type: one of 'IDLE', 'WALK', 'MOVE', 'RUN'
    """
    anims_dir = _get_anims_dir()
    # (normal_fbx, bone_down_fbx, start_normal, end_normal, start_B, end_B)
    mapping = {
        "WALK": ("WalkAnim_2.fbx",  "WalkAnim_B_4.fbx",  2, 17,  3, 19),
        "RUN":  ("RunAnim_2.fbx",   "RunAnim_B_5.fbx",   2, 17,  3, 17),
        "MOVE": ("MoveAnim_2.fbx",  "MoveAnim_B_7.fbx",  2, 660, 2, 660),
        "IDLE": ("IdleAnim_2.fbx",  "IdleAnim_B_5.fbx",  2, 242, 2, 242),
    }
    if anim_type not in mapping:
        return None, 0, 0
    normal, bone_down, start_n, end_n, start_b, end_b = mapping[anim_type]
    if bones_face_down:
        return os.path.join(anims_dir, bone_down), start_b, end_b
    else:
        return os.path.join(anims_dir, normal), start_n, end_n


def _get_spawned_armature():
    """Find the armature in the LC_Animation_Test collection."""
    col = bpy.data.collections.get(ANIM_COLLECTION_NAME)
    if col is None:
        return None
    for obj in col.all_objects:
        if obj.type == 'ARMATURE' and obj.name == _LC_Anim_V2_Globals.spawned_armature_name:
            return obj
    # fallback: first armature in collection
    for obj in col.all_objects:
        if obj.type == 'ARMATURE':
            return obj
    return None


def _is_rig_spawned():
    """True if the LC_Animation_Test collection exists with an armature."""
    return _get_spawned_armature() is not None


def _remove_existing_anim(armature):
    """Remove constraints and imported animation armature from the rig."""
    if armature is None:
        return

    # Stop any active playback first
    try:
        bpy.ops.screen.animation_cancel(restore_frame=False)
    except RuntimeError:
        pass

    # Collect ALL unique constraint targets before removing constraints
    targets_to_delete = set()
    for pb in armature.pose.bones:
        for c in list(pb.constraints):
            if hasattr(c, 'target') and c.target is not None:
                targets_to_delete.add(c.target)
            pb.constraints.remove(c)

    # Delete all collected animation armature targets
    for target in targets_to_delete:
        try:
            bpy.data.objects.remove(target, do_unlink=True)
        except ReferenceError:
            pass

    # Clean up orphan armatures
    for arm in [a for a in bpy.data.armatures if a.users == 0]:
        bpy.data.armatures.remove(arm)

    # Clean up the tracked imported action
    if _LC_Anim_V2_Globals.importedAction is not None:
        try:
            bpy.data.actions.remove(_LC_Anim_V2_Globals.importedAction)
        except ReferenceError:
            pass
        _LC_Anim_V2_Globals.importedAction = None

    # Also clean up any other orphan actions (leftover from FBX imports)
    for act in [a for a in bpy.data.actions if a.users == 0]:
        bpy.data.actions.remove(act)

    _LC_Anim_V2_Globals.currentAnim = ""
    _LC_Anim_V2_Globals.animationIsPlaying = False


def _attach_constraints(target_arm, source_arm):
    """Wire target_arm pose-bones to follow source_arm via Copy Rotation/Location."""
    skip = {"Root", "HumanoidRootNode"}
    for pb in target_arm.pose.bones:
        if pb.name in skip:
            continue
        try:
            src_pb = source_arm.pose.bones[pb.name]
        except KeyError:
            continue
        if pb.name == "LowerTorso":
            crc = pb.constraints.new('COPY_LOCATION')
            crc.target = source_arm
            crc.subtarget = src_pb.bone.name
            crc.use_x = False
            crc.use_y = False
        crc = pb.constraints.new('COPY_ROTATION')
        crc.target = source_arm
        crc.subtarget = src_pb.bone.name


# ─────────────────── rig name → collection name map ────────────────
# To add more rigs, uncomment or add a new entry below
# and add a matching enum item in props.py (rbx_lc_anim_v2_rig_enum)

RIG_MAP = {
    "OP1": "R15 Blocky Rig",          # Rig 1
    "OP2": "R15 Woman Rig",            # Rig 2
    #"OP3": "Plushie Template",        # Rig 3 (add when ready)
    #"OP4": "Multirig",               # Rig 4 (add when ready)
    #"OP5": "Multirig_faceless",      # Rig 5 (add when ready)
}


# ══════════════════════════ OPERATORS ══════════════════════════════

class RBX_OT_LC_ANIM_V2(bpy.types.Operator):
    """Spawn a rig beside the selected armature and copy & link items (no animation)."""
    bl_idname = "object.rbx_lc_anim_v2"
    bl_label = "Spawn Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs

        # 1. Get armature from prop_search
        src_armature = scene.rbx_lc_anim_armature
        if src_armature is None or src_armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select a valid Armature in the picker.")
            return {'CANCELLED'}

        # 2. Determine which rig to spawn
        rig_enum = rbx_prefs.rbx_lc_anim_v2_rig_enum
        rig_name = RIG_MAP.get(rig_enum)
        if rig_name is None:
            self.report({'ERROR'}, "Invalid rig selection.")
            return {'CANCELLED'}

        # 3. Spawn the rig (collection append from blend file)
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.wm.append(
            directory=glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection,
            filename=rig_name,
        )

        appended_objs = list(bpy.context.selected_objects)
        if not appended_objs:
            self.report({'ERROR'}, "Rig collection could not be appended.")
            return {'CANCELLED'}

        # Move rig +5 X beside original
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        bpy.ops.transform.translate(
            value=(5, 0, 0),
            orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            orient_matrix_type='GLOBAL',
            constraint_axis=(False, False, True),
        )

        # Identify the spawned rig collection & armature
        rig_collection = appended_objs[0].users_collection[0]
        spawned_armature = None
        for obj in rig_collection.all_objects:
            if obj.type == 'ARMATURE':
                spawned_armature = obj
                break

        if spawned_armature is None:
            self.report({'ERROR'}, "No armature found in spawned rig collection.")
            return {'CANCELLED'}

        # 4. Create working collection
        anim_collection = bpy.data.collections.new(ANIM_COLLECTION_NAME)
        bpy.context.scene.collection.children.link(anim_collection)

        # 5. Move spawned rig + children to anim collection (keep parenting)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in list(rig_collection.all_objects):
            for col in list(obj.users_collection):
                col.objects.unlink(obj)
            anim_collection.objects.link(obj)
        bpy.data.collections.remove(rig_collection)

        # Hide bones display and _Att objects
        spawned_armature.data.display_type = 'WIRE'
        spawned_armature.show_in_front = False
        spawned_armature.hide_set(True)
        for obj in list(anim_collection.all_objects):
            if "_Att" in obj.name:
                obj.hide_set(True)

        # 6. Create linked duplicates and parent to matching bones
        src_children = [c for c in src_armature.children if c.type == 'MESH']

        linked_dups = []
        for child in src_children:
            dup = child.copy()
            anim_collection.objects.link(dup)
            linked_dups.append((child, dup))

        # Compute a TRANSLATION-ONLY offset using a reference bone (LowerTorso).
        # This avoids: (1) rotation differences (src is 180° rotated), and
        # (2) armature origin height differences (src origin at Z=0.96, spawned at Z=0).
        # The LowerTorso bone world position represents where the character actually is.
        src_ref_bone = src_armature.data.bones.get('LowerTorso')
        spawned_ref_bone = spawned_armature.data.bones.get('LowerTorso')
        if src_ref_bone and spawned_ref_bone:
            src_ref = src_armature.matrix_world @ src_ref_bone.head_local
            spawned_ref = spawned_armature.matrix_world @ spawned_ref_bone.head_local
            visual_offset = spawned_ref - src_ref
        else:
            # Fallback: just X offset
            visual_offset = spawned_armature.location - src_armature.location
            visual_offset.z = 0  # don't shift Z

        for child, dup in linked_dups:
            parent_bone_name = child.parent_bone
            parent_type = child.parent_type

            # Step 1: Unparent (child.copy() leaves dup parented to src_armature)
            bpy.ops.object.select_all(action='DESELECT')
            dup.select_set(True)
            bpy.context.view_layer.objects.active = dup
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            bpy.context.view_layer.update()

            # Step 2: Move dup to correct position (translation only, no rotation)
            dup.matrix_world = child.matrix_world.copy()
            dup.location = dup.location + visual_offset
            bpy.context.view_layer.update()

            # Step 3: Parent to spawned rig
            if parent_type == 'BONE' and parent_bone_name:
                bpy.ops.object.select_all(action='DESELECT')
                spawned_armature.select_set(True)
                bpy.context.view_layer.objects.active = spawned_armature
                bpy.ops.object.mode_set(mode='EDIT')

                bone_found = False
                for bone in spawned_armature.data.edit_bones:
                    if bone.name == parent_bone_name:
                        bpy.ops.armature.select_all(action='DESELECT')
                        bone.select = True
                        spawned_armature.data.edit_bones.active = bone
                        bone_found = True
                        break

                bpy.ops.object.mode_set(mode='OBJECT')

                if bone_found:
                    bpy.ops.object.select_all(action='DESELECT')
                    dup.select_set(True)
                    spawned_armature.select_set(True)
                    bpy.context.view_layer.objects.active = spawned_armature
                    bpy.ops.object.parent_set(type='BONE')
                else:
                    bpy.ops.object.select_all(action='DESELECT')
                    dup.select_set(True)
                    spawned_armature.select_set(True)
                    bpy.context.view_layer.objects.active = spawned_armature
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            else:
                bpy.ops.object.select_all(action='DESELECT')
                dup.select_set(True)
                spawned_armature.select_set(True)
                bpy.context.view_layer.objects.active = spawned_armature
                if parent_type == 'ARMATURE':
                    bpy.ops.object.parent_set(type='ARMATURE')
                else:
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

            # Retarget any Armature modifiers to point to the spawned rig
            for mod in dup.modifiers:
                if mod.type == 'ARMATURE' and mod.object == src_armature:
                    mod.object = spawned_armature

        if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Store spawned armature name for other operators
        _LC_Anim_V2_Globals.spawned_armature_name = spawned_armature.name

        bpy.ops.object.select_all(action='DESELECT')
        self.report({'INFO'}, "Rig spawned successfully.")
        return {'FINISHED'}


# ───────────── Add Animation (no playback) ─────────────

class RBX_OT_LC_ANIM_V2_ADD_ANIM(bpy.types.Operator):
    """Add animation to the spawned rig (stays stationary until Play is pressed)."""
    bl_idname = "object.rbx_lc_anim_v2_add_anim"
    bl_label = "Add Animation"
    bl_options = {'REGISTER', 'UNDO'}

    anim_type: bpy.props.StringProperty(default="IDLE")  # type: ignore

    def execute(self, context):
        scene = context.scene
        spawned_armature = _get_spawned_armature()
        if spawned_armature is None:
            self.report({'ERROR'}, "No spawned rig found. Spawn a rig first.")
            return {'CANCELLED'}

        # Remove any existing animation first
        _remove_existing_anim(spawned_armature)

        bones_down = _check_bone_direction(spawned_armature)
        fbx_path, frame_start, frame_end = _get_anim_fbx_path(self.anim_type, bones_down)

        if not fbx_path or not os.path.isfile(fbx_path):
            self.report({'WARNING'}, f"Animation file not found: {fbx_path}")
            return {'CANCELLED'}

        # Store original frame range and FPS
        if _LC_Anim_V2_Globals.originalStart is None:
            _LC_Anim_V2_Globals.originalStart = scene.frame_start
            _LC_Anim_V2_Globals.originalEnd = scene.frame_end
            _LC_Anim_V2_Globals.originalFps = scene.render.fps

        # Import FBX animation
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.fbx(filepath=fbx_path)
        anim_arm = bpy.context.selected_objects[0] if bpy.context.selected_objects else None

        if anim_arm and anim_arm.type == 'ARMATURE':
            _LC_Anim_V2_Globals.importedAction = (
                anim_arm.animation_data.action if anim_arm.animation_data else None
            )

            # Wire constraints
            _attach_constraints(spawned_armature, anim_arm)

            # Hide the animation source armature
            anim_arm.hide_set(True)

            # Set frame range but do NOT play
            scene.frame_start = frame_start
            scene.frame_end = frame_end
            scene.frame_current = frame_start

            _LC_Anim_V2_Globals.currentAnim = self.anim_type
            self.report({'INFO'}, f"{self.anim_type} animation added.")
        else:
            self.report({'WARNING'}, "Animation FBX did not contain an armature.")

        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}


# ───────────── Play Animation ─────────────

class RBX_OT_LC_ANIM_V2_PLAY(bpy.types.Operator):
    """Toggle animation playback (Play / Pause)."""
    bl_idname = "object.rbx_lc_anim_v2_play"
    bl_label = "Play / Pause"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if not _LC_Anim_V2_Globals.currentAnim:
            self.report({'WARNING'}, "No animation loaded. Add an animation first.")
            return {'CANCELLED'}
        # screen.animation_play toggles: if playing it pauses, if paused it plays
        bpy.ops.screen.animation_play()
        _LC_Anim_V2_Globals.animationIsPlaying = not _LC_Anim_V2_Globals.animationIsPlaying
        return {'FINISHED'}


# ───────────── Stop Animation ─────────────

class RBX_OT_LC_ANIM_V2_STOP(bpy.types.Operator):
    """Pause animation playback at current frame."""
    bl_idname = "object.rbx_lc_anim_v2_stop"
    bl_label = "Pause"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        except RuntimeError:
            pass
        _LC_Anim_V2_Globals.animationIsPlaying = False
        return {'FINISHED'}


# ───────────── Delete Rig ─────────────

class RBX_OT_LC_ANIM_V2_DELETE(bpy.types.Operator):
    """Delete the spawned rig and the LC_Animation_Test collection."""
    bl_idname = "object.rbx_lc_anim_v2_delete"
    bl_label = "Delete Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        # Stop playback if running
        try:
            bpy.ops.screen.animation_cancel()
        except RuntimeError:
            pass

        if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Remove animation constraints/imported armature first
        spawned_armature = _get_spawned_armature()
        if spawned_armature:
            _remove_existing_anim(spawned_armature)

        # Delete all objects in the collection
        col = bpy.data.collections.get(ANIM_COLLECTION_NAME)
        if col is not None:
            for obj in list(col.all_objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(col)

        # Restore original frame range and FPS
        if _LC_Anim_V2_Globals.originalStart is not None:
            scene.frame_start = _LC_Anim_V2_Globals.originalStart
            scene.frame_end = _LC_Anim_V2_Globals.originalEnd
        if _LC_Anim_V2_Globals.originalFps is not None:
            scene.render.fps = _LC_Anim_V2_Globals.originalFps

        # Reset state
        _LC_Anim_V2_Globals.animationIsPlaying = False
        _LC_Anim_V2_Globals.currentAnim = ""
        _LC_Anim_V2_Globals.importedAction = None
        _LC_Anim_V2_Globals.originalStart = None
        _LC_Anim_V2_Globals.originalEnd = None
        _LC_Anim_V2_Globals.originalFps = None
        _LC_Anim_V2_Globals.spawned_armature_name = None

        # Clean up orphans
        for arm in [a for a in bpy.data.armatures if a.users == 0]:
            bpy.data.armatures.remove(arm)

        self.report({'INFO'}, "Rig deleted.")
        return {'FINISHED'}


# ───────────── Speed Control ─────────────

class RBX_OT_LC_ANIM_V2_SPEED(bpy.types.Operator):
    """Set animation playback speed."""
    bl_idname = "object.rbx_lc_anim_v2_speed"
    bl_label = "Speed"
    bl_options = {'REGISTER'}

    speed: bpy.props.FloatProperty(default=1.0)  # type: ignore

    def execute(self, context):
        scene = context.scene
        # Use FPS to control playback speed
        # Store original FPS if not yet stored
        if _LC_Anim_V2_Globals.originalFps is None:
            _LC_Anim_V2_Globals.originalFps = scene.render.fps
        base_fps = _LC_Anim_V2_Globals.originalFps
        scene.render.fps = max(1, int(base_fps * self.speed))
        _LC_Anim_V2_Globals.currentSpeed = round(self.speed, 2)
        self.report({'INFO'}, f"Speed set to {self.speed}x")
        return {'FINISHED'}
