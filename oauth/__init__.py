# Copyright © 2023 Roblox Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# SPDX-License-Identifier: MIT

import asyncio
import sys
import shutil
import os
import stat
import time
from pathlib import Path
from .lib.oauth2_client import RbxOAuth2Client
from .lib import oauth2_client
# Get the directory path of the current script
add_on_directory = Path(__file__).parent

def _force_remove(func, path, _exc):
    # Handle read-only files/dirs on Windows by making them writable first
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


# Everything below runs before sys.path is updated, so nothing in either dependency
# folder has been imported yet and no file in them is locked by this session.
_dependencies_directory = add_on_directory / "dependencies_public"
_staging_directory = add_on_directory / "dependencies_public_new"
# The old folder is renamed to this instead of being deleted up front, so a swap that
# fails halfway still leaves a working dependency folder to fall back on.
_retired_directory = add_on_directory / "dependencies_public_old"
_pending_wipe = add_on_directory / "_pending_dep_wipe"


def _rename_with_retry(source, destination, attempts=6):
    """os.rename with backoff. Returns None on success, else the last OSError.

    A pip install writes ~2000 files, and for a while afterwards Google Drive, the
    indexer and Defender still hold handles inside that tree. Windows refuses to rename
    a directory while files under it are open ([WinError 5] Access is denied), and the
    same applies to a folder that was just deleted but is still pending close. The locks
    are short-lived, so spaced-out retries clear them.
    """
    delay = 0.1
    last_exception = None
    for attempt in range(attempts):
        try:
            os.rename(str(source), str(destination))
            return None
        except OSError as exception:
            last_exception = exception
            if attempt < attempts - 1:
                time.sleep(delay)
                delay *= 2
    return last_exception


# Leftovers from a swap that was interrupted by a crash or a forced quit. If the swap
# died after the old folder was moved aside, it is the only copy left — restore it.
if _retired_directory.is_dir() and not _dependencies_directory.exists():
    _rename_with_retry(_retired_directory, _dependencies_directory)
if _retired_directory.is_dir() and _dependencies_directory.is_dir():
    shutil.rmtree(str(_retired_directory), onerror=_force_remove)

if _staging_directory.is_dir():
    # Promote a dependency install staged by a previous session. Installing writes to
    # dependencies_public_new because pip cannot replace modules the running Blender has
    # imported; the swap happens here instead, where nothing is loaded yet.
    _retired = False
    _error = None
    if _dependencies_directory.exists():
        _error = _rename_with_retry(_dependencies_directory, _retired_directory)
        _retired = _error is None
    if _error is None:
        _error = _rename_with_retry(_staging_directory, _dependencies_directory)
        if _error is not None and _retired:
            # Put the old folder back: broken-but-old dependencies still beat none at all.
            _rename_with_retry(_retired_directory, _dependencies_directory)

    if _error is None:
        print("[RBX Toolbox] Installed dependencies are now active.")
        try:
            _pending_wipe.unlink()
        except Exception:
            pass
    else:
        # The staged folder is left untouched, so the next start simply tries again.
        print(
            f"[RBX Toolbox] Could not activate the installed dependencies yet: {_error}\n"
            "[RBX Toolbox] Something is still holding those files open (cloud sync or "
            "antivirus). They will be activated the next time Blender starts."
        )

    # Only drop the old copy once a folder is actually in place — if the rollback above
    # failed too, this is the last set of dependencies the add-on has.
    if _retired_directory.is_dir() and _dependencies_directory.is_dir():
        shutil.rmtree(str(_retired_directory), onerror=_force_remove)
elif _pending_wipe.exists():
    # Wipe dependencies_public if a pending-wipe marker exists from a previous session.
    shutil.rmtree(str(_dependencies_directory), onerror=_force_remove)
    # Always remove the marker — even if some empty dirs remain, a fresh pip install
    # will work correctly and won't be blocked by leftover empty folders.
    try:
        _pending_wipe.unlink()
    except Exception:
        pass

# Append the dependencies directories to the path so we can access the bundled python modules
# If dependencies_public doesn't exist yet, the user is prompted to install them before using the plugin
sys.path.append(str(add_on_directory / "dependencies_private"))
sys.path.append(str(add_on_directory / "dependencies_public"))

if "bpy" in locals():
    # Imports have run before. Need to reload the imported modules
    import importlib

    if "event_loop" in locals():
        importlib.reload(event_loop) # type: ignore
    if "status_indicators" in locals():
        importlib.reload(status_indicators) # type: ignore
    if "roblox_properties" in locals():
        importlib.reload(roblox_properties) # type: ignore
    if "oauth2_login_operators" in locals():
        importlib.reload(oauth2_login_operators) # type: ignore
    if "RBX_OT_upload" in locals():
        importlib.reload(RBX_OT_upload) # type: ignore
    if "RBX_OT_upload_animation" in locals():
        importlib.reload(RBX_OT_upload_animation) # type: ignore
    if "RBX_OT_check_animation_emote" in locals():
        importlib.reload(RBX_OT_check_animation_emote) # type: ignore
    if "RbxOAuth2Client" in locals():
        importlib.reload(oauth2_client)
    if "get_selected_objects" in locals():
        importlib.reload(get_selected_objects) # type: ignore
    if "constants" in locals():
        importlib.reload(constants) # type: ignore
    if "creator_details" in locals():
        importlib.reload(creator_details) # type: ignore
    if "RBX_OT_install_dependencies" in locals():
        importlib.reload(RBX_OT_install_dependencies) # type: ignore

import bpy
from bpy.app.handlers import persistent
from bpy.props import (
    PointerProperty,
)

# bl_info = {
#     "name": "Upload to Roblox",
#     "author": "Roblox",
#     "description": "Uses Roblox's Open Cloud API to upload selected assets from Blender to Roblox",
#     "blender": (3, 2, 0),
#     "version": (1, 0, 3),
#     "location": "View3D",
#     "warning": "",
#     "category": "Import-Export",
# }



class RBX_PT_sidebar:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RBX Tools"



@persistent
def load_post(dummy):
    from .lib import event_loop

    event_loop.reset_timer_running()


def get_classes():
    from .lib import (
        event_loop,
        creator_details,
        oauth2_login_operators,
        roblox_properties,
    )
    from .lib.install_dependencies import RBX_OT_install_dependencies
    from .lib.upload_operator import RBX_OT_upload
    from .lib.upload_animation_operator import RBX_OT_upload_animation, RBX_OT_copy_to_clipboard
    from .lib.check_animation_operator import RBX_OT_check_animation_emote

    return (
        event_loop.RBX_OT_event_loop,
        RBX_OT_install_dependencies,
        creator_details.RbxCreatorData,
        oauth2_login_operators.RBX_OT_oauth2_login,
        oauth2_login_operators.RBX_OT_oauth2_cancel_login,
        oauth2_login_operators.RBX_OT_oauth2_logout,
        RBX_OT_upload,
        RBX_OT_upload_animation,
        RBX_OT_copy_to_clipboard,
        RBX_OT_check_animation_emote,
        roblox_properties.RbxStatusProperties,
        roblox_properties.RbxProperties,

    )


def register():
    for cls in get_classes():
        bpy.utils.register_class(cls)

    from .lib import roblox_properties

    bpy.types.WindowManager.rbx = PointerProperty(type=roblox_properties.RbxProperties)
    bpy.app.handlers.load_post.append(load_post)


def unregister():
    # We unregister in reverse order to ensure a class is not unregistered while
    # another still depends on it
    
    if bpy.app.handlers.load_post.count(load_post) > 0:
        bpy.app.handlers.load_post.remove(load_post)
    for cls in reversed(get_classes()):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.rbx
    
