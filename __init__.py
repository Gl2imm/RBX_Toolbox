# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import importlib
import traceback

bl_info = {
    "name": "RBX Toolbox",
    "author": "Papa_Boss332",
    "version": (6, 1, 0),  # to update in menu_ui as well #clean public lib, pycache and imports folder
    "blender": (3, 6, 0),
    "location": "Operator",
    "description": "Roblox UGC models toolbox",
    "warning": "Subscribe to NYTV :)",
    "category": "Object"
}
# Addon path and package name for installed addon
addon_path = os.path.dirname(os.path.abspath(__file__))
package_name = os.path.basename(addon_path)

# Add addon path to sys.path if not already present
if addon_path not in sys.path:
    sys.path.append(addon_path)
    
all_modules_names = [
    "glob_vars",
    "prefs",
    "props",
    "update",
    "update_aepbr",
    "oauth",
    "functions.url_handler",
    "functions.hdri_sky",
    "functions.rbx_import",
    "functions.ugc_bounds",
    "functions.cam_staging",
    "functions.dmy_buttons",
    "functions.wear_r6_rig",
    "functions.hair_buttons",
    "functions.dmy_lc_buttons",
    "functions.dmy_lc_buttons_anim",
    "functions.avatar_buttons",
    "functions.armature_buttons",
    "functions.func_export",
    "functions.funct_others",
    "functions.menu_pie",
    "functions.menu_ui",
]

# When bpy is already in local, reload modules for iterative testing
if "bpy" in locals():
    for module_name in all_modules_names:
        full_module_name = f"{package_name}.{module_name}"
        if full_module_name in sys.modules:
            try:
                importlib.reload(sys.modules[full_module_name])
                print(f"Reloaded module: {full_module_name}")
            except ModuleNotFoundError:
                print(f"Module {full_module_name} not found for reloading.")
                
                
from . import glob_vars
from .prefs import RBXToolsPreferences
from .props import PROPERTIES_RBX
from .functions.url_handler import URL_HANDLER
from .update import RBX_INSTALL_UPDATE
from .update_aepbr import RBX_UPDATE_AEPBR
from .functions.ugc_bounds import BUTTON_BNDS
from .functions.rbx_import import OBJECT_OT_add_object
from .functions.hdri_sky import RBX_BUTTON_HDRI
from .functions.cam_staging import BUTTON_CMR
from .functions.dmy_buttons import BUTTON_DMMY
from .functions.wear_r6_rig import BUTTON_WEAR
from .functions.hair_buttons import BUTTON_HAIR
from .functions.dmy_lc_buttons import RBX_BUTTON_LC
from .functions.dmy_lc_buttons_anim import RBX_BUTTON_LC_ANIM
from .functions.avatar_buttons import RBX_BUTTON_AVA
from .functions.armature_buttons import BUTTON_BN
from .functions.func_export import RBX_OPERATORS
from .functions.funct_others import RBX_BUTTON_OF
from .functions.menu_pie import RBX_MT_MENU
from .functions.menu_pie import RBX_MT_MENU2
from .functions.menu_pie import RBX_MT_MENU2_1
from .functions.menu_pie import RBX_MT_MENU2_2
from .functions.menu_pie import RBX_MT_MENU2_3
from .functions.menu_pie import RBX_MT_MENU3
from .functions.menu_pie import RBX_MT_MENU4
from .functions.menu_ui import TOOLBOX_MENU
from . import oauth
from bpy.types import Scene
from bpy.props import BoolProperty
import bpy


# List all classes
classes = (
    RBXToolsPreferences,
    PROPERTIES_RBX,
    URL_HANDLER,
    RBX_INSTALL_UPDATE,
    RBX_UPDATE_AEPBR,
    BUTTON_BNDS,
    RBX_BUTTON_HDRI,
    OBJECT_OT_add_object,
    BUTTON_CMR,
    BUTTON_DMMY,
    BUTTON_WEAR,
    BUTTON_HAIR,
    RBX_BUTTON_LC,
    RBX_BUTTON_LC_ANIM,
    RBX_BUTTON_AVA,
    BUTTON_BN,
    RBX_OPERATORS,
    RBX_BUTTON_OF,
    RBX_MT_MENU,
    RBX_MT_MENU2,
    RBX_MT_MENU2_1,
    RBX_MT_MENU2_2,
    RBX_MT_MENU2_3,
    RBX_MT_MENU3,
    RBX_MT_MENU4,
    TOOLBOX_MENU
)

# CLASS REGISTER


def register():
    try:
        oauth.register()
    except Exception as e:
        traceback.print_exc()
        print(f"Error during OAuth registration: {e}")
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.rbx_prefs = bpy.props.PointerProperty(type=PROPERTIES_RBX)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_bounds = BoolProperty(default=False)
    Scene.subpanel_hdri = BoolProperty(default=False)
    Scene.subpanel_imp_char = BoolProperty(default=False)
    Scene.subpanel_supported = BoolProperty(default=False)
    Scene.subpanel_dummy = BoolProperty(default=False)
    Scene.subpanel_rigs = BoolProperty(default=False)
    Scene.subpanel_hair = BoolProperty(default=False)
    Scene.subpanel_lc = BoolProperty(default=False)
    Scene.subpanel_ava = BoolProperty(default=False)
    Scene.subpanel_cams = BoolProperty(default=False)
    Scene.subpanel_bn = BoolProperty(default=False)
    Scene.subpanel_bn_st1 = BoolProperty(default=False)
    Scene.subpanel_other = BoolProperty(default=False)
    Scene.subpanel_export = BoolProperty(default=False)
    Scene.subpanel_upload = BoolProperty(default=False)
    Scene.subpanel_pie = BoolProperty(default=False)
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'Y', 'PRESS',
                              ctrl=False, alt=False, shift=False, repeat=False)
    kmi.properties.name = 'RBX_MT_MENU'
    glob_vars.addon_keymaps['F85A6'] = (km, kmi)


def unregister():
    try:
        oauth.unregister()
    except Exception as e:
        traceback.print_exc()
        print(f"Error during OAuth unregistration: {e}")
        
    for c in classes:
        bpy.utils.unregister_class(c)
        
    del bpy.types.Scene.rbx_prefs
    del Scene.subpanel_readme
    del Scene.subpanel_bounds
    del Scene.subpanel_hdri
    del Scene.subpanel_imp_char
    del Scene.subpanel_supported
    del Scene.subpanel_dummy
    del Scene.subpanel_rigs
    del Scene.subpanel_hair
    del Scene.subpanel_lc
    del Scene.subpanel_ava
    del Scene.subpanel_cams
    del Scene.subpanel_bn
    del Scene.subpanel_bn_st1
    del Scene.subpanel_other
    del Scene.subpanel_export
    del Scene.subpanel_upload
    del Scene.subpanel_pie
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in glob_vars.addon_keymaps.values():
        km.keymap_items.remove(kmi)
    glob_vars.addon_keymaps.clear()
