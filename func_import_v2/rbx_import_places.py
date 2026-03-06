import bpy
import os
import importlib
import asyncio
from RBX_Toolbox import glob_vars
from glob_vars import addon_path


### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


def download_place(context, download_all=False):
    """
    Download and import Roblox Place (.rbxm) as Blender primitives.
    Uses the same import pipeline as Models since Places are structurally
    identical in RBXM format.
    """
    from . import func_rbx_other
    importlib.reload(func_rbx_other)
    from . import func_rbx_cloud_api
    importlib.reload(func_rbx_cloud_api)
    from . import rbx_import_models
    importlib.reload(rbx_import_models)
    from .rbx_import_download_manager import ensure_local_asset

    rbx_prefs = context.scene.rbx_prefs
    at_origin = rbx_prefs.rbx_place_choice_at_origin
    add_textures = rbx_prefs.rbx_place_choice_add_textures

    # Auth
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get items from discovered data
    items = glob_vars.discovered_items_data.get("Places", [])
    if not items:
        dprint("No Place items found in discovered data.")
        return

    # Filter if not downloading all
    if not download_all:
        selected = rbx_prefs.rbx_enum_places
        if selected == "ALL":
            items_to_process = items
        elif selected == "NONE":
            return
        else:
            items_to_process = [i for i in items if str(i['id']) == selected]
    else:
        items_to_process = items

    # Determine tmp path
    rbx_tmp_rbxm_filepath = os.path.join(addon_path, glob_vars.rbx_import_main_folder, "tmp_rbxm")
    if not os.path.exists(rbx_tmp_rbxm_filepath):
        os.makedirs(rbx_tmp_rbxm_filepath)

    for item in items_to_process:
        asset_id = item['id']
        asset_name = item['name']
        dprint(f"Downloading Place: {asset_name} ({asset_id})")

        # Per-item subfolder
        item_clean_name = func_rbx_other.replace_restricted_char(asset_name)
        item_tmp_path = os.path.join(rbx_tmp_rbxm_filepath, item_clean_name)
        if not os.path.exists(item_tmp_path):
            os.makedirs(item_tmp_path)

        # Download RBXM
        success = ensure_local_asset(
            asset_id, headers, item_tmp_path,
            func_rbx_cloud_api, func_rbx_other
        )
        if not success:
            dprint(f"Failed to download place {asset_name}")
            continue

        # Import place (same as model)
        rbxm_path = os.path.join(item_tmp_path, str(asset_id) + ".rbxm")
        if os.path.isfile(rbxm_path):
            rbx_import_models.import_model(
                rbxm_file_path=rbxm_path,
                model_name=asset_name,
                at_origin=at_origin,
                add_textures=add_textures,
                func_rbx_other=func_rbx_other,
                headers=headers,
                tmp_path=item_tmp_path,
                func_rbx_cloud_api=func_rbx_cloud_api
            )

    dprint("Place download and import complete.")
