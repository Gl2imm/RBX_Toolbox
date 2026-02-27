
import bpy
import mathutils
import os
from RBX_Toolbox import glob_vars

from . import func_blndr_api # Ensure we have access to blender api helpers
### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


def apply_skin_weights(imported_meshes_data, arm_obj):
    """
    Applies skin weights from parsed mesh data to Blender mesh objects.
    Creates vertex groups for each bone and assigns weights based on skinIndices/skinWeights.
    Also adds an Armature modifier to each mesh pointing to arm_obj.
    
    imported_meshes_data: List of dicts {'object': obj, 'mesh_data': data, 'mesh_name': name, ...}
    arm_obj: The armature object to bind meshes to
    
    Data format (from mesh_reader.py):
        skinIndices: flat list[int], stride 4 per vertex (4 bone influences per vertex)
        skinWeights: flat list[float], stride 4 per vertex (normalized 0.0-1.0)
        bones: list of bone dicts with 'name' key
    """
    if not arm_obj:
        dprint("apply_skin_weights: No armature object provided, skipping.")
        return
    
    for mesh_info in imported_meshes_data:
        obj = mesh_info.get('object')
        mesh_data = mesh_info.get('mesh_data', {})
        mesh_name = mesh_info.get('mesh_name', 'Unknown')

        # Skip if no valid object
        if not obj:
            continue
        
        # Skip if missing required skinning data
        if 'bones' not in mesh_data or 'skinIndices' not in mesh_data or 'skinWeights' not in mesh_data:
            dprint(f"apply_skin_weights: Skipping '{mesh_name}' - missing skin data.")
            continue
            
        mesh_bones_array = mesh_data["bones"]
        skin_indices = mesh_data["skinIndices"]
        skin_weights = mesh_data["skinWeights"]
        
        # Create vertex groups for all referenced bones
        used_bones = set()
        for si in skin_indices:
            if si < len(mesh_bones_array):
                used_bones.add(mesh_bones_array[si]["name"])
        
        for bone_name in used_bones:
            if bone_name not in obj.vertex_groups:
                obj.vertex_groups.new(name=bone_name)

        # Assign weights
        # skinIndices/skinWeights are flat arrays with stride 4 (4 influences per vertex)
        # vertex 0 -> indices [0,1,2,3], vertex 1 -> indices [4,5,6,7], etc.
        count = len(skin_indices)
        
        for flat_i in range(count):
            bone_idx = skin_indices[flat_i]
            weight = skin_weights[flat_i]
            
            if weight <= 0:
                continue
                
            vert_idx = flat_i // 4  # 4 influences per vertex
            
            if bone_idx < len(mesh_bones_array):
                bone_name = mesh_bones_array[bone_idx]["name"]
                
                if bone_name not in obj.vertex_groups:
                    continue 
                    
                obj.vertex_groups[bone_name].add([vert_idx], weight, 'ADD')
        
        # Add Armature Modifier
        mod = obj.modifiers.new(name="Armature", type='ARMATURE')
        mod.object = arm_obj
        
        dprint(f"apply_skin_weights: Applied weights to '{mesh_name}' ({len(used_bones)} bone groups)")


def _strip_blender_suffix(name):
    """
    Strip Blender's auto-added numeric suffixes like .001, .002, etc.
    'UpperTorso.001' -> 'UpperTorso'
    'Head' -> 'Head'
    """
    import re
    return re.sub(r'\.\d{3,}$', '', name)


def link_armature_to_meshes(arm_obj, imported_meshes_data, asset_name=None):
    """
    Finds existing Blender mesh objects in the scene by matching mesh_name,
    and applies skin weights + armature modifier to them.
    
    This handles the case where body part meshes were imported separately
    before the armature was created (so 'object' is None in imported_meshes_data).
    
    arm_obj: The armature object to link meshes to
    imported_meshes_data: List of dicts with 'object', 'mesh_data', 'mesh_name', etc.
    asset_name: The main asset/bundle name — used to find the correct collection
                (so we don't accidentally match meshes from a different rig)
    """
    if not arm_obj:
        dprint("link_armature_to_meshes: No armature object provided, skipping.")
        return
    
    # Gather mesh_infos that have no object but have skin data
    unlinked = []
    for mesh_info in imported_meshes_data:
        if mesh_info.get('object') is not None:
            continue  # Already has an object, skip
        mesh_data = mesh_info.get('mesh_data', {})
        if 'bones' in mesh_data and 'skinIndices' in mesh_data and 'skinWeights' in mesh_data:
            unlinked.append(mesh_info)
    
    if not unlinked:
        dprint("link_armature_to_meshes: No unlinked meshes with skin data found.")
        return
    
    dprint(f"link_armature_to_meshes: Found {len(unlinked)} unlinked meshes, searching scene...")
    
    # Build candidate list: prefer objects inside the asset's collection
    # This ensures we match the correct rig when multiple rigs exist
    candidate_objects = []
    
    if asset_name:
        # Search for a collection matching the asset name (strip restricted chars)
        # The collection hierarchy is: asset_name -> "Body Parts" -> mesh objects
        for col in bpy.data.collections:
            col_base = _strip_blender_suffix(col.name)
            if col_base == asset_name or asset_name in col.name:
                # Collect all mesh objects recursively from this collection
                _collect_mesh_objects_recursive(col, candidate_objects)
                dprint(f"link_armature_to_meshes: Found collection '{col.name}' for asset '{asset_name}' ({len(candidate_objects)} mesh objects)")
                break
    
    # Fallback: if no collection found or no candidates, search all scene objects
    if not candidate_objects:
        dprint(f"link_armature_to_meshes: No collection found for '{asset_name}', searching all scene objects...")
        candidate_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    
    # Search for matching mesh objects
    linked_count = 0
    for mesh_info in unlinked:
        mesh_name = mesh_info.get('mesh_name', '')
        if not mesh_name:
            continue
        
        found_obj = None
        
        for obj in candidate_objects:
            # Strip Blender suffix for comparison
            obj_base_name = _strip_blender_suffix(obj.name)
            
            if obj_base_name == mesh_name:
                # Avoid matching objects that already have an armature modifier
                has_armature = any(mod.type == 'ARMATURE' for mod in obj.modifiers)
                if not has_armature:
                    found_obj = obj
                    break
        
        if found_obj:
            dprint(f"link_armature_to_meshes: Matched '{mesh_name}' -> '{found_obj.name}'")
            mesh_info['object'] = found_obj
            linked_count += 1
        else:
            dprint(f"link_armature_to_meshes: No scene object found for '{mesh_name}'")
    
    if linked_count > 0:
        dprint(f"link_armature_to_meshes: Applying weights to {linked_count} linked meshes...")
        apply_skin_weights(imported_meshes_data, arm_obj)
    else:
        dprint("link_armature_to_meshes: No meshes could be matched to scene objects.")


def _collect_mesh_objects_recursive(collection, result_list):
    """Recursively collect all MESH type objects from a collection and its children."""
    for obj in collection.objects:
        if obj.type == 'MESH' and obj not in result_list:
            result_list.append(obj)
    for child_col in collection.children:
        _collect_mesh_objects_recursive(child_col, result_list)


def import_bones(imported_meshes_data, mesh_reader, funct, rbx_at_origin, asset_name="R15_Character", suffix="", link_meshes=True):
    """
    Creates an armature and applies skinning based on the imported mesh data.
    imported_meshes_data: List of dicts {'object': obj, 'mesh_data': data, 'mesh_name': name}
    asset_name: Name of the asset (used for collection and object naming)
    """
    
    # 1. Collect all unique bones from all meshes
    all_bones_data = {}

    # Check mesh versions for armature compatibility
    has_old_meshes = False
    for mesh_info in imported_meshes_data:
        version_str = mesh_info.get("mesh_version", "4.00")
        try:
            version_float = float(version_str)
            if version_float < 4.00:
                has_old_meshes = True
                break
        except ValueError:
            pass
            
    if has_old_meshes:
        glob_vars.rbx_armature_warning_active = True


    #### Debug prints (Keep this disabled for normal use)  
    debug_txt_path = os.path.join(os.path.dirname(__file__), "bones_data.txt")
    write_debug = False
    
    if write_debug:
        try:
            f = open(debug_txt_path, "w", encoding="utf-8")
            f.write("--- BONES DATA BY MESH ---\n\n")
        except:
            f = None
    else:
        f = None

    for mesh_info in imported_meshes_data:
        mesh_data = mesh_info['mesh_data']
        mesh_name = mesh_info.get('mesh_name', 'UnknownMesh')
        
        if f: f.write(f"Mesh: {mesh_name}\n")
        
        if 'bones' in mesh_data:
            mesh_bones_array = mesh_data["bones"]
            if f:
                f.write(f"  Found {len(mesh_bones_array)} bones:\n")
            
            for bone in mesh_bones_array:
                if f:
                    f.write(f"    - {str(bone)}\n")
                
                if bone["name"] not in all_bones_data:
                    # 1. Transform Bone CFrame to Absolute World Matrix
                    bone_data = bone.copy()
                    part_cframe = mesh_info.get("cframe")
                    bone_local_cframe = bone.get("cframe")
                    
                    part_blender_matrix = funct.cframe_to_blender_matrix(part_cframe) if part_cframe else None
                    
                    if bone_local_cframe and part_blender_matrix:
                        bone_local_matrix = funct.cframe_to_blender_matrix(bone_local_cframe)
                        # World Blender Matrix (Unoriented) = Mesh * Bone
                        world_bone_matrix = part_blender_matrix @ bone_local_matrix
                        # Oriented World Matrix for Blender
                        oriented_world_bone_matrix = funct.blender_matrix_axis_conversion(world_bone_matrix)
                        
                        # Spawn at origin logic
                        actual_at_origin = mesh_info.get("actual_at_origin", False)
                        part_cframe_pivot = mesh_info.get("part_cframe_pivot")
                        
                        if actual_at_origin and part_cframe_pivot:
                            oriented_part_matrix = funct.blender_matrix_axis_conversion(part_blender_matrix)
                            blender_matrix_pivot = funct.cframe_to_blender_matrix(part_cframe_pivot)
                            raw_local_pivot = blender_matrix_pivot.translation
                            rot_mat = oriented_part_matrix.to_3x3()
                            rotated_pivot_vector = rot_mat @ raw_local_pivot
                            pivot_world_pos = oriented_part_matrix.translation + rotated_pivot_vector
                            
                            oriented_world_bone_matrix.translation -= pivot_world_pos
                        
                        bone_data["world_matrix"] = oriented_world_bone_matrix
                    else:
                        bone_data["world_matrix"] = None
                        
                    all_bones_data[bone["name"]] = bone_data
        else:
            if f: f.write("  No bones found in this mesh.\n")
            
        if f: f.write("\n")
        
    if f:
        try:
            f.write("--- FINAL COMBINED DATA ---\n\n")
            f.write(f"Total unique bones: {len(all_bones_data)}\n")
            for b_name, b_data in all_bones_data.items():
                f.write(f"  {b_name}: {str(b_data)}\n")
            f.close()
        except:
            pass


    if not all_bones_data:
        print("No bones found in imported data.")
        return

    # Find a reference mesh to align with (prefer Torso/Root)
    target_info = None
    for info in imported_meshes_data:
        name = info.get('mesh_name', '')
        if 'Torso' in name or 'Root' in name:
            target_info = info
            break
            
    if not target_info and imported_meshes_data:
        target_info = imported_meshes_data[0]
        
    armature_offset = mathutils.Vector((0,0,0))
    if target_info and not rbx_at_origin:
        # Re-derive world position instead of trusting matrix_world before dependency graph update
        part_cframe = target_info.get("cframe")
        part_cframe_pivot = target_info.get("part_cframe_pivot")
        if part_cframe and part_cframe_pivot:
            blender_matrix = funct.cframe_to_blender_matrix(part_cframe)
            blender_matrix_pivot = funct.cframe_to_blender_matrix(part_cframe_pivot)
            
            # Pivot World Matrix = Center * PivotOffset
            world_pivot_rbx = blender_matrix @ blender_matrix_pivot
            world_pivot_b3d = funct.blender_matrix_axis_conversion(world_pivot_rbx)
            
            # This matches exact logic from func_blndr_api
            armature_offset = world_pivot_b3d.translation

        for b_name, b_data in all_bones_data.items():
            world_matrix = b_data.get("world_matrix")
            if world_matrix:
                world_matrix.translation -= armature_offset

    # 2. Create Hierarchy & Object
    # User Request: item_name -> Armature -> arma obj 
    
    # Create/Get Armature Sub-Collection inside Item Name collection
    # We pass asset_name as parent_name. If asset_name doesn't exist, CreateCollection will create it at root.
    arm_col = func_blndr_api.blender_api_create_collection("Armature", asset_name)
    
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode='OBJECT')
        
    bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
    arm_obj = bpy.context.object
    arm = arm_obj.data
    
    # Name the object
    if suffix:
        arm_obj.name = f"Armature_{asset_name}_{suffix}"
    else:
        arm_obj.name = f"Armature_{asset_name}"
    
    # Link to Armature Collection and Unlink from elsewhere
    if arm_obj.name not in arm_col.objects:
        arm_col.objects.link(arm_obj)
        
    for col in arm_obj.users_collection:
        if col != arm_col:
            col.objects.unlink(arm_obj)


    # 3. Create Bones (Edit Mode)
    # --- PASS 1: Create all bones ---
    for bone_name, bd in all_bones_data.items():
        if bone_name not in arm.edit_bones.keys():
            eb = arm.edit_bones.new(bone_name)

            # Use computed world_matrix to place bone
            world_matrix = bd.get("world_matrix")
            if world_matrix:
                head, tail = funct.matrix_to_bone_positions(world_matrix)
                eb.head = head
                eb.tail = tail
            else:
                # fallback if no cframe
                eb.head = mathutils.Vector((0, 0, 0))
                eb.tail = mathutils.Vector((0, 0.1, 0))

    # --- PASS 2: Set parents ---
    for bone_name, bd in all_bones_data.items():
        parent = bd.get("parent")  # dict or None
        parent_name = parent["name"] if parent else None

        if parent_name and parent_name in arm.edit_bones.keys():
            child_bone = arm.edit_bones[bone_name]
            parent_bone = arm.edit_bones[parent_name]
            child_bone.parent = parent_bone
            child_bone.use_connect = False  # keep world-space head/tail
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # 4. Apply Skins (Vertex Weights)
    apply_skin_weights(imported_meshes_data, arm_obj)
    
    # 4b. Link existing scene meshes if objects were not spawned (armature-only import)
    if link_meshes:
        link_armature_to_meshes(arm_obj, imported_meshes_data, asset_name=asset_name)
    else:
        dprint("import_bones: Skipping mesh linking (link_meshes=False)")

    # 5. Position Armature Object
    # Because we mathematically subtracted this offset from the internal bones before generating them, 
    # the inside of the Armature is 'centered' around 0. Moving the entire Armature Object forward now
    # correctly places the Origin visually where the mesh is, while sweeping the inner internal bones precisely 
    # to their exact original world-space positions.
    if not rbx_at_origin:
        arm_obj.matrix_world.translation = armature_offset
