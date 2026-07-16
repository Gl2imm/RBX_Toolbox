"""FACS (facial animation) reader for Roblox meshes.

Parses the FACS data block that ships inside Dynamic Head meshes (mesh format
v5.00 binary, and the "FACS" chunk of v6.00/v7.00) and can build a preview
animation that cycles the head's own facial expressions onto its imported
face-bone armature.

Binary layout follows the community spec:
    https://devforum.roblox.com/t/roblox-filemesh-format-specification/326114

    struct FileMeshFacsData {
        uint  sizeof_faceBoneNamesBlob;
        uint  sizeof_faceControlNamesBlob;
        ulong sizeof_quantizedTransforms;
        uint  sizeof_twoPoseCorrectives;
        uint  sizeof_threePoseCorrectives;
        byte  faceBoneNamesBlob[...];       // null-separated UTF-8
        byte  faceControlNamesBlob[...];    // null-separated UTF-8
        QuantizedTransforms quantizedTransforms;  // px,py,pz,rx,ry,rz
        TwoPoseCorrective   twoPoseCorrectives[...];   // 2x uint16
        ThreePoseCorrective threePoseCorrectives[...]; // 3x uint16
    }
    struct QuantizedMatrix {
        ushort version;   // 1 = raw floats, 2 = quantized uint16
        uint   rows;      // = bone count
        uint   cols;      // = control count
        // v1: float[rows*cols]
        // v2: float min; float max; ushort[rows*cols]
    }
    Dequantize (v2): value = min + q * (max - min) / 65535

Rotation channels are stored in DEGREES, and each delta is re-expressed from the
Roblox joint-local frame into Blender's bone-local frame (change-of-basis) to
correct for Blender's auto-computed bone roll — both handled in
build_facs_animation. Tuning knobs: POS_SCALE, ROT_IS_DEGREES, ROT_EULER_ORDER.
"""

import struct


### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


# ---------------------------------------------------------------------------
# Binary parsing
# ---------------------------------------------------------------------------

def _split_names(blob):
    """Null-separated UTF-8 string blob -> list of names (empties dropped)."""
    return [p.decode("utf-8", "replace") for p in blob.split(b"\x00") if p]


def _read_quant_matrix(raw, off):
    """Read one QuantizedMatrix. Returns (matrix, new_offset).
    matrix is a 2D list indexed [row=bone][col=control] of floats."""
    version = struct.unpack_from("<H", raw, off)[0]; off += 2
    rows = struct.unpack_from("<I", raw, off)[0]; off += 4
    cols = struct.unpack_from("<I", raw, off)[0]; off += 4
    n = rows * cols

    if version == 1:
        vals = struct.unpack_from("<%df" % n, raw, off) if n else ()
        off += 4 * n
    elif version == 2:
        vmin = struct.unpack_from("<f", raw, off)[0]; off += 4
        vmax = struct.unpack_from("<f", raw, off)[0]; off += 4
        q = struct.unpack_from("<%dH" % n, raw, off) if n else ()
        off += 2 * n
        prec = (vmax - vmin) / 65535.0
        vals = tuple(vmin + qv * prec for qv in q)
    else:
        raise ValueError(f"Unknown QuantizedMatrix version {version}")

    matrix = [[vals[r * cols + c] for c in range(cols)] for r in range(rows)]
    return matrix, off


def parse_facs(raw):
    """Parse a FileMeshFacsData block (bytes). For the v6/v7 chunk, strip the
    leading uint facsDataSize before calling this (mesh_reader does that).

    Returns a dict, or None on any failure:
        {
          "bones":      [bone_name, ...],       # rows
          "controls":   [control_name, ...],    # cols (incl. correctives)
          "transforms": {"px":M,"py":M,"pz":M,"rx":M,"ry":M,"rz":M},
          "twoPose":    [(i0,i1), ...],
          "threePose":  [(i0,i1,i2), ...],
        }
    where each M is a 2D list [bone][control] of floats.
    """
    try:
        off = 0
        sz_bone = struct.unpack_from("<I", raw, off)[0]; off += 4
        sz_ctrl = struct.unpack_from("<I", raw, off)[0]; off += 4
        sz_quant = struct.unpack_from("<Q", raw, off)[0]; off += 8  # noqa: F841
        sz_two = struct.unpack_from("<I", raw, off)[0]; off += 4
        sz_three = struct.unpack_from("<I", raw, off)[0]; off += 4

        bones = _split_names(raw[off:off + sz_bone]); off += sz_bone
        controls = _split_names(raw[off:off + sz_ctrl]); off += sz_ctrl

        transforms = {}
        for key in ("px", "py", "pz", "rx", "ry", "rz"):
            transforms[key], off = _read_quant_matrix(raw, off)

        two = []
        for _ in range(sz_two // 4):
            two.append(struct.unpack_from("<HH", raw, off)); off += 4
        three = []
        for _ in range(sz_three // 6):
            three.append(struct.unpack_from("<HHH", raw, off)); off += 6

        result = {
            "bones": bones,
            "controls": controls,
            "transforms": transforms,
            "twoPose": [tuple(t) for t in two],
            "threePose": [tuple(t) for t in three],
        }
        dprint(f"parse_facs: {len(bones)} bones, {len(controls)} controls")
        return result
    except Exception as e:
        dprint(f"parse_facs failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Animation building (Blender)
# ---------------------------------------------------------------------------

# --- Tuning knobs (adjust these if the poses still look wrong on real heads) -
POS_SCALE = 1.0            # position deltas are studs; imported armature is 1:1
ROT_IS_DEGREES = True      # FACS rotation channels are stored in DEGREES
ROT_EULER_ORDER = 'XYZ'    # euler order used to rebuild the rotation matrix
# ---------------------------------------------------------------------------


def _matrix_has_motion(transforms, bone_index, eps=1e-6):
    """True if this bone has any non-zero delta across any control/channel."""
    for m in transforms.values():
        row = m[bone_index] if bone_index < len(m) else None
        if row and any(abs(v) > eps for v in row):
            return True
    return False


def _basis_change(pose_bone, rbx_world_matrix):
    """3x3 change-of-basis C mapping a vector/rotation expressed in the Roblox
    joint-local frame into this Blender bone's local frame.

        C = M_bl^-1 @ M_rbx

    where M_bl is the Blender bone's rest orientation (auto-rolled by the
    importer) and M_rbx is the same bone's Roblox joint frame (already converted
    to Blender axes). Both are orthonormal, so C is orthonormal. If the Roblox
    frame is unknown, returns identity (deltas applied as-is, less accurate).
    """
    from mathutils import Matrix
    m_bl = pose_bone.bone.matrix_local.to_3x3()
    if rbx_world_matrix is None:
        return Matrix.Identity(3)
    try:
        return m_bl.inverted() @ rbx_world_matrix.to_3x3()
    except Exception:
        return Matrix.Identity(3)


def build_facs_animation(arm_obj, facs, bone_world_matrices=None,
                         action_name="FACS_Preview", frame_step=1):
    """Build a preview action on `arm_obj` that steps through each FACS control
    as a distinct pose frame. Returns (action, info_str) or (None, error_str).

    bone_world_matrices: optional {bone_name: mathutils.Matrix} giving each face
    bone's Roblox joint rest frame (already in Blender axes). Used to correct for
    Blender's auto-computed bone roll; without it the poses are less accurate.

    Only bones present on the armature AND animated by the FACS data are keyed;
    each control frame is a full snapshot so frames read as discrete expressions.
    """
    import bpy, math
    from mathutils import Vector, Euler

    bones = facs.get("bones") or []
    controls = facs.get("controls") or []
    T = facs.get("transforms") or {}
    if not bones or not controls or len(T) < 6:
        return None, "FACS data incomplete"

    bone_world_matrices = bone_world_matrices or {}
    pose_bones = arm_obj.pose.bones

    # Precompute per-bone: index, pose_bone, change-of-basis C and its transpose.
    active = []
    for bi, bname in enumerate(bones):
        pb = pose_bones.get(bname)
        if pb is not None and _matrix_has_motion(T, bi):
            C = _basis_change(pb, bone_world_matrices.get(bname))
            pb.rotation_mode = 'QUATERNION'
            active.append((bi, pb, C, C.transposed()))
    if not active:
        return None, "No matching animated FACS bones on armature"

    # Fresh action
    if not arm_obj.animation_data:
        arm_obj.animation_data_create()
    action = bpy.data.actions.new(name=action_name)
    arm_obj.animation_data.action = action

    px, py, pz = T["px"], T["py"], T["pz"]
    rx, ry, rz = T["rx"], T["ry"], T["rz"]
    to_rad = math.radians if ROT_IS_DEGREES else (lambda v: v)

    for ci in range(len(controls)):
        frame = 1 + ci * frame_step
        for bi, pb, C, Ct in active:
            # Position: Roblox joint-local -> Blender bone-local.
            p = C @ Vector((px[bi][ci], py[bi][ci], pz[bi][ci]))
            pb.location = p * POS_SCALE
            # Rotation: build in Roblox joint-local, conjugate into bone-local.
            R = Euler((to_rad(rx[bi][ci]), to_rad(ry[bi][ci]), to_rad(rz[bi][ci])),
                      ROT_EULER_ORDER).to_matrix()
            pb.rotation_quaternion = (C @ R @ Ct).to_quaternion()
            pb.keyframe_insert("location", frame=frame)
            pb.keyframe_insert("rotation_quaternion", frame=frame)

    # Bind the action slot so it evaluates on Blender 4.4+ (slotted actions).
    slots = getattr(action, "slots", None)
    if slots and len(slots) > 0 and getattr(arm_obj.animation_data, "action_slot", None) is None:
        try:
            arm_obj.animation_data.action_slot = slots[0]
        except Exception:
            pass

    info = f"FACS preview: {len(controls)} expressions on {len(active)} bones"
    dprint(info)
    return action, info
