import os
import importlib
from . import func_rbx_cloud_api
from . import func_rbx_other
from . import func_blndr_api
from RBX_Toolbox import glob_vars

# Reload modules if needed, though usually handled by caller or auto-reload
importlib.reload(func_rbx_cloud_api)
importlib.reload(func_rbx_other)
importlib.reload(func_blndr_api)

### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

def find_texture_from_decals(node):
    """
    Recursively searches for a Decal object and returns its Texture property.
    """
    # Check children
    for child in node.GetChildren():
        if child.class_name == "Decal":
            try:
                tex_raw = child.get("Texture")
                tex = func_rbx_other.resolve_content_uri(tex_raw)
                if tex and tex != "":
                    dprint(f"Found texture in Decal: {tex}")
                    return tex
            except:
                pass
        
        # Recurse
        found = find_texture_from_decals(child)
        if found:
            return found
    return None


def resolve_rbxasset(rbx_path):
    """
    Resolves rbxasset:// paths to the local Roblox installation.
    Example: rbxasset://textures/face.png -> %LOCALAPPDATA%/Roblox/Versions/<latest>/content/textures/face.png
    """
    if not rbx_path.startswith("rbxasset://"):
        return None
    
    sub_path = rbx_path.replace("rbxasset://", "")
    sub_path = sub_path.replace("/", os.sep) # Normalize separators
    
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        dprint("LOCALAPPDATA environment variable not found.")
        return None
        
    versions_dir = os.path.join(local_app_data, "Roblox", "Versions")
    if not os.path.exists(versions_dir):
        dprint(f"Roblox Versions directory not found: {versions_dir}")
        return None
        
    # Find latest version folder
    versions = [os.path.join(versions_dir, d) for d in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, d)) and d.startswith("version-")]
    if not versions:
        dprint("No Roblox version folders found.")
        return None
        
    # Sort by modification time to get latest
    latest_version = max(versions, key=os.path.getmtime)
    dprint(f"Latest Roblox version: {latest_version}")
    
    full_path = os.path.join(latest_version, "content", sub_path)
    
    if os.path.exists(full_path):
        return full_path
    
    dprint(f"Resolved path does not exist: {full_path}")
    return None


def download_and_apply_textures(mesh_part, mesh_name, bundle_own_folder, headers, rbx_obj, asset_clean_name):
    """
    Downloads texture(s) for the mesh_part (Classic or SurfaceAppearance) and applies to rbx_obj.
    mesh_part is now an rbxm_reader Instance object.
    """

    # Check for SurfaceAppearance (PBR)
    rbx_SurfaceAppearance = mesh_part.FindFirstChildOfClass("SurfaceAppearance")
    # For SpecialMesh, SurfaceAppearance is a sibling (child of parent Part), not a child
    if rbx_SurfaceAppearance is None and mesh_part.parent:
        rbx_SurfaceAppearance = mesh_part.parent.FindFirstChildOfClass("SurfaceAppearance")
    
    # Aligning logic with bundle_char
    rbx_textures = {}
    try:
        if mesh_part.class_name == "SpecialMesh":
             # If the passed object is already the SpecialMesh
             special_mesh = mesh_part
        elif mesh_part.class_name == "Part":
            special_mesh = mesh_part.FindFirstChildOfClass("SpecialMesh")
        else:
            special_mesh = None

    except Exception as e:
        dprint(f"Error checking SpecialMesh for {mesh_name}: {e}")
        special_mesh = None

    if rbx_SurfaceAppearance:
        dprint(f"Found SurfaceAppearance for {mesh_name}")
        for tex_name in glob_vars.rbx_pbr_materials:
            try:
                # Direct property access via rbxm_reader Instance
                val_raw = rbx_SurfaceAppearance.get(tex_name)
                val = func_rbx_other.resolve_content_uri(val_raw)
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
                # SpecialMesh uses "TextureId"
                try:
                    raw = special_mesh.get("TextureId")
                    rbx_tex_id_value = func_rbx_other.resolve_content_uri(raw)
                except:
                    # Fallback: try TextureID
                    dprint(f"Failed to get TextureId from SpecialMesh. trying TextureID")
                    try:
                        raw = special_mesh.get("TextureID")
                        rbx_tex_id_value = func_rbx_other.resolve_content_uri(raw)
                    except:
                        pass
            else:
                 # MeshPart uses "TextureID"
                 try:
                    raw = mesh_part.get("TextureID")
                    rbx_tex_id_value = func_rbx_other.resolve_content_uri(raw)
                 except:
                    pass
            
            dprint(f"rbx_tex_id_value for {mesh_name}: {rbx_tex_id_value}")
            
            # FALLBACK: Decals
            if not rbx_tex_id_value or rbx_tex_id_value == "":
                dprint(f"TextureId not found for {mesh_name}, searching Decals...")
                rbx_tex_id_value = find_texture_from_decals(mesh_part)
                if rbx_tex_id_value:
                    dprint(f"Found texture via Decals: {rbx_tex_id_value}")

            if not rbx_tex_id_value or rbx_tex_id_value == "":
                 rbx_textures = None
            else:
                 # Check for local rbxasset://
                 resolved_local_path = resolve_rbxasset(str(rbx_tex_id_value))
                 if resolved_local_path:
                     dprint(f"Resolved local asset: {resolved_local_path}")
                     rbx_textures = {}
                     rbx_textures["Color"] = resolved_local_path
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
        # Check if tex_id is a local absolute path (from resolve_rbxasset)
        if os.path.isabs(str(tex_id)) and os.path.exists(str(tex_id)):
             # Copy local file to bundle folder
             import shutil
             tex_file_name = f"{mesh_name}_{tex_name}.png"
             tex_path = os.path.join(bundle_own_folder, tex_file_name)
             
             try:
                 if not os.path.exists(tex_path):
                     shutil.copy2(str(tex_id), tex_path)
                     dprint(f"Copied local asset to: {tex_path}")
             except Exception as e:
                 dprint(f"Error copying local asset: {e}")
             
             new_rbx_textures[tex_name] = tex_path
             continue

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

def classic_shirt_import(asset_id, asset_name, bundles_folder, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other):
    rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
    if not os.path.exists(rbx_tmp_rbxm_file): return

    from .readers import rbxm_reader
        
    try:
        file = rbxm_reader.parse(rbx_tmp_rbxm_file)
        shirt_node = file.FindFirstChildOfClass("Shirt")
        if shirt_node:
            template_raw = shirt_node.get("ShirtTemplate")
            template_id_val = func_rbx_other.resolve_content_uri(template_raw)
            if template_id_val:
                tex_id = func_rbx_other.strip_rbxassetid(template_id_val)
                asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
                tex_file_name = f"{asset_clean_name}.png"
                tex_path = os.path.join(bundles_folder, tex_file_name)
                
                tex_data, tex_error = func_rbx_cloud_api.get_asset_data(tex_id, headers)
                if not tex_error and tex_data:
                    with open(tex_path, "wb") as f:
                        f.write(tex_data)
                    dprint(f"Classic shirt saved to {tex_path}")
                else:
                    dprint(f"Error downloading classic shirt texture {tex_id}: {tex_error}")
    except Exception as e:
        dprint(f"Error processing classic shirt: {e}")

def classic_pants_import(asset_id, asset_name, bundles_folder, headers, rbx_tmp_rbxm_filepath, func_rbx_cloud_api, func_rbx_other):
    rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
    if not os.path.exists(rbx_tmp_rbxm_file): return

    from .readers import rbxm_reader
        
    try:
        file = rbxm_reader.parse(rbx_tmp_rbxm_file)
        pants_node = file.FindFirstChildOfClass("Pants")
        if pants_node:
            template_raw = pants_node.get("PantsTemplate")
            template_id_val = func_rbx_other.resolve_content_uri(template_raw)
            if template_id_val:
                tex_id = func_rbx_other.strip_rbxassetid(template_id_val)
                asset_clean_name = func_rbx_other.replace_restricted_char(asset_name)
                tex_file_name = f"{asset_clean_name}.png"
                tex_path = os.path.join(bundles_folder, tex_file_name)
                
                tex_data, tex_error = func_rbx_cloud_api.get_asset_data(tex_id, headers)
                if not tex_error and tex_data:
                    with open(tex_path, "wb") as f:
                        f.write(tex_data)
                    dprint(f"Classic pants saved to {tex_path}")
                else:
                    dprint(f"Error downloading classic pants texture {tex_id}: {tex_error}")
    except Exception as e:
        dprint(f"Error processing classic pants: {e}")
