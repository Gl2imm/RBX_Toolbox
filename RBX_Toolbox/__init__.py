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

import importlib
import sys
import os
import bpy
bl_info = {
    "name": "RBX Toolbox",
    "author": "Papa_Boss332",
    "version": (5, 3, 0),  # to update in menu_ui as well
    "blender": (3, 6, 0),
    "location": "Operator",
    "description": "Roblox UGC models toolbox",
    "warning": "Subscribe to NYTV :)",
    "category": "Object"
}


# Determine addon path based on context (Scripting tab or installed addon)
if __name__ == "__main__":
    # Running in Scripting tab: use .blend file directory
    addon_path = os.path.dirname(bpy.data.filepath)
    package_name = None  # No package context in Scripting tab
else:
    # Running as installed addon: use script directory and set package name
    addon_path = os.path.dirname(os.path.abspath(__file__))
    package_name = os.path.basename(addon_path)  # e.g., "RBX_Toolbox"

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
        full_module_name = f"{package_name}.{module_name}" if package_name else module_name
        if full_module_name in sys.modules:
            importlib.reload(sys.modules[full_module_name])

# Import modules dynamically
for module_name in all_modules_names:
    try:
        # Use package context for addons, plain module name for Scripting tab
        full_module_name = f"{package_name}.{module_name}" if package_name else module_name
        module = importlib.import_module(full_module_name)
        globals()[module_name.replace(".", "_")] = module
    except Exception as e:
        print(f"Error importing {module_name}: {e}")

# Import classes from connected modules
from bpy.props import BoolProperty
from bpy.types import Scene
if __name__ == "__main__":
    import oauth
    from functions.menu_ui import TOOLBOX_MENU
    from functions.menu_pie import RBX_MT_MENU4
    from functions.menu_pie import RBX_MT_MENU3
    from functions.menu_pie import RBX_MT_MENU2_3
    from functions.menu_pie import RBX_MT_MENU2_2
    from functions.menu_pie import RBX_MT_MENU2_1
    from functions.menu_pie import RBX_MT_MENU2
    from functions.menu_pie import RBX_MT_MENU
    from functions.funct_others import RBX_BUTTON_OF
    from functions.func_export import RBX_OPERATORS
    from functions.armature_buttons import BUTTON_BN
    from functions.avatar_buttons import RBX_BUTTON_AVA
    from functions.dmy_lc_buttons_anim import RBX_BUTTON_LC_ANIM
    from functions.dmy_lc_buttons import RBX_BUTTON_LC
    from functions.hair_buttons import BUTTON_HAIR
    from functions.wear_r6_rig import BUTTON_WEAR
    from functions.dmy_buttons import BUTTON_DMMY
    from functions.cam_staging import BUTTON_CMR
    from functions.hdri_sky import RBX_BUTTON_HDRI
    from functions.ugc_bounds import BUTTON_BNDS
    from update_aepbr import RBX_UPDATE_AEPBR
    from update import RBX_INSTALL_UPDATE
    from functions.url_handler import URL_HANDLER
    from props import PROPERTIES_RBX
    from prefs import RBXToolsPreferences
    import glob_vars
else:
    from . import oauth
    from .functions.menu_ui import TOOLBOX_MENU
    from .functions.menu_pie import RBX_MT_MENU4
    from .functions.menu_pie import RBX_MT_MENU3
    from .functions.menu_pie import RBX_MT_MENU2_3
    from .functions.menu_pie import RBX_MT_MENU2_2
    from .functions.menu_pie import RBX_MT_MENU2_1
    from .functions.menu_pie import RBX_MT_MENU2
    from .functions.menu_pie import RBX_MT_MENU
    from .functions.funct_others import RBX_BUTTON_OF
    from .functions.func_export import RBX_OPERATORS
    from .functions.armature_buttons import BUTTON_BN
    from .functions.avatar_buttons import RBX_BUTTON_AVA
    from .functions.dmy_lc_buttons_anim import RBX_BUTTON_LC_ANIM
    from .functions.dmy_lc_buttons import RBX_BUTTON_LC
    from .functions.hair_buttons import BUTTON_HAIR
    from .functions.wear_r6_rig import BUTTON_WEAR
    from .functions.dmy_buttons import BUTTON_DMMY
    from .functions.cam_staging import BUTTON_CMR
    from .functions.hdri_sky import RBX_BUTTON_HDRI
    from .functions.ugc_bounds import BUTTON_BNDS
    from update_aepbr import RBX_UPDATE_AEPBR
    from update import RBX_INSTALL_UPDATE
    from .functions.url_handler import URL_HANDLER
    from .props import PROPERTIES_RBX
    from .prefs import RBXToolsPreferences
    from . import glob_vars
    
# List all classes
classes = (
    RBXToolsPreferences,
    PROPERTIES_RBX,
    URL_HANDLER,
    RBX_INSTALL_UPDATE,
    RBX_UPDATE_AEPBR,
    BUTTON_BNDS,
    RBX_BUTTON_HDRI,
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
##########################################


def register():
    for c in classes:
        bpy.utils.register_class(c)
    try:
        oauth.register()
    except:
        oauth.unregister()
        oauth.register()

    bpy.types.Scene.rbx_prefs = bpy.props.PointerProperty(type=PROPERTIES_RBX)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_bounds = BoolProperty(default=False)
    Scene.subpanel_hdri = BoolProperty(default=False)
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
    for c in classes:
        bpy.utils.unregister_class(c)
    try:
        oauth.unregister()
    except:
        pass
    del bpy.types.Scene.rbx_prefs
    del Scene.subpanel_readme
    del Scene.subpanel_bounds
    del Scene.subpanel_hdri
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

### Only used in test mode, so it can clean up and reload addon without restarting Blender ###


def cleanse_modules():
    """search for your plugin modules in blender python sys.modules and remove them"""
    all_modules = sys.modules
    all_modules = dict(
        sorted(all_modules.items(), key=lambda x: x[0]))  # sort them

    for module_name in all_modules_names:
        for k, v in all_modules.items():
            if k.startswith(module_name):
                # print(k)
                try:
                    del sys.modules[k]
                except KeyError:
                    continue
    return None


if __name__ == "__main__":
    try:
        register()
    except ValueError:
        unregister()
        cleanse_modules()
        register()
