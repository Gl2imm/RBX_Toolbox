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
from pathlib import Path
from .lib.oauth2_client import RbxOAuth2Client
from .lib import oauth2_client
# Get the directory path of the current script
add_on_directory = Path(__file__).parent

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

    return (
        event_loop.RBX_OT_event_loop,
        RBX_OT_install_dependencies,
        creator_details.RbxCreatorData,
        oauth2_login_operators.RBX_OT_oauth2_login,
        oauth2_login_operators.RBX_OT_oauth2_cancel_login,
        oauth2_login_operators.RBX_OT_oauth2_logout,
        RBX_OT_upload,
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
    
