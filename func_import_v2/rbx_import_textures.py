import os
import importlib
from . import func_rbx_cloud_api
from . import func_rbx_other
from . import func_blndr_api
from RBX_Toolbox import glob_vars
from typing import TYPE_CHECKING

# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)

# Reload modules if needed, though usually handled by caller or auto-reload
importlib.reload(func_rbx_cloud_api)
importlib.reload(func_rbx_other)
importlib.reload(func_blndr_api)

### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def download_and_apply_textures(mesh_part, mesh_name, bundle_own_folder, headers, rbx_obj, asset_clean_name):
    """
    Downloads texture(s) for the mesh_part (Classic or SurfaceAppearance) and applies to rbx_obj.
    """
    # Removed load('coreclr') logic error - context is already loaded by caller
    import clr
    from System.Reflection import Assembly # type: ignore
    try:
        clr.AddReference(robloxfile_dll) # type: ignore
    except:
        pass

    if not TYPE_CHECKING:
        from RobloxFiles import RobloxFile, Folder, MeshPart, Part, WrapTarget, Attachment, SpecialMesh, SurfaceAppearance # type: ignore
    

    # Check for SurfaceAppearance (PBR)
    # Using typed FindFirstChild to ensure correct overload resolution
    rbx_SurfaceAppearance = mesh_part.FindFirstChild[SurfaceAppearance]("SurfaceAppearance")
    
    # Aligning logic with bundle_char
    rbx_textures = {}
    try:
        special_mesh = None
        if mesh_part.ClassName == "Part":
            special_mesh = mesh_part.FindFirstChildOfClass[SpecialMesh]()
            # Note: We are not extracting MeshId here as the function is focused on textures, 
            # but we need special_mesh for TextureId logic later.
    except Exception as e:
        dprint(f"Error checking SpecialMesh for {mesh_name}: {e}")
        pass

    if rbx_SurfaceAppearance:
        dprint(f"Found SurfaceAppearance for {mesh_name}")
        for tex_name in glob_vars.rbx_pbr_materials:
            try:
                # Direct property access (No Reflection fixes per user request)
                val = rbx_SurfaceAppearance.Properties[tex_name].Value
                part_TextureID = func_rbx_other.strip_rbxassetid(val)
                
                if part_TextureID == "" or part_TextureID == "None":
                    continue
                
                # Name mapping logic
                internal_name = tex_name
                if internal_name == "MetalnessMap":
                    internal_name = "MetallicMap"
                
                # Remove "Map" suffix
                if internal_name.endswith("Map"):
                    internal_name = internal_name[:-3]
                    
                rbx_textures[internal_name] = part_TextureID
            except Exception as e:
                dprint(f"Error accessing property {tex_name}: {e}")
                continue

    else:
        # Classic Textures
        try:
            rbx_tex_id_value = None
            
            if special_mesh:
                rbx_tex_id_value = special_mesh.Properties["TextureId"].Value
            else:
                rbx_tex_id_value = mesh_part.Properties["TextureID"].Value
            dprint(f"rbx_tex_id_value for {mesh_name}: {rbx_tex_id_value}")
            
            if not rbx_tex_id_value or str(rbx_tex_id_value) == "":
                 rbx_textures = None
            else:
                 part_TextureID = func_rbx_other.strip_rbxassetid(rbx_tex_id_value)
                 rbx_textures = {} 
                 rbx_textures["Color"] = part_TextureID
        except Exception as e:
            dprint(f"Error getting classic texture: {e}")
            rbx_textures = None


    if not rbx_textures:
        dprint(f"No textures found for {mesh_name}")
        return

    dprint(f"rbx_textures for {mesh_name}: {rbx_textures}")

    # Download Textures (Restored)
    new_rbx_textures = rbx_textures.copy()
    
    for tex_name, tex_id in rbx_textures.items():
        tex_file_name = f"{mesh_name}_{tex_name}.png"
        tex_path = os.path.join(bundle_own_folder, tex_file_name)
        
        if not os.path.exists(tex_path):
            tex_data, tex_error = func_rbx_cloud_api.get_asset_data(tex_id, headers)
            if not tex_error and tex_data:
                try:
                    with open(tex_path, "wb") as f:
                        f.write(tex_data)
                except Exception as e:
                    dprint(f"    Error saving texture {tex_file_name}: {e}")
                    # If save fails, we might still want to try next one, or remove this from map?
                    del new_rbx_textures[tex_name]
                    continue
            else:
                 dprint(f"    Error downloading texture {tex_id}: {tex_error}")
                 del new_rbx_textures[tex_name]
                 continue
        
        # Update path in dictionary
        new_rbx_textures[tex_name] = tex_path

    rbx_textures = new_rbx_textures

    if rbx_textures:
        # Apply Material (Restored)
        func_blndr_api.blender_api_assets_new_material(
            rbx_obj, mesh_part, rbx_textures, asset_clean_name, bool(rbx_SurfaceAppearance)
        )


