import struct
import pprint
import os

from . import draco_decoder

# ============================================================
# DEBUG CONTROLS
# ============================================================
# Set to True to write parsed mesh data to a text file
DEBUG_WRITE_OUTPUT = False
# Path for the debug output text file
DEBUG_OUTPUT_PATH = r"mesh_reader_output.txt"


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def parse(data):
    """
    Parse raw bytes of a Roblox .mesh file.
    Detects the version from the header and routes to the
    correct parser (text, binary, or chunked).
    Returns a dictionary with standardized mesh data keys.
    """
    # Read the 12-byte version header: "version X.XX"
    try:
        header_text = data[:12].decode("ascii")
    except UnicodeDecodeError:
        raise ValueError("Data is not a valid Roblox mesh (invalid header encoding).")
    version = header_text[8:].strip()

    print(f"Mesh version: {version}")

    # Route to the appropriate parser
    if version in ("1.00", "1.01"):
        result = parse_text(data, version)
    elif version in ("2.00", "3.00", "3.01", "4.00", "4.01", "5.00"):
        result = parse_bin(data, version)
    elif version in ("6.00", "7.00"):
        result = parse_chunked(data, version)
    else:
        raise ValueError(f"Unsupported mesh version: {version}")

    # Debug: write parsed output to text file
    if DEBUG_WRITE_OUTPUT:
        try:
            with open(DEBUG_OUTPUT_PATH, "w", encoding="utf-8") as debug_file:
                # Build a safe copy that avoids circular bone->parent references
                safe_result = _make_debug_safe(result)
                pprint.pprint(safe_result, stream=debug_file, width=120)
            print(f"Debug output written to: {DEBUG_OUTPUT_PATH}")
        except Exception as err:
            print(f"Failed to write debug output: {err}")

    return result


def _make_debug_safe(mesh_dict):
    """
    Create a copy of the mesh dictionary that replaces circular
    bone parent references with just the parent bone name,
    so pprint doesn't recurse infinitely.
    """
    safe = dict(mesh_dict)
    if "bones" in safe and safe["bones"]:
        safe_bones = []
        for bone in safe["bones"]:
            safe_bone = dict(bone)
            if safe_bone.get("parent") is not None:
                safe_bone["parent"] = safe_bone["parent"]["name"]
            safe_bones.append(safe_bone)
        safe["bones"] = safe_bones
    return safe


# ============================================================
# TEXT PARSER — v1.00, v1.01
# ============================================================

def parse_text(data, version):
    """
    Parse a version 1.xx mesh file.
    The file is plain ASCII with 3 lines:
      Line 1: version header
      Line 2: face count
      Line 3: concatenated bracket-delimited vertex vectors
    Returns the standard mesh dictionary.
    """
    text = data.decode("ascii")
    lines = text.split("\n")
    # Remove empty trailing lines
    lines = [l.strip() for l in lines if l.strip()]

    if len(lines) < 3:
        raise ValueError("v1.x mesh must have at least 3 lines")

    face_count = int(lines[1])
    raw_data = lines[2]

    # Strip outer brackets and split by "]["
    raw_data = raw_data.strip()
    if raw_data.startswith("["):
        raw_data = raw_data[1:]
    if raw_data.endswith("]"):
        raw_data = raw_data[:-1]
    vector_strings = raw_data.split("][")

    expected_vectors = face_count * 9  # 3 verts/face × 3 vectors/vert
    if len(vector_strings) != expected_vectors:
        raise ValueError(
            f"Expected {expected_vectors} vectors, got {len(vector_strings)}"
        )

    # Scale factor: v1.00 meshes are 2x oversized
    scale = 0.5 if version == "1.00" else 1.0

    vertices = []
    normals = []
    uvs = []
    faces = []
    total_verts = face_count * 3

    for vert_idx in range(total_verts):
        base = vert_idx * 3

        # Position vector
        pos_parts = vector_strings[base].split(",")
        px = float(pos_parts[0]) * scale
        py = float(pos_parts[1]) * scale
        pz = float(pos_parts[2]) * scale
        vertices.extend([px, py, pz])

        # Normal vector
        norm_parts = vector_strings[base + 1].split(",")
        nx = float(norm_parts[0])
        ny = float(norm_parts[1])
        nz = float(norm_parts[2])
        normals.extend([nx, ny, nz])

        # UV vector (only first 2 components)
        # v1.00 stores tex_V in OpenGL convention (V=0 at bottom),
        # which Roblox docs call "upside down" vs their DirectX standard.
        # Blender also uses OpenGL convention, so NO flip is needed here.
        # (The v2+ binary parser flips because v2+ stores V in DirectX convention.)
        uv_parts = vector_strings[base + 2].split(",")
        tu = float(uv_parts[0])
        tv = float(uv_parts[1])
        uvs.extend([tu, tv])

        # Faces are sequential — each vertex is unique in v1.x
        faces.append(vert_idx)

    return {
        "version":      version,
        "vertices":     vertices,
        "normals":      normals,
        "uvs":          uvs,
        "tangents":     [],
        "vertexColors": None,
        "faces":        faces,
        "lods":         [0, face_count],
    }


# ============================================================
# BINARY PARSER — v2.00, v3.xx, v4.xx, v5.00
# ============================================================

def parse_bin(data, version):
    """
    Parse a version 2.00 through 5.00 mesh file.
    The file has a text version header followed by a binary
    fixed-layout structure whose fields vary by version.
    Returns the standard mesh dictionary, including bones/skinning
    data for v4+ meshes that contain skeletal data.
    """
    offset = 0

    # --- Skip past the "version X.XX" + newline header ---
    offset = 12  # "version X.XX"
    # Handle CR+LF or just LF newline
    if data[offset] == 0x0D:
        offset += 2  # skip \r\n
    else:
        offset += 1  # skip \n

    data_begin = offset

    # --- Read version-specific header fields ---
    vertex_size = 40  # default for v4+/v5
    face_size = 12    # always 12 for faces
    lod_count = 0
    lod_size = 4
    bone_count = 0
    name_table_size = 0
    subset_count = 0
    facs_data_size = 0

    if version == "2.00":
        # v2 header: header_size(2) + vertex_size(1) + face_size(1) +
        #            vertex_count(4) + face_count(4)
        header_size = struct.unpack_from("<H", data, offset)[0]
        vertex_size = struct.unpack_from("<B", data, offset + 2)[0]
        face_size = struct.unpack_from("<B", data, offset + 3)[0]
        vertex_count = struct.unpack_from("<I", data, offset + 4)[0]
        face_count = struct.unpack_from("<I", data, offset + 8)[0]

    elif version in ("3.00", "3.01"):
        # v3 header: header_size(2) + vertex_size(1) + face_size(1) +
        #            lod_size(2) + lod_count(2) + vertex_count(4) + face_count(4)
        header_size = struct.unpack_from("<H", data, offset)[0]
        vertex_size = struct.unpack_from("<B", data, offset + 2)[0]
        face_size = struct.unpack_from("<B", data, offset + 3)[0]
        lod_size = struct.unpack_from("<H", data, offset + 4)[0]
        lod_count = struct.unpack_from("<H", data, offset + 6)[0]
        vertex_count = struct.unpack_from("<I", data, offset + 8)[0]
        face_count = struct.unpack_from("<I", data, offset + 12)[0]

    elif version in ("4.00", "4.01"):
        # v4 header: header_size(2) + padding(2) + vertex_count(4) +
        #            face_count(4) + lod_count(2) + bone_count(2) +
        #            name_table_size(4) + subset_count(2) + padding(2)
        header_size = struct.unpack_from("<H", data, offset)[0]
        vertex_count = struct.unpack_from("<I", data, offset + 4)[0]
        face_count = struct.unpack_from("<I", data, offset + 8)[0]
        lod_count = struct.unpack_from("<H", data, offset + 12)[0]
        bone_count = struct.unpack_from("<H", data, offset + 14)[0]
        name_table_size = struct.unpack_from("<I", data, offset + 16)[0]
        subset_count = struct.unpack_from("<H", data, offset + 20)[0]

    elif version == "5.00":
        # v5 header: same as v4 + facs fields
        header_size = struct.unpack_from("<H", data, offset)[0]
        vertex_count = struct.unpack_from("<I", data, offset + 4)[0]
        face_count = struct.unpack_from("<I", data, offset + 8)[0]
        lod_count = struct.unpack_from("<H", data, offset + 12)[0]
        bone_count = struct.unpack_from("<H", data, offset + 14)[0]
        name_table_size = struct.unpack_from("<I", data, offset + 16)[0]
        subset_count = struct.unpack_from("<H", data, offset + 20)[0]
        # skip 2 padding + skip 4 (facsDataFormat)
        facs_data_size = struct.unpack_from("<I", data, offset + 28)[0]

    # Seek past the header to the start of vertex data
    offset = data_begin + header_size

    # --- Read vertex data ---
    vertices, normals, uvs, tangents, vertex_colors = _read_vertices(
        data, offset, vertex_count, vertex_size
    )
    offset += vertex_count * vertex_size

    # --- Read skinning / envelope data (v4+ only, if bones exist) ---
    skin_indices = []
    skin_weights = []
    if version in ("4.00", "4.01", "5.00") and bone_count > 0:
        skin_indices, skin_weights = _read_skinning(data, offset, vertex_count)
        offset += vertex_count * 8  # 4 indices + 4 weights per vertex

    # --- Read face data ---
    faces = _read_faces(data, offset, face_count)
    offset += face_count * face_size
    # Skip any extra bytes per face beyond the 12 we read
    if face_size > 12:
        pass  # already accounted for in offset calculation

    # --- Read LOD offsets ---
    lods = _read_lods_bin(data, offset, lod_count, lod_size, face_count)
    offset += lod_count * lod_size

    # --- Read bone data (v4+/v5 only, if bones exist) ---
    bones = []
    if version in ("4.00", "4.01", "5.00") and bone_count > 0:
        bones = _read_bones(data, offset, bone_count, name_table_size)
        offset += bone_count * 60

    # --- Skip name table ---
    if name_table_size > 0:
        offset += name_table_size

    # --- Read subsets and remap skin indices ---
    if version in ("4.00", "4.01", "5.00") and subset_count > 0:
        _read_subsets_and_remap(data, offset, subset_count, skin_indices)
        offset += subset_count * 72

    # --- Skip FACS data (v5 only) ---
    if facs_data_size > 0:
        offset += facs_data_size

    # --- Build result dictionary ---
    result = {
        "version":      version,
        "vertices":     vertices,
        "normals":      normals,
        "uvs":          uvs,
        "tangents":     tangents,
        "vertexColors": vertex_colors if vertex_colors else None,
        "faces":        faces,
        "lods":         lods,
    }

    if bones:
        result["skinIndices"] = skin_indices
        result["skinWeights"] = skin_weights
        result["bones"] = bones

    return result


# ============================================================
# CHUNKED PARSER — v6.00, v7.00
# ============================================================

def parse_chunked(data, version):
    """
    Parse a version 6.00 or 7.00 mesh file.
    After the text header, data is organized into typed chunks
    that are read sequentially until end of file.
    Each chunk has an 8-byte type string, 4-byte version,
    4-byte payload size, then payload data.
    Returns the standard mesh dictionary.
    """
    offset = 12  # skip "version X.XX"
    # Handle newline (CR+LF or LF)
    if data[offset] == 0x0D:
        offset += 2
    else:
        offset += 1

    # Initialize result containers
    vertices = []
    normals = []
    uvs = []
    tangents = []
    vertex_colors = None
    faces = []
    lods = None
    skin_indices = []
    skin_weights = []
    bones = []

    # --- Read chunks until not enough bytes remain for a chunk header ---
    while offset + 16 <= len(data):
        # Chunk header: type(8) + version(4) + size(4)
        chunk_type = data[offset:offset + 8].decode("ascii").rstrip("\x00").strip()
        chunk_ver = struct.unpack_from("<I", data, offset + 8)[0]
        chunk_size = struct.unpack_from("<I", data, offset + 12)[0]
        chunk_data = data[offset + 16 : offset + 16 + chunk_size]
        offset += 16 + chunk_size

        if chunk_type == "COREMESH":
            if chunk_ver == 1:
                # Uncompressed core mesh — same vertex layout as binary parser
                vertices, normals, uvs, tangents, vertex_colors, faces = (
                    _parse_coremesh_v1(chunk_data)
                )
            elif chunk_ver == 2:
                # Draco-compressed mesh (v7.00)
                # First 4 bytes are a uint32 Draco payload size, skip them
                draco_payload = chunk_data[4:]
                draco_result = draco_decoder.decode_draco(bytes(draco_payload))
                vertices = draco_result.get("vertices", [])
                normals = draco_result.get("normals", [])
                uvs = draco_result.get("uvs", [])
                vertex_colors = draco_result.get("vertexColors", None)
                faces = draco_result.get("faces", [])
                tangents = []  # Draco payload does not include tangents

        elif chunk_type == "LODS":
            if chunk_ver == 1:
                lods = _parse_lods_chunk(chunk_data)

        elif chunk_type == "SKINNING":
            if chunk_ver == 1:
                skin_indices, skin_weights, bones = _parse_skinning_chunk(chunk_data)

        else:
            # Unknown or unneeded chunk (FACS, HSRAVIS, etc.) — skip
            pass

    # Default LODs if none were found
    if lods is None:
        face_count = len(faces) // 3
        lods = [0, face_count]

    result = {
        "version":      version,
        "vertices":     vertices,
        "normals":      normals,
        "uvs":          uvs,
        "tangents":     tangents,
        "vertexColors": vertex_colors,
        "faces":        faces,
        "lods":         lods,
    }

    if bones:
        result["skinIndices"] = skin_indices
        result["skinWeights"] = skin_weights
        result["bones"] = bones

    return result


# ============================================================
# CHUNK SUB-PARSERS
# ============================================================

def _parse_coremesh_v1(chunk_data):
    """
    Parse an uncompressed COREMESH v1 chunk.
    Reads vertex count, vertex data, face count, and face data.
    Vertex layout is identical to the binary parser (40 bytes each).
    Returns vertices, normals, uvs, tangents, vertex_colors, faces.
    """
    pos = 0
    num_verts = struct.unpack_from("<I", chunk_data, pos)[0]
    pos += 4

    # Each vertex is 40 bytes: pos(12) + norm(12) + uv(8) + tangent(4) + color(4)
    vertex_size = 40
    vertices, normals, uvs, tangents, vertex_colors = _read_vertices(
        chunk_data, pos, num_verts, vertex_size
    )
    pos += num_verts * vertex_size

    num_faces = struct.unpack_from("<I", chunk_data, pos)[0]
    pos += 4

    faces = _read_faces(chunk_data, pos, num_faces)

    return vertices, normals, uvs, tangents, vertex_colors, faces


def _parse_lods_chunk(chunk_data):
    """
    Parse a LODS v1 chunk.
    Reads lod_type, num_high_quality_lods, and the array of
    face-count boundary offsets.
    Returns the LOD offsets list, or a default if <= 2 entries.
    """
    pos = 0
    lod_type = struct.unpack_from("<H", chunk_data, pos)[0]
    pos += 2
    num_high_quality = struct.unpack_from("<B", chunk_data, pos)[0]
    pos += 1
    num_lods = struct.unpack_from("<I", chunk_data, pos)[0]
    pos += 4

    if num_lods <= 2:
        return None  # caller will use default

    lod_offsets = []
    for i in range(num_lods):
        val = struct.unpack_from("<I", chunk_data, pos)[0]
        lod_offsets.append(val)
        pos += 4

    return lod_offsets


def _parse_skinning_chunk(chunk_data):
    """
    Parse a SKINNING v1 chunk.
    Reads per-vertex skinning data, bones with name table,
    and subsets with bone index remapping.
    Returns skin_indices, skin_weights, bones.
    """
    pos = 0

    # --- Skinning per vertex ---
    num_verts = struct.unpack_from("<I", chunk_data, pos)[0]
    pos += 4
    skin_indices, skin_weights = _read_skinning(chunk_data, pos, num_verts)
    pos += num_verts * 8

    # --- Bones ---
    num_bones = struct.unpack_from("<I", chunk_data, pos)[0]
    pos += 4

    # The name table starts after all bone records + 4 bytes for name_table_size
    name_table_offset = pos + num_bones * 60 + 4

    bone_list = []
    for bone_idx in range(num_bones):
        bone, bytes_read = _read_single_bone(
            chunk_data, pos, bone_idx, bone_list, name_table_offset
        )
        bone_list.append(bone)
        pos += 60

    # Resolve forward parent references in a second pass
    for bone_idx, bone in enumerate(bone_list):
        parent_idx = bone.pop("_parent_index", None)
        if parent_idx is not None and parent_idx != 0xFFFF and parent_idx < len(bone_list):
            bone["parent"] = bone_list[parent_idx]

    # --- Skip name table ---
    name_table_size = struct.unpack_from("<I", chunk_data, pos)[0]
    pos += 4
    pos += name_table_size

    # --- Subsets ---
    num_subsets = struct.unpack_from("<I", chunk_data, pos)[0]
    pos += 4
    _read_subsets_and_remap(chunk_data, pos, num_subsets, skin_indices)

    return skin_indices, skin_weights, bone_list


# ============================================================
# SHARED BINARY READING HELPERS
# ============================================================

def _read_vertices(data, offset, vertex_count, vertex_size):
    """
    Read an array of mesh vertices from binary data.
    Each vertex contains position (3 floats), normal (3 floats),
    UV (2 floats, V flipped), tangent (4 signed bytes mapped to
    -1..+1), and optionally RGBA vertex color (4 bytes).
    Returns five lists: vertices, normals, uvs, tangents, vertex_colors.
    """
    vertices = []
    normals = []
    uvs = []
    tangents = []
    vertex_colors = []
    has_colors = vertex_size >= 40

    for i in range(vertex_count):
        base = offset + i * vertex_size

        # Position: 3 × float32 (12 bytes)
        px, py, pz = struct.unpack_from("<3f", data, base)
        vertices.extend([px, py, pz])

        # Normal: 3 × float32 (12 bytes)
        nx, ny, nz = struct.unpack_from("<3f", data, base + 12)
        normals.extend([nx, ny, nz])

        # UV: 2 × float32 (8 bytes), V is flipped
        tu, tv = struct.unpack_from("<2f", data, base + 24)
        uvs.extend([tu, 1.0 - tv])

        # Tangent: 4 × uint8 (4 bytes), each mapped from [0,254] to [-1,+1]
        t0, t1, t2, t3 = struct.unpack_from("<4B", data, base + 32)
        tangents.extend([
            t0 / 127.0 - 1.0,
            t1 / 127.0 - 1.0,
            t2 / 127.0 - 1.0,
            t3 / 127.0 - 1.0,
        ])

        # Vertex Color: 4 × uint8 (4 bytes), optional
        if has_colors:
            cr, cg, cb, ca = struct.unpack_from("<4B", data, base + 36)
            vertex_colors.extend([cr, cg, cb, ca])

    if not has_colors:
        vertex_colors = None

    return vertices, normals, uvs, tangents, vertex_colors


def _read_skinning(data, offset, vertex_count):
    """
    Read per-vertex skinning data: 4 bone indices (uint8 each)
    and 4 bone weights (uint8 each, normalized to 0.0–1.0).
    Returns two flat lists: skin_indices and skin_weights.
    """
    skin_indices = []
    skin_weights = []

    for i in range(vertex_count):
        base = offset + i * 8
        # 4 bone subset indices
        si0, si1, si2, si3 = struct.unpack_from("<4B", data, base)
        skin_indices.extend([si0, si1, si2, si3])
        # 4 bone weights, each byte / 255.0
        sw0, sw1, sw2, sw3 = struct.unpack_from("<4B", data, base + 4)
        skin_weights.extend([
            sw0 / 255.0,
            sw1 / 255.0,
            sw2 / 255.0,
            sw3 / 255.0,
        ])

    return skin_indices, skin_weights


def _read_faces(data, offset, face_count):
    """
    Read an array of triangle faces from binary data.
    Each face is 3 × uint32 vertex indices (12 bytes total).
    Returns a flat list of 0-based indices.
    """
    faces = []
    for i in range(face_count):
        base = offset + i * 12
        a, b, c = struct.unpack_from("<3I", data, base)
        faces.extend([a, b, c])
    return faces


def _read_lods_bin(data, offset, lod_count, lod_size, face_count):
    """
    Read LOD face-count boundary offsets from binary data.
    If lod_count <= 2, returns a default [0, face_count].
    Otherwise reads lod_count × uint32 values.
    Returns a list of face-count boundaries.
    """
    if lod_count <= 2:
        # Skip any LOD bytes that may still exist
        return [0, face_count]

    lod_offsets = []
    for i in range(lod_count):
        val = struct.unpack_from("<I", data, offset + i * lod_size)[0]
        lod_offsets.append(val)
    return lod_offsets


def _read_bones(data, offset, bone_count, name_table_size):
    """
    Read an array of bone records from binary data.
    Each bone is 60 bytes: name_offset(4), parent_index(2),
    lod_parent_index(2), culling(4), rotation_matrix(36),
    position(12).
    Resolves bone names from the name table that follows.
    Returns a list of bone dictionaries.
    """
    name_table_start = offset + bone_count * 60
    bone_list = []

    for bone_idx in range(bone_count):
        base = offset + bone_idx * 60

        name_offset = struct.unpack_from("<I", data, base)[0]
        parent_index = struct.unpack_from("<H", data, base + 4)[0]
        lod_parent_index = struct.unpack_from("<H", data, base + 6)[0]
        culling = struct.unpack_from("<f", data, base + 8)[0]

        # Rotation matrix: 9 × float32 (36 bytes)
        rot = struct.unpack_from("<9f", data, base + 12)
        # Position: 3 × float32 (12 bytes)
        pos = struct.unpack_from("<3f", data, base + 48)

        # CFrame: [px, py, pz, r00, r01, r02, r10, r11, r12, r20, r21, r22]
        cframe = [pos[0], pos[1], pos[2]] + list(rot)

        # Read bone name from name table (null-terminated UTF-8)
        name_start = name_table_start + name_offset
        name_end = data.index(b"\x00", name_start)
        bone_name = data[name_start:name_end].decode("utf-8")

        # Resolve parent: only if parent_index points to an already-read bone
        parent = None
        if parent_index != 0xFFFF and parent_index < bone_idx:
            parent = bone_list[parent_index]

        bone_list.append({
            "name":    bone_name,
            "parent":  parent,
            "cframe":  cframe,
            "culling": culling,
        })

    return bone_list


def _read_single_bone(data, offset, bone_idx, bone_list, name_table_offset):
    """
    Read a single 60-byte bone record from chunk data.
    Used by the chunked SKINNING parser where parent resolution
    may require a second pass (forward references).
    Returns the bone dict and 60 (bytes consumed).
    """
    name_offset_val = struct.unpack_from("<I", data, offset)[0]
    parent_index = struct.unpack_from("<H", data, offset + 4)[0]
    lod_parent_index = struct.unpack_from("<H", data, offset + 6)[0]
    culling = struct.unpack_from("<f", data, offset + 8)[0]

    rot = struct.unpack_from("<9f", data, offset + 12)
    pos = struct.unpack_from("<3f", data, offset + 48)

    cframe = [pos[0], pos[1], pos[2]] + list(rot)

    # Read bone name from the name table
    name_start = name_table_offset + name_offset_val
    name_end = data.index(b"\x00", name_start)
    bone_name = data[name_start:name_end].decode("utf-8")

    bone = {
        "name":          bone_name,
        "parent":        None,
        "cframe":        cframe,
        "culling":       culling,
        "_parent_index": parent_index,  # temporary, resolved later
    }

    return bone, 60


def _read_subsets_and_remap(data, offset, subset_count, skin_indices):
    """
    Read mesh subsets and remap per-vertex skinIndices from
    local subset bone indices to global bone array indices.
    Each subset is 72 bytes: facesBegin(4), facesLength(4),
    vertsBegin(4), vertsLength(4), numBoneIndices(4),
    boneIndices(26 × uint16 = 52).
    Modifies skin_indices in place.
    """
    for s in range(subset_count):
        base = offset + s * 72

        faces_begin = struct.unpack_from("<I", data, base)[0]
        faces_length = struct.unpack_from("<I", data, base + 4)[0]
        verts_begin = struct.unpack_from("<I", data, base + 8)[0]
        verts_length = struct.unpack_from("<I", data, base + 12)[0]
        num_bone_indices = struct.unpack_from("<I", data, base + 16)[0]

        # 26 × uint16 bone index lookup table
        bone_lut = struct.unpack_from("<26H", data, base + 20)

        # Remap each vertex's 4 skin indices using the lookup table
        for v in range(verts_begin, verts_begin + verts_length):
            for j in range(4):
                idx = v * 4 + j
                if idx < len(skin_indices):
                    local_idx = skin_indices[idx]
                    if local_idx < len(bone_lut):
                        skin_indices[idx] = bone_lut[local_idx]


#####################
def write_obj_from_mesh_json(mesh, out_path, lod_index=0, object_name="mesh"):
    ver = mesh["version"]
    if ver in ("1.00", "1.01", "2.00", "3.00", "3.01"):
        flip_v=False
    else:
        flip_v=True
     
    V = mesh["vertices"]                  # flat [x,y,z,...]
    N = mesh.get("normals")               # flat [nx,ny,nz,...]  (optional)
    UV = mesh.get("uvs")                  # flat [u,v,...]       (optional)
    F  = mesh["faces"]                    # flat [i0,i1,i2, i3,i4,i5, ...] (0-based)
    LOD = mesh.get("lods") or [0, len(F)//3]  # fallback: single range if no LODs present
    # choose one LOD's face range


    # choose one LOD's face range
    if lod_index < 0 or lod_index >= len(LOD):
        raise IndexError("lod_index out of range for provided 'lods'")

    start_face = LOD[lod_index]
    end_face   = (LOD[lod_index + 1] if lod_index + 1 < len(LOD) else len(F)//3)

    # slice the faces (each face = 3 indices)
    face_indices = F[start_face*3 : end_face*3]

    nv = len(V) // 3
    nn = (len(N)//3) if N else 0
    nt = (len(UV)//2) if UV else 0

    # Sanity: Roblox indices are 0-based; OBJ wants 1-based.
    def idx1(i): return i + 1

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Generated from Roblox mesh JSON (v{mesh.get('version','?')})\n")
        f.write(f"# Hello from RBX_Toolbox ;)\n")
        f.write(f"o {object_name}\n")

        # positions
        for i in range(0, len(V), 3):
            f.write(f"v {V[i]:.6f} {V[i+1]:.6f} {V[i+2]:.6f}\n")

        # uvs (optional)
        if UV:
            for i in range(0, len(UV), 2):
                u, v = UV[i], UV[i+1]
                if flip_v:  # not needed for v4+, only v1.00 quirk per spec
                    v = 1.0 - v
                f.write(f"vt {u:.6f} {v:.6f}\n")

        # normals (optional)
        if N:
            for i in range(0, len(N), 3):
                f.write(f"vn {N[i]:.6f} {N[i+1]:.6f} {N[i+2]:.6f}\n")

        # faces
        use_uvs = UV is not None and nt == nv
        use_nrm = N  is not None and nn == nv

        # Write f lines as vi[/ti][/ni] with matched indices.
        # In Roblox v2+ the index usually addresses a single "wedge" vertex
        # so pos/uv/normal share the same index — if your arrays align, this keeps them in sync.
        for i in range(0, len(face_indices), 3):
            a, b, c = face_indices[i], face_indices[i+1], face_indices[i+2]

            if use_uvs and use_nrm:
                f.write(f"f {idx1(a)}/{idx1(a)}/{idx1(a)} {idx1(b)}/{idx1(b)}/{idx1(b)} {idx1(c)}/{idx1(c)}/{idx1(c)}\n")
            elif use_uvs and not use_nrm:
                f.write(f"f {idx1(a)}/{idx1(a)} {idx1(b)}/{idx1(b)} {idx1(c)}/{idx1(c)}\n")
            elif use_nrm and not use_uvs:
                f.write(f"f {idx1(a)}//{idx1(a)} {idx1(b)}//{idx1(b)} {idx1()}//{idx1(c)}\n")
            else:
                f.write(f"f {idx1(a)} {idx1(b)} {idx1(c)}\n")


'''with open(r"D:\Mine\GDrive\Blender\Roblox\0. Addon\mesh reader\test files\lower_torso_4.1.mesh", "rb") as f:
    data = f.read()
    mesh = parse(data)
write_obj_from_mesh_json(mesh, "out.obj", lod_index=0, object_name="mesh")'''


'''mesh_file = r""
#mesh_file = r""
otput_obj = r""
with open(mesh_file, "rb") as f:
    data = f.read()'''

#mesh = RBXMeshParser.parse(data)
#import json
#print(json.dumps(mesh, indent=2))
#with open(r"C:\Users\tommy.ds\Downloads\mesh.json", "w") as f:
    #json.dump(mesh, f, indent=2)


#write_obj_from_mesh_json(mesh, otput_obj, lod_index=0, object_name="mesh")

