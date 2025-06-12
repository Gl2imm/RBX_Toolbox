import json
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
lts_title = None


## Tests
update_test = False # Set to True to test out update process without uploading new version to Github
rbx_update_test_down_link = "https://github.com/Gl2imm/RBX_Toolbox/releases/download/v.5.0/RBX_Toolbox_v.5.0.zip"


## Client Info ##
def get_addon_preferences():
    """Safely retrieves the addon's preferences object."""
    try:
        # The addon name must match the bl_idname in the preferences class
        return bpy.context.preferences.addons["RBX_Toolbox"].preferences
    except (AttributeError, KeyError):
        print("Warning: Could not access RBX_Toolbox preferences.")
        return None


def get_login_info():
    """
    Retrieves all login-related information directly from addon preferences.
    Returns a dictionary with the session data, or an empty dictionary if not logged in.
    """
    prefs = get_addon_preferences()
    if not prefs or not prefs.is_logged_in:
        return {}

    token_data = {}
    creators_data = []

    if prefs.saved_token_data_json:
        token_data = json.loads(prefs.saved_token_data_json)

    if prefs.saved_creators_json:
        creators_data = json.loads(prefs.saved_creators_json)

    # We can reconstruct a comprehensive info dictionary
    user_info = next(
        (creator for creator in creators_data if creator.get('type') == 'USER'), None)

    return {
        "is_logged_in": prefs.is_logged_in,
        "selected_creator": prefs.creator,
        "user_name": user_info.get('name') if user_info else None,
        "user_id": user_info.get('id') if user_info else None,
        "token_data": token_data,
        "creators": creators_data,
    }


def clear_login_info():
    """
    Clears all login-related information from addon preferences.
    This effectively logs the user out.
    """
    prefs = get_addon_preferences()
    if not prefs:
        return

    prefs.is_logged_in = False
    prefs.creator = ""
    prefs.saved_token_data_json = ""
    prefs.saved_creators_json = ""
    print("Login info cleared from preferences.")

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