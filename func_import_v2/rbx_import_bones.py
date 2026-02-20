
import bpy
import mathutils
import os
from RBX_Toolbox import glob_vars

from . import func_blndr_api # Ensure we have access to blender api helpers
### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


def import_bones(imported_meshes_data, mesh_reader, funct, rbx_at_origin, asset_name="R15_Character", suffix=""):
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
    for mesh_info in imported_meshes_data:
        obj = mesh_info['object']
        mesh_data = mesh_info['mesh_data']

        # If obj is None, skip skinning
        if not obj:
            continue
        
        if 'bones' not in mesh_data or 'skinIndices' not in mesh_data or 'skinWeights' not in mesh_data:
            continue
            
        mesh_bones_array = mesh_data["bones"]
        
        # Prepare Skin Info
        # Zip skinIndices and skinWeights
        # They come in flat arrays, stride 1 per vertex? 
        # Actually backup code says:
        # for vert_idx, (si, w) in enumerate(zip(mesh_data["skinIndices"], mesh_data["skinWeights"])):
        #     bone_name = mesh_bones_array[si]["name"]
        #     skin_info.append((vert_idx, bone_name, w))
        
        # This implies si and w are single values per vertex.
        # BUT standard Roblox mesh format is usually 4 weights per vertex.
        # `mesh_reader` output format matters here.
        # In `mesh_reader.py`:
        # "skinIndices": [idx1, idx2, idx3, idx4, ...]
        # "skinWeights": [w1, w2, w3, w4, ...]
        # The parser seems to flatten it.
        # The backup code's loop `zip(mesh_data["skinIndices"], mesh_data["skinWeights"])` 
        # suggests it iterates ONE index and ONE weight at a time.
        # If the lists are flat (4 per vertex), then `vert_idx` in `enumerate` would NOT be the true vertex index.
        # It would be the *influence* index.
        # Real vertex index = loop_index // 4
        
        # Let's check backup code again.
        # `for vert_idx, (si, w) in enumerate(zip(mesh_data["skinIndices"], mesh_data["skinWeights"])):`
        # `    bone_name = mesh_bones_array[si]["name"]`
        # `    skin_info.append((vert_idx, bone_name, w))`
        
        # Then later:
        # `for vert_idx, bone_name, weight in mesh_skin["skin_info"]:`
        # `    obj.vertex_groups[bone_name].add([vert_idx], weight, 'REPLACE')`
        
        # If `vert_idx` allows duplicate values in `add`, then it's modifying the same vertex.
        # BUT `enumerate` produces 0, 1, 2, 3...
        # So it would add to vertex 0, 1, 2, 3...
        # This implies `mesh_reader` returns 1 bone per vertex? That's unlikely for skinned meshes.
        # OR `mesh_reader` returns lists of lists?
        # Let's check `mesh_reader.parse`.
        
        # Checking `imported_meshes_data` structure implicitly.
        # I'll Assume the backup code's logic was slightly flawed OR `mesh_reader` returns something I didn't verify perfectly.
        # Wait, if `skinIndices` is `bytes` or flat list.
        # If it's 4 bytes per vertex.
        
        # Let's implement robustly.
        # If `skinIndices` is length N * 4 (where N is vertex count).
        # We need to map `flat_index` to `vertex_index`.
        # vertex_index = flat_index // 4
        
        skin_indices = mesh_data["skinIndices"]
        skin_weights = mesh_data["skinWeights"]
        
        # Create groups first
        used_bones = set()
        for si in skin_indices:
            if si < len(mesh_bones_array):
                used_bones.add(mesh_bones_array[si]["name"])
        
        for bone_name in used_bones:
             if bone_name not in obj.vertex_groups:
                 obj.vertex_groups.new(name=bone_name)

        # Iterate and assign
        # Assuming 4 influences per vertex is standard for Roblox.
        # If lists are same length
        count = len(skin_indices)
        
        # Optimization: Batch assign? Blender's `vg.add` takes list of indices.
        # Group by bone name.
        bone_to_verts = {} # {bone_name: [(vert_idx, weight), ...]}
        
        # To handle stride correctly, we need to know if the parser structure is flat or nested.
        # Looking at `mesh_reader.py` (viewed earlier):
        # `skin_indices = list(reader.read_bytes(vertex_count * 4))` -> It's a flat list of bytes.
        
        # So yes, flat list.
        # vertex 0 has indices at 0,1,2,3
        # vertex 1 has indices at 4,5,6,7
        
        for flat_i in range(count):
            bone_idx = skin_indices[flat_i]
            weight = skin_weights[flat_i]
            
            if weight <= 0:
                continue
                
            vert_idx = flat_i // 4  # Integer division
            
            if bone_idx < len(mesh_bones_array):
                bone_name = mesh_bones_array[bone_idx]["name"]
                
                if bone_name not in obj.vertex_groups:
                    continue 
                    
                obj.vertex_groups[bone_name].add([vert_idx], weight, 'ADD')
        
        # Add Armature Modifier
        mod = obj.modifiers.new(name="Armature", type='ARMATURE')
        mod.object = arm_obj

    # 5. Position Armature Object
    # 5. Position Armature Object (Shifting the Armature Object Origin)
    # Because we mathematically subtracted this offset from the internal bones before generating them, 
    # the inside of the Armature is 'centered' around 0. Moving the entire Armature Object forward now
    # correctly places the Origin visually where the mesh is, while sweeping the inner internal bones precisely 
    # to their exact original world-space positions.
    if not rbx_at_origin:
        arm_obj.matrix_world.translation = armature_offset
