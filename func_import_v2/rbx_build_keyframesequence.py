"""Advanced Upload: build a Roblox KeyframeSequence from the selected rig.

WHY
---
Roblox's FBX importer is ROTATION-ONLY: it silently drops every translation
channel, so bones offset in Blender snap back in Studio. This bypasses the FBX
round-trip entirely and builds the animation in Studio directly, where
Pose.CFrame carries rotation AND position in one value.

The emitted Luau goes to the clipboard; the user pastes it into Studio's
command bar and runs it, which creates the KeyframeSequence in ServerStorage.

WHAT GETS EMITTED
-----------------
Per joint, its transform RELATIVE TO ITS REST POSE, expressed in Roblox space --
exactly what Pose.CFrame means:

    orig = parent_rest^-1 @ rest          (rest joint transform)
    cur  = parent_now^-1  @ now           (posed joint transform)
    pose = orig^-1 @ cur                  (delta -> Pose.CFrame)
"""

import math

import bpy
from mathutils import Matrix

# Roblox caps animations at 70 fps; keys closer than 1/70s are rejected on upload.
MAX_FPS = 70

# Lift the clip so its lowest foot rests on the floor instead of sinking through.
#
# In Blender the floor is wherever you put it, so a retarget that drops the hips
# still looks planted. Roblox cannot do that: the Humanoid pins HumanoidRootPart
# at a fixed HipHeight, so the rig's REST ankle height IS the floor and anything
# below it clips through.
#
# The correction is a single constant added to LowerTorso's Y for the whole clip,
# so every relative motion (including root bob) is preserved exactly.
# LIFT-ONLY by design: a clip whose feet never drop below rest gets 0.0 and comes
# out byte-identical.
FLOOR_LOCK = True
FOOT_BONES = ("LeftFoot", "RightFoot")

# Blender bone name -> Roblox joint (part) name.
NAME_MAP = {"HumanoidRootNode": "HumanoidRootPart"}

# Roblox R15 joint tree. The Pose hierarchy inside each Keyframe mirrors this.
R15_TREE = [
    ("LowerTorso",    "HumanoidRootPart"),
    ("UpperTorso",    "LowerTorso"),
    ("Head",          "UpperTorso"),
    ("LeftUpperArm",  "UpperTorso"),
    ("LeftLowerArm",  "LeftUpperArm"),
    ("LeftHand",      "LeftLowerArm"),
    ("RightUpperArm", "UpperTorso"),
    ("RightLowerArm", "RightUpperArm"),
    ("RightHand",     "RightLowerArm"),
    ("LeftUpperLeg",  "LowerTorso"),
    ("LeftLowerLeg",  "LeftUpperLeg"),
    ("LeftFoot",      "LeftLowerLeg"),
    ("RightUpperLeg", "LowerTorso"),
    ("RightLowerLeg", "RightUpperLeg"),
    ("RightFoot",     "RightLowerLeg"),
]

JOINTS = [j for j, _ in R15_TREE]
RBX_TO_BONE = {v: k for k, v in NAME_MAP.items()}

# 180deg about the vertical axis. Armature space IS Roblox space (Y-up), so
# "vertical" is +Y here. Corrects the X/Z mirror between the rig and Roblox.
Y180 = Matrix.Rotation(math.radians(180.0), 4, 'Y')

# A rig with fewer matched joints than this is not an R15 rig and the export
# would be silently useless.
MIN_JOINTS = 6


# ───────────────────────────── conversion ───────────────────────────────

def bone_for(joint, arm):
    """Roblox joint name -> pose bone, honouring NAME_MAP."""
    return arm.pose.bones.get(RBX_TO_BONE.get(joint, joint))


def joint_matrix(pb, skip_to_armature=False):
    """Joint transform relative to its rest pose, expressed in Roblox space.

    Two things here are worth spelling out.

    1. The axis conversion must be a CONJUGATION, not a pre-multiplication.
       Pose.CFrame is a bone-LOCAL operator, so changing its basis means
       C @ M @ C^-1. Pre-multiplying puts the conversion on both sides of the
       inverse below, where it simply cancels and nothing is converted at all.

    2. skip_to_armature: measure relative to the ARMATURE rest rather than the
       parent bone, so the joint absorbs all of its ancestors' motion. Used for
       LowerTorso to soak up Root/HumanoidRootNode, whose translation Roblox
       discards if left on the root joint.
    """
    rest = pb.bone.matrix_local
    now = pb.matrix

    par = pb.parent
    if par is not None and not skip_to_armature:
        p_rest = par.bone.matrix_local
        p_now = par.matrix
    else:
        p_rest = p_now = Matrix.Identity(4)

    orig = p_rest.inverted() @ rest
    cur = p_now.inverted() @ now
    local = orig.inverted() @ cur

    # No AXIS conversion: on these rigs every bone's rest orientation in armature
    # space is 0.000 deg, because the +90deg X sits on the armature OBJECT.
    # Armature space already IS Roblox space (Y-up). Conjugating by the
    # Z-up<->Y-up matrix swaps Y and Z and turns a vertical bob into front/back
    # travel.
    #
    # But the rig IS MIRRORED relative to Roblox: rest heads put LeftUpperArm at
    # x = +1.0 where Roblox R15 puts left at -X. So X is flipped, and Z with it,
    # while Y (up) is unchanged -- which is a 180deg rotation about Y. Without
    # this, a delta that pulls the arms IN in Blender pushes them OUT in Studio.
    #
    # Applied as a CONJUGATION so it re-expresses the joint in the mirrored frame
    # rather than rotating the motion. Y180 is its own inverse.
    return Y180 @ local @ Y180


def verify_rest_identity(arm):
    """Rest orientation of each joint, worst first, in degrees.

    Exporting raw local deltas is only correct if each bone's REST orientation in
    armature space is the identity. If a bone's rest is rotated, its local delta
    is expressed in a tilted frame and Roblox reads it tilted -- which shows up
    only as "the arms look a bit off", so it is worth announcing.
    """
    worst = []
    for j in JOINTS:
        pb = bone_for(j, arm)
        if pb is None:
            continue
        worst.append((math.degrees(pb.bone.matrix_local.to_quaternion().angle), j))
    worst.sort(reverse=True)
    return worst


def sample(context, arm):
    """Walk the action and return (frames, fps, missing joints, floor lift)."""
    scene = context.scene
    act = arm.animation_data.action
    fps = scene.render.fps / scene.render.fps_base
    f0 = int(round(act.frame_range[0]))
    f1 = int(round(act.frame_range[1]))

    frames = []          # [(time, {joint: (px,py,pz,qx,qy,qz,qw)}), ...]
    missing = []
    lowest_ankle = None  # armature space, Y up

    keep = scene.frame_current
    try:
        for f in range(f0, f1 + 1):
            scene.frame_set(f)
            context.view_layer.update()
            t = round((f - f0) / fps, 5)
            poses = {}
            for j in JOINTS:
                pb = bone_for(j, arm)
                if pb is None:
                    if j not in missing:
                        missing.append(j)
                    continue
                # LowerTorso measures against the ARMATURE, not its parent, so it
                # absorbs the whole Root/HumanoidRootNode chain -- both the bob
                # (translation, which Roblox discards on the root joint but
                # honours here) and the root's -90deg X, which stands the rig up.
                m = joint_matrix(pb, skip_to_armature=(j == "LowerTorso"))
                p = m.to_translation()
                q = m.to_quaternion()
                # CFrame.new(x,y,z, qx,qy,qz,qw) -- quaternion form, 7 numbers
                # instead of the 12-component matrix form, purely to keep the
                # pasted script small. Mathematically identical.
                poses[j] = (round(p.x, 5), round(p.y, 5), round(p.z, 5),
                            round(q.x, 6), round(q.y, 6), round(q.z, 6), round(q.w, 6))
            for fb in FOOT_BONES:
                fpb = arm.pose.bones.get(fb)
                if fpb is not None:
                    y = fpb.matrix.translation.y
                    lowest_ankle = y if lowest_ankle is None else min(lowest_ankle, y)
            frames.append((t, poses))
    finally:
        scene.frame_set(keep)

    # Constant lift so the lowest ankle meets the rest ankle height (= the floor
    # in Roblox). max(0, ...) makes this lift-only: clips that never sink get 0.
    lift = 0.0
    if FLOOR_LOCK and lowest_ankle is not None:
        ref = arm.data.bones.get(FOOT_BONES[0])
        if ref is not None:
            lift = max(0.0, ref.head_local.y - lowest_ankle)
    if lift > 1e-6:
        # Y is untouched by the Y180 conjugation, so this applies cleanly to the
        # already-converted values.
        for _, poses in frames:
            if "LowerTorso" in poses:
                v = poses["LowerTorso"]
                poses["LowerTorso"] = (v[0], round(v[1] + lift, 5)) + v[2:]

    return frames, fps, missing, lift


def check_spacing(frames):
    """Roblox rejects keyframes closer together than 1/70s."""
    lim = 1.0 / MAX_FPS
    bad = []
    for i in range(1, len(frames)):
        gap = frames[i][0] - frames[i - 1][0]
        if gap < lim - 1e-9:
            bad.append((frames[i - 1][0], frames[i][0], gap))
    return bad


def variation(frames):
    """Per-joint peak-to-peak movement across the clip.

    Guards the failure that produces N byte-identical keyframes and still reports
    success: an action whose bones are all keyed but all hold the same pose.
    Silence there is indistinguishable from a working export until you load it in
    Studio and watch nothing happen.
    """
    out = {}
    for j in JOINTS:
        vals = [p[j] for _, p in frames if j in p]
        if not vals:
            continue
        out[j] = max(max(abs(v[i] - vals[0][i]) for i in range(7)) for v in vals)
    return out


def _lua_str(s):
    """Quote a Python string as a Lua string literal."""
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def emit(frames, duration, clip_name):
    """Build the Luau payload.

    NOTE: only --[[ ]] block comments are used, never -- line comments. Studio's
    command bar can flatten a pasted script onto one line, and a line comment
    there would swallow everything after it.
    """
    L = []
    L.append("--[[ KeyframeSequence generated by RBX Toolbox from Blender.")
    L.append("     Carries rotation AND position, bypassing Roblox's FBX importer")
    L.append("     which discards all translation. Paste and run in Studio. ]]")
    L.append("local CLIP_NAME = %s" % _lua_str(clip_name))
    L.append("local DURATION  = %.5f" % duration)
    L.append("local TREE = {")
    for joint, parent in R15_TREE:
        L.append("\t{%s,%s}," % (_lua_str(joint), _lua_str(parent)))
    L.append("}")

    # K = { {time, {joint = {px,py,pz,qx,qy,qz,qw}, ...}}, ... }
    L.append("local K = {")
    for t, poses in frames:
        L.append("\t{%.5f,{" % t)
        for j in JOINTS:
            v = poses.get(j)
            if v is None:
                continue
            L.append("\t\t%s={%.5f,%.5f,%.5f,%.6f,%.6f,%.6f,%.6f}," % ((j,) + v))
        L.append("\t}},")
    L.append("}")

    L.append(r'''--[[ ServerStorage root, deliberately. The Animation Editor keeps its saves
     under ServerStorage.RBX_ANIMSAVES.<RigName>, but that path is not safe to
     target: the editor may not be open when this runs, and the rig the user
     picks can be named anything. Dropping it at the root works regardless. ]]
local dest = game:GetService("ServerStorage")

local old = dest:FindFirstChild(CLIP_NAME)
if old then old:Destroy() end

local seq = Instance.new("KeyframeSequence")
seq.Name = CLIP_NAME
seq.Loop = false
seq.Priority = Enum.AnimationPriority.Action

local nPose = 0
for _, entry in ipairs(K) do
	local kf = Instance.new("Keyframe")
	kf.Time = entry[1]

	--[[ HumanoidRootPart is the root Pose and carries no motion of its own. ]]
	local poses = {}
	local root = Instance.new("Pose")
	root.Name = "HumanoidRootPart"
	root.CFrame = CFrame.new()
	root.Weight = 1
	root.Parent = kf
	poses.HumanoidRootPart = root

	--[[ Build in TREE order so every parent Pose exists before its children. ]]
	for _, e in ipairs(TREE) do
		local name, parent = e[1], e[2]
		local p = Instance.new("Pose")
		p.Name = name
		p.Weight = 1
		p.EasingStyle = Enum.PoseEasingStyle.Linear
		p.EasingDirection = Enum.PoseEasingDirection.In
		local v = entry[2][name]
		if v then
			p.CFrame = CFrame.new(v[1], v[2], v[3], v[4], v[5], v[6], v[7])
			nPose = nPose + 1
		else
			p.CFrame = CFrame.new()
		end
		p.Parent = poses[parent]
		poses[name] = p
	end

	kf.Parent = seq
end

seq.Parent = dest

print(string.format("Built %s", seq:GetFullName()))
print(string.format("  duration %.3fs   keyframes %d   poses written %d", DURATION, #K, nPose))
print("Move it into ServerStorage.RBX_ANIMSAVES.<YourRig>, then Load it in the Animation Editor.")''')
    return "\n".join(L)


def build_for_armature(context, arm, clip_name):
    """Full pipeline. Returns (luau_text, report_dict)."""
    frames, fps, missing, lift = sample(context, arm)
    duration = frames[-1][0] if frames else 0.0
    report = {
        "fps": fps,
        "duration": duration,
        "keyframes": len(frames),
        "missing": missing,
        "lift": lift,
        "bad_spacing": check_spacing(frames),
        "variation": variation(frames),
        "rest_tilt": [(a, j) for a, j in verify_rest_identity(arm) if a > 1.0],
    }
    return emit(frames, duration, clip_name), report


# ─────────────────── "Copied to Clipboard" button feedback ──────────────────

# The Generate button swaps its label for 3s after a successful copy. Blender has
# no notion of a transient button state, so the flag lives here and draw() reads
# it; the timer both clears it and forces the redraw that would otherwise never
# happen while the mouse sits still.
_COPIED_FLAG = False
CONFIRM_SECONDS = 3.0


def copied_recently():
    """True while the Generate button should read 'Copied to Clipboard'."""
    return _COPIED_FLAG


def _redraw_sidebars():
    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        return
    for win in wm.windows:
        screen = getattr(win, "screen", None)
        if screen is None:
            continue
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def _clear_copied_flag():
    global _COPIED_FLAG
    _COPIED_FLAG = False
    _redraw_sidebars()
    return None  # one shot


def _flash_copied():
    global _COPIED_FLAG
    _COPIED_FLAG = True
    if bpy.app.timers.is_registered(_clear_copied_flag):
        bpy.app.timers.unregister(_clear_copied_flag)
    bpy.app.timers.register(_clear_copied_flag, first_interval=CONFIRM_SECONDS)
    _redraw_sidebars()


# ───────────────────────────── operators ────────────────────────────────

def _selected_armature(context):
    selected = context.selected_objects
    if len(selected) == 1 and selected[0].type == "ARMATURE":
        return selected[0]
    return None


class RBX_OT_generate_keyframes(bpy.types.Operator):
    """Copy this animation to the clipboard as a Roblox KeyframeSequence script.

Paste it into Studio's command bar and run it"""

    bl_idname = "rbx.generate_keyframes"
    bl_label = "Generate Keyframes"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return _selected_armature(context) is not None

    def execute(self, context):
        arm = _selected_armature(context)
        if arm is None:
            self.report({'ERROR'}, "Select a single armature first")
            return {'CANCELLED'}

        action = arm.animation_data.action if arm.animation_data else None
        if action is None:
            self.report({'ERROR'}, "The selected armature has no action assigned")
            return {'CANCELLED'}

        found = [j for j in JOINTS if bone_for(j, arm) is not None]
        if len(found) < MIN_JOINTS:
            self.report({'ERROR'}, "Not an R15 rig: only %d of %d joints found"
                        % (len(found), len(JOINTS)))
            return {'CANCELLED'}

        clip_name = (context.scene.rbx_prefs.rbx_adv_anim_name or "").strip()
        if not clip_name:
            clip_name = action.name

        try:
            script, rep = build_for_armature(context, arm, clip_name)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.report({'ERROR'}, "Failed to build keyframes: %s" % exc)
            return {'CANCELLED'}

        self._print_report(clip_name, rep, len(script))

        moving = [j for j, v in rep["variation"].items() if v > 1e-4]
        if not moving:
            self.report({'ERROR'}, "Nothing moves in this action - every joint holds "
                                   "the same pose. Nothing was copied")
            return {'CANCELLED'}

        try:
            context.window_manager.clipboard = script
        except Exception as exc:
            self.report({'ERROR'}, "Could not write to clipboard: %s" % exc)
            return {'CANCELLED'}

        _flash_copied()

        if rep["bad_spacing"]:
            self.report({'WARNING'}, "Copied, but %d keyframe gaps are under 1/%ds - "
                                     "Roblox may reject the upload"
                        % (len(rep["bad_spacing"]), MAX_FPS))
        elif rep["missing"]:
            self.report({'WARNING'}, "Copied, but %d joints were missing: %s"
                        % (len(rep["missing"]), ", ".join(rep["missing"])))
        else:
            self.report({'INFO'}, "Copied to clipboard: %d keyframes, %.2fs"
                        % (rep["keyframes"], rep["duration"]))
        return {'FINISHED'}

    def _print_report(self, clip_name, rep, nchars):
        print("=" * 70)
        print("RBX Toolbox - KeyframeSequence build")
        print("clip name : %s" % clip_name)
        print("fps %.4g   duration %.3fs   keyframes %d   chars %d"
              % (rep["fps"], rep["duration"], rep["keyframes"], nchars))

        if rep["rest_tilt"]:
            print("REST NOT IDENTITY -- local deltas are in tilted frames:")
            for a, j in rep["rest_tilt"][:6]:
                print("   %-16s %.2f deg" % (j, a))
            print("   ^ export will be rotated on these joints")

        if FLOOR_LOCK:
            if rep["lift"] > 1e-6:
                print("floor lock : lifted clip %.4f studs (lowest foot was below the"
                      " rest ankle, i.e. through Roblox's floor)" % rep["lift"])
            else:
                print("floor lock : 0.0000 -- feet never drop below rest, clip unchanged")

        if rep["missing"]:
            print("MISSING BONES (no pose written): %s" % ", ".join(rep["missing"]))

        var = rep["variation"]
        moving = [j for j, v in var.items() if v > 1e-4]
        if not moving:
            print("")
            print("*** NOTHING MOVES ***")
            print("Every joint holds the same pose for the whole clip. The bones are")
            print("probably all keyed at one pose -- check the action in the Action Editor.")
        else:
            print("joints that MOVE (%d of %d):" % (len(moving), len(var)))
            for j in JOINTS:
                if j in var:
                    print("   %-16s %s %.5f"
                          % (j, "moves " if j in moving else "STATIC", var[j]))

        if rep["bad_spacing"]:
            print("%dfps VIOLATIONS: %d -- Roblox will reject the upload"
                  % (MAX_FPS, len(rep["bad_spacing"])))
            for a, b, g in rep["bad_spacing"][:5]:
                print("   %.6f -> %.6f  gap %.6f" % (a, b, g))
        else:
            print("key spacing: ok (no pair closer than %.6fs)" % (1.0 / MAX_FPS))
        print("=" * 70)


class RBX_OT_adv_upload_info_popup(bpy.types.Operator):
    """Click Me"""
    bl_idname = "object.rbx_adv_upload_info_popup"
    bl_label = "Advanced Upload"
    bl_options = {'REGISTER', 'INTERNAL'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=470)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Advanced Upload - transfer the animation as-is.", icon='INFO')
        layout.separator()

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Uploading animations with the standard Roblox tools strips")
        col.label(text="off bone movement: bones that were moved away from their")
        col.label(text="original locations snap back. This tool transfers the")
        col.label(text="animation to Roblox exactly as it was made in Blender.")

        box = layout.box()
        col = box.column(align=True)
        col.label(text="How to use:", icon='PLAY')
        col.label(text="1. Select the armature with the animation.")
        col.label(text='2. Press "Generate Keyframes". This copies the keyframes')
        col.label(text="    to your Windows clipboard.")
        col.label(text="3. Open Roblox Studio and paste it into the console field")
        col.label(text="    (usually at the bottom), then press Enter or Run.")
        col.label(text="4. This creates a KeyframeSequence asset in ServerStorage.")
        col.label(text="    You can now publish it to Roblox, or test it.")

        box = layout.box()
        col = box.column(align=True)
        col.label(text="To test:", icon='ARMATURE_DATA')
        col.label(text="1. Spawn a rig via the Avatar tab, then open the Animation")
        col.label(text="    Editor in the same tab.")
        col.label(text="2. A new folder appears in ServerStorage: RBX_ANIMSAVES.")
        col.label(text="    Inside it is a folder named after your rig.")
        col.label(text="3. Move the created KeyframeSequence into that folder.")
        col.label(text='4. In the Animation Editor click "..." and select Load,')
        col.label(text="    then pick your animation and test it.")

    def execute(self, context):
        return {'FINISHED'}
