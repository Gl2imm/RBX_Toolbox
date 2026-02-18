import bpy
import os
import asyncio
import requests
import json
import importlib
from RBX_Toolbox import glob_vars
from glob_vars import addon_path


# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)

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
    "Gear": ["rbx_enum_gear"],
    "Store Model": []
}

class RBX_OT_import_discovery(bpy.types.Operator):
    """Asset Discovery"""
    bl_idname = "object.rbx_import_discovery"
    bl_label = "Asset Discovery"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Clear previous errors
        glob_vars.rbx_imp_error = None

        from pythonnet import load
        load('coreclr')
        import clr
        from System.Reflection import Assembly # type: ignore
        clr.AddReference(robloxfile_dll) # type: ignore
        # this is import from dll in runtime
        if not TYPE_CHECKING:
            from RobloxFiles import RobloxFile, Folder, MeshPart, Part, WrapTarget, Attachment, SpecialMesh, SurfaceAppearance, Shirt, Pants, Accessory   # type: ignore
        from . import mesh_reader
        importlib.reload(mesh_reader)
        from . import func_rbx_other
        importlib.reload(func_rbx_other)
        from . import func_rbx_cloud_api
        importlib.reload(func_rbx_cloud_api)
        from . import func_rbx_api
        importlib.reload(func_rbx_api)


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
            
            # Map type ID to name
            type_name = glob_vars.rbx_bundle_types.get(rbx_asset_type_id)
            if not type_name:
                 type_name = glob_vars.rbx_asset_types.get(rbx_asset_type_id, f"Unknown Type ({rbx_asset_type_id})")
            glob_vars.rbx_asset_type = type_name

            # Reset and populate discovered items
            glob_vars.discovered_items_data = {cat: [] for cat in glob_vars.supported_assets}
            glob_vars.rbx_default_head_used = False
            
            if rbx_bundledItems:
                for item in rbx_bundledItems:
                    if item.get('type') == 'Asset':
                        asset_type = item.get('assetType')
                        # Find which category this asset type belongs to
                        for category, types in glob_vars.supported_assets.items():
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
        
        # Reset Input Field to default (or empty, or placeholder)
        # Using the default property value or a standard placeholder
        # rbx_prefs.property_unset("rbx_item_field_entry") # This resets to default
        # Or manually:
        # rbx_prefs.rbx_item_field_entry = "Input ID or URL"  
        
        # Clear discovered items
        glob_vars.discovered_items_data = {}
        glob_vars.rbx_default_head_used = False

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
        # Reload modules to ensure latest code is used
        from . import rbx_import_download_manager
        importlib.reload(rbx_import_download_manager)
        
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
            row.enabled = False 
            row.prop(rbx_prefs, 'rbx_bndl_char_choice_add_bones', text="Armature (in development)")
            
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
            # No Motor6D or Cages for now as per user request ("except cages, motor6d")
            
            row = box.row()
            row.enabled = rbx_prefs.rbx_accessory_choice_add_meshes
            row.prop(rbx_prefs, 'rbx_accessory_choice_add_ver_col')
            
            box.prop(rbx_prefs, 'rbx_accessory_choice_clean_tmp_meshes')

        # Generic Checkbox Loop
        if category in category_checkboxes:
            for prop_name in category_checkboxes[category]:
                # Skip properties already manually handled for certain categories
                if category == "Body Parts": 
                    continue 
                if category == "Dynamic Head" and prop_name == "rbx_enum_dynamic_head":
                     # rbx_enum_dynamic_head is the dropdown, usually shown in main panel, but we iterate here
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
        
        if category == "Body Parts":
            target_subfolder = glob_vars.rbx_import_v2_bundles
        elif category == "Dynamic Head":
            target_subfolder = glob_vars.rbx_import_v2_bundles
        elif category in ["Accessory", "Layered Cloth", "Gear"]:
            target_subfolder = glob_vars.rbx_imported_acc_fldr
        
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
