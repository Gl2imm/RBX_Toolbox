import bpy
import os
import importlib
from RBX_Toolbox import glob_vars
from typing import TYPE_CHECKING, List, Any, Dict, Union

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def download_and_apply_attachments(target: Union[int, Any], mesh_name: str, bundle_own_folder: str, headers: dict, 
                             asset_clean_name: str, rbx_tmp_rbxm_filepath: str, 
                             at_origin: bool, add_attachment: bool, add_motor6d_attachment: bool,
                             mesh_reader: Any, funct: Any,
                             func_rbx_cloud_api: Any = None, func_rbx_other: Any = None, func_blndr_api: Any = None,
                             skip_download: bool = False, is_layered_clothing: bool = False, is_face_parts: bool = False):
    """
    Downloads the RBXM asset and iterates through its Body Parts to apply attachments.
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
        dprint(f"Processing Attachments for Asset ID: {asset_id}")

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
        is_accessory = False # Default to False, updated if Accessory found

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

            children = rbxm_file.roots
            child_names = [c.name for c in children]
            child_types = [c.class_name for c in children]
            dprint(f"RBXM Children: {child_names} Types: {child_types}")
            
            head_part = rbxm_file.FindFirstChild("Head")
            if head_part and head_part.class_name == "MeshPart":
                dprint("Found Head MeshPart. Processing as Dynamic Head.")
                # For dynamic head, the bundle folder is the target
                target_bundle_folder = bundle_own_folder 
                parts_to_process.append((head_part, "Head"))
            else:

                 # Fallback: check all children for MeshParts (e.g. Accessories with "Handle")
                 dprint("No Head MeshPart found. Checking all children for MeshParts...")
                 target_bundle_folder = bundle_own_folder
                 
                 found_any = False
                 # User requested loop with break
                 is_accessory = False
                 for child in children:
                     # 1. Check if child is an Accessory (container)
                     if child.class_name == "Accessory":
                         is_accessory = True
                         for acc_child in child.GetChildren():
                             if acc_child.class_name == "MeshPart":
                                 dprint(f"Found Accessory MeshPart: {acc_child.name}")
                                 parts_to_process.append((acc_child, acc_child.name))
                                 found_any = True
                                 break # Stop searching inside this Accessory
                             elif acc_child.class_name == "Part":
                                 dprint(f"Found Accessory Part: {acc_child.name}")
                                 parts_to_process.append((acc_child, acc_child.name))
                                 found_any = True
                                 break # Stop searching inside this Accessory
                         
                         if found_any:
                             break # Stop searching other children if found an Accessory Handle
                             
                         # If found accessory but not handle, reset is_accessory? 
                         if not found_any: is_accessory = False
                     
                     # 2. Check if child is directly a MeshPart
                     elif child.class_name == "MeshPart":
                         dprint(f"Found generic MeshPart: {child.name}")
                         parts_to_process.append((child, child.name))
                         found_any = True
                         break # Stop searching

                 if not parts_to_process:
                     dprint(f"No MeshParts found in {asset_clean_name if asset_clean_name else str(asset_id)}")
                     return

        if is_layered_clothing or is_face_parts:
             # Calculate unique attachment collection name: "LC Attachments XX" or "FP Attachments XX"
             lc_att_cols_parent_name = asset_clean_name
             
             prefix = "FP" if is_face_parts else "LC"
             target_att_name = f"{prefix} Attachments 00" # Default
             
             import re
             max_suffix = -1
             pattern = re.compile(rf"{prefix} Attachments (\d+)")
             
             for col in bpy.data.collections:
                 match = pattern.match(col.name)
                 if match:
                     val = int(match.group(1))
                     if val > max_suffix:
                         max_suffix = val
             
             # Increment
             target_att_name = f"{prefix} Attachments {max_suffix + 1:02d}"
        else:
             target_att_name = None

        for mesh_part, part_name in parts_to_process:
            dprint(f"  -> Found Body Part: {part_name}, checking for attachments...")
            # Process single attachment
            _process_single_attachment(
                mesh_part, part_name, target_bundle_folder, headers, 
                asset_clean_name, at_origin, add_attachment, add_motor6d_attachment, funct, func_blndr_api, func_rbx_other,
                is_accessory=is_accessory, is_layered_clothing=is_layered_clothing, is_face_parts=is_face_parts,
                lc_target_att_name=target_att_name
            )
        
        return
    
    # === CASE 2: Target is MeshPart (Called from Bundle Importer) ===
    else:
        # Assuming target is an rbxm_reader Instance object
        if hasattr(target, "FindFirstChild"):
             _process_single_attachment(
                target, mesh_name, bundle_own_folder, headers, 
                asset_clean_name, at_origin, add_attachment, add_motor6d_attachment, funct, func_blndr_api, func_rbx_other,
                is_accessory=False, is_layered_clothing=is_layered_clothing, is_face_parts=is_face_parts,
                lc_target_att_name=None
            )
        else:
             dprint(f"Invalid target type for attachments: {type(target)}")
             return


def _process_single_attachment(mesh_part, mesh_name, bundle_own_folder, headers, 
                          asset_clean_name, at_origin, add_attachment, add_motor6d_attachment, funct, 
                          func_blndr_api, func_rbx_other, is_accessory=False, is_layered_clothing=False, is_face_parts=False,
                          lc_target_att_name=None):

    # Reuse logic from meshes script but standalone
    # We need the CFrame and Pivot of the parent part to act as reference
    
    cframe = mesh_part.get("CFrame")
    
    # Try to get PivotOffset from MeshPart
    part_cframe_pivot = mesh_part.get("PivotOffset")
    if part_cframe_pivot is None:
        part_cframe_pivot = funct.cframe_identity()

    # Check if pivot is identity
    pivot_comps = funct.cframe_get_components(part_cframe_pivot)
    identity_comps = (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
    is_identity = True
    if len(pivot_comps) == 12:
        for a, b in zip(pivot_comps, identity_comps):
            if abs(a - b) > 0.0001: 
                is_identity = False
                break
    
    # If pivot is identity, force at_origin to False
    # UNLESS it is an Accessory, which we want to center even if identity
    actual_at_origin = at_origin
    if is_identity and not is_accessory:
        actual_at_origin = False

        
    # Calculate main collection name if not available or passed
    main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
    main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)

    # Logic from backup: Split into "Accessory Attachments" and "Motor6D Attachments"
    
    # 1. Accessory Attachments
    if add_attachment:
        att_col_name = f"{asset_clean_name}_Attachments" if is_accessory else "Body Attachments"
        
        if is_layered_clothing or is_face_parts:
            if is_face_parts:
                folder_name = "Face Parts"
            else:
                folder_name = "Layered Clothing"
            
            # Determine parent like in meshes script
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

            prefix = "FP" if is_face_parts else "LC"
            target_name = lc_target_att_name if lc_target_att_name else f"{prefix} Attachments"
            attachments_collection = func_blndr_api.blender_api_create_collection(target_name, asset_col.name)
            
        else:
            parent_col_name = asset_clean_name if is_accessory else main_collection_name
            attachments_collection = func_blndr_api.blender_api_create_collection(att_col_name, parent_col_name)
        existing_attachment_names = set(obj.name for obj in attachments_collection.objects)

        for child in mesh_part.GetChildren():
            if child.class_name == "Attachment":
                if "RigAttachment" not in str(child.name):
                    # Clean name check
                    att_name = child.name
                    if att_name in existing_attachment_names:
                        dprint(f"    -> Skipping Duplicate Attachment: {att_name}")
                        continue

                    dprint(f"    -> Found Attachment: {child.name} in {mesh_name}")
                    att_cframe = child.get("CFrame")
                    func_blndr_api.blender_api_add_attachments(
                        child, att_cframe, cframe, part_cframe_pivot, 
                        actual_at_origin, funct, is_accessory=is_accessory
                    )

    # 2. Motor6D Attachments
    if add_motor6d_attachment:
        motor6d_collection = func_blndr_api.blender_api_create_collection("Motor6D Attachments", main_collection_name)
        existing_motor6d_names = set(obj.name for obj in motor6d_collection.objects)

        for child in mesh_part.GetChildren():
            if child.class_name == "Attachment":
                if "RigAttachment" in str(child.name):
                    # Clean name check
                    att_name = child.name
                    if att_name in existing_motor6d_names:
                        dprint(f"    -> Skipping Duplicate Motor6D Attachment: {att_name}")
                        continue

                    dprint(f"    -> Found Motor6D Attachment: {child.name} in {mesh_name}")
                    att_cframe = child.get("CFrame")
                    func_blndr_api.blender_api_add_attachments(
                        child, att_cframe, cframe, part_cframe_pivot, 
                        actual_at_origin, funct, is_accessory=is_accessory
                    )
