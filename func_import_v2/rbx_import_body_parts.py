import bpy
import os
import importlib
import json
import requests
import asyncio
from RBX_Toolbox import glob_vars
from glob_vars import addon_path

# Code to run only in editor (type checking)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import func_rbx_api
    from . import func_rbx_other

# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def download_body_parts(context, category_name="Body Parts"):
    from pythonnet import load
    load('coreclr')
    import clr
    from System.Reflection import Assembly # type: ignore
    clr.AddReference(robloxfile_dll) # type: ignore
    
    if not TYPE_CHECKING:
        from RobloxFiles import RobloxFile, Folder, MeshPart, Part, WrapTarget, Attachment # type: ignore
        from RobloxFiles.DataTypes import Vector3, CFrame

    from . import conversion_funct as funct
    importlib.reload(funct)
    from . import func_rbx_other
    importlib.reload(func_rbx_other)
    from . import func_rbx_api
    importlib.reload(func_rbx_api)
    from . import func_blndr_api
    importlib.reload(func_blndr_api)
    from . import func_rbx_cloud_api
    importlib.reload(func_rbx_cloud_api)
    from . import rbx_import_textures
    importlib.reload(rbx_import_textures)
    
    rbx_prefs = context.scene.rbx_prefs
    selected_item_id = rbx_prefs.rbx_enum_body_parts
    
    # Get items to process
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

    # Auth Token (needed for get_asset_data)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Preferences for logic
    rbx_bndl_char_choice_at_origin = rbx_prefs.rbx_bndl_char_choice_at_origin
    rbx_bndl_char_choice_add_meshes = rbx_prefs.rbx_bndl_char_choice_add_meshes
    rbx_bndl_char_choice_add_textures = rbx_prefs.rbx_bndl_char_choice_add_textures
    rbx_bndl_char_choice_add_cages = rbx_prefs.rbx_bndl_char_choice_add_cages
    rbx_bndl_char_choice_add_attachment = rbx_prefs.rbx_bndl_char_choice_add_attachment
    rbx_bndl_char_choice_add_motor6d_attachment = rbx_prefs.rbx_bndl_char_choice_add_motor6d_attachment # Not used in code snippet but might be relevant? 
    # Logic in bundle_char uses it for attachments processing? No, mostly manual.
    # Ah, blender_api_add_attachments is used.
    
    rbx_bndl_char_choice_add_ver_col = rbx_prefs.rbx_bndl_char_choice_add_ver_col
    rbx_bndl_char_choice_clean_tmp_meshes = rbx_prefs.rbx_bndl_char_choice_clean_tmp_meshes
    
    from . import mesh_reader
    importlib.reload(mesh_reader)

    # Process Loop
    for item in items_to_process:
        asset_id = item['id']
        asset_name = item['name']
        dprint(f"Processing Body Part: {asset_name} ({asset_id})")
        
        # 1. Download RBXM
        rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
        asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(asset_id, headers)
        
        if rbx_imp_error or not asset_data:
            dprint(f"Error downloading asset {asset_id}: {rbx_imp_error}")
            continue

        try:
            with open(rbx_tmp_rbxm_file, "wb") as f:
                f.write(asset_data)
        except Exception as e:
            dprint(f"Error saving RBXM {asset_id}: {e}")
            continue
            
        # 2. Open RBXM and Extract
        try:
            rbxm_file = RobloxFile.Open(rbx_tmp_rbxm_file)
        except Exception as e:
            dprint(f"Error opening RBXM {asset_id}: {e}")
            continue

        # Look for R15Fixed folder
        R15Fixed = rbxm_file.FindFirstChild[Folder]("R15Fixed")
        
        if not R15Fixed:
            dprint(f"No R15Fixed folder found in {asset_name}")
            # Fallback: maybe it's just a MeshPart directly?
            # For now strictly following bundle logic which expects R15Fixed
            continue
            
        # 3. Create Collection and Folder
        # Use asset name or bundle name?
        # User might want them in a folder named after bundle or the asset itself?
        # Let's use the asset name for the subfolder
        asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
        bundle_own_folder = os.path.join(bundles_folder, asset_clean_name)
        
        # We need to reuse the same collection if we are processing "ALL" and they belong to same bundle?
        # But here we treat them as individual assets.
        # Let's create a collection for this asset.
        
        # Wait, if we are downloading "Body Parts", usually they are part of a Character.
        # Ideally they should go into one Collection "Character Name".
        # But we only have individual asset info here.
        # Unless we use glob_vars.rbx_asset_name (which is the Bundle/Asset Name from discovery).
        
        main_collection_name = glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else "Imported Body Parts"
        main_collection_name = func_rbx_other.replace_restricted_char(main_collection_name)
        
        rbx_collection = func_blndr_api.blender_api_create_collection(main_collection_name)
        
        # Create folder for textures/objs
        # logic in bundle_char uses: bundles_folder/rbx_asset_name_clean
        # We should map to that.
        
        bundle_own_folder = os.path.join(bundles_folder, main_collection_name)
        if not os.path.exists(bundle_own_folder):
            os.makedirs(bundle_own_folder)

        # 4. Process MeshParts
        rbx_avatar_bundle_parts = [
                "LeftUpperArm", "LeftLowerArm", "LeftHand",
                "RightUpperArm", "RightLowerArm", "RightHand",
                "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
                "RightUpperLeg", "RightLowerLeg", "RightFoot",
                "UpperTorso", "LowerTorso", "Head"
            ]

        mesh_parts_to_process = []
        for mesh_name in rbx_avatar_bundle_parts:
            mesh_part = R15Fixed.FindFirstChild[MeshPart](mesh_name)
            if mesh_part:
                mesh_parts_to_process.append((mesh_part, mesh_name))
        
        # Process extracted parts
        for mesh_part, mesh_name in mesh_parts_to_process:
            dprint(f"  - Processing MeshPart: {mesh_name}")
            
            # Extract Mesh Data
            mesh_id = mesh_part.MeshId
            if not mesh_id:
                dprint(f"    No MeshId for {mesh_name}")
                continue

            # Download Mesh Data
            try:
                # Clean Mesh ID
                # We need to strip 'rbxassetid://' if present
                mesh_id_clean = func_rbx_other.strip_rbxassetid(mesh_id)
                
                # Download metadata/file
                # In bundle_char it calls get_asset_data with headers
                asset_data, rbx_imp_error = func_rbx_cloud_api.get_asset_data(mesh_id_clean, headers)
                
                if rbx_imp_error:
                    dprint(f"    Error downloading mesh {mesh_name}: {rbx_imp_error}")
                    continue
                    
                # Parse
                if asset_data:
                    # We can parse directly from bytes without saving to temp file if we want, 
                    # but bundle_char saves it. Let's parse directly for efficiency unless we need the file later.
                    # bundle_char saves it to .mesh file. 
                    # Let's just parse.
                    mesh_data = mesh_reader.RBXMeshParser.parse(asset_data)
                else:
                    dprint(f"    No data received for mesh {mesh_name}")
                    continue

            except Exception as e:
                dprint(f"    Error reading/parsing mesh data for {mesh_name}: {e}")
                continue
                
            if not mesh_data:
                dprint(f"    No mesh data for {mesh_name}")
                continue
                
            # Create Object in Blender
            cframe = mesh_part.CFrame
            # For pivot, if R15Fixed is a Folder it might not have WorldPivot. 
            # In rbx_import_bundle_char, it uses R15Fixed.WorldPivot if available, else Identity.
            # But R15Fixed is a Folder? Folders don't have WorldPivot in older API? check RobloxFiles.
            # Actually R15Fixed in bundles is usually a Model? NO, it's a Folder in the bundle structure?
            # Let's assume CFrame() identity for pivot if not found or just use the part's CFrame.
            # R15Fixed in bundles is a Folder. Folders don't have WorldPivot.

            
            # Try to get PivotOffset from MeshPart
            part_cframe_pivot = mesh_part.Properties["PivotOffset"].Value


            # Check if pivot is identity (0,0,0, 1,0,0, ...)
            pivot_comps = part_cframe_pivot.GetComponents()
            identity_comps = (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
            is_identity = True
            if len(pivot_comps) == 12:
                for a, b in zip(pivot_comps, identity_comps):
                    if abs(a - b) > 0.0001: 
                        is_identity = False
                        break
            
            # If pivot is identity, force at_origin to False
            actual_at_origin = rbx_bndl_char_choice_at_origin
            if is_identity:
                actual_at_origin = False

            # Force meshes if textures are requested (Logic from Reference)
            if rbx_bndl_char_choice_add_textures and not rbx_bndl_char_choice_add_meshes:
                rbx_bndl_char_choice_add_meshes = True

            rbx_obj = None
            if rbx_bndl_char_choice_add_meshes:
                rbx_obj = func_blndr_api.blender_api_add_meshes_as_obj(
                    bundle_own_folder, mesh_part, mesh_data, cframe, part_cframe_pivot, 
                    actual_at_origin, mesh_reader, funct, mesh_name=mesh_name
                )
            
            # Add Vertex Colors
            if rbx_bndl_char_choice_add_meshes and rbx_bndl_char_choice_add_ver_col and rbx_obj:
                 func_blndr_api.blender_api_add_ver_col(rbx_obj, mesh_data)

            # Add Textures
            if rbx_bndl_char_choice_add_meshes and rbx_bndl_char_choice_add_textures and rbx_obj:
                 rbx_import_textures.download_and_apply_textures(
                     mesh_part, mesh_name, bundle_own_folder, headers, rbx_obj, asset_clean_name
                 )

            # Move to Collection
            if rbx_collection:
                 # Check if object is in collection
                 if rbx_obj.name not in rbx_collection.objects:
                     rbx_collection.objects.link(rbx_obj)
                     # Start unlink from other collections? 
                     # Usually creating object puts it in active collection.
                     # We set active layer collection to rbx_collection earlier? No, we just created it.
                     # blender_api_create_collection sets active layer collection.
                     pass

            # Attachments
            if rbx_bndl_char_choice_add_attachment:
                for child in mesh_part.GetChildren():
                    if child.ClassName == "Attachment":
                        func_blndr_api.blender_api_add_attachments(
                            child, child.CFrame, cframe, cframe_pivot, 
                            actual_at_origin, funct
                        )

    dprint("Body Parts Download Finished.")

    # Cleanup
    if rbx_bndl_char_choice_clean_tmp_meshes:
         # Clean tmp folder
         pass # Implement if needed
    
