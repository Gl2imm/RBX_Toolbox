import bpy
import os
import importlib
import asyncio
from RBX_Toolbox import glob_vars
from glob_vars import addon_path
from typing import TYPE_CHECKING

# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def ensure_local_asset(asset_id, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other, RobloxAssetFormat=None):
    """
    Downloads the asset if not present, checking for Dynamic Head status and upgrading if necessary.
    Returns:
        bool: True if file exists (or was downloaded/upgraded successfully), False otherwise.
    """
    rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
    
    # Always download to ensure freshness (matching previous behavior)
    # But now we do it ONCE here.
    asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(asset_id, headers, RobloxAssetFormat=RobloxAssetFormat)
    
    if rbx_imp_error or not asset_data:
        dprint(f"Error downloading asset {asset_id}: {rbx_imp_error}")
        glob_vars.rbx_imp_error = f"Error downloading {asset_id}: {rbx_imp_error}"
        return False

    if len(asset_data) == 0:
        dprint(f"Error: Downloaded asset {asset_id} is empty.")
        glob_vars.rbx_imp_error = f"Error: Downloaded asset {asset_id} is empty."
        return False

    dprint(f"Downloaded {len(asset_data)} bytes for {asset_id}. Saving to {rbx_tmp_rbxm_file}")

    try:
        with open(rbx_tmp_rbxm_file, "wb") as f:
            f.write(asset_data)
            f.flush()
            os.fsync(f.fileno()) # Force write to disk
    except Exception as e:
        dprint(f"Error saving RBXM {asset_id}: {e}")
        glob_vars.rbx_imp_error = f"Error saving RBXM {asset_id}: {e}"
        return False
        
    return True


def download_body_parts(context, category_name="Body Parts", download_all=False):
    # Initialize Context
    import clr
    from System.Reflection import Assembly # type: ignore
    try:
        clr.AddReference(robloxfile_dll) # type: ignore
    except:
        pass
    
    # Reload Dependencies
    from . import mesh_reader, conversion_funct as funct, func_rbx_other, func_rbx_api, func_blndr_api, func_rbx_cloud_api
    from . import rbx_import_meshes, rbx_import_cages, rbx_import_attachments, rbx_import_textures
    
    importlib.reload(mesh_reader)
    importlib.reload(funct)
    importlib.reload(func_rbx_other)
    importlib.reload(func_rbx_api)
    importlib.reload(func_blndr_api)
    importlib.reload(func_rbx_cloud_api)
    importlib.reload(rbx_import_meshes)
    # importlib.reload(rbx_import_meshes) # Removing duplicate
    importlib.reload(rbx_import_cages)
    importlib.reload(rbx_import_attachments)
    importlib.reload(rbx_import_textures)
    
    # Preferences
    rbx_prefs = context.scene.rbx_prefs
    
    selected_item_id = None
    if category_name == "Dynamic Head":
        selected_item_id = rbx_prefs.rbx_enum_dynamic_head
    elif category_name == "Accessory":
        selected_item_id = rbx_prefs.rbx_enum_accessory
    elif category_name == "Layered Cloth":
        selected_item_id = rbx_prefs.rbx_enum_layered_cloth
    elif category_name == "Gear":
        selected_item_id = rbx_prefs.rbx_enum_gear
    else:
        selected_item_id = rbx_prefs.rbx_enum_body_parts
    
    # Get Items
    items_to_process = []
    all_items = glob_vars.discovered_items_data.get(category_name, [])

    if download_all or selected_item_id == 'ALL':
        items_to_process = all_items
    else:
        for item in all_items:
            if str(item['id']) == selected_item_id:
                items_to_process.append(item)
                break
    
    if not items_to_process:
        dprint(f"No items to process for {category_name}.")
        return

    # Setup Folders
    bundles_folder = os.path.join(addon_path, glob_vars.rbx_import_main_folder, glob_vars.rbx_import_v2_bundles)
    rbx_tmp_rbxm_filepath = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp_rbxm')
    
    if not os.path.exists(bundles_folder):
        os.makedirs(bundles_folder)
    if not os.path.exists(rbx_tmp_rbxm_filepath):
        os.makedirs(rbx_tmp_rbxm_filepath)

    # Auth Token
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Gather Preferences
    if category_name == "Dynamic Head":
        prefs = {
            'at_origin': rbx_prefs.rbx_dyn_heads_choice_at_origin,
            'add_meshes': rbx_prefs.rbx_dyn_heads_choice_add_meshes,
            'add_textures': rbx_prefs.rbx_dyn_heads_choice_add_textures,
            'add_cages': rbx_prefs.rbx_dyn_heads_choice_add_cages,
            'add_attachment': rbx_prefs.rbx_dyn_heads_choice_add_attachment,
            'add_motor6d_attachment': rbx_prefs.rbx_dyn_heads_choice_add_motor6d_attachment,
            'add_ver_col': rbx_prefs.rbx_dyn_heads_choice_add_ver_col,
            'clean_tmp_meshes': rbx_prefs.rbx_dyn_heads_choice_clean_tmp_meshes
        }
    elif category_name == "Accessory":
        prefs = {
            'at_origin': rbx_prefs.rbx_accessory_choice_at_origin,
            'add_meshes': rbx_prefs.rbx_accessory_choice_add_meshes,
            'add_textures': rbx_prefs.rbx_accessory_choice_add_textures,
            'add_cages': False, # Explicitly False per user request
            'add_attachment': rbx_prefs.rbx_accessory_choice_add_attachment,
            'add_motor6d_attachment': False, # Explicitly False per user request
            'add_ver_col': rbx_prefs.rbx_accessory_choice_add_ver_col,
            'clean_tmp_meshes': rbx_prefs.rbx_accessory_choice_clean_tmp_meshes,

        }
    elif category_name == "Layered Cloth":
        prefs = {
            'at_origin': rbx_prefs.rbx_lc_choice_at_origin,
            'add_meshes': rbx_prefs.rbx_lc_choice_add_meshes,
            'add_textures': rbx_prefs.rbx_lc_choice_add_textures,
            'add_cages': rbx_prefs.rbx_lc_choice_add_cages,
            'add_attachment': rbx_prefs.rbx_lc_choice_add_attachment,
            'add_motor6d_attachment': False, 
            'add_ver_col': rbx_prefs.rbx_lc_choice_add_ver_col,
            'clean_tmp_meshes': rbx_prefs.rbx_lc_choice_clean_tmp_meshes,

        }
    elif category_name == "Gear":
        prefs = {
            'at_origin': rbx_prefs.rbx_gears_choice_at_origin,
            'add_meshes': rbx_prefs.rbx_gears_choice_add_meshes,
            'add_textures': rbx_prefs.rbx_gears_choice_add_textures,
            'add_cages': False,
            'add_attachment': False,
            'add_motor6d_attachment': False, 
            'add_ver_col': False,
            'clean_tmp_meshes': rbx_prefs.rbx_gears_choice_clean_tmp_meshes,

        }
    else: # Default to Body Parts / Bundles
        prefs = {
            'at_origin': rbx_prefs.rbx_bndl_char_choice_at_origin,
            'add_meshes': rbx_prefs.rbx_bndl_char_choice_add_meshes,
            'add_textures': rbx_prefs.rbx_bndl_char_choice_add_textures,
            'add_cages': rbx_prefs.rbx_bndl_char_choice_add_cages,
            'add_attachment': rbx_prefs.rbx_bndl_char_choice_add_attachment,
            'add_motor6d_attachment': rbx_prefs.rbx_bndl_char_choice_add_motor6d_attachment,
            'add_ver_col': rbx_prefs.rbx_bndl_char_choice_add_ver_col,
            'clean_tmp_meshes': rbx_prefs.rbx_bndl_char_choice_clean_tmp_meshes
        }

    # Process Loop
    for item in items_to_process:
        asset_id = item['id']
        asset_name = item['name']
        dprint(f"Processing Item: {asset_name} ({asset_id})")
        
        # Centralized Download Step
        # Determine format based on category
        asset_format = None
        if category_name == "Dynamic Head":
            asset_format = "avatar_meshpart_head"
        elif category_name == "Accessory":
            asset_format = "avatar_meshpart_accessory"
        elif category_name == "Layered Cloth":
            asset_format = "avatar_meshpart_accessory" # Layered Cloth are accessories
            
        success = ensure_local_asset(asset_id, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other, RobloxAssetFormat=asset_format)
        if not success:
            dprint(f"Skipping {asset_name} due to download failure.")
            continue

        # 1. Process Meshes
        is_layered_clothing = (category_name == "Layered Cloth")
        
        if prefs['add_meshes']:
            parent_name = glob_vars.rbx_asset_name
            # if category_name == "Accessory":
            #     parent_name = "Accessories"
            rbx_import_meshes.process_mesh_asset(
                asset_id, asset_name, headers, prefs, 
                bundles_folder, rbx_tmp_rbxm_filepath, 
                mesh_reader, funct, func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                parent_name=parent_name,
                skip_download=True, is_layered_clothing=is_layered_clothing
            )
            
        if prefs['add_cages']:
             # Clean name needed for arguments
             asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
             rbx_import_cages.download_and_apply_cages(
                asset_id, asset_name, bundles_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                prefs['at_origin'], prefs['add_ver_col'],
                mesh_reader, funct, [],
                func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                skip_download=True, is_layered_clothing=is_layered_clothing
            )
        
        if prefs['add_attachment'] or prefs['add_motor6d_attachment']:
             # Clean name needed for arguments
             asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
             rbx_import_attachments.download_and_apply_attachments(
                asset_id, asset_name, bundles_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                prefs['at_origin'], prefs['add_attachment'], prefs.get('add_motor6d_attachment', False),
                mesh_reader, funct,
                func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                skip_download=True, is_layered_clothing=is_layered_clothing
            )

    # Cleanup RBXM file if requested
    if prefs.get('clean_tmp_meshes', False):
        rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
        if os.path.exists(rbx_tmp_rbxm_file):
            try:
                os.remove(rbx_tmp_rbxm_file)
                dprint(f"Cleaned up RBXM: {rbx_tmp_rbxm_file}")
            except Exception as e:
                dprint(f"Error cleaning up RBXM {asset_id}: {e}")

    dprint(f"Download Finished for {category_name}.")



