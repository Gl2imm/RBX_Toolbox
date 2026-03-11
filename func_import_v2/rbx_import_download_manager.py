import bpy
import os
import importlib
import asyncio
from RBX_Toolbox import glob_vars
from glob_vars import addon_path
from typing import TYPE_CHECKING



### Debug prints
DEBUG = False
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
    # Initialize Context — .NET no longer needed, sub-modules use rbxm_reader
    
    # Reload Dependencies
    from .readers import mesh_reader
    from . import conversion_funct as funct, func_rbx_other, func_rbx_api, func_blndr_api, func_rbx_cloud_api
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
    # Nest temp files under the main discovered item name folder
    main_item_name = func_rbx_other.replace_restricted_char(
        getattr(glob_vars, 'rbx_asset_name', None) or "Unknown"
    )
    rbx_tmp_rbxm_filepath = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp_rbxm', main_item_name)
    
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
                suffix=armature_suffix,
                link_meshes=rbx_prefs.rbx_bndl_char_choice_armature_link_meshes
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

    # Move tracked objects to origin is now handled by execute_global_spawn_tracker() after all categories finish.

    # Cleanup main item tmp folder if requested
    if prefs.get('clean_tmp_meshes', False):
        import shutil
        if os.path.exists(rbx_tmp_rbxm_filepath):
            try:
                shutil.rmtree(rbx_tmp_rbxm_filepath)
                dprint(f"Cleaned up tmp folder: {rbx_tmp_rbxm_filepath}")
            except Exception as e:
                dprint(f"Error cleaning up tmp folder: {e}")

    dprint(f"Download Finished for {category_name}.")
    
    # Collapse Outliner
    try:
        func_blndr_api.blender_api_collapse_outliner()
    except Exception as e:
        dprint(f"Failed to collapse outliner: {e}")


def download_animation(context, apply_index=-1):
    """Download animation RBXM and parse KeyframeSequences or CurveAnimations.
    
    If apply_index < 0: downloads and discovers sub-animations, storing them in glob_vars.
    If apply_index >= 0: applies that sub-animation index to the selected armature.
    """
    from .readers import rbxm_reader, animation_reader, curve_animation_reader
    from . import func_rbx_cloud_api, func_rbx_other, func_blndr_api
    importlib.reload(func_rbx_cloud_api)
    importlib.reload(func_rbx_other)
    importlib.reload(func_blndr_api)
    importlib.reload(animation_reader)
    importlib.reload(curve_animation_reader)

    rbx_prefs = context.scene.rbx_prefs
    
    if apply_index >= 0:
        # Apply the sub-animation at the given index to the selected armature
        armature = rbx_prefs.rbx_anim_armature_target
        if armature is None or armature.type != 'ARMATURE':
            dprint("No armature selected.")
            glob_vars.rbx_imp_error = "No armature found. Select an armature first."
            return
        
        anim_subs = getattr(glob_vars, 'rbx_anim_sub_items', [])
        if apply_index >= len(anim_subs):
            dprint(f"Invalid sub-animation index: {apply_index}")
            glob_vars.rbx_imp_error = "Invalid animation index."
            return
        
        sub = anim_subs[apply_index]
        anim_data = sub['anim_data']
        action_name = sub['name']
        
        if sub.get('is_curve_anim', False):
            func_blndr_api.blender_api_apply_curve_animation(
                armature, anim_data, action_name=action_name
            )
        else:
            func_blndr_api.blender_api_apply_animation(
                armature, anim_data, action_name=action_name
            )
        dprint(f"Animation '{action_name}' applied to '{armature.name}'.")
        return
    
    # Phase 1: Download and discover sub-animations
    # Get auth headers
    loop = asyncio.get_event_loop()
    access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
    headers = {"Authorization": f"Bearer {access_token}"}
    
    selected_item_id = rbx_prefs.rbx_enum_animations
    if selected_item_id == 'NONE':
        dprint("No animation item selected.")
        return
    
    all_items = glob_vars.discovered_items_data.get("Animations", [])
    
    # Find selected items
    items_to_process = []
    if selected_item_id == 'ALL':
        items_to_process = all_items
    else:
        for item in all_items:
            if str(item['id']) == selected_item_id:
                items_to_process.append(item)
                break
    
    if not items_to_process:
        dprint("No animation items to process.")
        return
    
    # Setup tmp folder — nest under the main discovered item name
    main_item_name = func_rbx_other.replace_restricted_char(
        getattr(glob_vars, 'rbx_asset_name', None) or "Unknown"
    )
    rbx_tmp_rbxm_filepath = os.path.join(addon_path, glob_vars.rbx_import_main_folder, 'tmp_rbxm', main_item_name)
    if not os.path.exists(rbx_tmp_rbxm_filepath):
        os.makedirs(rbx_tmp_rbxm_filepath)
    
    # Clear previous sub-animations
    glob_vars.rbx_anim_sub_items = []
    
    for item in items_to_process:
        asset_id = item['id']
        asset_name = item['name']
        dprint(f"Downloading animation: {asset_name} (ID: {asset_id})")
        
        # Download
        if not ensure_local_asset(asset_id, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other):
            continue
        
        rbxm_file_path = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
        
        try:
            model = rbxm_reader.parse(rbxm_file_path)
        except Exception as e:
            dprint(f"Error parsing animation RBXM {asset_id}: {e}")
            continue
        
        # Find all KeyframeSequences in the file
        ks_list = []
        for inst in model.GetDescendants():
            if inst.class_name == "KeyframeSequence":
                ks_list.append(inst)
        
        # Find all CurveAnimations in the file
        ca_list = []
        for inst in model.GetDescendants():
            if inst.class_name == "CurveAnimation":
                ca_list.append(inst)
        
        # If no direct KeyframeSequence found, check for Animation instances
        # Animation instances have an AnimationId property pointing to the actual data
        if not ks_list and not ca_list:
            dprint(f"No direct KeyframeSequence/CurveAnimation in {asset_name}. Checking for Animation instances...")
            for inst in model.GetDescendants():
                if inst.class_name == "Animation":
                    anim_id_raw = inst.get("AnimationId")
                    anim_uri = func_rbx_other.resolve_content_uri(anim_id_raw)
                    if anim_uri:
                        anim_content_id = func_rbx_other.strip_rbxassetid(anim_uri)
                        dprint(f"  Found Animation '{inst.name}' → AnimationId: {anim_content_id}")
                        
                        # Download the actual animation data
                        anim_data_bytes, err = func_rbx_cloud_api.get_asset_data(anim_content_id, headers)
                        if not err and anim_data_bytes:
                            anim_tmp_path = os.path.join(rbx_tmp_rbxm_filepath, f"anim_{anim_content_id}.rbxm")
                            with open(anim_tmp_path, "wb") as f:
                                f.write(anim_data_bytes)
                            
                            try:
                                anim_model = rbxm_reader.parse(anim_tmp_path)
                                for sub_inst in anim_model.GetDescendants():
                                    if sub_inst.class_name == "KeyframeSequence":
                                        ks_list.append(sub_inst)
                                    elif sub_inst.class_name == "CurveAnimation":
                                        ca_list.append(sub_inst)
                            except Exception as e2:
                                dprint(f"  Error parsing animation content {anim_content_id}: {e2}")
                        else:
                            dprint(f"  Error downloading animation content {anim_content_id}: {err}")
        
        if not ks_list and not ca_list:
            dprint(f"No KeyframeSequence or CurveAnimation found in {asset_name} (even after AnimationId lookup)")
            continue
        
        # Parse KeyframeSequences
        if ks_list:
            dprint(f"Found {len(ks_list)} KeyframeSequence(s) in {asset_name}")
        
        for ks in ks_list:
            try:
                anim_data = animation_reader.read_animation(ks)
                sub_name = anim_data.get("name", ks.name or asset_name)
                # Prefix with asset name if multiple items
                if len(items_to_process) > 1:
                    sub_name = f"{asset_name} - {sub_name}"
                
                glob_vars.rbx_anim_sub_items.append({
                    'name': sub_name,
                    'anim_data': anim_data
                })
                dprint(f"  Parsed sub-animation: {sub_name} ({len(anim_data['keyframes'])} tracks, {anim_data['length']:.2f}s)")
            except Exception as e:
                dprint(f"  Error parsing KeyframeSequence '{ks.name}': {e}")
                continue
        
        # Parse CurveAnimations
        if ca_list:
            dprint(f"Found {len(ca_list)} CurveAnimation(s) in {asset_name}")
        
        for ca in ca_list:
            try:
                anim_data = curve_animation_reader.read_curve_animation(ca)
                sub_name = anim_data.get("name", ca.name or asset_name)
                if len(items_to_process) > 1:
                    sub_name = f"{asset_name} - {sub_name}"
                
                glob_vars.rbx_anim_sub_items.append({
                    'name': sub_name,
                    'anim_data': anim_data,
                    'is_curve_anim': True
                })
                dprint(
                    f"  Parsed CurveAnimation: {sub_name} "
                    f"({len(anim_data['keyframes'])} tracks, {anim_data['length']:.2f}s)"
                )
            except Exception as e:
                dprint(f"  Error parsing CurveAnimation '{ca.name}': {e}")
                continue
    
    dprint(f"Total sub-animations discovered: {len(glob_vars.rbx_anim_sub_items)}")


def download_model(context, download_all=False):
    """
    Download and import Roblox Model (.rbxm) as Blender primitives.
    """
    from . import func_rbx_other
    importlib.reload(func_rbx_other)
    from . import func_rbx_cloud_api
    importlib.reload(func_rbx_cloud_api)
    from . import rbx_import_models
    importlib.reload(rbx_import_models)

    rbx_prefs = context.scene.rbx_prefs
    at_origin = rbx_prefs.rbx_model_choice_at_origin
    add_textures = rbx_prefs.rbx_model_choice_add_textures

    # Auth
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get items from discovered data
    items = glob_vars.discovered_items_data.get("Models", [])
    if not items:
        dprint("No Model items found in discovered data.")
        return

    # Filter if not downloading all
    if not download_all:
        selected = rbx_prefs.rbx_enum_models
        if selected == "ALL":
            items_to_process = items
        elif selected == "NONE":
            return
        else:
            items_to_process = [i for i in items if str(i['id']) == selected]
    else:
        items_to_process = items

    # Determine tmp path — nest under the main discovered item name
    main_item_name = func_rbx_other.replace_restricted_char(
        getattr(glob_vars, 'rbx_asset_name', None) or "Unknown"
    )
    rbx_tmp_rbxm_filepath = os.path.join(addon_path, glob_vars.rbx_import_main_folder, "tmp_rbxm", main_item_name)
    if not os.path.exists(rbx_tmp_rbxm_filepath):
        os.makedirs(rbx_tmp_rbxm_filepath)

    imported_count = 0
    failed_permission = []
    failed_other = []

    for item in items_to_process:
        asset_id = item['id']
        asset_name = item['name']
        dprint(f"Downloading Model: {asset_name} ({asset_id})")

        # Download RBXM
        success = ensure_local_asset(
            asset_id, headers, rbx_tmp_rbxm_filepath,
            func_rbx_cloud_api, func_rbx_other
        )
        if not success:
            dprint(f"Failed to download model {asset_name}")
            err = glob_vars.rbx_imp_error or ""
            if "401" in err or "403" in err or "Access Denied" in err or "Permission" in err:
                failed_permission.append(str(asset_id))
            else:
                failed_other.append(str(asset_id))
            continue

        # Import model
        rbxm_path = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
        if os.path.isfile(rbxm_path):
            root_col = rbx_import_models.import_model(
                rbxm_file_path=rbxm_path,
                model_name=asset_name,
                at_origin=at_origin,
                add_textures=add_textures,
                func_rbx_other=func_rbx_other,
                headers=headers,
                tmp_path=rbx_tmp_rbxm_filepath,
                func_rbx_cloud_api=func_rbx_cloud_api
            )
            if root_col is not None:
                try:
                    imported_count += len(root_col.all_objects)
                except Exception as e:
                    dprint(f"Could not count imported objects: {e}")

    dprint("Model download and import complete.")
    
    def show_summary():
        try:
            override_ctx = {}
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                override_ctx['window'] = window
                                override_ctx['screen'] = window.screen
                                override_ctx['area'] = area
                                override_ctx['region'] = region
                                break
                        break
                if 'window' in override_ctx:
                    break
                    
            if hasattr(bpy.context, "temp_override"):
                with bpy.context.temp_override(**override_ctx):
                    bpy.ops.wm.rbx_import_model_summary('INVOKE_DEFAULT', 
                        imported_count=imported_count,
                        failed_permission=",".join(failed_permission),
                        failed_other=",".join(failed_other))
            else:
                bpy.ops.wm.rbx_import_model_summary(override_ctx, 'INVOKE_DEFAULT', 
                    imported_count=imported_count,
                    failed_permission=",".join(failed_permission),
                    failed_other=",".join(failed_other))
        except Exception as e:
            dprint(f"Failed to show import summary: {e}")
        return None

    try:
        bpy.app.timers.register(show_summary, first_interval=0.1)
    except Exception as e:
        dprint(f"Failed to register summary timer: {e}")


def execute_global_spawn_tracker():
    """
    Moves all globally tracked imported objects to the origin iteratively 
    so that relative offsets are preserved, and then clears the tracker.
    Must be called at the very end of the import operator after all categories process.
    """
    if glob_vars.rbx_spawn_tracker:
        dprint(f"Moving {len(glob_vars.rbx_spawn_tracker)} tracked objects to origin...")
        bpy.ops.object.select_all(action='DESELECT')
        
        valid_objs = []
        for obj in glob_vars.rbx_spawn_tracker:
            try:
                if obj.name in bpy.data.objects:
                    obj.select_set(True)
                    valid_objs.append(obj)
            except ReferenceError:
                pass
                
        if valid_objs:
            bpy.context.view_layer.objects.active = valid_objs[0]
            bpy.context.scene.cursor.location = (0, 0, 0)
            
            override_ctx = None
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                override_ctx = {'window': window, 'screen': window.screen, 'area': area, 'region': region}
                                break
                        if override_ctx: break
                if override_ctx: break
            
            if override_ctx:
                with bpy.context.temp_override(**override_ctx):
                    bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
            else:
                dprint("No 3D View found, cannot perform group snap to cursor.")
                
            bpy.ops.object.select_all(action='DESELECT')
            
        glob_vars.rbx_spawn_tracker.clear()
