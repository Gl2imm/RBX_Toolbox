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
    1072: 0.85,  # Asphalt (actually "Rock" in engine)
    1088: 0.95,  # WoodPlanks
    1280: 0.1,   # Glass
    1296: 0.05,  # Neon (emissive, very smooth)
    1312: 0.1,   # ForceField
    832: 0.55,   # CorrodedMetal
    1584: 0.3,   # Plastic (default)
}
DEFAULT_ROUGHNESS = 0.5


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


def apply_part_material(blender_obj, part_instance, func_rbx_other=None):
    """
    Create and assign a Principled BSDF material to a Blender object
    using the Roblox Part's Color3uint8, Material, Transparency, and Reflectance.
    
    This is a standalone function that can be called separately.
    """
    color_raw = part_instance.get("Color3uint8")
    material_id = part_instance.get("Material") or 1584
    transparency = part_instance.get("Transparency") or 0.0
    reflectance = part_instance.get("Reflectance") or 0.0
    part_name = part_instance.properties.get("Name", "Part")

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
            # Base Color from Color3uint8
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
                mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else None
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


def _cframe_to_blender_transform(cframe_dict):
    """
    Convert a Roblox CFrame dict to Blender location + rotation matrix.
    Applies the Roblox→Blender coordinate conversion:
      Blender X = Roblox X
      Blender Y = Roblox -Z
      Blender Z = Roblox Y
    """
    from mathutils import Matrix, Vector

    pos = cframe_dict.get("position", (0, 0, 0))
    rot = cframe_dict.get("rotation", None)

    # Convert position: Roblox (x, y, z) → Blender (x, -z, y)
    bx = pos[0]
    by = -pos[2]
    bz = pos[1]

    if rot and rot[0] == "matrix":
        # Rotation is a 3×3 rotation matrix (row-major)
        # r00, r01, r02, r10, r11, r12, r20, r21, r22
        rm = rot[1]
        # Apply coordinate swap to the rotation matrix
        # Roblox row 0 → Blender row 0 with column swap
        # Roblox row 1 → Blender row 2 with column swap
        # Roblox row 2 → Blender row 1 (negated) with column swap
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


def _create_box(name, size_roblox, cframe_dict, at_origin):
    """
    Create a Blender box mesh matching a Roblox Part.
    size_roblox: (sx, sy, sz) in studs (Roblox coords)
    """
    from mathutils import Matrix, Vector

    # Default Roblox Part size
    if size_roblox is None:
        size_roblox = (4.0, 1.2, 2.0)

    # Convert size: Roblox (sx, sy, sz) → Blender (sx, sz, sy)
    bsx = size_roblox[0]
    bsy = size_roblox[2]  # Roblox Z → Blender Y
    bsz = size_roblox[1]  # Roblox Y → Blender Z

    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.name = name

    # Scale to match Part dimensions
    obj.scale = (bsx, bsy, bsz)

    # Apply CFrame transform
    if cframe_dict and not at_origin:
        transform = _cframe_to_blender_transform(cframe_dict)
        obj.matrix_world = transform
        # Scale must be re-applied after setting matrix_world
        obj.scale = (bsx, bsy, bsz)
    elif at_origin:
        obj.location = (0, 0, 0)

    return obj


def import_model(
    rbxm_file_path: str,
    model_name: str,
    at_origin: bool = True,
    add_textures: bool = True,
    func_rbx_other: Any = None,
    func_blndr_api: Any = None
):
    """
    Import a Roblox Model (.rbxm) as a collection of Blender box primitives.
    
    Each Part in the model becomes a scaled cube with material properties
    applied from its Color3uint8, Material, Transparency, and Reflectance.
    
    Model hierarchy is preserved via Blender collections.
    """
    from . import func_rbx_other as api_other
    from .readers import rbxm_reader

    if func_rbx_other is None:
        func_rbx_other = api_other
    importlib.reload(func_rbx_other)

    dprint(f"Importing model: {model_name} from {rbxm_file_path}")

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

    def process_children(children, parent_collection):
        """Recursively process Model children, creating sub-collections for Models."""
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

            elif child.class_name in ("Part", "MeshPart"):
                part_name = child.properties.get("Name", "Part")
                size = child.get("size")
                cframe = child.get("CFrame")
                transparency = child.get("Transparency") or 0.0

                # Skip fully transparent parts
                if transparency >= 1.0:
                    continue

                if child.class_name == "MeshPart":
                    # MeshPart has a MeshId — download and import the actual mesh
                    mesh_id_raw = child.get("MeshId")
                    mesh_uri = func_rbx_other.resolve_content_uri(mesh_id_raw) if mesh_id_raw else None
                    if mesh_uri:
                        # For now, create a placeholder box matching the part size
                        # Full mesh import can be added later
                        obj = _create_box(part_name, size, cframe, at_origin)
                    else:
                        obj = _create_box(part_name, size, cframe, at_origin)
                else:
                    # Regular Part — create box
                    obj = _create_box(part_name, size, cframe, at_origin)

                if obj is None:
                    continue

                # Apply material properties (color, roughness, etc.)
                if add_textures:
                    apply_part_material(obj, child, func_rbx_other)

                # Link to parent collection, unlink from Scene Collection
                if obj.name not in parent_collection.objects:
                    parent_collection.objects.link(obj)
                for col in list(obj.users_collection):
                    if col != parent_collection:
                        col.objects.unlink(obj)

                imported_count += 1

            elif child.class_name == "Folder":
                # Folder → sub-collection
                folder_name = func_rbx_other.replace_restricted_char(
                    child.properties.get("Name", "Folder")
                )
                folder_col = bpy.data.collections.new(folder_name)
                parent_collection.children.link(folder_col)
                process_children(child.GetChildren(), folder_col)

    # Start processing from roots
    for root in model.roots:
        if root.class_name == "Model":
            # Use the root model name as the collection
            process_children(root.GetChildren(), root_col)
        elif root.class_name in ("Part", "MeshPart"):
            # Standalone Part at root level
            part_name = root.properties.get("Name", "Part")
            size = root.get("size")
            cframe = root.get("CFrame")
            transparency = root.get("Transparency") or 0.0

            if transparency >= 1.0:
                continue

            obj = _create_box(part_name, size, cframe, at_origin)
            if obj:
                if add_textures:
                    apply_part_material(obj, root, func_rbx_other)
                if obj.name not in root_col.objects:
                    root_col.objects.link(obj)
                for col in list(obj.users_collection):
                    if col != root_col:
                        col.objects.unlink(obj)
                imported_count += 1

    dprint(f"Model import complete: {imported_count} parts imported.")

    # Collapse all collections in the outliner for a clean view.
    # Must be deferred — outliner ops don't work during operator execution.
    def _deferred_collapse():
        try:
            for area in bpy.context.screen.areas:
                if area.type == 'OUTLINER':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            with bpy.context.temp_override(area=area, region=region):
                                bpy.ops.outliner.select_all(action='SELECT')
                                for _ in range(10):
                                    bpy.ops.outliner.show_one_level(open=False)
                                bpy.ops.outliner.select_all(action='DESELECT')
                            break
                    break
        except Exception as e:
            dprint(f"Could not collapse outliner: {e}")
        return None  # Don't repeat timer

    bpy.app.timers.register(_deferred_collapse, first_interval=0.1)

    return root_col
