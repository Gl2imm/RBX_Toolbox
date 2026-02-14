import bpy
import os
import importlib
from RBX_Toolbox import glob_vars
from typing import TYPE_CHECKING, Any, Dict, List

# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def process_mesh_asset(asset_id: int, asset_name: str, headers: dict, prefs: Dict[str, Any], 
                       bundles_folder: str, rbx_tmp_rbxm_filepath: str, 
                       mesh_reader: Any, funct: Any, func_rbx_cloud_api: Any, func_rbx_other: Any, func_blndr_api: Any):
    
    # Initialize Context & Dependencies
    import clr
    from System.Reflection import Assembly # type: ignore
    try:
        clr.AddReference(robloxfile_dll) # type: ignore
    except:
        pass
    
    # Reload Dependencies
    from . import func_blndr_api, rbx_import_textures
    importlib.reload(func_blndr_api)
    importlib.reload(rbx_import_textures)

    if not TYPE_CHECKING:
        from RobloxFiles import RobloxFile, Folder, MeshPart # type: ignore

    rbx_meshes_to_clean_up_lst = []

    # Unpack Preferences
    at_origin = prefs.get('at_origin', False)
    add_meshes = prefs.get('add_meshes', True)
    add_textures = prefs.get('add_textures', True)
    add_attachment = prefs.get('add_attachment', False)
    add_ver_col = prefs.get('add_ver_col', False)
    
    # Force meshes if textures are requested
    if add_textures and not add_meshes:
        add_meshes = True

    # 1. Download RBXM
    rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
    
    # Always download to ensure freshness or handle missing files
    asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(asset_id, headers)
    
    if rbx_imp_error or not asset_data:
        dprint(f"Error downloading asset {asset_id}: {rbx_imp_error}")
        return

    try:
        with open(rbx_tmp_rbxm_file, "wb") as f:
            f.write(asset_data)
    except Exception as e:
        dprint(f"Error saving RBXM {asset_id}: {e}")
        return
        
    # 2. Open RBXM
    try:
        rbxm_file = RobloxFile.Open(rbx_tmp_rbxm_file)
    except Exception as e:
        dprint(f"Error opening RBXM {asset_id}: {e}")
        return

    # Look for R15Fixed folder
    R15Fixed = rbxm_file.FindFirstChild[Folder]("R15Fixed")
    if not R15Fixed:
        dprint(f"No R15Fixed folder found in {asset_name}")
        return
        
    # 3. Create Collection and Folder
    main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
    main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)
    
    rbx_collection = func_blndr_api.blender_api_create_collection("Meshes", main_collection_name)
    
    bundle_own_folder = os.path.join(bundles_folder, main_collection_name)
    if not os.path.exists(bundle_own_folder):
        os.makedirs(bundle_own_folder)
        
    asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)

    # 4. Process MeshParts
    rbx_avatar_bundle_parts = [
            "LeftUpperArm", "LeftLowerArm", "LeftHand",
            "RightUpperArm", "RightLowerArm", "RightHand",
            "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
            "RightUpperLeg", "RightLowerLeg", "RightFoot",
            "UpperTorso", "LowerTorso", "Head"
        ]

    mesh_parts_to_process = []
    for mesh_name in rbx_avatar_bundle_parts:
        mesh_part = R15Fixed.FindFirstChild[MeshPart](mesh_name)
        if mesh_part:
            mesh_parts_to_process.append((mesh_part, mesh_name))
    
    # Process extracted parts
    for mesh_part, mesh_name in mesh_parts_to_process:
        dprint(f"  - Processing MeshPart: {mesh_name}")
        
        # Extract Mesh Data
        mesh_id = mesh_part.MeshId
        if not mesh_id:
            dprint(f"    No MeshId for {mesh_name}")
            continue

        # Download Mesh Data
        try:
            mesh_id_clean = func_rbx_other.strip_rbxassetid(mesh_id)
            asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(mesh_id_clean, headers)
            
            if rbx_imp_error or not asset_data:
                dprint(f"    Error downloading/reading mesh {mesh_name}: {rbx_imp_error}")
                continue
                
            mesh_data = mesh_reader.RBXMeshParser.parse(asset_data)
            
            if not mesh_data:
                dprint(f"    No mesh data parsed for {mesh_name}")
                continue
                
            # --- START SPAWN LOGIC INLINED ---
            
            # Pivot Logic
            cframe = mesh_part.CFrame
            
            # Try to get PivotOffset from MeshPart
            try:
                part_cframe_pivot = mesh_part.Properties["PivotOffset"].Value
            except:
                from RobloxFiles.DataTypes import CFrame as RbxCFrame
                part_cframe_pivot = RbxCFrame()

            # Check if pivot is identity
            pivot_comps = part_cframe_pivot.GetComponents()
            identity_comps = (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
            is_identity = True
            if len(pivot_comps) == 12:
                for a, b in zip(pivot_comps, identity_comps):
                    if abs(a - b) > 0.0001: 
                        is_identity = False
                        break
            
            # If pivot is identity, force at_origin to False
            actual_at_origin = at_origin
            if is_identity:
                actual_at_origin = False

            rbx_obj = None
            if add_meshes:
                rbx_obj = func_blndr_api.blender_api_add_meshes_as_obj(
                    bundle_own_folder, mesh_part, mesh_data, cframe, part_cframe_pivot, 
                    actual_at_origin, mesh_reader, funct, mesh_name=mesh_name
                )
            
            # Add Vertex Colors
            if add_meshes and add_ver_col and rbx_obj:
                    func_blndr_api.blender_api_add_ver_col(rbx_obj, mesh_data)

            # Add Textures
            if add_meshes and add_textures and rbx_obj:
                    rbx_import_textures.download_and_apply_textures(
                        mesh_part, mesh_name, bundle_own_folder, headers, rbx_obj, asset_clean_name
                    )

            # Move to Collection
            if rbx_collection and rbx_obj:
                    if rbx_obj.name not in rbx_collection.objects:
                        rbx_collection.objects.link(rbx_obj)



            # Append to cleanup list for .mesh files
            rbx_meshes_to_clean_up_lst.append(mesh_name)

        except Exception as e:
            dprint(f"    Error processing mesh data for {mesh_name}: {e}")
            continue

    # Cleanup (per asset)
    if prefs.get('clean_tmp_meshes', False):
         func_rbx_other.cleanup_tmp_files(rbx_meshes_to_clean_up_lst, ".mesh")
