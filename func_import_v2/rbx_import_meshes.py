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
                       parent_name: str = None, skip_download: bool = False, is_layered_clothing: bool = False, is_face_parts: bool = False, parse_bones: bool = False):
    
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
        from RobloxFiles import RobloxFile, Folder, MeshPart, Part, Accessory, Tool, SpecialMesh # type: ignore

    rbx_meshes_to_clean_up_lst = []

    # Unpack Preferences
    add_meshes = prefs.get('add_meshes')
    
    # If not adding meshes and not parsing bones, we can just return empty
    if not add_meshes and not parse_bones:
        return []
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
    
    # Download manager now routes the exact bundle folder via bundles_folder
    bundle_own_folder = bundles_folder
    if not os.path.exists(bundle_own_folder):
        os.makedirs(bundle_own_folder)

    # Look for R15Fixed folder
    # Look for R15Fixed folder
    R15Fixed = rbxm_file.FindFirstChild[Folder]("R15Fixed")
    acc_obj = rbxm_file.FindFirstChildOfClass[Accessory]()

    mesh_parts_to_process = []
    imported_meshes_data = []
    is_gear = False
    
    # Process extracted parts
    if acc_obj:
        dprint(f"Accessory found: {acc_obj.Name}")
        acc_mesh_part = acc_obj.FindFirstChildOfClass[MeshPart]()

        if acc_mesh_part:
             # User Request: "the item added to blender should have same name as it shown in discovery, not handle."
             mesh_parts_to_process.append((acc_mesh_part, asset_name))
        else:
             part_obj = acc_obj.FindFirstChild[Part]("Handle")
             if not part_obj:
                  part_obj = acc_obj.FindFirstChildOfClass[Part]()
             
             if part_obj:
                  special_mesh = part_obj.FindFirstChildOfClass[SpecialMesh]()
                  if special_mesh:
                       mesh_parts_to_process.append((special_mesh, asset_name))
                  else:
                       dprint("Accessory found but no SpecialMesh inside Part.")
             else:
                  dprint("Accessory found but no MeshPart or Part inside.")
            
    elif not R15Fixed:
        # Check for Tool / Gear
        # User requested iteration to find Tool
        tool_obj = rbxm_file.FindFirstChildOfClass[Tool]()
            
        if tool_obj:
            is_gear = True
            dprint(f"Tool (Gear) found: {tool_obj.Name}")
            # Find all Parts / MeshParts inside Tool
            for child in tool_obj.GetChildren():
                if child.ClassName == "Part":
                     dprint(f"  Part found: {child.Name}")
                     special_mesh = child.FindFirstChildOfClass[SpecialMesh]()
                     if special_mesh:
                          dprint(f"    SpecialMesh found in {child.Name}")
                          # We treat this SpecialMesh as the MeshPart to process
                          mesh_parts_to_process.append((special_mesh, child.Name))
                     else:
                          dprint(f"    No SpecialMesh found in {child.Name}.")
                elif child.ClassName == "MeshPart":
                     dprint(f"  MeshPart found: {child.Name}")
                     mesh_parts_to_process.append((child, child.Name))
            
            if not mesh_parts_to_process:
                 dprint("  No Part with SpecialMesh or MeshPart found in Tool.")

        else:
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
        if acc_obj or is_layered_clothing or is_face_parts:
            dprint(f"DEBUG: process_mesh_asset acc_obj found or is_lc/is_fp. is_layered_clothing={is_layered_clothing}, is_face_parts={is_face_parts}")
            # Hierarchy: Main -> Accessories/LC/FP -> AssetName -> Object
            if is_face_parts:
                folder_name = "Face Parts"
            elif is_layered_clothing:
                folder_name = "Layered Clothing"
            else:
                folder_name = "Accessories"
            
            # Determine parent for the Main "Layered Clothing"/"Accessories" folder
            # If collection_name (parent_name/rbx_asset_name) is same as asset_name, we are likely in single import
            # So "Layered Clothing" should be at Root, not inside the Asset Folder.
            lc_parent_col_name = collection_name
            if collection_name == asset_clean_name:
                 lc_parent_col_name = None # Root
            
            dprint(f"DEBUG: creating collection folder_name={folder_name} under parent={lc_parent_col_name}")
            acc_main_col = func_blndr_api.blender_api_create_collection(folder_name, lc_parent_col_name)
            
            # Create specific collection for this accessory inside Accessories/LC
            # This is the "Item Name" collection
            rbx_meshes_col = func_blndr_api.blender_api_create_collection(asset_clean_name, acc_main_col.name)
            
            # Fix for double-linking: If in LC, ensure not in Accessories
            if is_layered_clothing:
                acc_col_obj = bpy.data.collections.get("Accessories")
                if acc_col_obj and rbx_meshes_col.name in acc_col_obj.children:
                    dprint(f"Unlinking {rbx_meshes_col.name} from Accessories...")
                    acc_col_obj.children.unlink(rbx_meshes_col)
                    
        elif is_gear:
            # Hierarchy: Main -> Gears -> AssetName -> Object
            # User request: "Gears - Item_name - item_obj"
            
            # Check if we are in single import mode or bundle
            gear_parent_col_name = collection_name
            if collection_name == asset_clean_name:
                 gear_parent_col_name = None # Root

            gears_main_col = func_blndr_api.blender_api_create_collection("Gears", gear_parent_col_name)
            rbx_meshes_col = func_blndr_api.blender_api_create_collection(asset_clean_name, gears_main_col.name)

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
                #mesh_data = mesh_reader.RBXMeshParser.parse(asset_data)
                mesh_data = mesh_reader.parse(asset_data)
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
            cframe = None
            part_scale = None
            
            # Special Handling for SpecialMesh (Gears)
            if mesh_part.ClassName == "SpecialMesh":
                # CFrame is on the Parent (Part)
                if mesh_part.Parent:
                    cframe = mesh_part.Parent.CFrame
                    # For SpecialMesh, the visual scale is Property Scale (Vector3) * Part.Size? 
                    # Actually SpecialMesh.Scale is usually relative to the file. 
                    # But often used to fit the Part.Size.
                    # Let's try to just use SpecialMesh.Scale first if available.
                    try:
                        part_scale = mesh_part.Scale
                    except:
                        pass
                else:
                    dprint(f"    SpecialMesh {mesh_name} has no Parent!")
                    continue
            else:
                # MeshPart
                cframe = mesh_part.CFrame
            
            # Try to get PivotOffset from MeshPart
            part_cframe_pivot = None
            try:
                # If SpecialMesh, Pivot is on Parent
                obj_for_pivot = mesh_part.Parent if mesh_part.ClassName == "SpecialMesh" else mesh_part
                part_cframe_pivot = obj_for_pivot.Properties["PivotOffset"].Value
            except:
                from RobloxFiles.DataTypes import CFrame as RbxCFrame
                part_cframe_pivot = RbxCFrame()
            
            dprint(f"part_cframe_pivot: {part_cframe_pivot}")
            
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
                # For SpecialMesh (Gear), Parent is Part, Part Parent is Tool. Tool might be "Accessory"-like behavior?
                # Keeping simple check for now.
                check_obj = mesh_part
                if mesh_part.ClassName == "SpecialMesh":
                     check_obj = mesh_part.Parent
                
                if check_obj and check_obj.Parent and check_obj.Parent.ClassName == "Accessory":
                    is_accessory = True

                if is_identity and not is_accessory:
                    actual_at_origin = False

            
            rbx_obj = None
            if add_meshes:
                rbx_obj = func_blndr_api.blender_api_add_meshes_as_obj(
                    bundle_own_folder, mesh_part, mesh_data, cframe, part_cframe_pivot, 
                    actual_at_origin, mesh_reader, funct, mesh_name=mesh_name, 
                    special_mesh_scale=part_scale
                )
            
                # Add Vertex Colors
                if add_ver_col and rbx_obj:
                        func_blndr_api.blender_api_add_ver_col(rbx_obj, mesh_data)


                # Add Textures
                if add_textures and rbx_obj:
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

            # Collect data for bones if object was created or parsing bones
            if (rbx_obj or parse_bones) and mesh_data:
                imported_meshes_data.append({
                    "object": rbx_obj,
                    "mesh_data": mesh_data, # Contains bones, skinIndices, skinWeights, version
                    "mesh_version": mesh_data.get("version", "4.00"),
                    "mesh_name": mesh_name,
                    "cframe": cframe,
                    "actual_at_origin": actual_at_origin,
                    "part_cframe_pivot": part_cframe_pivot
                })

        except Exception as e:
            dprint(f"    Error processing mesh data for {mesh_name}: {e}")
            continue

    # Cleanup (per asset)
    if prefs.get('clean_tmp_meshes', False):
         func_rbx_other.cleanup_tmp_files(rbx_meshes_to_clean_up_lst, ".mesh")
    
    return imported_meshes_data

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
