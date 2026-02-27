import bpy
import os
import importlib
import re
from RBX_Toolbox import glob_vars
from typing import TYPE_CHECKING, List, Any, Dict, Union

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def download_and_apply_cages(target: Union[int, Any], mesh_name: str, bundle_own_folder: str, headers: dict, 
                             asset_clean_name: str, rbx_tmp_rbxm_filepath: str, 
                             at_origin: bool, add_ver_col: bool,
                             mesh_reader: Any, funct: Any, rbx_meshes_to_clean_up_lst: List[str],
                             func_rbx_cloud_api: Any = None, func_rbx_other: Any = None, func_blndr_api: Any = None,
                             skip_download: bool = False, is_layered_clothing: bool = False, is_face_parts: bool = False):
    """
    Downloads the RBXM asset and iterates through its Body Parts to apply cages.
    """
    
    # Reload Dependencies & Setup Context
    from . import func_rbx_cloud_api as api_cloud, func_rbx_other as api_other, func_blndr_api as api_blend
    from . import rbxm_reader
    
    if func_rbx_cloud_api is None: func_rbx_cloud_api = api_cloud
    if func_rbx_other is None: func_rbx_other = api_other
    if func_blndr_api is None: func_blndr_api = api_blend

    importlib.reload(func_rbx_cloud_api)
    importlib.reload(func_rbx_other)
    importlib.reload(func_blndr_api)

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
            rbxm_file = rbxm_reader.parse(rbx_tmp_rbxm_file)
        except Exception as e:
            dprint(f"Error opening RBXM {asset_id}: {e}")
            return

        R15Fixed = rbxm_file.FindFirstChild("R15Fixed")
        
        parts_to_process = []

        if R15Fixed:
            dprint(f"Found R15Fixed folder. Checking children...")
            # Create folder structure for the bundle
            main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
            main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)
            
            target_bundle_folder = bundle_own_folder
            
            if not os.path.exists(target_bundle_folder):
                os.makedirs(target_bundle_folder)
            
            # Loop children
            rbx_avatar_bundle_parts = [
                    "LeftUpperArm", "LeftLowerArm", "LeftHand",
                    "RightUpperArm", "RightLowerArm", "RightHand",
                    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
                    "RightUpperLeg", "RightLowerLeg", "RightFoot",
                    "UpperTorso", "LowerTorso", "Head"
                ]

            for part_name in rbx_avatar_bundle_parts:
                mesh_part = R15Fixed.FindFirstChild(part_name)
                if mesh_part:
                    parts_to_process.append((mesh_part, part_name))
        else:
            dprint(f"No R15Fixed folder found. Checking for Dynamic Head MeshPart...")
            # Search for MeshPart named "Head"
            head_part = rbxm_file.FindFirstChild("Head")
            if head_part and head_part.class_name == "MeshPart":
                dprint("Found Head MeshPart. Processing as Dynamic Head.")
                target_bundle_folder = bundle_own_folder
                parts_to_process.append((head_part, "Head"))
            else:
                dprint(f"No Head MeshPart found in {asset_clean_name if asset_clean_name else str(asset_id)}")
                # Debug: List children
                children = [c.name for c in rbxm_file.GetDescendants() if c.parent is None or c.parent not in rbxm_file.roots]
                children_root = [c.name for c in rbxm_file.roots] if hasattr(rbxm_file, 'roots') else []
                dprint(f"Root children found: {children_root}")
                
                 # Fallback: check all children for MeshParts (e.g. Accessories with "Handle")
                dprint("No Head MeshPart found. Checking all children for MeshParts...")
                target_bundle_folder = bundle_own_folder
                 
                found_any = False
                for child in rbxm_file.roots:
                     # 1. Check if child is an Accessory (container)
                     if child.class_name == "Accessory":
                         for acc_child in child.GetChildren():
                             if acc_child.class_name == "MeshPart":
                                 dprint(f"Found Accessory MeshPart: {acc_child.name}")
                                 parts_to_process.append((acc_child, acc_child.name))
                                 found_any = True
                                 break 
                         
                         if found_any:
                             break 
                     
                     # 2. Check if child is directly a MeshPart
                     elif child.class_name == "MeshPart":
                         dprint(f"Found generic MeshPart: {child.name}")
                         parts_to_process.append((child, child.name))
                         found_any = True
                         break 
                
                if not parts_to_process:
                    return

        # Calculate unique Cages collection name if LC or FP
        lc_target_cage_name = None
        if is_layered_clothing or is_face_parts:
             import re
             max_suffix = -1
             pattern = re.compile(r"Cages (\d+)")
             
             for col in bpy.data.collections:
                 match = pattern.match(col.name)
                 if match:
                     val = int(match.group(1))
                     if val > max_suffix:
                         max_suffix = val
             
             lc_target_cage_name = f"Cages {max_suffix + 1:02d}"

        for mesh_part, part_name in parts_to_process:
            dprint(f"  -> Found Body Part: {part_name}, checking for cages...")
            # Process single cage
            _process_single_cage(
                mesh_part, part_name, target_bundle_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                at_origin, add_ver_col,
                mesh_reader, funct, rbx_meshes_to_clean_up_lst,
                func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                is_layered_clothing=is_layered_clothing,
                is_face_parts=is_face_parts,
                lc_target_cage_name=lc_target_cage_name
            )
        
        # Cleanup
        pass
        
        return
    
    # === CASE 2: Target is MeshPart Instance (Called from Bundle Importer) ===
    else:
        # Assuming target is an rbxm_reader Instance object
        if hasattr(target, "FindFirstChild"):
             _process_single_cage(
                target, mesh_name, bundle_own_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                at_origin, add_ver_col,
                mesh_reader, funct, rbx_meshes_to_clean_up_lst,
                func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                is_layered_clothing=is_layered_clothing,
                is_face_parts=is_face_parts,
                lc_target_cage_name=None 
            )
        else:
             dprint(f"Invalid target type for cages: {type(target)}")
             return


def _process_single_cage(mesh_part, mesh_name, bundle_own_folder, headers, 
                         asset_clean_name, rbx_tmp_rbxm_filepath, 
                         at_origin, add_ver_col,
                         mesh_reader, funct, rbx_meshes_to_clean_up_lst,
                         func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                         is_layered_clothing: bool = False,
                         is_face_parts: bool = False,
                         lc_target_cage_name: str = None):
    

    # Unpack Preferences
    # at_origin and add_ver_col are now passed directly

    cage_part = None
    is_wrap_layer = False
    
    if is_layered_clothing or is_face_parts:
        # Layered Clothing and Face Parts use WrapLayer
        for child in mesh_part.GetChildren():
             if child.class_name == "WrapLayer":
                 cage_part = child
                 is_wrap_layer = True
                 dprint(f"    -> Found WrapLayer: {child.name}")
                 break
    
    if not cage_part:
        # Fallback to WrapTarget (Body Parts)
        cage_part = mesh_part.FindFirstChild(mesh_name + "WrapTarget")
        if not cage_part:
            cage_part = mesh_part.FindFirstChild(mesh_name)
            # Verify it's actually a WrapTarget
            if cage_part and cage_part.class_name != "WrapTarget":
                cage_part = None
    
    if cage_part:
        if not is_wrap_layer:
             dprint(f"    -> Found WrapTarget for {mesh_name}")
        
        # Calculate main collection name if not available or passed
        main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
        main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)
        
        if is_layered_clothing or is_face_parts:
            if is_face_parts:
                folder_name = "Face Parts"
            else:
                folder_name = "Layered Clothing"
            
            # Parent logic same as meshes
            lc_parent_col_name = main_collection_name
            if main_collection_name == asset_clean_name:
                 lc_parent_col_name = None 

            lc_col = func_blndr_api.blender_api_create_collection(folder_name, lc_parent_col_name)
            asset_col = func_blndr_api.blender_api_create_collection(asset_clean_name, lc_col.name)
            
            # Fix for double-linking: If in LC, ensure not in Accessories
            acc_col_obj = bpy.data.collections.get("Accessories")
            if acc_col_obj and asset_col.name in acc_col_obj.children:
                dprint(f"Unlinking {asset_col.name} from Accessories...")
                acc_col_obj.children.unlink(asset_col)

            target_cages_name = lc_target_cage_name if lc_target_cage_name else "Cages"
            func_blndr_api.blender_api_create_collection(target_cages_name, asset_col.name)
        else:
            func_blndr_api.blender_api_create_collection("Cages", main_collection_name)
        
        try:
            # Setup Lists of Cages to Process
            # (MeshId, NameSuffix)
            cages_to_import = []
            
            if is_wrap_layer:
                # WrapLayer has CageMeshId (Inner) and ReferenceMeshId (Outer)
                cage_mesh_raw = cage_part.get("CageMeshId")
                if cage_mesh_raw is not None:
                    cage_uri = func_rbx_other.resolve_content_uri(cage_mesh_raw)
                    if cage_uri:
                        cages_to_import.append((cage_uri, "_outer_cage"))
                
                ref_mesh_raw = cage_part.get("ReferenceMeshId")
                if ref_mesh_raw is not None:
                    ref_uri = func_rbx_other.resolve_content_uri(ref_mesh_raw)
                    if ref_uri:
                        cages_to_import.append((ref_uri, "_inner_cage"))
            else:
                # WrapTarget has CageMeshId (Inner)
                cage_mesh_raw = cage_part.get("CageMeshId")
                if cage_mesh_raw is not None:
                    cage_uri = func_rbx_other.resolve_content_uri(cage_mesh_raw)
                    if cage_uri:
                        cages_to_import.append((cage_uri, "_inner_cage"))

            # Loop through cages
            for cage_mesh_id_raw, name_suffix in cages_to_import:
                cage_mesh_id = func_rbx_other.strip_rbxassetid(cage_mesh_id_raw)
                
                if not cage_mesh_id:
                    continue

                # CageOrigin logic
                cage_cframe = mesh_part.get("CFrame")
                cage_origin = cage_part.get("CageOrigin")
                if cage_origin is not None:
                    # cage_cframe = mesh_part.CFrame * cage_part.CageOrigin
                    # For now, use CageOrigin as the cage CFrame offset
                    # This is a local offset relative to mesh_part CFrame
                    cage_cframe_matrix = funct.cframe_to_blender_matrix(cage_cframe)
                    cage_origin_matrix = funct.cframe_to_blender_matrix(cage_origin)
                    combined = cage_cframe_matrix @ cage_origin_matrix
                    # Convert back to CFrame dict for downstream
                    cage_cframe = {
                        "position": (combined[0][3], combined[1][3], combined[2][3]),
                        "rotation": ("matrix", (
                            combined[0][0], combined[0][1], combined[0][2],
                            combined[1][0], combined[1][1], combined[1][2],
                            combined[2][0], combined[2][1], combined[2][2],
                        ))
                    }
                
                cage_cframe_pivot = cage_part.get("ImportOrigin")
                
                dprint(f"Processing Cage: {name_suffix} ID: {cage_mesh_id}") 
                
                if cage_cframe is None: 
                    continue

                # Check if MESH pivot is identity (The Cage must follow the Mesh's placement)
                mesh_pivot = mesh_part.get("PivotOffset")
                if mesh_pivot is None:
                    mesh_pivot = funct.cframe_identity()

                mesh_pivot_comps = funct.cframe_get_components(mesh_pivot)
                identity_comps = (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
                mesh_is_identity = True
                if len(mesh_pivot_comps) == 12:
                    for a, b in zip(mesh_pivot_comps, identity_comps):
                        if abs(a - b) > 0.0001: 
                            mesh_is_identity = False
                            break

                is_accessory = False
                check_obj = mesh_part
                if mesh_part.class_name == "SpecialMesh":
                     check_obj = mesh_part.parent
                if check_obj and check_obj.parent and check_obj.parent.class_name == "Accessory":
                    is_accessory = True

                # If pivot is identity (for the Mesh), force at_origin to False (unless accessory)
                actual_at_origin = at_origin
                if mesh_is_identity and not is_accessory:
                    actual_at_origin = False
                    
                # The cage shares the exact same logical pivot as the mesh part it's wrapped around
                cage_cframe_pivot = mesh_pivot

                
                # Ensure folder exists
                if not os.path.exists(bundle_own_folder):
                    os.makedirs(bundle_own_folder)
                    
                cage_mesh_file_path = os.path.join(rbx_tmp_rbxm_filepath, cage_part.name + name_suffix + ".mesh")
                
                asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(cage_mesh_id, headers)
                
                if not rbx_imp_error and asset_data:
                    rbx_imp_error = func_rbx_other.save_to_file(cage_mesh_file_path, asset_data)
                    
                    if not rbx_imp_error:
                        rbx_meshes_to_clean_up_lst.append(cage_part.name)

                        with open(cage_mesh_file_path, "rb") as f:
                            data = f.read()
                        cage_data = mesh_reader.parse(data)

                        if cage_data:
                            # Naming convention: 
                            # If LC, use asset_clean_name (Item Name) + suffix
                            # If not LC (Body Parts), use mesh_name (e.g. LeftUpperArm) + suffix
                            if is_layered_clothing:
                                final_mesh_name = f"{asset_clean_name}{name_suffix}"
                            else:
                                final_mesh_name = f"{mesh_name}{name_suffix}"

                            rbx_obj = func_blndr_api.blender_api_add_meshes_as_obj(
                                bundle_own_folder, cage_part, cage_data, cage_cframe, cage_cframe_pivot, 
                                actual_at_origin, mesh_reader, funct, mesh_name=final_mesh_name
                            )

                            if add_ver_col:
                                func_blndr_api.blender_api_add_ver_col(rbx_obj, cage_data)
    
        except Exception as e:
            dprint(f"Error processing cage for {mesh_name}: {e}")
            import traceback
            traceback.print_exc()
    else:
        dprint(f"    -> No WrapTarget found for {mesh_name} (Expected: {mesh_name}WrapTarget)")
