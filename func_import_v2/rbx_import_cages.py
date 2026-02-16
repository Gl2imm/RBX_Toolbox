import bpy
import os
import importlib
import re
from RBX_Toolbox import glob_vars
from typing import TYPE_CHECKING, List, Any, Dict, Union

# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def download_and_apply_cages(target: Union[int, Any], mesh_name: str, bundle_own_folder: str, headers: dict, 
                             asset_clean_name: str, rbx_tmp_rbxm_filepath: str, 
                             at_origin: bool, add_ver_col: bool,
                             mesh_reader: Any, funct: Any, rbx_meshes_to_clean_up_lst: List[str],
                             func_rbx_cloud_api: Any = None, func_rbx_other: Any = None, func_blndr_api: Any = None,
                             skip_download: bool = False):
    """
    Downloads the RBXM asset and iterates through its Body Parts to apply cages.
    """
    
    # Reload Dependencies & Setup Context
    from . import func_rbx_cloud_api as api_cloud, func_rbx_other as api_other, func_blndr_api as api_blend
    
    if func_rbx_cloud_api is None: func_rbx_cloud_api = api_cloud
    if func_rbx_other is None: func_rbx_other = api_other
    if func_blndr_api is None: func_blndr_api = api_blend

    importlib.reload(func_rbx_cloud_api)
    importlib.reload(func_rbx_other)
    importlib.reload(func_blndr_api)

    import clr
    from System.Reflection import Assembly # type: ignore
    try:
        clr.AddReference(robloxfile_dll) # type: ignore
    except:
        pass

    if not TYPE_CHECKING:
        from RobloxFiles import RobloxFile, Folder, MeshPart, WrapTarget, SpecialMesh # type: ignore

    # === CASE 1: Target is Asset ID (Polymorphic Entry) ===
    if isinstance(target, int) or (isinstance(target, str) and str(target).isdigit()):
        asset_id = int(target)
        dprint(f"Processing Cages for Asset ID: {asset_id}")

        rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
        
        if not skip_download:
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
            
        try:
            rbxm_file = RobloxFile.Open(rbx_tmp_rbxm_file)
        except Exception as e:
            dprint(f"Error opening RBXM {asset_id}: {e}")
            return

        R15Fixed = rbxm_file.FindFirstChild[Folder]("R15Fixed")
        
        parts_to_process = []
        if not R15Fixed:
            dprint(f"No R15Fixed folder found using standard check. Checking for Dynamic Head SpecialMesh...")
            
            # Check for SpecialMesh "Mesh" (Raw Dynamic Head)
            special_mesh = rbxm_file.FindFirstChild[SpecialMesh]("Mesh")
            if special_mesh:
                dprint("Special Mesh 'Mesh' found, attempting to upgrade to Dynamic Head MeshPart...")
                
                # Re-download as avatar_meshpart_head
                asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(asset_id, headers, RobloxAssetFormat="avatar_meshpart_head")
                
                if not rbx_imp_error and asset_data:
                    # Overwrite temp file with new data
                    try:
                        with open(rbx_tmp_rbxm_file, "wb") as f:
                            f.write(asset_data)
                        
                        # Re-open the file
                        rbxm_file = RobloxFile.Open(rbx_tmp_rbxm_file)
                        head_part = rbxm_file.FindFirstChild[MeshPart]("Head")
                        
                        if head_part:
                             dprint("Successfully upgraded to Dynamic Head MeshPart 'Head'. Processing...")
                             parts_to_process.append((head_part, "Head"))
                        else:
                            dprint("Downloaded data but 'Head' MeshPart not found.")
                            return
                    except Exception as e:
                        dprint(f"Error re-processing dynamic head RBXM: {e}")
                        return
                else:
                    dprint(f"Failed to download avatar_meshpart_head: {rbx_imp_error}")
                    return

            else:
                 # Check if we already have a Head MeshPart (maybe it was already processed/cached?)
                head_part = rbxm_file.FindFirstChild[MeshPart]("Head")
                if head_part:
                    dprint("Found Dynamic Head MeshPart 'Head' directly. Processing...")
                    parts_to_process.append((head_part, "Head"))
                else:
                    children = [c.Name for c in rbxm_file.GetChildren()]
                    dprint(f"Children found: {children}")
                    return
        else:    
            dprint(f"Found R15Fixed folder. Checking children...")
            # Loop children
            rbx_avatar_bundle_parts = [
                    "LeftUpperArm", "LeftLowerArm", "LeftHand",
                    "RightUpperArm", "RightLowerArm", "RightHand",
                    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
                    "RightUpperLeg", "RightLowerLeg", "RightFoot",
                    "UpperTorso", "LowerTorso", "Head"
                ]
            
            for part_name in rbx_avatar_bundle_parts:
                mesh_part = R15Fixed.FindFirstChild[MeshPart](part_name)
                if mesh_part:
                    parts_to_process.append((mesh_part, part_name))

        # Create folder structure for the bundle
        main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
        main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)
        
        target_bundle_folder = os.path.join(bundle_own_folder, main_collection_name) if 'Imported Body Parts' in bundle_own_folder else bundle_own_folder
        
        if not os.path.exists(target_bundle_folder):
                if not os.path.exists(bundle_own_folder): # Safe check
                    os.makedirs(bundle_own_folder)


        for mesh_part, part_name in parts_to_process:
            dprint(f"  -> Found Body Part: {part_name}, checking for cages...")
            # Process single cage
            _process_single_cage(
                mesh_part, part_name, target_bundle_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                at_origin, add_ver_col,
                mesh_reader, funct, rbx_meshes_to_clean_up_lst,
                func_rbx_cloud_api, func_rbx_other, func_blndr_api
            )
        
        # Cleanup
        
        # Cleanup
        # Note: clean_tmp_meshes is not passed in anymore, assuming it's handled outside or defaults to False for now to match signature
        # Or better, we can assume if this is called from bundle char, cleanup happens there. 
        # But wait, download_manager invokes this too. 
        # For now, let's remove the prefs check and rely on caller to cleanup if needed, 
        # OR we just remove this block since rbx_import_bundle_char handles its own cleanup.
        # But download_manager might need it. 
        # Let's check if rbx_meshes_to_clean_up_lst is populated.
        # If the caller provided the list, they can clean it up.
        pass
        
        return
    
    # === CASE 2: Target is MeshPart (Called from Bundle Importer) ===
    else:
        # Assuming target is a MeshPart object (or duck-typed enough)
        # Verify it has FindFirstChild
        if hasattr(target, "FindFirstChild"):
             _process_single_cage(
                target, mesh_name, bundle_own_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                at_origin, add_ver_col,
                mesh_reader, funct, rbx_meshes_to_clean_up_lst,
                func_rbx_cloud_api, func_rbx_other, func_blndr_api
            )
        else:
             dprint(f"Invalid target type for cages: {type(target)}")
             return


def _process_single_cage(mesh_part, mesh_name, bundle_own_folder, headers, 
                         asset_clean_name, rbx_tmp_rbxm_filepath, 
                         at_origin, add_ver_col,
                         mesh_reader, funct, rbx_meshes_to_clean_up_lst,
                         func_rbx_cloud_api, func_rbx_other, func_blndr_api):

    # Unpack Preferences
    # at_origin and add_ver_col are now passed directly
    
    if not TYPE_CHECKING:
        from RobloxFiles import WrapTarget # type: ignore

    cage_part = mesh_part.FindFirstChild[WrapTarget](mesh_name)
    if not cage_part:
        cage_part = mesh_part.FindFirstChild[WrapTarget](mesh_name + "WrapTarget")
    
    if cage_part:
        dprint(f"    -> Found WrapTarget for {mesh_name}")
        # Calculate main collection name if not available or passed
        main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
        main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)
        
        func_blndr_api.blender_api_create_collection("Cages", main_collection_name)
        
        try:
            # Match backup style: direct property access and specific variable names
            cage_inner_MeshId = func_rbx_other.strip_rbxassetid(cage_part.Properties["CageMeshId"].Value)

            # NOTE: CageOrigin is a LOCAL offset relative to the MeshPart.
            # To get the Global/World CFrame for the Cage, we must multiply the MeshPart's CFrame by the CageOrigin.
            # Blender API expects a World CFrame.
            cage_cframe = mesh_part.CFrame * cage_part.Properties["CageOrigin"].Value
            
            cage_cframe_pivot = cage_part.Properties["ImportOrigin"].Value
            
            dprint("cage_inner_MeshId: ", cage_inner_MeshId) 
            
            if cage_cframe is None: 
                return 

            
            dprint("cage_inner_MeshId: ", cage_inner_MeshId) 
            
            if cage_cframe is None: 
                return None

            # Pivot Logic:
            # func_blndr_api no longer uses pivot to move to origin for individual parts.
            # We simply pass the raw values.
            
            # Ensure folder exists (redundant check but safe)
            if not os.path.exists(bundle_own_folder):
                os.makedirs(bundle_own_folder)
                
            cage_mesh_file_path = os.path.join(rbx_tmp_rbxm_filepath, cage_part.Name + ".mesh")
            
            asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(cage_inner_MeshId, headers)
            
            rbx_obj = None
            if not rbx_imp_error and asset_data:
                rbx_imp_error = func_rbx_other.save_to_file(cage_mesh_file_path, asset_data)
                
                if not rbx_imp_error:
                    rbx_meshes_to_clean_up_lst.append(cage_part.Name)

                    try:
                        with open(cage_mesh_file_path, "rb") as f:
                            data = f.read()
                        cage_data = mesh_reader.RBXMeshParser.parse(data)
                    except Exception as e:
                        error_msg = f"Error processing cage {cage_part.Name}: {e}"
                        dprint(error_msg)
                        glob_vars.rbx_imp_error = error_msg
                        bpy.context.workspace.status_text_set(error_msg)
                        return None

                    if cage_data:
                        cage_mesh_name = cage_part.Name + "_inner_cage"
                        rbx_obj = func_blndr_api.blender_api_add_meshes_as_obj(
                            bundle_own_folder, cage_part, cage_data, cage_cframe, cage_cframe_pivot, 
                            at_origin, mesh_reader, funct, mesh_name=cage_mesh_name
                        )

                        if add_ver_col:
                            func_blndr_api.blender_api_add_ver_col(rbx_obj, cage_data)
            
            return rbx_obj

        except Exception as e:
            error_msg = f"Error processing cage for {mesh_name}: {e}"
            dprint(error_msg)
            glob_vars.rbx_imp_error = error_msg
            bpy.context.workspace.status_text_set(error_msg)
            import traceback
            traceback.print_exc()
            return None
    else:
        dprint(f"    -> No WrapTarget found for {mesh_name} (Expected: {mesh_name}WrapTarget)")
        return None
