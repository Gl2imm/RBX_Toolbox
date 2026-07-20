if "bpy" in locals():
    import importlib

import bpy

# Roblox's hard limit is 30 studs/s, but it measures on its own R15 rig which is larger
# than typical Blender rigs, and measures part centers rather than joint pivots.
# Observed ratio between Blender speeds and Roblox speeds varies ~1.09–1.17.
# SPEED_LIMIT is the Blender-space detection threshold; RBX_SCALE converts it for display
# so that violations always appear as ≥ 30 in the UI (matching Roblox's unit).
SPEED_LIMIT = 26.0
RBX_SCALE   = 30.0 / SPEED_LIMIT   # = 1.1538...

# The bone that represents HumanoidRootPart — try these names in order.
ROOT_BONE_NAMES = ("HumanoidRootPart", "HumanoidRootNode")

SPHERE_NAME   = "RBX_SafeZoneSphere"
SPHERE_RADIUS = 5.0  # Roblox's validateBounds limit in studs


def _delete_sphere():
    obj = bpy.data.objects.get(SPHERE_NAME)
    if obj:
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def _create_sphere(context):
    import bmesh as _bmesh
    _delete_sphere()

    bm = _bmesh.new()
    _bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=SPHERE_RADIUS)
    mesh = bpy.data.meshes.new(SPHERE_NAME)
    bm.to_mesh(mesh)
    bm.free()

    sphere = bpy.data.objects.new(SPHERE_NAME, mesh)
    sphere.display_type = "WIRE"
    sphere.hide_render = True
    sphere.hide_select = True  # Reference gizmo — must not be dragged or picked up by upload
    context.scene.collection.objects.link(sphere)
    return sphere


def _root_location_at_start(context, arm, root_name):
    """World-space location of the rig's root bone on the action's first frame."""
    scene = context.scene
    action = arm.animation_data.action if arm.animation_data else None
    if action is None:
        return (arm.matrix_world @ arm.pose.bones[root_name].head).copy()

    original_frame = scene.frame_current
    try:
        scene.frame_set(int(action.frame_range[0]))
        return (arm.matrix_world @ arm.pose.bones[root_name].head).copy()
    finally:
        scene.frame_set(original_frame)


def _update_safe_zone(self, context):
    """BoolProperty update callback for Scene.rbx_show_safe_zone."""
    show = self.rbx_show_safe_zone

    if not show:
        _delete_sphere()  # Remove from scene entirely, not just hide it
        return

    sphere = bpy.data.objects.get(SPHERE_NAME)

    # Find the selected armature that has a valid root bone.
    arm = None
    root_name = None
    for obj in (context.selected_objects or []):
        if obj.type == "ARMATURE":
            candidate = next((n for n in ROOT_BONE_NAMES if n in obj.pose.bones), None)
            if candidate:
                arm = obj
                root_name = candidate
                break

    if arm is None:
        return  # No valid armature — leave checkbox on but do nothing

    if sphere is None:
        sphere = _create_sphere(context)

    # Pin the sphere to where the rig starts, so playing the animation shows
    # whether the character leaves the bounds. Constraints are cleared to undo
    # the follow-the-rig behaviour from spheres saved by older versions.
    sphere.constraints.clear()
    sphere.hide_select = True
    sphere.location = _root_location_at_start(context, arm, root_name)
    sphere.hide_viewport = False


class RBX_OT_check_animation_emote(bpy.types.Operator):
    """Check active animation for Roblox Emote violations (speed > 30 studs/s)"""

    bl_idname = "rbx.check_animation_emote"
    bl_label = "Check Emote"

    _violations: list = []

    @classmethod
    def poll(cls, context):
        sel = context.selected_objects
        if len(sel) != 1 or sel[0].type != "ARMATURE":
            return False
        arm = sel[0]
        return bool(arm.animation_data and arm.animation_data.action)

    def invoke(self, context, event):
        self._violations, bone_max_speeds = self._run_speed_check(context)

        fps = context.scene.render.fps / context.scene.render.fps_base
        print(f"[RBX Emote Check] ── Top bone speeds (est. Roblox studs/s)  FPS={fps:.4g} ──")
        for bname, v in sorted(bone_max_speeds.items(), key=lambda x: -x[1]["speed"])[:15]:
            marker = " ← VIOLATION" if v["speed"] > SPEED_LIMIT else ""
            print(f"  fr.{v['frame']:>4}  t={v['time']:.3f}s  {bname:<30}  ~{v['speed'] * RBX_SCALE:.2f} studs/s{marker}")
        unique_speed_bones = len(set(v["bone"] for v in self._violations))
        print(f"[RBX Emote Check] Speed — violating bones={unique_speed_bones}  frames={len(self._violations)}")

        return context.window_manager.invoke_popup(self, width=470)

    def execute(self, context):
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        if not self._violations:
            layout.label(text="No speed violations found!", icon="CHECKMARK")
            return

        unique_bones = len(set(v["bone"] for v in self._violations))
        layout.label(text=f"SPEED: {unique_bones} bone(s) will likely exceed 30 studs/s:", icon="ERROR")
        layout.label(text="(estimated — actual Roblox value may differ slightly)", icon="INFO")
        layout.separator()
        col = layout.column(align=True)
        for v in sorted(self._violations, key=lambda x: -x["speed"]):
            row = col.row()
            row.label(text=f"fr.{v['frame']}  ({v['time']:.2f}s)   {v['bone']}")
            row.label(text=f"~{v['speed'] * RBX_SCALE:.1f} studs/s")

    def _run_speed_check(self, context):
        arm = context.selected_objects[0]
        action = arm.animation_data.action
        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base

        frame_start = int(action.frame_range[0])
        frame_end = int(action.frame_range[1])

        original_frame = scene.frame_current
        violations = []
        bone_max_speeds = {}

        try:
            prev_positions = {}
            for frame in range(frame_start, frame_end + 1):
                scene.frame_set(frame)
                current_positions = {}
                for pbone in arm.pose.bones:
                    pos = (arm.matrix_world @ pbone.head).copy()
                    current_positions[pbone.name] = pos

                if prev_positions:
                    dt = 1.0 / fps
                    time_s = (frame - frame_start) / fps
                    for bname, pos in current_positions.items():
                        prev = prev_positions.get(bname)
                        if prev is not None:
                            speed = (pos - prev).length / dt

                            if bname not in bone_max_speeds or speed > bone_max_speeds[bname]["speed"]:
                                bone_max_speeds[bname] = {"frame": frame, "time": time_s, "speed": speed}

                            if speed > SPEED_LIMIT:
                                violations.append(
                                    {
                                        "frame": frame,
                                        "time": time_s,
                                        "bone": bname,
                                        "speed": speed,
                                    }
                                )

                prev_positions = current_positions
        finally:
            scene.frame_set(original_frame)

        return violations, bone_max_speeds
