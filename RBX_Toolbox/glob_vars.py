import os
import bpy
import platform


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


## Toolbox vars ##
lts_ver = None

## AEPBR vars ##
rbx_aepbr_fldr = "rig_aepbr"
rbx_aepbr_collection = "AEPBR (Main Preset)"
aepbr_lts_ver = None
aepbr_lts_title = None



### For Blender HDRI ### 
bldr_path = (os.path.dirname(bpy.app.binary_path))
bldr_ver = bpy.app.version_string.split('.')
bldr_fdr = bldr_ver[0] + '.' + bldr_ver[1]


print("**********************************************")
print("RBX Toolbox Log")
print("OS Platform: " + platform.system())
print("Blender ver:", bldr_ver)
print("Addon path:", addon_path)
print("**********************************************")


if platform.system() == 'Windows':
    fbs = '\\'
    rbx_blend_file = ("\\RBX_Templates.blend")
    ugc_bound_file = ("\\Bounds.blend")
    ap_node = ("\\NodeTree")
    ap_object = ("\\Object")
    ap_collection = ("\\Collection")
    ap_material = ("\\Material")
    ap_image = ("\\Image")
    ap_world = ("\\World")
    ap_action = ("\\Action")
    bldr_hdri_path = (bldr_path + "\\" + bldr_fdr + "\\datafiles\\studiolights\\world\\")
else:
    fbs = '/'   #forward/back slashes (MacOs)
    rbx_blend_file = ("/RBX_Templates.blend")
    ugc_bound_file = ("/Bounds.blend")
    ap_node = ("/NodeTree")
    ap_object = ("/Object")
    ap_collection = ("/Collection")
    ap_material = ("/Material")
    ap_image = ("/Image")
    ap_world = ("/World")
    ap_action = ("/Action")
    bldr_hdri_path = (bldr_path + "/" + bldr_fdr + "/datafiles/studiolights/world/")      
info = 'info' #info folder



cams = ['Camera_F','Camera_B','Camera_L','Camera_R']
bn_selection = None
bn_error = None
msh_selection = None
msh_error = None
rbx_username = None
rbx_accessory = None
rbx_asset_netw_error = None
rbx_char_netw_error = None
rbx_face_netw_error = None
rbx_shirt_netw_error = None
rbx_pants_netw_error = None
rbx_face_name = None
rbx_shirt_name = None
rbx_pants_name = None
rbx_face_filename = None
rbx_shirt_filename = None
rbx_pants_filename = None

# PIE Menu
addon_keymaps = {}