import os
import importlib
from . import func_rbx_cloud_api
from . import func_rbx_other
from . import func_blndr_api

# Reload modules if needed, though usually handled by caller or auto-reload
importlib.reload(func_rbx_cloud_api)
importlib.reload(func_rbx_other)
importlib.reload(func_blndr_api)

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def download_and_apply_textures(mesh_part, mesh_name, bundle_own_folder, headers, rbx_obj, asset_clean_name):
    """
    Downloads texture for the mesh_part and applies it to rbx_obj.
    """
    tex_id = mesh_part.TextureID
    if not tex_id:
        return

    tex_id_clean = func_rbx_other.strip_rbxassetid(tex_id)
    if not tex_id_clean:
        return

    tex_file_name = f"{mesh_name}_diff.png"
    tex_path = os.path.join(bundle_own_folder, tex_file_name)
    
    if not os.path.exists(tex_path):
        tex_data, tex_error = func_rbx_cloud_api.get_asset_data(tex_id_clean, headers)
        if not tex_error and tex_data:
            try:
                with open(tex_path, "wb") as f:
                    f.write(tex_data)
            except Exception as e:
                dprint(f"    Error saving texture {tex_file_name}: {e}")
    
    if os.path.exists(tex_path):
        rbx_textures = {"Color": tex_path}
        # rbx_SurfaceAppearance = False for now, strictly classic textures
        func_blndr_api.blender_api_assets_new_material(
            rbx_obj, mesh_part, rbx_textures, asset_clean_name, False
        )
