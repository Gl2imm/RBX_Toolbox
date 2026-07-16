"""Standalone importer for the logged-in user's own Roblox avatar (3D).

Uses the OAuth-scoped Avatar 3D thumbnail endpoint (requires the
`thumbnail:read` scope) to fetch the avatar's OBJ + MTL + textures, then
imports them into the scene reusing the shared func_import_v2 helpers.

Flow (mirrors the legacy `my_avatar` flow, adapted to the current API):
  1. Renew OAuth token -> Bearer headers.
  2. GET .../v1/users/avatar-3d?userId=<id>  (authorized) -> metadata JSON url.
  3. GET metadata JSON -> obj / mtl / textures references.
     Roblox now returns full CDN URLs directly (legacy hash->CDN conversion is
     no longer required), and field names may change over time, so parsing is
     kept tolerant of both formats/names.
  4. Download + save obj, mtl and textures.
  5. Rewrite the MTL to reference the local texture files and strip transparency.
  6. Import the OBJ, fix textures, reposition, remove doubles.
  7. Optionally separate the imported mesh by material.
"""

import bpy
import os
import re
import time
import asyncio
import requests
import importlib

from .. import glob_vars


# code here runs only in editor
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rbx_import_user_avatar import *


### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


#############################################
##### Avatar 3D API response parsing ########
#############################################

def _state_and_image_url(data):
    """Pull (state, imageUrl) out of an avatar-3d response, tolerating both the
    flat `{...}` shape and the batch `{"data": [ {...} ]}` shape."""
    if not isinstance(data, dict):
        return None, None
    first = {}
    if isinstance(data.get("data"), list) and data["data"]:
        first = data["data"][0] or {}
    state = data.get("state") or first.get("state")
    image_url = data.get("imageUrl") or first.get("imageUrl")
    return state, image_url


def get_avatar_meta_url(rbx_user_id, headers, max_retries=6, delay=1.0):
    """Call the OAuth-scoped avatar-3d endpoint and return (meta_url, error).

    Requires the `thumbnail:read` scope on the access token. Retries while the
    thumbnail is still rendering ("Pending"/"...")."""
    url = f"https://thumbnails.roblox.com/v1/users/avatar-3d?userId={rbx_user_id}"
    for attempt in range(max_retries):
        try:
            r = requests.get(url, headers=headers)
        except Exception as e:
            return None, f"Avatar API error: {e}"

        if r.status_code in (401, 403):
            return None, ("Avatar scope not authorized.\n"
                          "Please Log Out and Log In again\nto grant avatar access.")
        if r.status_code != 200:
            return None, f"{r.status_code}: Error contacting Avatar API"

        try:
            data = r.json()
        except Exception as e:
            return None, f"Error reading Avatar API response: {e}"

        state, image_url = _state_and_image_url(data)
        if state == "Completed" or (state is None and image_url):
            return image_url, None
        if state == "Blocked":
            return None, "Avatar API: Banned User - unable to get avatar"

        dprint(f"Avatar API state: {state}. Retry {attempt + 1}/{max_retries}")
        time.sleep(delay)

    return None, f"Avatar API not ready after {max_retries} retries"


def get_avatar_meta(meta_url, headers):
    """Download and parse the avatar metadata JSON. Returns (meta_dict, error).

    Tries the public request first (the metadata lives on the CDN) and falls
    back to an authorized request if needed."""
    if not meta_url:
        return None, "Avatar metadata URL missing in API response"

    last_status = None
    for hdr in (None, headers):
        try:
            r = requests.get(meta_url) if hdr is None else requests.get(meta_url, headers=hdr)
        except Exception as e:
            last_status = f"exception: {e}"
            continue
        last_status = r.status_code
        if r.status_code == 200:
            try:
                return r.json(), None
            except Exception as e:
                return None, f"Error parsing avatar metadata: {e}"

    return None, f"{last_status}: Error downloading avatar metadata"


def classify_avatar_refs(meta):
    """Extract (obj_ref, mtl_ref, [texture_refs]) from the metadata dict.

    Tolerant to Roblox renaming keys: falls back to matching by key name and,
    for textures, to the first list-of-strings value found."""
    if not isinstance(meta, dict):
        return None, None, []

    obj_ref = meta.get("obj")
    mtl_ref = meta.get("mtl")
    tex = meta.get("textures")

    if obj_ref is None or mtl_ref is None or tex is None:
        for k, v in meta.items():
            lk = str(k).lower()
            if obj_ref is None and isinstance(v, str) and "obj" in lk:
                obj_ref = v
            elif mtl_ref is None and isinstance(v, str) and "mtl" in lk:
                mtl_ref = v
            elif tex is None and isinstance(v, list) and ("tex" in lk or "image" in lk):
                tex = v

    # Last resort for textures: first list of non-empty strings.
    if tex is None:
        for v in meta.values():
            if isinstance(v, list) and v and all(isinstance(x, str) for x in v):
                tex = v
                break

    tex_refs = [t for t in tex if isinstance(t, str)] if isinstance(tex, list) else []
    return obj_ref, mtl_ref, tex_refs


def resolve_ref_url(ref):
    """A ref may already be a full CDN URL (current format) or a bare hash
    (legacy). Return a downloadable URL."""
    from . import func_rbx_other
    ref = str(ref)
    if ref.startswith("http://") or ref.startswith("https://"):
        return ref
    # Legacy fallback: bare content hash -> CDN url.
    return func_rbx_other.get_cdn_url(ref)


def ref_token(ref):
    """The token an MTL/OBJ file uses to reference this asset: the last path
    segment (the CDN hash), stripped of any query string."""
    ref = str(ref).split("?")[0].rstrip("/")
    return ref.split("/")[-1]


#############################################
##### Download helper ########################
#############################################

def download_bytes(url, itm_type):
    """Download raw bytes from a CDN url. Returns (data, error)."""
    try:
        r = requests.get(url)
    except Exception as e:
        return None, f"Error downloading {itm_type}: {e}"
    if r.status_code == 200:
        return r.content, None
    return None, f"{r.status_code}: Error downloading {itm_type} file"


#############################################
##### Blender helpers (avatar specific) ######
#############################################

def _avatar_reposition():
    """Center on cursor and rotate 180deg on Z so the avatar faces the viewer
    (matches the legacy avatar import orientation)."""
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
    bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL',
                             orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                             orient_matrix_type='GLOBAL')


def _avatar_remove_doubles():
    """Merge doubles and set smooth shading (matches legacy avatar import)."""
    if bpy.context.mode == 'OBJECT':
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
    elif bpy.context.mode == 'EDIT_MESH':
        bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.customdata_custom_splitnormals_clear()
    if float(glob_vars.bldr_fdr) < 4.1:
        bpy.context.object.data.use_auto_smooth = False
    else:
        bpy.ops.object.shade_flat()
    bpy.ops.object.shade_smooth()


def _separate_by_material(context):
    """Separate the active mesh into one object per material. Returns error str."""
    obj = context.active_object
    if obj is None or obj.type != 'MESH':
        return "No mesh object to separate."
    if not obj.material_slots:
        return "No materials assigned to avatar object."

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='MATERIAL')
    bpy.ops.object.editmode_toggle()

    base_name = obj.name
    i = 1
    for selected in list(context.selected_objects):
        if selected.name == obj.name:
            obj.select_set(False)
        else:
            context.view_layer.objects.active = selected
            selected.name = f"{base_name}_Part_{i}"
            i += 1
    bpy.ops.object.select_all(action='DESELECT')
    return None


#############################################
##### Main import routine ####################
#############################################

def import_user_avatar(context, rbx_user_id, user_name_clean, headers, separate=False):
    """Download and import the user's avatar. Returns error string or None."""
    from . import func_rbx_other, func_blndr_api

    # 1. Avatar folder
    char_path = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder,
                             glob_vars.rbx_imported_char_fldr, user_name_clean)
    try:
        os.makedirs(char_path, exist_ok=True)
    except Exception as e:
        return f"Error creating avatar folder: {e}"

    # 2. Metadata url (authorized) -> 3. metadata json
    meta_url, error = get_avatar_meta_url(rbx_user_id, headers)
    if error:
        return error
    meta, error = get_avatar_meta(meta_url, headers)
    if error:
        return error

    obj_ref, mtl_ref, _tex_refs = classify_avatar_refs(meta)
    if not obj_ref or not mtl_ref:
        return f"Unexpected avatar data (keys: {list(meta.keys())})"
    dprint("obj_ref:", obj_ref, "| mtl_ref:", mtl_ref)

    obj_file = os.path.join(char_path, user_name_clean + ".obj")
    mtl_file = os.path.join(char_path, user_name_clean + ".mtl")

    # 4. Download OBJ + MTL. The CDN serves them gzip-encoded but sets
    #    Content-Encoding: gzip, so requests hands back the decompressed text.
    obj_data, error = download_bytes(resolve_ref_url(obj_ref), "OBJ")
    if error:
        return error
    mtl_data, error = download_bytes(resolve_ref_url(mtl_ref), "MTL")
    if error:
        return error

    # 5. Rewrite MTL: download every referenced texture and repoint the map_*
    #    lines at the local files. The MTL references each texture by a full
    #    signed CDN URL (whose token differs from meta["textures"]), so we parse
    #    the MTL directly rather than string-matching hashes.
    mtl_text = mtl_data.decode("utf-8", "replace")
    mtl_text, error = _rewrite_mtl_download_textures(mtl_text, char_path, user_name_clean)
    if error:
        return error
    error = func_rbx_other.save_to_file(mtl_file, mtl_text.encode("utf-8"))
    if error:
        return error

    # 6. Save OBJ, ensuring it references our MTL (Roblox's OBJ ships without a
    #    mtllib line, so the importer would otherwise skip materials entirely).
    obj_text = obj_data.decode("utf-8", "replace")
    obj_text = _ensure_obj_mtllib(obj_text, user_name_clean + ".mtl")
    error = func_rbx_other.save_to_file(obj_file, obj_text.encode("utf-8"))
    if error:
        return error

    # 7. Import + fix transparency + reposition + remove doubles
    try:
        func_blndr_api.blender_api_import_obj(obj_file)
        func_blndr_api.blender_api_transparent_textures()
        _avatar_reposition()
        _avatar_remove_doubles()
    except Exception as e:
        return f"Error importing avatar into Blender: {e}"

    # 8. Optional: separate by material
    if separate:
        try:
            sep_err = _separate_by_material(context)
            if sep_err:
                return sep_err
        except Exception as e:
            return f"Error separating by material: {e}"

    return None


# MTL directives whose argument is a texture reference (a full signed CDN URL).
_MTL_MAP_RE = re.compile(r'^\s*(map_\w+|bump|disp|decal|refl)\s+(.+)$', re.IGNORECASE)


def _rewrite_mtl_download_textures(mtl_text, char_path, name_clean):
    """Rewrite MTL `map_*` lines to reference locally-downloaded texture files.

    Each unique texture (keyed by its stable CDN path token) is downloaded once
    and saved as `<name>_tex-N.png`; the map line is repointed at that local
    file. Transparency (`map_d`) is dropped and ambient (`map_Ka`) is commented
    out, matching the legacy avatar import behaviour. Returns (new_text, error).
    """
    from . import func_rbx_other

    token_to_file = {}
    counter = [0]

    def local_file_for(url_arg):
        token = ref_token(url_arg)
        if token in token_to_file:
            return token_to_file[token], None
        data, error = download_bytes(resolve_ref_url(url_arg), f"Texture {counter[0]}")
        if error:
            return None, error
        fname = f"{name_clean}_tex-{counter[0]}.png"
        err = func_rbx_other.save_to_file(os.path.join(char_path, fname), data)
        if err:
            return None, err
        token_to_file[token] = fname
        counter[0] += 1
        return fname, None

    out_lines = []
    for line in mtl_text.splitlines():
        m = _MTL_MAP_RE.match(line)
        if not m:
            out_lines.append(line)
            continue
        keyword, arg = m.group(1), m.group(2).strip()
        kw = keyword.lower()
        if kw == "map_d":
            continue  # drop transparency map (legacy behaviour)
        fname, error = local_file_for(arg)
        if error:
            return None, error
        if kw == "map_ka":
            out_lines.append(f"# {keyword} {fname}")  # comment out ambient map
        else:
            out_lines.append(f"{keyword} {fname}")

    return "\n".join(out_lines) + "\n", None


def _ensure_obj_mtllib(obj_text, mtl_name):
    """Return OBJ text guaranteed to reference `mtl_name` via a single mtllib
    directive. Roblox's avatar OBJ ships without one, so we insert it at the top;
    if one is present we normalise it to our saved MTL filename."""
    lines = obj_text.splitlines()
    for idx, line in enumerate(lines):
        if line.lstrip().lower().startswith("mtllib"):
            lines[idx] = f"mtllib {mtl_name}"
            return "\n".join(lines) + "\n"
    lines.insert(0, f"mtllib {mtl_name}")
    return "\n".join(lines) + "\n"


#############################################
##### Operator ###############################
#############################################

class RBX_OT_import_user_avatar(bpy.types.Operator):
    """Import your own Roblox avatar (3D) into the scene"""
    bl_idname = "object.rbx_import_user_avatar"
    bl_label = "Import My Avatar"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        glob_vars.rbx_imp_error = None

        from . import func_rbx_other, func_blndr_api
        importlib.reload(func_rbx_other)
        importlib.reload(func_blndr_api)

        rbx_prefs = context.scene.rbx_prefs

        # Renew OAuth token -> Bearer headers
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        try:
            access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
        except Exception as e:
            msg = f"Auth error: {e}"
            glob_vars.rbx_imp_error = msg
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}
        headers = {"Authorization": f"Bearer {access_token}"}

        info = glob_vars.get_login_info()
        rbx_user_id = info.get("user_id")
        rbx_user_name = info.get("user_name")
        if not rbx_user_id:
            msg = "Not logged in."
            glob_vars.rbx_imp_error = msg
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}

        user_name_clean = func_rbx_other.replace_restricted_char(rbx_user_name) or f"user_{rbx_user_id}"
        glob_vars.rbx_user_name_clean = user_name_clean

        error = import_user_avatar(
            context, rbx_user_id, user_name_clean, headers,
            separate=getattr(rbx_prefs, "rbx_avatar_separate_by_material", False),
        )
        if error:
            glob_vars.rbx_imp_error = error
            self.report({'ERROR'}, error)
            return {'CANCELLED'}

        self.report({'INFO'}, f"Avatar '{rbx_user_name}' imported")
        return {'FINISHED'}
