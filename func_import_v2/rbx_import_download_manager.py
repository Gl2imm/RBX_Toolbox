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
    elif category_name == "Face Parts":
        selected_item_id = rbx_prefs.rbx_enum_face_parts
    elif category_name == "Classics":
        selected_item_id = rbx_prefs.rbx_enum_classics
    elif category_name == "Armature":
        selected_item_id = rbx_prefs.rbx_arma_enum
    else:
        selected_item_id = rbx_prefs.rbx_enum_body_parts
    
    # Get Items
    items_to_process = []
    all_imported_meshes = []
    all_items = glob_vars.discovered_items_data.get(category_name, [])

    if download_all or selected_item_id == 'ALL':
        items_to_process = all_items
    else:
        for item in all_items:
            if str(item['id']) == selected_item_id:
                items_to_process.append(item)
                break
    
    if not items_to_process and category_name != "Armature":
        dprint(f"No items to process for {category_name}.")
        return

    # Setup Folders
    target_subfolder = glob_vars.rbx_import_v2_bundles # Default to "Bundles"
    
    if category_name == "Accessory":
        target_subfolder = "Accessories"
    elif category_name == "Gear":
        target_subfolder = "Gears"
    elif category_name == "Layered Cloth":
        target_subfolder = "Layered Clothing"
    elif category_name == "Dynamic Head":
        target_subfolder = "Dynamic Heads"
    elif category_name == "Face Parts":
        target_subfolder = "Face Parts"
    elif category_name == "Classics":
        target_subfolder = "Classics"
        
    bundles_folder = os.path.join(addon_path, glob_vars.rbx_import_main_folder, target_subfolder)
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
    elif category_name == "Face Parts":
        prefs = {
            'at_origin': rbx_prefs.rbx_fp_choice_at_origin,
            'add_meshes': rbx_prefs.rbx_fp_choice_add_meshes,
            'add_textures': rbx_prefs.rbx_fp_choice_add_textures,
            'add_cages': rbx_prefs.rbx_fp_choice_add_cages,
            'add_attachment': rbx_prefs.rbx_fp_choice_add_attachment,
            'add_motor6d_attachment': False, 
            'add_ver_col': rbx_prefs.rbx_fp_choice_add_ver_col,
            'clean_tmp_meshes': rbx_prefs.rbx_fp_choice_clean_tmp_meshes,

        }
    elif category_name == "Classics":
        prefs = {
            'at_origin': False,
            'add_meshes': False,
            'add_textures': False,
            'add_cages': False,
            'add_attachment': False,
            'add_motor6d_attachment': False, 
            'add_ver_col': False,
            'clean_tmp_meshes': False,
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
    elif category_name == "Armature":
        # Armature Import Logic:
        # Respect selected_item_id which now contains prefix "BODYPART_" or "DYNHEAD_"
        # followed by the ID. 
        # If Logic fails or is generic, fallback (though new props.py logic shouldn't fail).
        
        target_id_str = str(selected_item_id)
        dprint(f"Processing Armature Import for Target: {target_id_str}")
        
        # Determine strict category and ID
        strict_cat = None
        strict_id = None
        
        if target_id_str.startswith("BODYPART_"):
            strict_cat = "Body Parts"
            strict_id = int(target_id_str.split("_")[1])
        elif target_id_str.startswith("DYNHEAD_"):
            strict_cat = "Dynamic Head"
            strict_id = int(target_id_str.split("_")[1])
        else:
            # Fallback (old behavior or check all?)
            # If user somehow selected something else or error.
            # Let's assume aggregation if no prefix, but correct prop setup prevents this.
            dprint(f"Warning: Armature selection '{target_id_str}' has no known prefix. Checking all...")
            pass

        categories_to_scan = ["Body Parts", "Dynamic Head", "Layered Cloth"]
        if strict_cat:
            categories_to_scan = [strict_cat] # Optimize to scan only relevant
            
        primary_asset_name = "R15_Character" # Default
        found_target = False

        for cat in categories_to_scan:
            if cat in glob_vars.discovered_items_data:
                cat_items = glob_vars.discovered_items_data[cat]
                
                # Determine Suffix for Armature Name
                # Instead of being empty, pass the category so it reads "Armature_{Name}_dynamic_head"
                armature_suffix = ""
                if strict_cat and strict_cat != "Body Parts":
                    armature_suffix = strict_cat.lower().replace(" ", "_")
                
                for item in cat_items:
                    asset_id = item['id']
                    
                    # Filter: 
                    # If this is "Body Parts", we want ALL items in the list (since they belong to the bundle).
                    # The `strict_id` is the Bundle ID, which won't match the Part IDs.
                    # So we skip the check for Body Parts.
                    is_body_bundle = (cat == "Body Parts" and strict_cat == "Body Parts")
                    
                    if strict_id and not is_body_bundle and asset_id != strict_id:
                        continue
                        
                    asset_name = item['name']
                    # Set primary asset name if this is our target
                    primary_asset_name = getattr(glob_vars, 'rbx_asset_name', asset_name)
                    found_target = True
                    
                    dprint(f"Processing bones for: {asset_name} ({asset_id})...")
                    
                    # Ensure Asset Local (Download if needed)
                    # Use appropriate format if known, else default
                    asset_format = None
                    if cat == "Dynamic Head": asset_format = "avatar_meshpart_head"
                    elif cat == "Layered Cloth": asset_format = "avatar_meshpart_accessory"
                    
                    success = ensure_local_asset(asset_id, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other, RobloxAssetFormat=asset_format)
                    if not success: continue

                    # Process for Bones Only
                    bone_prefs = {
                        'add_meshes': False,
                        # Explicitly False to prevent forcing add_meshes=True
                        'add_textures': False, 
                        'at_origin': rbx_prefs.rbx_bndl_char_choice_at_origin, 
                        'clean_tmp_meshes': False
                    }
                    
                    mesh_results = rbx_import_meshes.process_mesh_asset(
                        asset_id, asset_name, headers, bone_prefs, 
                        bundles_folder, rbx_tmp_rbxm_filepath, 
                        mesh_reader, funct, func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                        parent_name=None,
                        skip_download=True, is_layered_clothing=(cat=="Layered Cloth"),
                        parse_bones=True
                    )
                    
                    if mesh_results:
                        all_imported_meshes.extend(mesh_results)
        
        if not found_target and strict_id:
            dprint(f"Error: Target Armature item {strict_id} not found in discovered data.")

        # After collecting all bones
        if all_imported_meshes:
            dprint(f"Importing Armature with data from {len(all_imported_meshes)} meshes...")
            from . import rbx_import_bones
            importlib.reload(rbx_import_bones)
            
            # Pass the captured primary_asset_name
            # Provide the newly separated Armature-specific 'At Origin' flag 
            rbx_import_bones.import_bones(
                all_imported_meshes, 
                mesh_reader, funct, 
                rbx_prefs.rbx_bndl_char_choice_armature_at_origin, 
                asset_name=primary_asset_name,
                suffix=armature_suffix
            ) 
        else:
             dprint("No mesh data found to generate armature.")
        
        return # Exit after processing Armature category specific logic

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
        elif category_name == "Layered Cloth":
            asset_format = "avatar_meshpart_accessory" # Layered Cloth are accessories
            
        success = ensure_local_asset(asset_id, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other, RobloxAssetFormat=asset_format)
        if not success:
            dprint(f"Skipping {asset_name} due to download failure.")
            continue

        if category_name == "Classics":
            dprint(f"Processing Classic Textures for {asset_name}...")
            rbx_import_textures.classic_shirt_import(
                asset_id, asset_name, bundles_folder, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other
            )
            rbx_import_textures.classic_pants_import(
                asset_id, asset_name, bundles_folder, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other
            )
            continue

        # 1. Process Meshes
        is_layered_clothing = (category_name == "Layered Cloth")
        is_face_parts = (category_name == "Face Parts")
        
        # Calculate strict target folder for this asset
        parent_name = glob_vars.rbx_asset_name
        target_folder_name = func_rbx_other.replace_restricted_char(parent_name) if parent_name else func_rbx_other.replace_restricted_char(asset_name)
        asset_own_folder = os.path.join(bundles_folder, target_folder_name)
        if not os.path.exists(asset_own_folder):
            os.makedirs(asset_own_folder)
        
        if prefs['add_meshes']:
            mesh_results = rbx_import_meshes.process_mesh_asset(
                asset_id, asset_name, headers, prefs, 
                asset_own_folder, rbx_tmp_rbxm_filepath, 
                mesh_reader, funct, func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                parent_name=parent_name,
                skip_download=True, is_layered_clothing=is_layered_clothing, is_face_parts=is_face_parts
            )
            if mesh_results:
                all_imported_meshes.extend(mesh_results)
            
        if prefs['add_cages']:
             # Clean name needed for arguments
             asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
             rbx_import_cages.download_and_apply_cages(
                asset_id, asset_name, asset_own_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                prefs['at_origin'], prefs['add_ver_col'],
                mesh_reader, funct, [],
                func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                skip_download=True, is_layered_clothing=is_layered_clothing, is_face_parts=is_face_parts
            )
        
        if prefs['add_attachment'] or prefs['add_motor6d_attachment']:
             # Clean name needed for arguments
             asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
             rbx_import_attachments.download_and_apply_attachments(
                asset_id, asset_name, asset_own_folder, headers, 
                asset_clean_name, rbx_tmp_rbxm_filepath, 
                prefs['at_origin'], prefs['add_attachment'], prefs.get('add_motor6d_attachment', False),
                mesh_reader, funct,
                func_rbx_cloud_api, func_rbx_other, func_blndr_api,
                skip_download=True, is_layered_clothing=is_layered_clothing, is_face_parts=is_face_parts
            )

    # 4. Process Bones (Armature) - REMOVED
    # if prefs.get('add_bones') and all_imported_meshes:
    #    dprint(f"Processing Bones for {len(all_imported_meshes)} meshes...")
    #    from . import rbx_import_bones
    #    importlib.reload(rbx_import_bones)
    #    rbx_import_bones.import_bones(all_imported_meshes, mesh_reader, funct, prefs.get('at_origin'))

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



