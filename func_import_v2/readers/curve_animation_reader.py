"""
curve_animation_reader.py
─────────────────────────
Converts a Roblox CurveAnimation (parsed by rbxm_reader.py) into
sparse per-bone keyframe data ready for the Blender animation script.

CurveAnimation structure (from rbxm tree):
  CurveAnimation
    Folder (root part, e.g. "HumanoidRootPart")
      Folder (bone, e.g. "LowerTorso")
        Vector3Curve "Position"
          FloatCurve "X"   ← ValuesAndTimes binary
          FloatCurve "Y"
          FloatCurve "Z"
        EulerRotationCurve "Rotation"  ← has RotationOrder property
          FloatCurve "X"
          FloatCurve "Y"
          FloatCurve "Z"
        Folder (child bone, e.g. "UpperTorso")
          ... (recursive)

FloatCurve binary format (ValuesAndTimes):
  uint32  kf_count        total keyframes
  uint32  segment_count   number of non-trivial segments (0 = constant curve)

  If segment_count == 0 (constant / identity curve):
    uint32  interp_mode   (usually 1)
    float32 const_value   single constant value for the entire curve

  If segment_count > 0:
    Per keyframe (14 bytes each):
      uint8   interp_mode   (0=constant, 1=linear, 2=cubic)
      uint8   reserved
      float32 value
      float32 left_tangent
      float32 right_tangent
    Trailing time data:
      uint32  time_format   (usually 1)
      uint32  time_count    (matches kf_count)
      float32[] times       one per keyframe

Rotation uses Euler angles (radians), converted to quaternion by rotation order.
RotationOrder enum: 0=XYZ, 1=XZY, 2=YZX, 3=YXZ, 4=ZXY, 5=ZYX
"""

import struct
import math


# ─────────────────────────────────────────────
#  Euler rotation order mapping
# ─────────────────────────────────────────────

ROTATION_ORDERS = {
    0: "XYZ",
    1: "XZY",
    2: "YZX",
    3: "YXZ",
    4: "ZXY",
    5: "ZYX",
}


# ─────────────────────────────────────────────
#  Euler → Quaternion conversion
#  Derived from the SpinCalc decomposition:
#    mathworks.com/matlabcentral/fileexchange/20696
#  and the Three.js Quaternion.setFromEuler approach:
#    github.com/mrdoob/three.js
#
#  Each intrinsic Euler rotation R(order) = R_a3(z) @ R_a2(y) @ R_a1(x)
#  can be decomposed using half-angle products of the three axes.
# ─────────────────────────────────────────────

def _euler_to_quat(angle_x, angle_y, angle_z, order="XYZ"):
    """Convert intrinsic Euler angles (radians) to a unit quaternion.

    Uses the half-angle decomposition from the SpinCalc / Three.js method.
    Each rotation order defines a unique product of half-angle sin/cos terms.

    Args:
        angle_x: rotation around X axis in radians
        angle_y: rotation around Y axis in radians
        angle_z: rotation around Z axis in radians
        order:   intrinsic rotation order string, e.g. "XYZ", "ZXY"

    Returns:
        (w, x, y, z) quaternion in Blender component order
    """
    # Half-angle cosines and sines for each axis
    hx = angle_x * 0.5
    hy = angle_y * 0.5
    hz = angle_z * 0.5

    cx, sx = math.cos(hx), math.sin(hx)
    cy, sy = math.cos(hy), math.sin(hy)
    cz, sz = math.cos(hz), math.sin(hz)

    # Products used across all orders
    # Each order picks a unique combination of these 8 products
    sss = sx * sy * sz
    ssc = sx * sy * cz
    scs = sx * cy * sz
    scc = sx * cy * cz
    css = cx * sy * sz
    csc = cx * sy * cz
    ccs = cx * cy * sz
    ccc = cx * cy * cz

    # Compose quaternion (w, x, y, z) based on rotation order
    # The sign pattern for each order is derived from the rotation matrix product
    if order == "XYZ":
        w = ccc - sss
        x = scc + css
        y = csc - scs
        z = ccs + ssc
    elif order == "YXZ":
        w = ccc + sss
        x = scc + css
        y = csc - scs
        z = ccs - ssc
    elif order == "ZXY":
        w = ccc - sss
        x = css - scc
        y = csc + scs
        z = ccs + ssc
    elif order == "ZYX":
        w = ccc + sss
        x = css - scc
        y = csc + scs
        z = ccs - ssc
    elif order == "YZX":
        w = ccc - sss
        x = scc + css
        y = csc + scs
        z = ccs - ssc
    elif order == "XZY":
        w = ccc + sss
        x = scc - css
        y = csc - scs
        z = ccs + ssc
    else:
        # Default fallback to XYZ
        w = ccc - sss
        x = scc + css
        y = csc - scs
        z = ccs + ssc

    return (w, x, y, z)


# ─────────────────────────────────────────────
#  FloatCurve binary decoder
# ─────────────────────────────────────────────

def _decode_float_curve(raw_bytes, curve_name=""):
    """Decode a FloatCurve ValuesAndTimes binary blob into keyframe list.

    Binary layout:
      uint32  header_word    (type/version, usually 2)
      uint32  entry_count    (actual number of keyframe entries)

      If entry_count == 0 (constant curve):
        uint32  interp_mode
        float32 const_value

      If entry_count > 0:
        Per entry (14 bytes): interp(1) + pad(1) + value(4) + lt(4) + rt(4)
        Trailing: time_format(4) + time_count(4) + uint32[] time_ticks

    Returns list of dicts with time, value, interp_mode, left_tangent, right_tangent.
    """
    if raw_bytes is None or len(raw_bytes) < 8:
        return []

    n = len(raw_bytes)
    header_word = struct.unpack_from("<I", raw_bytes, 0)[0]
    entry_count = struct.unpack_from("<I", raw_bytes, 4)[0]

    if header_word == 0 and entry_count == 0:
        return []

    # Constant curve: entry_count == 0, total size = 16 bytes
    # Format: header(4) + 0(4) + interp(4) + value(4)
    if entry_count == 0:
        interp = struct.unpack_from("<I", raw_bytes, 8)[0]
        const_val = struct.unpack_from("<f", raw_bytes, 12)[0]
        return [{
            "time": 0.0,
            "value": const_val,
            "interp_mode": interp,
            "left_tangent": 0.0,
            "right_tangent": 0.0,
        }]

    # Full curve: header(8) + entry_count * 14 bytes + trailing time data
    KF_STRIDE = 14  # interp(1) + pad(1) + value(4) + lt(4) + rt(4)
    keyframes = []
    off = 8

    for i in range(entry_count):
        if off + KF_STRIDE > n:
            print(f"[CurveAnim] WARNING: truncated at entry {i}/{entry_count}, off={off}, n={n}")
            break

        interp_mode = raw_bytes[off]
        # off+1 is reserved/padding byte
        value = struct.unpack_from("<f", raw_bytes, off + 2)[0]
        left_tangent = struct.unpack_from("<f", raw_bytes, off + 6)[0]
        right_tangent = struct.unpack_from("<f", raw_bytes, off + 10)[0]

        keyframes.append({
            "time": 0.0,  # placeholder, filled from trailing data
            "value": value,
            "interp_mode": interp_mode,
            "left_tangent": left_tangent,
            "right_tangent": right_tangent,
        })
        off += KF_STRIDE

    # Parse trailing time data: time_format(4) + time_count(4) + uint32[] time_ticks
    # Times are stored as uint32 ticks, NOT float32 seconds!
    TICKS_PER_SECOND = 2400.0

    if off + 8 <= n:
        time_format = struct.unpack_from("<I", raw_bytes, off)[0]
        time_count = struct.unpack_from("<I", raw_bytes, off + 4)[0]
        off += 8

        raw_ticks = []
        for i in range(min(time_count, len(keyframes))):
            if off + 4 > n:
                break
            ticks = struct.unpack_from("<I", raw_bytes, off)[0]
            raw_ticks.append(ticks)
            off += 4

        # Convert ticks to seconds
        for i, ticks in enumerate(raw_ticks):
            keyframes[i]["time"] = ticks / TICKS_PER_SECOND

    return keyframes


# ─────────────────────────────────────────────
#  Cubic Hermite spline interpolation
# ─────────────────────────────────────────────

def _hermite_interpolate(kf_before, kf_after, blend, duration):
    """Cubic Hermite spline interpolation between two keyframes.

    Standard Hermite basis polynomials:
      h00(t) =  2t^3 - 3t^2 + 1   (value at start)
      h10(t) =   t^3 - 2t^2 + t   (tangent at start)
      h01(t) = -2t^3 + 3t^2       (value at end)
      h11(t) =   t^3 -  t^2       (tangent at end)

    Args:
        kf_before: previous keyframe dict
        kf_after:  next keyframe dict
        blend:     interpolation factor 0..1
        duration:  time span between the two keyframes
    """
    start_val = kf_before["value"]
    end_val = kf_after["value"]
    start_slope = kf_before["right_tangent"] * duration
    end_slope = kf_after["left_tangent"] * duration

    blend_sq = blend * blend
    blend_cb = blend_sq * blend

    h00 = 2.0 * blend_cb - 3.0 * blend_sq + 1.0
    h10 = blend_cb - 2.0 * blend_sq + blend
    h01 = -2.0 * blend_cb + 3.0 * blend_sq
    h11 = blend_cb - blend_sq

    return h00 * start_val + h10 * start_slope + h01 * end_val + h11 * end_slope


# ─────────────────────────────────────────────
#  Tree walker: recurse bone hierarchy
# ─────────────────────────────────────────────

def _walk_bones(folder_inst, parent_name, result):
    """Recursively walk the CurveAnimation Folder hierarchy.

    Each Folder is a bone. Inside a bone folder we look for:
      - Vector3Curve "Position" → 3× FloatCurve X/Y/Z
      - EulerRotationCurve "Rotation" → 3× FloatCurve X/Y/Z + RotationOrder

    Child Folders inside a bone are sub-bones (recursive).
    """
    for child in folder_inst.GetChildren():
        if child.class_name == "Folder":
            bone_name = child.name
            track_key = f"{parent_name}.{bone_name}"

            pos_curves = {"x": [], "y": [], "z": []}
            rot_curves = {"x": [], "y": [], "z": []}
            rot_order = "XYZ"

            for prop_child in child.GetChildren():
                if prop_child.class_name == "Vector3Curve" and prop_child.name == "Position":
                    for fc in prop_child.GetChildren():
                        if fc.class_name == "FloatCurve":
                            axis = fc.name.lower()
                            if axis in pos_curves:
                                vat = fc.get("ValuesAndTimes")
                                if isinstance(vat, (bytes, bytearray)):
                                    pos_curves[axis] = _decode_float_curve(vat, f"{track_key}.Pos.{axis}")

                elif prop_child.class_name == "EulerRotationCurve" and prop_child.name == "Rotation":
                    rot_order_idx = prop_child.get("RotationOrder", 0)
                    rot_order = ROTATION_ORDERS.get(rot_order_idx, "XYZ")

                    for fc in prop_child.GetChildren():
                        if fc.class_name == "FloatCurve":
                            axis = fc.name.lower()
                            if axis in rot_curves:
                                vat = fc.get("ValuesAndTimes")
                                if isinstance(vat, (bytes, bytearray)):
                                    rot_curves[axis] = _decode_float_curve(vat, f"{track_key}.Rot.{axis}")

                elif prop_child.class_name == "Folder":
                    # Sub-bone: will be handled in recursive call below
                    pass

            # Store if we found any data
            has_pos = any(len(v) > 0 for v in pos_curves.values())
            has_rot = any(len(v) > 0 for v in rot_curves.values())

            if has_pos or has_rot:
                result[track_key] = {
                    "position": pos_curves,
                    "rotation": rot_curves,
                    "rotation_order": rot_order,
                }

            # Recurse into child bone folders
            _walk_bones(child, bone_name, result)


# ─────────────────────────────────────────────
#  Collect all unique times across axes
# ─────────────────────────────────────────────

def _collect_times(pos_curves, rot_curves):
    """Gather sorted unique time values from all axis curves."""
    times = set()
    for axis_kfs in pos_curves.values():
        for kf in axis_kfs:
            times.add(kf["time"])
    for axis_kfs in rot_curves.values():
        for kf in axis_kfs:
            times.add(kf["time"])
    return sorted(times)


def _sample_axis_at_time(kf_list, t):
    """Sample a single FloatCurve axis at a given time.

    Interpolation modes:
      0 = constant (hold previous value until next keyframe)
      1 = linear blend between keyframes
      2 = cubic Hermite spline using tangent data
    """
    if not kf_list:
        return 0.0

    # If only one keyframe or t <= first keyframe time
    if len(kf_list) == 1 or t <= kf_list[0]["time"]:
        return kf_list[0]["value"]

    # If t >= last keyframe time
    if t >= kf_list[-1]["time"]:
        return kf_list[-1]["value"]

    # Find bracketing keyframes
    for i in range(1, len(kf_list)):
        if kf_list[i]["time"] >= t:
            kf_before = kf_list[i - 1]
            kf_after = kf_list[i]
            break
    else:
        return kf_list[-1]["value"]

    # Exact match with start keyframe
    if t == kf_before["time"]:
        return kf_before["value"]

    duration = kf_after["time"] - kf_before["time"]
    if duration <= 0:
        return kf_before["value"]

    blend = (t - kf_before["time"]) / duration

    # Constant interpolation: hold value until next keyframe
    if kf_before["interp_mode"] == 0:
        return kf_before["value"]

    # Cubic Hermite spline
    if kf_before["interp_mode"] == 2:
        return _hermite_interpolate(kf_before, kf_after, blend, duration)

    # Linear (default for mode 1 and any unknown modes)
    return kf_before["value"] * (1.0 - blend) + kf_after["value"] * blend


# ─────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────

def read_curve_animation(ca):
    """Parse a CurveAnimation into sparse per-bone keyframe data.

    Output format is compatible with blender_api_apply_animation:
      {
        "name": str,
        "loop": bool,
        "priority": int,
        "length": float (seconds),
        "keyframes": {
          "ParentBone.ChildBone": [
            {
              "time": float,
              "pos":  (x, y, z),
              "rot":  (w, x, y, z),   quaternion, Blender order
              "easingstyle": 5,
              "easingdir": 2,
            },
            ...
          ],
          ...
        }
      }

    Track key format "ParentBone.ChildBone" — same as KeyframeSequence reader.
    """
    if ca is None:
        raise ValueError("CurveAnimation is None.")
    if ca.class_name != "CurveAnimation":
        raise ValueError(f"Expected CurveAnimation, got {ca.class_name!r}.")

    # Walk the bone hierarchy to extract raw curve data
    raw_tracks = {}
    for root_folder in ca.GetChildren():
        if root_folder.class_name == "Folder":
            root_part = root_folder.name  # e.g. "HumanoidRootPart"
            _walk_bones(root_folder, root_part, raw_tracks)

    # Convert raw curve tracks into the unified keyframe format
    keyframes = {}
    length = 0.0

    for track_key, track_data in raw_tracks.items():
        pos_curves = track_data["position"]
        rot_curves = track_data["rotation"]
        rot_order = track_data["rotation_order"]

        # Collect all unique times across all 6 axis curves
        all_times = _collect_times(pos_curves, rot_curves)

        if not all_times:
            continue

        track_kfs = []
        for t in all_times:
            # Sample each position axis
            px = _sample_axis_at_time(pos_curves.get("x", []), t)
            py = _sample_axis_at_time(pos_curves.get("y", []), t)
            pz = _sample_axis_at_time(pos_curves.get("z", []), t)

            # Sample each rotation axis (Euler radians)
            rx = _sample_axis_at_time(rot_curves.get("x", []), t)
            ry = _sample_axis_at_time(rot_curves.get("y", []), t)
            rz = _sample_axis_at_time(rot_curves.get("z", []), t)

            # Convert Euler angles to quaternion
            qw, qx, qy, qz = _euler_to_quat(rx, ry, rz, rot_order)

            track_kfs.append({
                "time": t,
                "pos": (px, py, pz),
                "rot": (qw, qx, qy, qz),
                "easingstyle": 5,  # CubicV2 (not used for CurveAnim, placeholder)
                "easingdir": 2,
            })

            if t > length:
                length = t

        if track_kfs:
            keyframes[track_key] = track_kfs

    result = {
        "name": ca.get("Name", "CurveAnimation"),
        "loop": ca.get("Loop", False),
        "priority": ca.get("Priority", 2),
        "length": length,
        "keyframes": keyframes,
    }

    # Debug summary
    print(f"[CurveAnim] === PARSED: '{result['name']}' ===")
    print(f"[CurveAnim]   Length={length:.4f}s, Tracks={len(keyframes)}, Loop={result['loop']}")
    for tk, kfs in keyframes.items():
        times = [round(k["time"], 4) for k in kfs[:5]]
        print(f"[CurveAnim]   {tk}: {len(kfs)} kf, times(first5)={times}")

    return result


def print_summary(data):
    """Print a human-readable summary for debugging."""
    print(f"Name     : {data['name']}")
    print(f"Loop     : {data['loop']}")
    print(f"Length   : {data.get('length', '?'):.3f}s")
    print(f"Tracks   : {len(data['keyframes'])}")
    for track, kfs in data["keyframes"].items():
        times = [round(k["time"], 4) for k in kfs]
        print(f"  {track:<36} {len(kfs):>3} kf  {times}")
