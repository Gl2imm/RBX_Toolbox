import bpy
import os
import asyncio
import requests
import json
import importlib
from RBX_Toolbox import glob_vars
from glob_vars import addon_path


# code here runs only in editor
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rbx_import_discovery import *

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


category_checkboxes = {
    "Body Parts": ["rbx_enum_body_parts"],
    "Accessory": [],
    "Dynamic Head": ["rbx_enum_dynamic_head"],
    "Layered Cloth": ["rbx_enum_layered_cloth", "rbx_bnds_lc_enum", "rbx_lc_dum_enum", "rbx_lc_spl_enum", "rbx_lc_dum_anim_enum", "rbx_lc_anim_enum"],
    "Face Parts": ["rbx_enum_face_parts", "rbx_bnds_lc_enum", "rbx_lc_dum_enum", "rbx_lc_spl_enum", "rbx_lc_dum_anim_enum", "rbx_lc_anim_enum"],
    "Classics": ["rbx_enum_classics"],
    "Gear": ["rbx_enum_gear"],
    "Armature": [],
    "Store Model": [],
    "Models": []
}

class RBX_OT_import_discovery(bpy.types.Operator):
    """Asset Discovery"""
    bl_idname = "object.rbx_import_discovery"
    bl_label = "Asset Discovery"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Clear previous errors
        glob_vars.rbx_imp_error = None

        from .readers import mesh_reader
        importlib.reload(mesh_reader)
        from . import func_rbx_other
        importlib.reload(func_rbx_other)
        from . import func_rbx_cloud_api
        importlib.reload(func_rbx_cloud_api)
        from . import func_rbx_api
        importlib.reload(func_rbx_api)
        from . import rbx_import_download_manager
        importlib.reload(rbx_import_download_manager)
        from . import rbx_import_meshes
        importlib.reload(rbx_import_meshes)
        from . import rbx_import_cages
        importlib.reload(rbx_import_cages)
        from . import rbx_import_attachments
        importlib.reload(rbx_import_attachments)


        # Enable Beta Mode (Gray out input)
        context.scene.rbx_prefs.rbx_import_beta_active = True

        # Run async function from sync context and refresh Auth Token if need
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # We might need token for some operations, keeping it consistent with other importers
        access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        rbx_prefs = context.scene.rbx_prefs
        rbx_item_field_entry = rbx_prefs.rbx_item_field_entry
        
        # 1. Extract ID
        rbx_asset_id, rbx_imp_error = func_rbx_other.item_field_extract_id(rbx_item_field_entry)
        
        if rbx_imp_error:
            self.report({'ERROR'}, rbx_imp_error)
            return {'CANCELLED'}
        
        dprint(f"Asset Discovery started for ID: {rbx_asset_id}")
        if not rbx_imp_error:
            rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, rbx_bundledItems, rbx_imp_error = func_rbx_api.get_catalog_bundle_data(rbx_asset_id, headers)
            
            # If Bundle failed, try as Single Asset
            if rbx_imp_error:
                inStr = str(rbx_imp_error)
                if "404" in inStr:
                    dprint("Bundle not found, trying as Single Asset...")
                    asset_name, asset_type_id, asset_creator, asset_error = func_rbx_api.get_catalog_asset_data(rbx_asset_id, headers)
                    
                    if asset_name:
                        dprint(f"Found Single Asset: {asset_name} (Type: {asset_type_id})")
                        rbx_imp_error = None # Clear error
                        glob_vars.rbx_imp_error = None
                        rbx_asset_name = asset_name
                        rbx_asset_type_id = asset_type_id 
                        rbx_asset_creator = asset_creator
                        
                        # Create a "fake" bundled item list for the single asset to reuse existing logic
                        rbx_bundledItems = [{
                            'id': int(rbx_asset_id),
                            'name': rbx_asset_name,
                            'type': 'Asset',
                            'assetType': asset_type_id
                        }]
                    else:
                        dprint("Single Asset check failed:", asset_error)
                        self.report({'ERROR'}, f"Discovery Failed: {asset_error}")
                        return {'CANCELLED'}
                else:
                    # Some other error occurred
                    self.report({'ERROR'}, f"Bundle Discovery Failed: {rbx_imp_error}")
                    return {'CANCELLED'}

            dprint("rbx_bundledItems: ", rbx_bundledItems)
            
            # Store details in glob_vars for UI
            glob_vars.rbx_asset_name = rbx_asset_name
            glob_vars.rbx_asset_creator = rbx_asset_creator
            glob_vars.rbx_asset_id = int(rbx_asset_id) # Store Bundle/Asset ID for props reference
            
            # Map type ID to name
            type_name = glob_vars.rbx_bundle_types.get(rbx_asset_type_id)
            if not type_name:
                 type_name = glob_vars.rbx_asset_types.get(rbx_asset_type_id, f"Unknown Type ({rbx_asset_type_id})")
            glob_vars.rbx_asset_type = type_name

            # Reset and populate discovered items
            glob_vars.discovered_items_data = {cat: [] for cat in glob_vars.supported_assets_v2}
            glob_vars.rbx_default_head_used = False
            
            if rbx_bundledItems:
                for item in rbx_bundledItems:
                    if item.get('type') == 'Asset':
                        asset_type = item.get('assetType')
                        # Find which category this asset type belongs to
                        for category, types in glob_vars.supported_assets_v2.items():
                            if asset_type in types:
                                glob_vars.discovered_items_data[category].append({
                                    'id': item.get('id'),
                                    'name': item.get('name')
                                })
                                break # Stop after finding the category
            
            # Logic: If Character Bundle (Type 1) AND No Dynamic Head -> Use Default (ID 10687288296)
            # Since Type 17 is now in "Dynamic Head" category, if it's found, get("Dynamic Head") will be truthy.
            if rbx_asset_type_id == 1 and not glob_vars.discovered_items_data.get("Dynamic Head"):
                dprint("No Dynamic Head found for Character Bundle. Adding Default (ID 10687288296).")
                glob_vars.discovered_items_data["Dynamic Head"].append({
                    'id': 10687288296, # Default Dynamic Head ID
                    'name': "Dylan Standard (Default)"
                })
                glob_vars.rbx_default_head_used = True

            dprint("Grouped Items:", glob_vars.discovered_items_data)

            # --- Thumbnail Preview Implementation ---
            # 1. Clean Name
            rbx_asset_name_clean = func_rbx_other.replace_restricted_char(rbx_asset_name)
            glob_vars.rbx_asset_name_clean = rbx_asset_name_clean
            
            # 2. Determine if bundle
            is_bundle = (rbx_asset_type_id in glob_vars.rbx_bundle_types.keys())
            # Also check if it was treated as a single asset with fake bundle list
            if len(rbx_bundledItems) == 1 and rbx_bundledItems[0]['id'] == int(rbx_asset_id):
                 # It was a single asset, but let's double check type. 
                 # If type in bundle types, it is bundle. If in asset types, it is asset.
                 # However, get_asset_and_bundle_img_url expects boolean. 
                 # rbx_asset_type_id comes from get_catalog_bundle_data or get_catalog_asset_data.
                 pass

            # 3. Get URL
            img_url, img_error = func_rbx_api.get_asset_and_bundle_img_url(rbx_asset_id, is_bundle)
            
            if not img_error and img_url:
                # 4. Get Image Data
                img_data, img_error = func_rbx_api.get_asset_and_bundle_img(img_url)
                
                if not img_error and img_data:
                    # 5. Save to Tmp
                    try:
                        # Clear old image if exists
                        old_img = bpy.data.images.get(rbx_asset_name_clean + ".png")
                        if old_img:
                            bpy.data.images.remove(old_img)
                            
                        # Ensure tmp folder
                        tmp_dir = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp')
                        if not os.path.exists(tmp_dir):
                            os.makedirs(tmp_dir)
                            
                        img_path = os.path.join(tmp_dir, rbx_asset_name_clean + ".png")
                        
                        with open(img_path, "wb") as f:
                            f.write(img_data)
                            
                        # 6. Load into Blender
                        bpy.data.images.load(img_path)
                        dprint(f"Thumbnail loaded: {img_path}")
                        
                    except Exception as e:
                        dprint(f"Error saving/loading thumbnail: {e}")
                else:
                    dprint(f"Error getting image data: {img_error}")
            else:
                 dprint(f"Error getting image URL: {img_error}")


        return {'FINISHED'}


class RBX_OT_import_reset(bpy.types.Operator):
    """Reset Import (Beta)"""
    bl_idname = "object.rbx_import_reset"
    bl_label = "Reset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        glob_vars.rbx_imp_error = None
        rbx_prefs = context.scene.rbx_prefs
        
        # Reset UI State
        rbx_prefs.rbx_import_beta_active = False
        
        # Clear discovered items
        glob_vars.discovered_items_data = {}
        glob_vars.rbx_default_head_used = False
        glob_vars.rbx_armature_warning_active = False
        glob_vars.rbx_anim_sub_items = []

        self.report({'INFO'}, "Import (Beta) Reset")
        return {'FINISHED'}


class RBX_OT_import_discovery_download(bpy.types.Operator):
    """Download Discovered Items"""
    bl_idname = "object.rbx_import_discovery_download"
    bl_label = "Download"
    bl_options = {'REGISTER', 'UNDO'}
    
    category: bpy.props.StringProperty() # type: ignore

    def execute(self, context):
        self.report({'INFO'}, f"Download triggered for category: {self.category}")
        
        # Reload modules to ensure latest code is used
        from . import rbx_import_download_manager
        importlib.reload(rbx_import_download_manager)
        
        glob_vars.rbx_armature_warning_active = False
        
        download_all_items = (self.category == "ALL_CATEGORIES")

        if self.category == "Body Parts" or self.category == "ALL_CATEGORIES":
            self.report({'INFO'}, "Downloading Body Parts...")
            rbx_import_download_manager.download_body_parts(context, category_name="Body Parts", download_all=download_all_items)
            
        if self.category == "Dynamic Head" or self.category == "ALL_CATEGORIES":
            self.report({'INFO'}, "Downloading Dynamic Heads...")
            rbx_import_download_manager.download_body_parts(context, category_name="Dynamic Head", download_all=download_all_items)

        if self.category == "Accessory" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Accessories...")
             rbx_import_download_manager.download_body_parts(context, category_name="Accessory", download_all=download_all_items)

        if self.category == "Layered Cloth" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Layered Cloth...")
             rbx_import_download_manager.download_body_parts(context, category_name="Layered Cloth", download_all=download_all_items)

        if self.category == "Face Parts" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Face Parts...")
             rbx_import_download_manager.download_body_parts(context, category_name="Face Parts", download_all=download_all_items)

        if self.category == "Classics" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Classics...")
             rbx_import_download_manager.download_body_parts(context, category_name="Classics", download_all=download_all_items)

        if self.category == "Gear" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Gears...")
             rbx_import_download_manager.download_body_parts(context, category_name="Gear", download_all=download_all_items)

        if self.category == "Armature" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Armature...")
             rbx_import_download_manager.download_body_parts(context, category_name="Armature", download_all=download_all_items)

        # Animations are NOT included in ALL_CATEGORIES per user request
        if self.category == "Animations":
             self.report({'INFO'}, "Downloading Animations...")
             rbx_import_download_manager.download_animation(context)

        # Models download handler
        if self.category == "Models" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Models...")
             rbx_import_download_manager.download_model(context, download_all=download_all_items)

        # Places download handler
        if self.category == "Places" or self.category == "ALL_CATEGORIES":
             self.report({'INFO'}, "Downloading Places...")
             from . import rbx_import_places
             importlib.reload(rbx_import_places)
             rbx_import_places.download_place(context, download_all=download_all_items)

        if self.category.startswith("Animations_Apply_"):
             anim_idx = int(self.category.split("_")[-1])
             self.report({'INFO'}, "Applying Animation...")
             rbx_import_download_manager.download_animation(context, apply_index=anim_idx)

        return {'FINISHED'}


class RBX_OT_import_discovery_options(bpy.types.Operator):
    """Configuration Options for Discovery Category"""
    bl_idname = "object.rbx_import_discovery_options"
    bl_label = "Options"
    bl_options = {'REGISTER', 'UNDO'}
    
    category: bpy.props.StringProperty() # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        rbx_prefs = context.scene.rbx_prefs
        category = self.category
        
        box = layout.box()
        box.label(text=f"Options: {category}", icon='PREFERENCES')

        if category == "Body Parts":
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_at_origin') 
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_add_meshes')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_bndl_char_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_bndl_char_choice_add_textures')
            
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_add_cages')
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_add_attachment')
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_add_motor6d_attachment')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_bndl_char_choice_add_meshes or rbx_prefs.rbx_bndl_char_choice_add_cages
            row.prop(rbx_prefs, 'rbx_bndl_char_choice_add_ver_col')
            
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_clean_tmp_meshes')

        if category == "Dynamic Head":
            box.prop(rbx_prefs, 'rbx_dyn_heads_choice_at_origin') 
            box.prop(rbx_prefs, 'rbx_dyn_heads_choice_add_meshes')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_dyn_heads_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_dyn_heads_choice_add_textures')
            
            box.prop(rbx_prefs, 'rbx_dyn_heads_choice_add_cages')
            box.prop(rbx_prefs, 'rbx_dyn_heads_choice_add_attachment')
            box.prop(rbx_prefs, 'rbx_dyn_heads_choice_add_motor6d_attachment')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_dyn_heads_choice_add_meshes or rbx_prefs.rbx_dyn_heads_choice_add_cages
            row.prop(rbx_prefs, 'rbx_dyn_heads_choice_add_ver_col')
            
            box.prop(rbx_prefs, 'rbx_dyn_heads_choice_clean_tmp_meshes')

        if category == "Accessory":
            box.prop(rbx_prefs, 'rbx_accessory_choice_at_origin') 
            box.prop(rbx_prefs, 'rbx_accessory_choice_add_meshes')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_accessory_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_accessory_choice_add_textures')
            
            box.prop(rbx_prefs, 'rbx_accessory_choice_add_attachment')
            
            row = box.row()
            # Gray out if Accessory Attachments not selected
            row.enabled = rbx_prefs.rbx_accessory_choice_add_attachment

            # No Motor6D or Cages for now as per user request ("except cages, motor6d")
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_accessory_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_accessory_choice_add_ver_col')
            
            box.prop(rbx_prefs, 'rbx_accessory_choice_clean_tmp_meshes')

        if category == "Layered Cloth":
            box.prop(rbx_prefs, 'rbx_lc_choice_at_origin') 
            box.prop(rbx_prefs, 'rbx_lc_choice_add_meshes')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_lc_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_lc_choice_add_textures')
            
            box.prop(rbx_prefs, 'rbx_lc_choice_add_cages')
            
            box.prop(rbx_prefs, 'rbx_lc_choice_add_attachment')
            
            row = box.row()
            # Gray out if Attachments not selected
            row.enabled = rbx_prefs.rbx_lc_choice_add_attachment

            
            row = box.row()
            row.enabled = rbx_prefs.rbx_lc_choice_add_meshes or rbx_prefs.rbx_lc_choice_add_cages
            row.prop(rbx_prefs, 'rbx_lc_choice_add_ver_col')
            
            box.prop(rbx_prefs, 'rbx_lc_choice_clean_tmp_meshes')

        if category == "Face Parts":
            box.prop(rbx_prefs, 'rbx_fp_choice_at_origin') 
            box.prop(rbx_prefs, 'rbx_fp_choice_add_meshes')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_fp_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_fp_choice_add_textures')
            
            box.prop(rbx_prefs, 'rbx_fp_choice_add_cages')
            
            box.prop(rbx_prefs, 'rbx_fp_choice_add_attachment')
            
            row = box.row()
            # Gray out if Attachments not selected
            row.enabled = rbx_prefs.rbx_fp_choice_add_attachment

            
            row = box.row()
            row.enabled = rbx_prefs.rbx_fp_choice_add_meshes or rbx_prefs.rbx_fp_choice_add_cages
            row.prop(rbx_prefs, 'rbx_fp_choice_add_ver_col')
            
            box.prop(rbx_prefs, 'rbx_fp_choice_clean_tmp_meshes')

        if category == "Gear":
            box.prop(rbx_prefs, 'rbx_gears_choice_at_origin') 
            box.prop(rbx_prefs, 'rbx_gears_choice_add_meshes')
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_gears_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_gears_choice_add_textures')
            
            box.prop(rbx_prefs, 'rbx_gears_choice_clean_tmp_meshes')

        if category == "Armature":
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_armature_at_origin') # Reusing bundle origin pref
            box.prop(rbx_prefs, 'rbx_bndl_char_choice_armature_link_meshes')

        if category == "Models":
            box.prop(rbx_prefs, 'rbx_model_choice_at_origin')
            box.prop(rbx_prefs, 'rbx_model_choice_add_textures')

        if category == "Places":
            box.prop(rbx_prefs, 'rbx_place_choice_at_origin')
            box.prop(rbx_prefs, 'rbx_place_choice_add_textures')

        # Generic Checkbox Loop
        if category in category_checkboxes:
            for prop_name in category_checkboxes[category]:
                # Skip properties already manually handled for certain categories
                if category == "Body Parts": 
                    continue 
                if category in ["Layered Cloth", "Face Parts"]:
                    continue
                if category == "Dynamic Head" and prop_name == "rbx_enum_dynamic_head":
                     # rbx_enum_dynamic_head is the dropdown, usually shown in main panel, but we iterate here
                     continue
                if category == "Gear" and prop_name == "rbx_enum_gear":
                     continue
                if hasattr(rbx_prefs, prop_name):
                    box.prop(rbx_prefs, prop_name)

    def execute(self, context):
        return {'FINISHED'}


class RBX_OT_import_discovery_open_folder(bpy.types.Operator):
    """Open Import Folder"""
    bl_idname = "object.rbx_import_discovery_open_folder"
    bl_label = "Open Folder"
    bl_options = {'REGISTER', 'UNDO'}
    
    category: bpy.props.StringProperty() # type: ignore

    def execute(self, context):
        category = self.category
        
        # Determine folder based on category 
        target_subfolder = glob_vars.rbx_import_v2_bundles # Default to Bundles
        
        if category == "Accessory":
            target_subfolder = "Accessories"
        elif category == "Gear":
            target_subfolder = "Gears"
        elif category == "Layered Cloth":
            target_subfolder = "Layered Clothing"
        elif category == "Dynamic Head":
            target_subfolder = "Dynamic Heads"
        elif category == "Face Parts":
            target_subfolder = "Face Parts"
        elif category == "Classics":
            target_subfolder = "Classics"
        elif category == "Armature":
            target_subfolder = glob_vars.rbx_import_v2_bundles # Armatures come from bundles mostly
        elif category == "Models":
            target_subfolder = "Models"
        
        # Construct full path
        folder_path = os.path.join(addon_path, glob_vars.rbx_import_main_folder, target_subfolder)
        
        if folder_path:
            # Ensure folder exists
            if not os.path.exists(folder_path):
                try:
                    os.makedirs(folder_path)
                    self.report({'INFO'}, f"Created folder: {folder_path}")
                except Exception as e:
                    self.report({'ERROR'}, f"Could not create folder: {e}")
                    return {'CANCELLED'}
            
            # Open folder
            try:
                os.startfile(folder_path)
                self.report({'INFO'}, f"Opened folder: {folder_path}")
            except Exception as e:
                self.report({'ERROR'}, f"Could not open folder: {e}")
        else:
             self.report({'WARNING'}, f"No folder mapped for category: {category}")

        return {'FINISHED'}
