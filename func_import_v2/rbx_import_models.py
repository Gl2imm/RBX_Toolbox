import bpy
import os
import math
import importlib
from RBX_Toolbox import glob_vars
from typing import Any, Dict, List

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


# Roblox Material enum → approximate roughness
# See: https://create.roblox.com/docs/reference/engine/enums/Material
MATERIAL_ROUGHNESS = {
    256: 0.8,    # Brick
    272: 0.15,   # SmoothPlastic
    288: 0.85,   # Granite
    512: 0.45,   # Wood
    528: 0.9,    # Slate
    784: 0.7,    # Concrete
    800: 0.5,    # Metal
    816: 0.55,   # CorrodedMetal
    832: 0.6,    # DiamondPlate
    848: 0.3,    # Foil
    864: 0.65,   # Grass
    880: 0.05,   # Ice
    896: 0.75,   # Marble
    912: 0.5,    # Pebble
    1024: 0.4,   # Sand
    1040: 0.2,   # Fabric
    1056: 0.8,   # Cobblestone
    1072: 0.85,  # Rock
    1088: 0.95,  # WoodPlanks
    1280: 0.1,   # Glass
    1296: 0.05,  # Neon (emissive, very smooth)
    1312: 0.1,   # ForceField
    1584: 0.3,   # Plastic (default)
}
DEFAULT_ROUGHNESS = 0.5


# BrickColor ID → (R, G, B) sRGB 0-255 lookup table
# Full official list from Roblox engine
BRICKCOLOR_MAP = {
    1: (242,243,243), 2: (161,165,162), 3: (249,233,153), 5: (215,197,154),
    6: (194,218,184), 9: (232,186,200), 11: (128,187,219), 12: (203,132,66),
    18: (204,142,105), 21: (196,40,28), 22: (196,112,160), 23: (13,105,172),
    24: (245,205,48), 25: (98,71,50), 26: (27,42,53), 27: (109,110,108),
    28: (40,127,71), 29: (161,196,140), 36: (243,207,155), 37: (75,151,75),
    38: (160,95,53), 39: (193,202,222), 40: (236,236,236), 41: (205,84,75),
    42: (193,223,240), 43: (123,182,232), 44: (247,241,141), 45: (180,210,228),
    47: (217,133,108), 48: (132,182,141), 49: (156,186,54), 50: (226,220,188),
    100: (238,196,182), 101: (218,134,122), 102: (110,153,202), 103: (199,193,183),
    104: (107,50,124), 105: (226,155,64), 106: (218,133,65), 107: (0,143,156),
    108: (104,92,67), 110: (67,84,147), 111: (191,183,177), 112: (104,116,172),
    113: (228,173,200), 115: (199,210,60), 116: (85,165,175), 118: (183,215,213),
    119: (164,189,71), 120: (217,228,167), 121: (231,172,88), 123: (211,111,76),
    124: (146,57,120), 125: (234,184,146), 126: (165,165,203), 127: (220,188,129),
    128: (174,122,89), 131: (156,163,168), 133: (213,115,61), 134: (216,221,86),
    135: (116,134,157), 136: (135,124,144), 137: (224,152,100), 138: (149,138,115),
    140: (32,58,86), 141: (39,70,45), 143: (207,226,247), 145: (121,136,171),
    146: (149,142,163), 147: (147,135,103), 148: (87,88,87), 149: (22,29,50),
    150: (171,173,172), 151: (120,144,130), 153: (149,121,119), 154: (123,46,47),
    157: (255,246,123), 158: (226,176,135), 168: (117,108,98), 176: (151,105,91),
    178: (180,132,85), 179: (137,135,136), 180: (215,169,75), 190: (249,214,46),
    191: (232,171,45), 192: (105,64,40), 193: (207,96,36), 194: (163,162,165),
    195: (70,103,164), 196: (35,71,139), 198: (142,66,133), 199: (99,95,98),
    200: (130,138,93), 208: (229,228,223), 209: (176,167,132), 210: (112,149,120),
    211: (121,181,181), 212: (159,195,233), 213: (108,129,183), 216: (143,76,42),
    217: (124,92,70), 218: (150,103,102), 219: (107,98,155), 220: (167,169,206),
    221: (205,142,211), 222: (228,173,200), 223: (220,144,149), 224: (240,213,160),
    225: (255,152,48), 226: (253,234,141), 227: (253,218,28), 228: (63,54,43),
    229: (255,193,37), 230: (255,215,131), 232: (127,142,100), 234: (243,195,7),
    235: (0,80,96), 236: (39,70,45), 1001: (248,248,248), 1002: (205,205,205),
    1003: (17,17,17), 1004: (255,0,0), 1005: (255,175,0), 1006: (180,128,255),
    1007: (163,75,75), 1008: (175,148,131), 1009: (255,255,0), 1010: (0,0,255),
    1011: (0,32,96), 1012: (33,84,185), 1013: (4,175,236), 1014: (170,85,0),
    1015: (170,0,0), 1016: (255,102,204), 1017: (255,175,0), 1018: (18,238,212),
    1019: (0,255,255), 1020: (255,255,255), 1021: (255,0,191), 1022: (255,0,0),
    1023: (255,255,0), 1024: (0,255,0), 1025: (255,120,0), 1026: (157,172,222),
    1027: (90,76,66), 1028: (131,109,90), 1029: (255,255,183), 1030: (255,130,67),
    1031: (160,160,160), 1032: (149,185,233),
}

# BrickColor name → BrickColor ID
# Covers common named BrickColors
BRICKCOLOR_NAME_MAP = {
    "white": 1, "grey": 2, "light yellow": 3, "brick yellow": 5,
    "light green (mint)": 6, "light reddish violet": 9, "pastel blue": 11,
    "light orange brown": 12, "nougat": 18, "bright red": 21,
    "med. reddish violet": 22, "bright blue": 23, "bright yellow": 24,
    "earth orange": 25, "black": 26, "dark grey": 27, "dark green": 28,
    "medium green": 29, "lig. yellowich orange": 36, "bright green": 37,
    "dark orange": 38, "light bluish violet": 39, "transparent": 40,
    "tr. red": 41, "tr. lg blue": 42, "tr. blue": 43, "tr. yellow": 44,
    "light blue": 45, "tr. flu. reddish orange": 47, "tr. green": 48,
    "tr. flu. green": 49, "phosph. white": 50, "light red": 100,
    "medium red": 101, "medium blue": 102, "light grey": 103,
    "bright violet": 104, "br. yellowish orange": 105, "bright orange": 106,
    "bright bluish green": 107, "earth yellow": 108, "bright bluish violet": 110,
    "tr. brown": 111, "medium bluish violet": 112, "tr. medi. reddish violet": 113,
    "med. yellowish green": 115, "med. bluish green": 116,
    "light bluish green": 118, "br. yellowish green": 119,
    "lig. yellowish green": 120, "med. yellowish orange": 121,
    "br. reddish orange": 123, "bright reddish violet": 124,
    "light orange": 125, "tr. bright bluish violet": 126, "gold": 127,
    "dark nougat": 128, "silver": 131, "neon orange": 133,
    "neon green": 134, "sand blue": 135, "sand violet": 136,
    "medium orange": 137, "sand yellow": 138, "earth blue": 140,
    "earth green": 141, "tr. flu. blue": 143, "sand blue metallic": 145,
    "sand violet metallic": 146, "sand yellow metallic": 147,
    "dark grey metallic": 148, "black metallic": 149, "light grey metallic": 150,
    "sand green": 151, "sand red": 153, "dark red": 154,
    "tr. flu. yellow": 157, "tr. flu. red": 158, "gun metallic": 168,
    "red flip/flop": 176, "yellow flip/flop": 178, "silver flip/flop": 179,
    "curry": 180, "fire yellow": 190, "flame yellowish orange": 191,
    "reddish brown": 192, "flame reddish orange": 193, "medium stone grey": 194,
    "royal blue": 195, "dark royal blue": 196, "bright reddish lilac": 198,
    "dark stone grey": 199, "lemon metalic": 200, "light stone grey": 208,
    "dark curry": 209, "faded green": 210, "turquoise": 211,
    "light royal blue": 212, "medium royal blue": 213, "rust": 216,
    "brown": 217, "reddish lilac": 218, "lilac": 219,
    "light lilac": 220, "bright purple": 221, "light pink": 222,
    "light brick yellow": 223, "warm yellowish orange": 224,
    "cool yellow": 225, "dove blue": 226, "medium lilac": 227,
    "olive": 228, "bright bluish yellow": 229, "new yeller": 226,
    "really red": 1004, "really blue": 1010, "alder": 217,
    "dusty rose": 9, "cga brown": 217, "dark indigo": 11,
    "institutional white": 1001, "mid gray": 1002, "really black": 1003,
    "deep orange": 1005, "lavender": 1006, "salmon": 1007,
    "toothpaste": 1019, "lime green": 1020, "hot pink": 1016,
    "magenta": 1021, "crimson": 1022, "deep blue": 1011,
    "teal": 1018, "smoky grey": 1013, "pine cone": 1027,
    "pearl": 1029, "fog": 1030, "ghost grey": 1031, "baby blue": 1032,
}


def _roblox_material_to_roughness(material_id: int) -> float:
    """Convert Roblox Material enum value to approximate roughness [0,1]."""
    return MATERIAL_ROUGHNESS.get(material_id, DEFAULT_ROUGHNESS)


def _color3uint8_to_linear(color_tuple):
    """
    Convert Roblox Color3uint8 (0-255 sRGB tuple) to Blender linear [0,1] RGBA.
    Applies sRGB → linear conversion for correct display in Blender.
    """
    def srgb_to_linear(c):
        c = c / 255.0
        if c <= 0.04045:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4

    r, g, b = color_tuple
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b), 1.0)


def _resolve_part_color(part_instance):
    """
    Resolve a Part's color from Color3uint8 or BrickColor properties.
    Returns (R, G, B) tuple in 0-255 sRGB, or None if no color found.
    
    Priority:
    1. Color3uint8 (direct RGB)
    2. BrickColor (integer ID → lookup)
    3. BrickColor (string name → lookup)
    """
    # Try Color3uint8 first
    color = part_instance.get("Color3uint8")
    if color:
        return color

    # Try BrickColor (can be int ID or string name)
    brick_color = part_instance.get("BrickColor")
    if brick_color is not None:
        if isinstance(brick_color, int):
            # BrickColor ID → RGB lookup
            rgb = BRICKCOLOR_MAP.get(brick_color)
            if rgb:
                return rgb
        elif isinstance(brick_color, str):
            # BrickColor name → ID → RGB lookup
            bc_name = brick_color.strip().lower()
            bc_id = BRICKCOLOR_NAME_MAP.get(bc_name)
            if bc_id:
                rgb = BRICKCOLOR_MAP.get(bc_id)
                if rgb:
                    return rgb
            dprint(f"  Unknown BrickColor name: '{brick_color}'")

    return None


def apply_part_material(blender_obj, part_instance, func_rbx_other=None):
    """
    Create and assign a Principled BSDF material to a Blender object
    using the Roblox Part's color, Material, Transparency, and Reflectance.
    
    Color is resolved from Color3uint8 or BrickColor (ID or name).
    This is a standalone function that can be called separately.
    """
    color_raw = _resolve_part_color(part_instance)
    material_id = part_instance.get("Material") or 1584
    transparency = part_instance.get("Transparency") or 0.0
    reflectance = part_instance.get("Reflectance") or 0.0

    # Create unique material name per color+material combo
    if color_raw:
        r, g, b = color_raw
        mat_name = f"RBX_{r}_{g}_{b}_M{material_id}"
    else:
        mat_name = f"RBX_Default_M{material_id}"

    # Reuse existing material if it already exists (same color + material)
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")

        if bsdf:
            # Base Color from resolved color
            if color_raw:
                bsdf.inputs["Base Color"].default_value = _color3uint8_to_linear(color_raw)

            # Roughness from Material enum
            roughness = _roblox_material_to_roughness(material_id)
            bsdf.inputs["Roughness"].default_value = roughness

            # Metallic from Reflectance (0.0-1.0)
            bsdf.inputs["Metallic"].default_value = min(reflectance, 1.0)

            # Alpha from Transparency
            if transparency > 0.0:
                bsdf.inputs["Alpha"].default_value = 1.0 - transparency
                if hasattr(mat, 'blend_method'):
                    mat.blend_method = 'BLEND'
                mat.use_backface_culling = True

            # Neon material gets emission
            if material_id == 1296 and color_raw:
                linear_color = _color3uint8_to_linear(color_raw)
                # Blender 4.x: "Emission Color" input
                emission_input = bsdf.inputs.get("Emission Color")
                if emission_input is None:
                    emission_input = bsdf.inputs.get("Emission")
                if emission_input:
                    emission_input.default_value = linear_color
                emission_str = bsdf.inputs.get("Emission Strength")
                if emission_str:
                    emission_str.default_value = 3.0

    # Assign to object
    if blender_obj.data.materials:
        blender_obj.data.materials[0] = mat
    else:
        blender_obj.data.materials.append(mat)


def _special_angles_to_matrix(angles_deg):
    """
    Convert Roblox 'special' Euler angles (degrees) to a 3×3 rotation matrix.
    Roblox special angles are (rx, ry, rz) applied as:
      R = Rz(rz) * Ry(ry) * Rx(rx)  (intrinsic YXZ-like order)
    Returns a flat 9-element tuple in row-major order.
    """
    rx_rad = math.radians(angles_deg[0])
    ry_rad = math.radians(angles_deg[1])
    rz_rad = math.radians(angles_deg[2])

    cx, sx = math.cos(rx_rad), math.sin(rx_rad)
    cy, sy = math.cos(ry_rad), math.sin(ry_rad)
    cz, sz = math.cos(rz_rad), math.sin(rz_rad)

    # Rotation matrix: R = Rz * Ry * Rx (row-major)
    r00 = cy * cz + sy * sx * sz
    r01 = -cy * sz + sy * sx * cz
    r02 = sy * cx
    r10 = cx * sz
    r11 = cx * cz
    r12 = -sx
    r20 = -sy * cz + cy * sx * sz
    r21 = sy * sz + cy * sx * cz
    r22 = cy * cx

    return (r00, r01, r02, r10, r11, r12, r20, r21, r22)


def _cframe_to_blender_transform(cframe_dict):
    """
    Convert a Roblox CFrame dict to Blender location + rotation matrix.
    Applies the Roblox→Blender coordinate conversion:
      Blender X = Roblox X
      Blender Y = Roblox -Z
      Blender Z = Roblox Y
    Supports both 'matrix' (3×3 row-major) and 'special' (Euler angles in degrees).
    """
    from mathutils import Matrix, Vector

    pos = cframe_dict.get("position", (0, 0, 0))
    rot = cframe_dict.get("rotation", None)

    # Convert position: Roblox (x, y, z) → Blender (x, -z, y)
    bx = pos[0]
    by = -pos[2]
    bz = pos[1]

    rm = None
    if rot:
        if rot[0] == "matrix":
            rm = rot[1]
        elif rot[0] == "special":
            # Convert Euler angles (degrees) to rotation matrix
            rm = _special_angles_to_matrix(rot[1])

    if rm:
        # Rotation is a 3×3 rotation matrix (row-major)
        # r00, r01, r02, r10, r11, r12, r20, r21, r22
        # Apply coordinate swap to the rotation matrix
        blender_mat = Matrix((
            (rm[0],  -rm[2],  rm[1],  bx),
            (-rm[6],  rm[8], -rm[7],  by),
            (rm[3],  -rm[5],  rm[4],  bz),
            (0,       0,      0,      1)
        ))
        return blender_mat
    else:
        # Identity rotation
        return Matrix.Translation(Vector((bx, by, bz)))


def _cframe_to_blender_transform_mesh(cframe_dict):
    """
    Convert a Roblox CFrame dict to Blender matrix_world for mesh objects
    whose OBJ vertices are still in Roblox local space (Y-up).

    Unlike _cframe_to_blender_transform (which swaps both rows AND columns
    for Blender-native primitives), this applies R_conv @ R_roblox only
    (row swap, no column swap), because the mesh vertices haven't been
    converted from Roblox to Blender coordinate space.

    R_conv = 90° around X = [[1,0,0],[0,0,-1],[0,1,0]]
    Result = R_conv @ M_cf (position also converted)
    Supports both 'matrix' and 'special' (Euler angles in degrees).
    """
    from mathutils import Matrix, Vector

    pos = cframe_dict.get("position", (0, 0, 0))
    rot = cframe_dict.get("rotation", None)

    # Convert position: Roblox (x, y, z) → Blender (x, -z, y)
    bx = pos[0]
    by = -pos[2]
    bz = pos[1]

    rm = None
    if rot:
        if rot[0] == "matrix":
            rm = rot[1]
        elif rot[0] == "special":
            rm = _special_angles_to_matrix(rot[1])

    if rm:
        # R_conv @ R_roblox — only swap rows, keep columns as-is
        # Row 0 = row 0 of R_roblox
        # Row 1 = -row 2 of R_roblox  (from R_conv row 1 = [0, 0, -1])
        # Row 2 = row 1 of R_roblox   (from R_conv row 2 = [0, 1, 0])
        blender_mat = Matrix((
            ( rm[0],  rm[1],  rm[2],  bx),
            (-rm[6], -rm[7], -rm[8],  by),
            ( rm[3],  rm[4],  rm[5],  bz),
            ( 0,      0,      0,      1)
        ))
        return blender_mat
    else:
        return Matrix.Translation(Vector((bx, by, bz)))


def _create_single_truss(name, bsx, bsy, bsz, cframe_dict):
    """
    Create a single 2×2×2 truss unit (wireframe cube) at the given Blender size.
    Returns the created Blender object.
    """
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    wire_mod = obj.modifiers.new(name="Truss", type='WIREFRAME')
    wire_mod.thickness = 0.15
    wire_mod.use_replace = True
    wire_mod.use_even_offset = True
    obj.name = name
    obj.data.name = name
    obj.scale = (bsx, bsy, bsz)
    if cframe_dict:
        transform = _cframe_to_blender_transform(cframe_dict)
        obj.matrix_world = transform
        obj.scale = (bsx, bsy, bsz)
    return obj


def _create_truss_staggered(name, size_roblox, cframe_dict):
    """
    Create a TrussPart as staggered 2×2×2 truss units.
    A single truss unit is always 2×2×2 studs. If the TrussPart size exceeds
    this, multiple truss units are placed to fill the volume.
    Returns a list of created Blender objects.
    """
    if size_roblox is None:
        size_roblox = (2.0, 2.0, 2.0)

    TRUSS_UNIT = 2.0
    sx, sy, sz = size_roblox

    # Blender unit size for a single truss cell
    unit_bsx = TRUSS_UNIT
    unit_bsy = TRUSS_UNIT  # Roblox Z → Blender Y (each unit = 2)
    unit_bsz = TRUSS_UNIT  # Roblox Y → Blender Z (each unit = 2)

    # Number of truss units along each Roblox axis
    nx = max(1, round(sx / TRUSS_UNIT))
    ny = max(1, round(sy / TRUSS_UNIT))
    nz = max(1, round(sz / TRUSS_UNIT))

    # If it's a single unit, just create one truss directly
    if nx == 1 and ny == 1 and nz == 1:
        # Convert size: Roblox (sx, sy, sz) → Blender (sx, sz, sy)
        bsx = sx
        bsy = sz
        bsz = sy
        obj = _create_single_truss(name, bsx, bsy, bsz, cframe_dict)
        return [obj]

    from mathutils import Matrix, Vector

    # Get the base transform from the CFrame
    if cframe_dict:
        base_transform = _cframe_to_blender_transform(cframe_dict)
    else:
        base_transform = Matrix.Identity(4)

    objects = []
    # Calculate start offsets (center the grid of units around the origin)
    start_x = -(sx - TRUSS_UNIT) / 2.0
    start_y = -(sy - TRUSS_UNIT) / 2.0
    start_z = -(sz - TRUSS_UNIT) / 2.0

    for ix in range(nx):
        for iy in range(ny):
            for iz in range(nz):
                # Local offset in Roblox coords
                local_x = start_x + ix * TRUSS_UNIT
                local_y = start_y + iy * TRUSS_UNIT
                local_z = start_z + iz * TRUSS_UNIT

                # Convert local offset: Roblox (x,y,z) → Blender (x,-z,y)
                bl_offset = Vector((local_x, -local_z, local_y))

                unit_name = f"{name}_unit_{ix}_{iy}_{iz}"
                bpy.ops.mesh.primitive_cube_add(size=1)
                obj = bpy.context.active_object
                wire_mod = obj.modifiers.new(name="Truss", type='WIREFRAME')
                wire_mod.thickness = 0.15
                wire_mod.use_replace = True
                wire_mod.use_even_offset = True
                obj.name = unit_name
                obj.data.name = unit_name

                # Position each unit: base_transform position + rotated offset
                rot_part = base_transform.to_3x3()
                world_offset = rot_part @ bl_offset
                unit_pos = base_transform.translation + world_offset

                unit_transform = base_transform.copy()
                unit_transform.translation = unit_pos
                obj.matrix_world = unit_transform
                obj.scale = (unit_bsx, unit_bsy, unit_bsz)

                objects.append(obj)

    return objects


# Cache for template meshes — avoids expensive bpy.ops calls for every part
_mesh_template_cache: Dict[str, bpy.types.Mesh] = {}


def _get_template_mesh(shape_key: str) -> bpy.types.Mesh:
    """Get or create a template mesh for the given shape key.
    Returns a Mesh datablock that can be copied for each new object."""
    if shape_key in _mesh_template_cache:
        return _mesh_template_cache[shape_key]

    import bmesh

    if shape_key == "CornerWedgePart":
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.verts.ensure_lookup_table()
        verts_to_remove = [v for v in bm.verts if v.co.z > 0 and v.co.y > 0]
        bmesh.ops.delete(bm, geom=verts_to_remove, context='VERTS')
        mesh = bpy.data.meshes.new(f"_template_{shape_key}")
        bm.to_mesh(mesh)
        bm.free()

    elif shape_key == "WedgePart":
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bm.verts.ensure_lookup_table()
        verts_to_merge = [v for v in bm.verts if v.co.z > 0 and v.co.y > 0]
        for v in verts_to_merge:
            v.co.y = -v.co.y
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
        mesh = bpy.data.meshes.new(f"_template_{shape_key}")
        bm.to_mesh(mesh)
        bm.free()

    elif shape_key == "Ball":
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=0.5)
        mesh = bpy.data.meshes.new(f"_template_{shape_key}")
        bm.to_mesh(mesh)
        bm.free()
        for p in mesh.polygons:
            p.use_smooth = True

    elif shape_key == "Cylinder":
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, segments=24, radius1=0.5, radius2=0.5, depth=1.0, cap_ends=True, cap_tris=False)
        mesh = bpy.data.meshes.new(f"_template_{shape_key}")
        bm.to_mesh(mesh)
        bm.free()
        for p in mesh.polygons:
            p.use_smooth = True

    else:
        # Block (default cube)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        mesh = bpy.data.meshes.new(f"_template_{shape_key}")
        bm.to_mesh(mesh)
        bm.free()

    _mesh_template_cache[shape_key] = mesh
    return mesh


def _create_part(name, size_roblox, cframe_dict, shape=1, class_name="Part"):
    """
    Create a Blender primitive matching a Roblox Part's Shape property.
    size_roblox: (sx, sy, sz) in studs (Roblox coords)
    shape: Roblox PartType enum — 0=Ball, 1=Block (default), 2=Cylinder
    class_name: Roblox class name — "WedgePart" gets wedge geometry
    """
    # Default Roblox Part size
    if size_roblox is None:
        size_roblox = (4.0, 1.2, 2.0)

    # Convert size: Roblox (sx, sy, sz) → Blender (sx, sz, sy)
    bsx = size_roblox[0]
    bsy = size_roblox[2]  # Roblox Z → Blender Y
    bsz = size_roblox[1]  # Roblox Y → Blender Z

    # NOTE: TrussPart is handled separately by _create_truss_staggered
    if class_name == "TrussPart":
        obj = _create_single_truss(name, bsx, bsy, bsz, cframe_dict)
        return obj

    # Determine shape key for template cache lookup
    if class_name in ("CornerWedgePart", "WedgePart"):
        shape_key = class_name
    elif shape == 0:
        shape_key = "Ball"
    elif shape == 2:
        shape_key = "Cylinder"
    else:
        shape_key = "Block"

    # Get cached template and copy its mesh data for this object
    template_mesh = _get_template_mesh(shape_key)
    new_mesh = template_mesh.copy()
    new_mesh.name = name
    obj = bpy.data.objects.new(name, new_mesh)
    bpy.context.collection.objects.link(obj)

    # Cylinder axis rotation (Roblox cylinder axis = X)
    if shape_key == "Cylinder":
        obj.rotation_euler[1] = math.radians(90)

    # Scale to match Part dimensions
    obj.scale = (bsx, bsy, bsz)

    # Apply CFrame transform
    if cframe_dict:
        transform = _cframe_to_blender_transform(cframe_dict)
        obj.matrix_world = transform
        # Scale must be re-applied after setting matrix_world
        obj.scale = (bsx, bsy, bsz)

    return obj


def _import_special_mesh(
    mesh_instance, parent_part, part_name,
    headers, tmp_path, func_rbx_other, func_rbx_cloud_api
):
    """
    Download and import a SpecialMesh/Mesh child as an OBJ mesh in Blender.
    CFrame and Size come from the parent Part.
    Uses the model importer's own _cframe_to_blender_transform for positioning,
    consistent with how _create_box places parts.
    Returns the imported Blender object or None.
    """
    from .readers import mesh_reader
    from . import func_blndr_api
    importlib.reload(func_blndr_api)

    # Get the MeshId from the SpecialMesh/Mesh instance
    mesh_id_raw = mesh_instance.get("MeshId")
    if not mesh_id_raw:
        dprint(f"    SpecialMesh {part_name} has no MeshId")
        return None

    mesh_id = func_rbx_other.resolve_content_uri(mesh_id_raw)
    if not mesh_id:
        dprint(f"    Could not resolve MeshId for {part_name}")
        return None

    mesh_id_clean = func_rbx_other.strip_rbxassetid(mesh_id)

    # Download mesh data
    try:
        asset_data, dl_error = func_rbx_cloud_api.get_asset_data(mesh_id_clean, headers)
        if dl_error or not asset_data:
            dprint(f"    Error downloading mesh {part_name}: {dl_error}")
            return None

        mesh_data = mesh_reader.parse(asset_data)
        if not mesh_data:
            dprint(f"    No mesh data parsed for {part_name}")
            return None
    except Exception as e:
        dprint(f"    Error processing mesh for {part_name}: {e}")
        return None

    # Write OBJ and import into Blender
    # Mesh vertices/normals stay in Roblox Y-up space;
    # _cframe_to_blender_transform_mesh handles the coordinate conversion
    # via matrix_world so that UV mapping and textures remain correct.
    obj_file_path = os.path.join(tmp_path, part_name + ".obj")
    mesh_reader.write_obj_from_mesh_json(mesh_data, obj_file_path, lod_index=0, object_name=part_name)
    func_blndr_api.blender_api_import_obj(obj_file_path)

    rbx_obj = bpy.context.selected_objects[0]
    rbx_obj.name = part_name

    # Deselect and select only the new object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    bpy.data.objects[rbx_obj.name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_obj.name]

    # Apply SpecialMesh Scale if available
    special_mesh_scale = mesh_instance.get("Scale")
    if special_mesh_scale:
        try:
            rbx_obj.scale = (special_mesh_scale[0], special_mesh_scale[1], special_mesh_scale[2])
        except Exception as e:
            dprint(f"    Error applying special mesh scale: {e}")

    # Apply CFrame from parent Part using the mesh-specific coordinate conversion
    # Uses _cframe_to_blender_transform_mesh (R_conv @ R_roblox) because
    # mesh OBJ vertices are in Roblox local space (Y-up), unlike box primitives.
    # This preserves correct UV/texture mapping.
    cframe = parent_part.get("CFrame")
    if cframe:
        transform = _cframe_to_blender_transform_mesh(cframe)
        rbx_obj.matrix_world = transform
        # Re-apply scale after setting matrix_world
        if special_mesh_scale:
            try:
                rbx_obj.scale = (special_mesh_scale[0], special_mesh_scale[1], special_mesh_scale[2])
            except Exception:
                pass

    return rbx_obj


def _apply_decal_texture(
    part_instance, blender_obj, part_name,
    headers, tmp_path, func_rbx_other, func_rbx_cloud_api
):
    """
    Check if a Part has Decal children and apply the first valid decal's
    texture image to the Blender object's material.
    """
    if not headers or not func_rbx_cloud_api:
        return

    for child in part_instance.GetChildren():
        if child.class_name != "Decal":
            continue

        tex_raw = child.get("Texture")
        if not tex_raw:
            continue

        tex_uri = func_rbx_other.resolve_content_uri(tex_raw)
        if not tex_uri:
            # Texture might be a plain URL string like http://www.roblox.com/asset/?id=...
            tex_uri = str(tex_raw)

        tex_id = func_rbx_other.strip_rbxassetid(tex_uri)
        if not tex_id or tex_id == "" or tex_id == "None":
            continue

        dprint(f"    Downloading decal texture for {part_name}: ID={tex_id}")

        # Download texture image
        try:
            tex_data, tex_error = func_rbx_cloud_api.get_asset_data(tex_id, headers)
            if tex_error or not tex_data:
                dprint(f"    Error downloading decal texture {tex_id}: {tex_error}")
                continue

            # Save to tmp
            tex_file_name = f"{part_name}_decal_{tex_id}.png"
            tex_path = os.path.join(tmp_path, tex_file_name)
            with open(tex_path, "wb") as f:
                f.write(tex_data)

            # Apply texture to material using image node
            mat = blender_obj.active_material
            if mat is None:
                mat = bpy.data.materials.new(name=f"Decal_{part_name}")
                mat.use_nodes = True
                if blender_obj.data.materials:
                    blender_obj.data.materials[0] = mat
                else:
                    blender_obj.data.materials.append(mat)

            if mat.use_nodes:
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                bsdf = nodes.get("Principled BSDF")
                if bsdf:
                    # Load image
                    img = bpy.data.images.load(tex_path)
                    # Create image texture node
                    tex_node = nodes.new(type='ShaderNodeTexImage')
                    tex_node.image = img
                    tex_node.location = (-300, 300)
                    # Connect to Base Color
                    links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

            dprint(f"    Applied decal texture to {part_name}")
            return  # Apply first valid decal only

        except Exception as e:
            dprint(f"    Error applying decal texture for {part_name}: {e}")
            continue


def _move_collection_objects_to_origin(collection):
    """
    Select all objects in the collection (and sub-collections),
    then snap to cursor (which is at origin) with 'Offset' enabled
    so relative positions are preserved.
    """
    # Deselect all first
    bpy.ops.object.select_all(action='DESELECT')

    # Collect all objects recursively from the collection
    def gather_objects(col):
        objs = []
        for obj in col.objects:
            objs.append(obj)
        for child_col in col.children:
            objs.extend(gather_objects(child_col))
        return objs

    all_objs = gather_objects(collection)
    if not all_objs:
        return

    # Select all objects in the model collection
    for obj in all_objs:
        obj.select_set(True)

    # Set active object
    bpy.context.view_layer.objects.active = all_objs[0]

    # Make sure 3D cursor is at origin
    bpy.context.scene.cursor.location = (0, 0, 0)

    # Snap selection to cursor with offset (preserves relative positions)
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)

    # Deselect when done
    bpy.ops.object.select_all(action='DESELECT')


# Part class names that should be imported as geometry
PART_CLASS_NAMES = (
    "Part", "MeshPart", "WedgePart", "TrussPart",
    "CornerWedgePart", "SpawnLocation"
)


def import_model(
    rbxm_file_path: str,
    model_name: str,
    at_origin: bool = False,
    add_textures: bool = True,
    func_rbx_other: Any = None,
    func_blndr_api: Any = None,
    headers: dict = None,
    tmp_path: str = None,
    func_rbx_cloud_api: Any = None
):
    """
    Import a Roblox Model (.rbxm) as a collection of Blender box primitives.
    
    Each Part in the model becomes a scaled cube with material properties
    applied from Color3uint8/BrickColor, Material, Transparency, Reflectance.
    
    Parts with SpecialMesh/Mesh children get actual mesh geometry imported.
    Parts with Decal children get decal textures applied.
    Model hierarchy is preserved via Blender collections.
    Recursively scans all children including unsupported containers
    (e.g. Accessory, Tool) for hidden Part-like items.
    """
    from . import func_rbx_other as api_other
    from .readers import rbxm_reader

    if func_rbx_other is None:
        func_rbx_other = api_other
    importlib.reload(func_rbx_other)

    dprint(f"Importing model: {model_name} from {rbxm_file_path}")

    # Reset template mesh cache for this import session
    _mesh_template_cache.clear()

    # Parse RBXM
    try:
        model = rbxm_reader.parse(rbxm_file_path)
    except Exception as e:
        dprint(f"Error parsing RBXM: {e}")
        return None

    # Create root collection
    clean_name = func_rbx_other.replace_restricted_char(model_name)
    root_col = bpy.data.collections.new(clean_name)
    bpy.context.scene.collection.children.link(root_col)

    imported_count = 0

    def _import_part_node(child, parent_collection):
        """
        Import a single Part-like node into the given collection.
        Handles SpecialMesh, MeshPart mesh import, TrussPart staggering,
        material, and decal application.
        Returns the number of objects imported.
        """
        nonlocal imported_count

        part_name = child.properties.get("Name", "Part")
        size = child.get("size")
        cframe = child.get("CFrame")
        transparency = child.get("Transparency") or 0.0

        # Skip fully transparent parts
        if transparency >= 1.0:
            return

        # Check for SpecialMesh/Mesh children
        special_mesh = None
        for sub_child in child.GetChildren():
            if sub_child.class_name in ("SpecialMesh", "Mesh"):
                mesh_id = sub_child.get("MeshId")
                if mesh_id:
                    special_mesh = sub_child
                    break

        obj = None
        if special_mesh and headers and func_rbx_cloud_api:
            # Import actual mesh geometry from SpecialMesh/Mesh child
            mesh_tmp = tmp_path or os.path.dirname(rbxm_file_path)
            obj = _import_special_mesh(
                special_mesh, child, part_name,
                headers, mesh_tmp, func_rbx_other, func_rbx_cloud_api
            )

        if obj is None:
            if child.class_name == "MeshPart":
                # MeshPart with MeshId — try importing its own mesh
                mesh_id_raw = child.get("MeshId")
                if mesh_id_raw and headers and func_rbx_cloud_api:
                    mesh_tmp = tmp_path or os.path.dirname(rbxm_file_path)
                    obj = _import_special_mesh(
                        child, child, part_name,
                        headers, mesh_tmp, func_rbx_other, func_rbx_cloud_api
                    )

            # Fallback to primitive shape if no mesh imported
            if obj is None:
                # Issue-1: TrussPart staggering for sizes > 2×2×2
                if child.class_name == "TrussPart":
                    TRUSS_UNIT = 2.0
                    truss_size = size or (2.0, 2.0, 2.0)
                    is_multi = (
                        truss_size[0] > TRUSS_UNIT + 0.01 or
                        truss_size[1] > TRUSS_UNIT + 0.01 or
                        truss_size[2] > TRUSS_UNIT + 0.01
                    )
                    if is_multi:
                        # Create staggered truss units in a Truss sub-collection
                        truss_col_name = f"Truss_{part_name}"
                        truss_col = bpy.data.collections.new(truss_col_name)
                        parent_collection.children.link(truss_col)

                        truss_objs = _create_truss_staggered(
                            part_name, truss_size, cframe
                        )
                        for t_obj in truss_objs:
                            if add_textures:
                                apply_part_material(t_obj, child, func_rbx_other)
                            if t_obj.name not in truss_col.objects:
                                truss_col.objects.link(t_obj)
                            for col in list(t_obj.users_collection):
                                if col != truss_col:
                                    col.objects.unlink(t_obj)
                            imported_count += 1
                        return  # Done with TrussPart

                # Try both casings — rbxm binary may store as "shape" or "Shape"
                shape = child.get("shape")
                if shape is None:
                    shape = child.get("Shape")
                if shape is None:
                    shape = 1  # Default Block
                dprint(f"  Part '{part_name}' shape={shape} class={child.class_name}")
                obj = _create_part(
                    part_name, size, cframe,
                    shape=shape, class_name=child.class_name
                )

        if obj is None:
            return

        # Determine if this mesh has SurfaceAppearance or TextureId
        # to use the full PBR texture pipeline instead of just BrickColor
        has_surface_appearance = (
            child.FindFirstChildOfClass("SurfaceAppearance") is not None
        )
        has_texture_id = False

        def _is_valid_texture_ref(tid):
            """Check if a TextureId value is a real texture reference.
            The XML parser returns {"type": "None"} for null Content props,
            which is truthy — we must reject it."""
            if not tid:
                return False
            if isinstance(tid, dict):
                return tid.get("type") == "Uri" and bool(tid.get("uri"))
            # Binary parser may return a plain string URI
            return bool(str(tid).strip())

        if child.class_name == "MeshPart":
            try:
                tid = child.get("TextureID")
                if _is_valid_texture_ref(tid):
                    has_texture_id = True
            except:
                pass
        # Also check SpecialMesh TextureId
        if special_mesh:
            try:
                tid = special_mesh.get("TextureId") or special_mesh.get("TextureID")
                if _is_valid_texture_ref(tid):
                    has_texture_id = True
            except:
                pass

        mesh_imported = (special_mesh is not None) or (child.class_name == "MeshPart")

        if add_textures and mesh_imported and (has_surface_appearance or has_texture_id) and headers and func_rbx_cloud_api:
            # Use the full texture pipeline (SurfaceAppearance PBR, TextureId, Decals)
            from . import rbx_import_textures
            importlib.reload(rbx_import_textures)
            mesh_tmp = tmp_path or os.path.dirname(rbxm_file_path)
            # The texture source is either the SpecialMesh or the MeshPart itself
            tex_source = special_mesh if special_mesh else child
            asset_clean = func_rbx_other.replace_restricted_char(part_name)
            rbx_import_textures.download_and_apply_textures(
                tex_source, part_name, mesh_tmp,
                headers, obj, asset_clean
            )
        elif add_textures:
            # Fallback: apply BrickColor-based material
            apply_part_material(obj, child, func_rbx_other)

        # Issue-3: Apply decal textures if present (only if no PBR was applied)
        if not (has_surface_appearance or has_texture_id):
            has_decal = any(
                c.class_name == "Decal" for c in child.GetChildren()
            )
            if has_decal and headers and func_rbx_cloud_api:
                mesh_tmp = tmp_path or os.path.dirname(rbxm_file_path)
                _apply_decal_texture(
                    child, obj, part_name,
                    headers, mesh_tmp, func_rbx_other, func_rbx_cloud_api
                )

        # Link to parent collection, unlink from Scene Collection
        if obj.name not in parent_collection.objects:
            parent_collection.objects.link(obj)
        for col in list(obj.users_collection):
            if col != parent_collection:
                col.objects.unlink(obj)

        imported_count += 1

    # Known item types that have their own specialized import pipeline
    TYPED_ITEM_CLASSES = ("Accessory", "Tool")

    def _import_typed_item(child, parent_collection):
        """
        Import a recognized typed item (Accessory, Tool) as a simple mesh
        at its CFrame coordinates, then apply textures via the existing
        texture pipeline (SurfaceAppearance, TextureId, Decals).
        Uses _import_special_mesh for proven CFrame positioning.
        """
        nonlocal imported_count
        from . import rbx_import_textures
        importlib.reload(rbx_import_textures)

        item_name = child.properties.get("Name", child.class_name)
        dprint(f"  Typed item [{child.class_name}]: {item_name}")

        # Collect all mesh parts to import from this typed item
        mesh_parts_to_import = []  # list of (mesh_instance, parent_part, label)

        if child.class_name == "Accessory":
            handle = child.FindFirstChild("Handle")
            if not handle:
                # Fallback: find first MeshPart child
                handle = child.FindFirstChildOfClass("MeshPart")
            if handle:
                if handle.class_name == "MeshPart":
                    mesh_parts_to_import.append((handle, handle, item_name))
                elif handle.class_name == "Part":
                    sm = handle.FindFirstChildOfClass("SpecialMesh")
                    if sm:
                        mesh_parts_to_import.append((sm, handle, item_name))

        elif child.class_name == "Tool":
            for tc in child.GetChildren():
                tc_name = tc.properties.get("Name", tc.class_name)
                if tc.class_name == "MeshPart":
                    mesh_parts_to_import.append((tc, tc, tc_name))
                elif tc.class_name == "Part":
                    sm = tc.FindFirstChildOfClass("SpecialMesh")
                    if sm:
                        mesh_parts_to_import.append((sm, tc, tc_name))

        if not mesh_parts_to_import:
            # No mesh found; fall back to recursive scan for Part children
            dprint(f"    No mesh in {child.class_name} '{item_name}', scanning children")
            process_children(child.GetChildren(), parent_collection)
            return

        mesh_tmp = tmp_path or os.path.dirname(rbxm_file_path)

        for mesh_instance, parent_part, label in mesh_parts_to_import:
            # Import mesh geometry using the proven _import_special_mesh
            # (handles CFrame positioning correctly)
            obj = _import_special_mesh(
                mesh_instance, parent_part, label,
                headers, mesh_tmp, func_rbx_other, func_rbx_cloud_api
            )

            if obj is None:
                dprint(f"    Failed to import mesh for {label}")
                continue

            # Apply textures via existing texture pipeline
            # (handles SurfaceAppearance PBR, TextureId, Decals)
            if add_textures and headers and func_rbx_cloud_api:
                asset_clean = func_rbx_other.replace_restricted_char(item_name)
                rbx_import_textures.download_and_apply_textures(
                    mesh_instance, label, mesh_tmp,
                    headers, obj, asset_clean
                )

            # Link to parent collection
            if obj.name not in parent_collection.objects:
                parent_collection.objects.link(obj)
            for col in list(obj.users_collection):
                if col != parent_collection:
                    col.objects.unlink(obj)

            imported_count += 1

    def process_children(children, parent_collection):
        """Recursively process all children, creating sub-collections for Models/Folders.
        Detects typed items (Accessory, Tool) and routes them through the existing
        mesh import pipeline. Other unknown containers are still recursively scanned
        for hidden Part-like children."""
        nonlocal imported_count

        for child in children:
            if child.class_name == "Model":
                # Create sub-collection for this Model
                sub_name = func_rbx_other.replace_restricted_char(
                    child.properties.get("Name", "Model")
                )
                sub_col = bpy.data.collections.new(sub_name)
                parent_collection.children.link(sub_col)

                # Recurse into sub-model children
                process_children(child.GetChildren(), sub_col)

            elif child.class_name in PART_CLASS_NAMES:
                _import_part_node(child, parent_collection)

            elif child.class_name in TYPED_ITEM_CLASSES:
                # Route Accessory/Tool through the proper mesh import pipeline
                _import_typed_item(child, parent_collection)

            elif child.class_name == "Folder":
                # Folder → sub-collection
                folder_name = func_rbx_other.replace_restricted_char(
                    child.properties.get("Name", "Folder")
                )
                folder_col = bpy.data.collections.new(folder_name)
                parent_collection.children.link(folder_col)
                process_children(child.GetChildren(), folder_col)

            else:
                # Unknown containers — recurse into children to find Part-like items
                sub_children = child.GetChildren()
                if sub_children:
                    process_children(sub_children, parent_collection)

    # Start processing from roots
    for root in model.roots:
        if root.class_name == "Model":
            # Use the root model name as the collection
            process_children(root.GetChildren(), root_col)
        elif root.class_name in PART_CLASS_NAMES:
            _import_part_node(root, root_col)
        elif root.class_name == "Folder":
            folder_name = func_rbx_other.replace_restricted_char(
                root.properties.get("Name", "Folder")
            )
            folder_col = bpy.data.collections.new(folder_name)
            root_col.children.link(folder_col)
            process_children(root.GetChildren(), folder_col)
        else:
            # Issue-4: Scan unsupported root items for Part children
            sub_children = root.GetChildren()
            if sub_children:
                process_children(sub_children, root_col)

    dprint(f"Model import complete: {imported_count} parts imported.")

    # Snap to origin if requested (preserves relative offsets)
    if at_origin:
        _move_collection_objects_to_origin(root_col)

    # Collapse all collections in the outliner for a clean view
    try:
        for area in bpy.context.screen.areas:
            if area.type == 'OUTLINER':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        with bpy.context.temp_override(area=area, region=region):
                            # Select all items first so collapse applies to everything
                            bpy.ops.outliner.select_all(action='SELECT')
                            # Collapse multiple levels deep
                            for _ in range(10):
                                bpy.ops.outliner.show_one_level(open=False)
                            bpy.ops.outliner.select_all(action='DESELECT')
                        break
                break
    except Exception as e:
        dprint(f"Could not collapse outliner: {e}")

    return root_col
