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

def download_body_parts(context, category_name="Body Parts"):
    # Initialize Context
    import clr
    from System.Reflection import Assembly # type: ignore
    try:
        clr.AddReference(robloxfile_dll) # type: ignore
    except:
        pass
    
    # Reload Dependencies
    from . import mesh_reader, conversion_funct as funct, func_rbx_other, func_rbx_api, func_blndr_api, func_rbx_cloud_api
    from . import rbx_import_meshes, rbx_import_cages, rbx_import_attachments
    
    importlib.reload(mesh_reader)
    importlib.reload(funct)
    importlib.reload(func_rbx_other)
    importlib.reload(func_rbx_api)
    importlib.reload(func_blndr_api)
    importlib.reload(func_rbx_cloud_api)
    importlib.reload(rbx_import_meshes)
    importlib.reload(rbx_import_meshes)
    importlib.reload(rbx_import_cages)
    importlib.reload(rbx_import_attachments)
    
    # Preferences
    rbx_prefs = context.scene.rbx_prefs
    selected_item_id = rbx_prefs.rbx_enum_body_parts
    
    # Get Items
    items_to_process = []
    all_items = glob_vars.discovered_items_data.get(category_name, [])

    if selected_item_id == 'ALL':
        items_to_process = all_items
    else:
        for item in all_items:
            if str(item['id']) == selected_item_id:
                items_to_process.append(item)
                break
    
    if not items_to_process:
        dprint("No items to process for Body Parts.")
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
        dprint(f"Processing Body Part: {asset_name} ({asset_id})")
        
        # 1. Process Meshes
        if prefs['add_meshes']:
            rbx_import_meshes.process_mesh_asset(
                asset_id, asset_name, headers, prefs, 
                bundles_folder, rbx_tmp_rbxm_filepath, 
                mesh_reader, funct, func_rbx_cloud_api, func_rbx_other, func_blndr_api
            )
                
            
        if prefs['add_cages']:
             # Clean name needed for arguments
             asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
             rbx_import_cages.download_and_apply_cages(
                asset_id, asset_name, bundles_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                prefs['at_origin'], prefs['add_ver_col'],
                mesh_reader, funct, [],
                func_rbx_cloud_api, func_rbx_other, func_blndr_api
            )
        
        if prefs['add_attachment'] or prefs['add_motor6d_attachment']:
             # Clean name needed for arguments
             asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
             rbx_import_attachments.download_and_apply_attachments(
                asset_id, asset_name, bundles_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                prefs['at_origin'], prefs['add_attachment'], prefs['add_motor6d_attachment'],
                mesh_reader, funct,
                func_rbx_cloud_api, func_rbx_other, func_blndr_api
            )
            

    dprint("Body Parts Download Finished.")
