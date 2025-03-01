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

bl_info = {
    "name": "RBX Toolbox",
    "author": "Papa_Boss332",
    "version": (5, 0, 0),   #to update in menu_ui as well
    "blender": (3, 6, 0),
    "location": "Operator",
    "description": "Roblox UGC models toolbox",
    "warning": "Subscribe to NYTV :)",
    "category": "Object" 
}

import bpy
import os
import sys
import importlib

### Auto switch addon from test mode to live mode ###
### Addon folder name should be same with blend file name ###
if __name__ == "__main__": #running in test mode
    #Get filename and use it as folder name of addon during tests
    file_path = os.path.dirname(os.path.abspath(__file__))
    filename_full = os.path.basename(file_path)
    filename_strip = filename_full.split(".")[0]
    blend_file_path = os.path.dirname(bpy.data.filepath)
    addon_path = os.path.join(blend_file_path,filename_strip)
else:
    addon_path = os.path.dirname(os.path.abspath(__file__))


if addon_path not in sys.path:
    sys.path.append(addon_path)


all_modules_names = ["glob_vars",
                     "prefs",
                     "props",
                     "update",
                     "update_aepbr",
                     "url_handler",
                     "hdri_sky",
                     "ugc_bounds",
                     "cam_staging",
                     "dmy_buttons",
                     "wear_r6_rig",
                     "hair_buttons",
                     "dmy_lc_buttons",
                     "dmy_lc_buttons_anim",
                     "avatar_buttons",
                     "armature_buttons",
                     "func_export",
                     "funct_others",
                     "menu_pie",
                     "menu_ui"
                     ]


# When bpy is already in local, we know this is not the initial import...
if "bpy" in locals():
    # ...so we need to reload our submodule(s) using importlib
    for module_name in all_modules_names:
        if module_name in locals():
            module = importlib.import_module(module_name)
            importlib.reload(module)

### Import modules
if __name__ == "__main__":  # In test mode
    for module_name in all_modules_names:
        if module_name == "glob_vars":    #needed to share addon keymap
            import glob_vars
        else:
            globals()[module_name] = __import__(module_name)
else:  # Actual live addon
    for module_name in all_modules_names:
        if module_name == "glob_vars":
            from . import glob_vars
        else:
            globals()[module_name] = __import__(f".{module_name}", fromlist=[module_name])
            #globals()[module_name] = importlib.import_module(f".{module_name}", package=__name__)





### Import classes from connected modules
from prefs import RBXToolsPreferences
from props import PROPERTIES_RBX
from url_handler import URL_HANDLER
from update import RBX_INSTALL_UPDATE
from update_aepbr import RBX_UPDATE_AEPBR
from ugc_bounds import BUTTON_BNDS
from hdri_sky import RBX_BUTTON_HDRI
from cam_staging import BUTTON_CMR
from dmy_buttons import BUTTON_DMMY
from wear_r6_rig import BUTTON_WEAR
from hair_buttons import BUTTON_HAIR
from dmy_lc_buttons import RBX_BUTTON_LC
from dmy_lc_buttons_anim import RBX_BUTTON_LC_ANIM
from avatar_buttons import RBX_BUTTON_AVA
from armature_buttons import BUTTON_BN
from func_export import RBX_OPERATORS
from funct_others import RBX_BUTTON_OF
from menu_pie import RBX_MT_MENU
from menu_pie import RBX_MT_MENU2
from menu_pie import RBX_MT_MENU2_1
from menu_pie import RBX_MT_MENU2_2
from menu_pie import RBX_MT_MENU2_3
from menu_pie import RBX_MT_MENU3
from menu_pie import RBX_MT_MENU4
from menu_ui import TOOLBOX_MENU


### List all classes
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




from bpy.types import (Scene)
from bpy.props import (BoolProperty)
import bpy.utils.previews






             
    #CLASS REGISTER 
##########################################
def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.rbx_prefs = bpy.props.PointerProperty(type= PROPERTIES_RBX)
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
    all_modules = dict(sorted(all_modules.items(),key= lambda x:x[0])) #sort them
    
    for module_name in all_modules_names:
        for k,v in all_modules.items():
            if k.startswith(module_name):
                #print(k)
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