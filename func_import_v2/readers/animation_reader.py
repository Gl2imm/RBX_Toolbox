"""
animation_reader.py
───────────────────
Converts a Roblox KeyframeSequence (parsed by rbxm_reader.py) into
sparse per-bone keyframe data ready for the Blender animation script.

Usage:
    from rbxm_reader import parse
    from animation_reader import read_animation

    model = parse("walk.rbxm")
    ks    = model.FindFirstChildOfClass("KeyframeSequence")
    data  = read_animation(ks)
"""

import math


# ─────────────────────────────────────────────
#  CFrame → position + quaternion
# ─────────────────────────────────────────────

def _cframe_to_pos_quat(cframe: dict):
    """Extract position (x,y,z) and quaternion (w,x,y,z) from a CFrame dict.
    No coordinate conversion — raw Roblox values work directly on Blender bones.
    """
    if cframe is None:
        return (0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0)

    pos    = cframe.get("position", (0.0, 0.0, 0.0))
    rot    = cframe.get("rotation", ("matrix", (1,0,0, 0,1,0, 0,0,1)))
    
    if rot[0] == "matrix":
        matrix = rot[1]
    elif rot[0] == "special":
        # Convert Euler angles (Y,X,Z degrees) to rotation matrix
        yd, xd, zd = rot[1]
        yr, xr, zr = math.radians(yd), math.radians(xd), math.radians(zd)
        cy, sy = math.cos(yr), math.sin(yr)
        cx, sx = math.cos(xr), math.sin(xr)
        cz, sz = math.cos(zr), math.sin(zr)
        # Combined rotation matrix: Ry * Rx * Rz
        matrix = (
            cy*cz + sy*sx*sz,  -cy*sz + sy*sx*cz,  sy*cx,
            cx*sz,              cx*cz,              -sx,
            -sy*cz + cy*sx*sz,  sy*sz + cy*sx*cz,   cy*cx,
        )
    else:
        matrix = (1,0,0, 0,1,0, 0,0,1)

    r00,r01,r02, r10,r11,r12, r20,r21,r22 = matrix
    trace = r00 + r11 + r22

    if trace > 0.0:
        s  = 0.5 / math.sqrt(trace + 1.0)
        qw = 0.25 / s
        qx = (r21 - r12) * s
        qy = (r02 - r20) * s
        qz = (r10 - r01) * s
    elif r00 > r11 and r00 > r22:
        s  = 2.0 * math.sqrt(1.0 + r00 - r11 - r22)
        qw = (r21 - r12) / s
        qx = 0.25 * s
        qy = (r01 + r10) / s
        qz = (r02 + r20) / s
    elif r11 > r22:
        s  = 2.0 * math.sqrt(1.0 + r11 - r00 - r22)
        qw = (r02 - r20) / s
        qx = (r01 + r10) / s
        qy = 0.25 * s
        qz = (r12 + r21) / s
    else:
        s  = 2.0 * math.sqrt(1.0 + r22 - r00 - r11)
        qw = (r10 - r01) / s
        qx = (r02 + r20) / s
        qy = (r12 + r21) / s
        qz = 0.25 * s

    return pos, (qw, qx, qy, qz)


# ─────────────────────────────────────────────
#  Pose collector
# ─────────────────────────────────────────────

def _parse_poses(root_pose, result: dict, time: float) -> None:
    """Recursively collect pose keyframes.
    Zero-weight poses are skipped but their children are still traversed
    because a child may have its own non-zero weight.
    """
    for pose in root_pose.GetChildren():
        if pose.class_name != "Pose":
            continue

        if pose.get("Weight", 1.0) > 0:
            track = f"{root_pose.name}.{pose.name}"

            if track not in result:
                result[track] = []

            pos, quat = _cframe_to_pos_quat(pose.get("CFrame"))

            result[track].append({
                "time":        time,
                "pos":         pos,
                "rot":         quat,           # (w, x, y, z) Blender order
                "easingstyle": pose.get("EasingStyle",     5),
                "easingdir":   pose.get("EasingDirection", 2),
            })

        # Always recurse — children may have non-zero weight
        _parse_poses(pose, result, time)


# ─────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────

def read_animation(ks) -> dict:
    """Parse a KeyframeSequence into sparse per-bone keyframe data.

    Returns:
        {
          "name"     : str,
          "loop"     : bool,
          "priority" : int,
          "length"   : float,         total duration in seconds
          "keyframes": {
            "ParentBone.ChildBone": [
              {
                "time"       : float,
                "pos"        : (x, y, z),
                "rot"        : (w, x, y, z),  Blender component order
                "easingstyle": int,
                "easingdir"  : int,
              },
              ...  sorted by time ascending
            ],
            ...
          }
        }

    Track key format "ParentBone.ChildBone" — bone name is track.split(".")[1].
    """
    if ks is None:
        raise ValueError("KeyframeSequence is None — check FindFirstChildOfClass.")
    if ks.class_name != "KeyframeSequence":
        raise ValueError(f"Expected KeyframeSequence, got {ks.class_name!r}.")

    keyframes: dict  = {}
    length:    float = 0.0

    for kf_inst in ks.GetChildren():
        if kf_inst.class_name != "Keyframe":
            continue

        time = kf_inst.get("Time", 0.0)
        if time > length:
            length = time

        # Each top-level child of a Keyframe is a root pose (e.g. HumanoidRootPart).
        # We pass it as the parent — _parse_poses will add its CHILDREN as tracks.
        for pose_inst in kf_inst.GetChildren():
            if pose_inst.class_name == "Pose":
                _parse_poses(pose_inst, keyframes, time)

    for kf_list in keyframes.values():
        kf_list.sort(key=lambda k: k["time"])

    return {
        "name":      ks.get("Name", "Animation"),
        "loop":      ks.get("Loop", False),
        "priority":  ks.get("Priority", 2),
        "length":    length,
        "keyframes": keyframes,
    }


def print_summary(data: dict) -> None:
    """Print a human-readable summary for debugging."""
    print(f"Name     : {data['name']}")
    print(f"Loop     : {data['loop']}")
    print(f"Length   : {data.get('length', '?'):.3f}s")
    print(f"Tracks   : {len(data['keyframes'])}")
    for track, kfs in data["keyframes"].items():
        times = [round(k["time"], 4) for k in kfs]
        print(f"  {track:<36} {len(kfs):>3} kf  {times}")