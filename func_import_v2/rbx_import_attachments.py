import bpy
import os
import importlib
from RBX_Toolbox import glob_vars
from typing import TYPE_CHECKING, List, Any, Dict, Union

# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def download_and_apply_attachments(target: Union[int, Any], mesh_name: str, bundle_own_folder: str, headers: dict, 
                             asset_clean_name: str, rbx_tmp_rbxm_filepath: str, 
                             at_origin: bool, add_attachment: bool, add_motor6d_attachment: bool,
                             mesh_reader: Any, funct: Any,
                             func_rbx_cloud_api: Any = None, func_rbx_other: Any = None, func_blndr_api: Any = None):
    """
    Downloads the RBXM asset and iterates through its Body Parts to apply attachments.
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
        from RobloxFiles import RobloxFile, Folder, MeshPart, Attachment # type: ignore

    # === CASE 1: Target is Asset ID (Polymorphic Entry) ===
    if isinstance(target, int) or (isinstance(target, str) and str(target).isdigit()):
        asset_id = int(target)
        dprint(f"Processing Attachments for Asset ID: {asset_id}")

        rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
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
        if not R15Fixed:
            dprint(f"No R15Fixed folder found in {asset_clean_name if asset_clean_name else str(asset_id)}")
            return
            
        dprint(f"Found R15Fixed folder. Checking children...")

        # Create folder structure for the bundle
        main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
        main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)
        
        target_bundle_folder = os.path.join(bundle_own_folder, main_collection_name) if 'Imported Body Parts' in bundle_own_folder else bundle_own_folder
        
        if not os.path.exists(target_bundle_folder):
                if not os.path.exists(bundle_own_folder): # Safe check
                    os.makedirs(bundle_own_folder)

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
                dprint(f"  -> Found Body Part: {part_name}, checking for attachments...")
                # Process single attachment
                _process_single_attachment(
                    mesh_part, part_name, target_bundle_folder, headers, 
                    asset_clean_name, at_origin, add_attachment, add_motor6d_attachment, funct, func_blndr_api, func_rbx_other
                )
        
        return
    
    # === CASE 2: Target is MeshPart (Called from Bundle Importer) ===
    else:
        # Assuming target is a MeshPart object (or duck-typed enough)
        if hasattr(target, "FindFirstChild"):
             _process_single_attachment(
                target, mesh_name, bundle_own_folder, headers, 
                asset_clean_name, at_origin, add_attachment, add_motor6d_attachment, funct, func_blndr_api, func_rbx_other
            )
        else:
             dprint(f"Invalid target type for attachments: {type(target)}")
             return


def _process_single_attachment(mesh_part, mesh_name, bundle_own_folder, headers, 
                         asset_clean_name, at_origin, add_attachment, add_motor6d_attachment, funct, func_blndr_api, func_rbx_other):

    # Unpack Preferences
    # at_origin is passed directly
    
    if not TYPE_CHECKING:
        from RobloxFiles import Attachment, MeshPart # type: ignore

    # Reuse logic from meshes script but standalone
    # We need the CFrame and Pivot of the parent part to act as reference
    
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

        
    # Calculate main collection name if not available or passed
    main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
    main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)

    # Logic from backup: Split into "Accessory Attachments" and "Motor6D Attachments"
    
    # 1. Accessory Attachments
    if add_attachment:
        attachments_collection = func_blndr_api.blender_api_create_collection("Accessory Attachments", main_collection_name)
        existing_attachment_names = set(obj.name for obj in attachments_collection.objects)

        for child in mesh_part.GetChildren():
            if child.ClassName == "Attachment":
                if "RigAttachment" not in str(child.Name):
                    # Clean name check
                    att_name = child.Name
                    if att_name in existing_attachment_names:
                        dprint(f"    -> Skipping Duplicate Attachment: {att_name}")
                        continue

                    dprint(f"    -> Found Attachment: {child.Name} in {mesh_name}")
                    func_blndr_api.blender_api_add_attachments(
                        child, child.CFrame, cframe, part_cframe_pivot, 
                        actual_at_origin, funct
                    )

    # 2. Motor6D Attachments
    if add_motor6d_attachment:
        motor6d_collection = func_blndr_api.blender_api_create_collection("Motor6D Attachments", main_collection_name)
        existing_motor6d_names = set(obj.name for obj in motor6d_collection.objects)

        for child in mesh_part.GetChildren():
            if child.ClassName == "Attachment":
                if "RigAttachment" in str(child.Name):
                    # Clean name check
                    att_name = child.Name
                    if att_name in existing_motor6d_names:
                        dprint(f"    -> Skipping Duplicate Motor6D Attachment: {att_name}")
                        continue

                    dprint(f"    -> Found Motor6D Attachment: {child.Name} in {mesh_name}")
                    func_blndr_api.blender_api_add_attachments(
                        child, child.CFrame, cframe, part_cframe_pivot, 
                        actual_at_origin, funct
                    )