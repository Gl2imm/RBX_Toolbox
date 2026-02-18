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
                       mesh_reader: Any, funct: Any, func_rbx_cloud_api: Any, func_rbx_other: Any, func_blndr_api: Any,
                       parent_name: str = None, skip_download: bool = False):
    
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
        from RobloxFiles import RobloxFile, Folder, MeshPart, Part, Accessory # type: ignore

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
    
    if not skip_download:
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

    # Check/Create per-asset folder
    asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
    
    # Use parent name for folder grouping if available? 
    # Current behavior puts each part in its own folder. Keeping that for now to avoid complexity unless requested.
    bundle_own_folder = os.path.join(bundles_folder, asset_clean_name)
    if not os.path.exists(bundle_own_folder):
        os.makedirs(bundle_own_folder)

    # Look for R15Fixed folder
    # Look for R15Fixed folder
    R15Fixed = rbxm_file.FindFirstChild[Folder]("R15Fixed")
    acc_obj = rbxm_file.FindFirstChildOfClass[Accessory]()

    mesh_parts_to_process = []
    
    # Process extracted parts
    if acc_obj:
        dprint(f"Accessory found: {acc_obj.Name}")
        acc_mesh_part = acc_obj.FindFirstChildOfClass[MeshPart]()

        if acc_mesh_part:
             # User Request: "the item added to blender should have same name as it shown in discovery, not handle."
             mesh_parts_to_process.append((acc_mesh_part, asset_name))
        else:
            dprint("Accessory found but no MeshPart inside.")
            
    elif not R15Fixed:
        dprint(f"No R15Fixed folder found in {asset_name}. Checking for Dynamic Head...")
        
        # Try Dynamic Head Import
        head_mesh_part, new_rbxm_file = process_dynamic_head(
            headers, rbx_tmp_rbxm_filepath, rbxm_file, func_rbx_cloud_api, str(asset_id)
        )
        
        if head_mesh_part:
            dprint("Dynamic Head Found and Processed.")
            mesh_parts_to_process.append((head_mesh_part, "Head"))
            # Update rbxm_file ref if needed, though we operate on the mesh_part mainly
        else:
            dprint("Dynamic Head check failed or not a head.")
            return


    else:
        # 4. Standard R15Fixed Processing
        rbx_avatar_bundle_parts = [
                "LeftUpperArm", "LeftLowerArm", "LeftHand",
                "RightUpperArm", "RightLowerArm", "RightHand",
                "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
                "RightUpperLeg", "RightLowerLeg", "RightFoot",
                "UpperTorso", "LowerTorso", "Head"
            ]

        for mesh_name in rbx_avatar_bundle_parts:
            mesh_part = R15Fixed.FindFirstChild[MeshPart](mesh_name)
            if mesh_part:
                mesh_parts_to_process.append((mesh_part, mesh_name))
    
    # Process extracted parts
    # Check/Create Main Asset Collection
    
    # Determine Collection Name
    # Determine Collection Name
    if parent_name:
        collection_name = func_rbx_other.replace_restricted_char(parent_name)
    else:
        collection_name = asset_clean_name

    if add_meshes:
        if acc_obj:
            # Hierarchy: Main -> Accessories -> AssetName -> Object
            acc_main_col = func_blndr_api.blender_api_create_collection("Accessories", collection_name)
            # Create specific collection for this accessory inside Accessories
            rbx_meshes_col = func_blndr_api.blender_api_create_collection(asset_clean_name, acc_main_col.name)
        else:
            # Hierarchy: Main -> Body Parts -> Object
            rbx_meshes_col = func_blndr_api.blender_api_create_collection("Body Parts", collection_name)



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
                
            try:
                mesh_data = mesh_reader.RBXMeshParser.parse(asset_data)
            except Exception as e:
                error_msg = f"Error processing mesh {mesh_name}: {e}"
                dprint(error_msg)
                glob_vars.rbx_imp_error = error_msg
                bpy.context.workspace.status_text_set(error_msg)
                continue
            
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
            
            # Note: at_origin logic is now handled post-import as a group operation.
            # We pass 'at_origin' but it is ignored by the blender_api function for individual placement.
            # Effectively we are placing everything at World Coordinates first.
            
            # Check if Pivot is Identity
            # If so, disable "Spawn at Origin" for this mesh
            actual_at_origin = at_origin
            if part_cframe_pivot:
                pivot_comps = part_cframe_pivot.GetComponents()
                identity_comps = (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
                is_identity = True
                if len(pivot_comps) == 12:
                    for a, b in zip(pivot_comps, identity_comps):
                        if abs(a - b) > 0.0001: 
                            is_identity = False
                            break
                            
                # Special Case: Accessories
                # Accessories often have Identity Pivot on Handle but should still respect "Spawn at Origin"
                # because the user wants them centered, not at World Position.
                is_accessory = False
                if mesh_part.Parent and mesh_part.Parent.ClassName == "Accessory":
                    is_accessory = True

                if is_identity and not is_accessory:
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

            # Move to Collection (Meshes Sub-Collection)
            if rbx_meshes_col and rbx_obj:
                # Link to proper collection
                if rbx_obj.name not in rbx_meshes_col.objects:
                    rbx_meshes_col.objects.link(rbx_obj)
                
                # Unlink from other collections (e.g. Scene Collection where it was spawned)
                for col in rbx_obj.users_collection:
                    if col != rbx_meshes_col:
                        col.objects.unlink(rbx_obj)
            
            # Append to cleanup list for .mesh files
            rbx_meshes_to_clean_up_lst.append(mesh_name)

        except Exception as e:
            dprint(f"    Error processing mesh data for {mesh_name}: {e}")
            continue

    # Cleanup (per asset)
    if prefs.get('clean_tmp_meshes', False):
         func_rbx_other.cleanup_tmp_files(rbx_meshes_to_clean_up_lst, ".mesh")
    
    return

def process_dynamic_head(headers: dict, rbx_tmp_rbxm_filepath: str, rbxm_file, 
                         func_rbx_cloud_api, rbxm_id: str):
    """
    Checks for and processes a Dynamic Head from the RBXM file.
    Returns the MeshPart object if found and successfully processed/reloaded, else None.
    """
    if not TYPE_CHECKING:
        from RobloxFiles import RobloxFile, MeshPart, SpecialMesh, Folder # type: ignore

    # Check if we already have the Dynamic Head (e.g. upgraded by download manager)
    head_part_existing = rbxm_file.FindFirstChild[MeshPart]("Head")
    if head_part_existing:
        dprint("Found existing Dynamic Head MeshPart 'Head'. Skipping re-download.")
        return head_part_existing, rbxm_file

    special_mesh = rbxm_file.FindFirstChild[SpecialMesh]("Mesh")
    if special_mesh:
        dprint("Special Mesh 'Mesh' found, checking if it is a dynamic head candidate...")
        
        is_dynamic_head = True # Tentative
        dprint("Special Mesh exist, mesh is a dynamic head candidate")
        
        # Download as avatar_meshpart_head
        dprint(f"Re-downloading {rbxm_id} as avatar_meshpart_head...")
        asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(rbxm_id, headers, RobloxAssetFormat="avatar_meshpart_head")
        
        if not rbx_imp_error and asset_data:
            rbxm_file_path = os.path.join(rbx_tmp_rbxm_filepath, str(rbxm_id) + ".rbxm")
            
            with open(rbxm_file_path, "wb") as f:
                f.write(asset_data)
            
            # Re-open the file
            try:
                if not TYPE_CHECKING:
                    from RobloxFiles import RobloxFile, MeshPart # type: ignore

                rbxm_file_reloaded = RobloxFile.Open(rbxm_file_path)
                # Now expect a MeshPart named "Head" (usually)
                head_part = rbxm_file_reloaded.FindFirstChild[MeshPart]("Head")
                
                if head_part:
                     dprint("Successfully upgraded to Dynamic Head MeshPart!")
                     return head_part, rbxm_file_reloaded 
                else:
                    dprint("Downloaded data but 'Head' MeshPart not found.")
                    return None, None
            except Exception as e:
                dprint(f"Error re-opening dynamic head RBXM: {e}")
                return None, None
        else:
            dprint(f"Failed to download dynamic head data: {rbx_imp_error}")
            return None, None

    return None, None
