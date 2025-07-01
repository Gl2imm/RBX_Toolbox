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
update_test = False # Set to True to test out update process without uploading new version to Github (nothing else need change)
rbx_update_test_down_link = "https://github.com/Gl2imm/RBX_Toolbox/releases/download/v.6.1/RBX_Toolbox_v.6.1.zip"
need_restart_blender = False

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



### RBX Import
rbx_import_main_folder = "RBX_Import"
rbx_imported_char_fldr = "Characters/"
rbx_imported_acc_fldr = "Accessories/"
rbx_supported_type = False
rbx_user_name = None
rbx_user_name_clean = None
rbx_char_error = None

rbx_asset_error = None
rbx_asset_name = None
rbx_asset_name_clean = None
rbx_asset_creator = None
rbx_asset_type = None
rbx_supported_type_category = None
rbx_asset_id = None
rbx_is_bundle = False
rbx_is_bundled_item = False




bn_selection = None
bn_error = None
msh_selection = None
msh_error = None
rbx_face_netw_error = None
rbx_shirt_netw_error = None
rbx_pants_netw_error = None
rbx_face_name = None
rbx_shirt_name = None
rbx_pants_name = None
rbx_face_filename = None
rbx_shirt_filename = None
rbx_pants_filename = None
cams = ['Camera_F','Camera_B','Camera_L','Camera_R']

# PIE Menu
addon_keymaps = {}






#https://create.roblox.com/docs/reference/engine/enums/AssetType
rbx_asset_types = {
    1 :'Image',
    2 :'T-Shirt',
    3 :'Audio',
    4 :'Mesh',
    5 :'Lua',
    6 :'None',
    7 :'None',
    8 :'Hat',
    9 :'Place',
    10 :'Model',
    11 :'Shirt',
    12 :'Pants',
    13 :'Decal',
    17 :'Head',
    18 :'Face',
    19 :'Gear',
    20 :'None',
    21 :'Badge',
    22 :'None',
    23 :'None',
    24 :'Animation',
    25 :'None',
    26 :'None',
    27 :'Torso',
    28 :'RightArm',
    29 :'LeftArm',
    30 :'LeftLeg',
    31 :'RightLeg',
    32 :'Package',
    33 :'None',
    34 :'GamePass',
    35 :'None',
    36 :'None',
    37 :'None',
    38 :'Plugin',
    39 :'None',
    40 :'MeshPart',
    41 :'HairAccessory',
    42 :'FaceAccessory',
    43 :'NeckAccessory',
    44 :'ShoulderAccessory',
    45 :'FrontAccessory',
    46 :'BackAccessory',
    47 :'WaistAccessory',
    48 :'ClimbAnimation',
    49 :'DeathAnimation',
    50 :'FallAnimation',
    51 :'IdleAnimation',
    52 :'JumpAnimation',
    53 :'RunAnimation',
    54 :'SwimAnimation',
    55 :'WalkAnimation',
    56 :'PoseAnimation',
    57 :'EarAccessory',
    58 :'EyeAccessory',
    59 :'None',
    60 :'None',
    61 :'EmoteAnimation',
    62 :'Video',
    64 :'TShirtAccessory',
    65 :'ShirtAccessory',
    66 :'PantsAccessory',
    67 :'JacketAccessory',
    68 :'SweaterAccessory',
    69 :'ShortsAccessory',
    70 :'LeftShoeAccessory',
    71 :'RightShoeAccessory',
    72 :'DressSkirtAccessory',
    73 :'FontFamily',
    74 :'None',
    75 :'None',
    76 :'EyebrowAccessory',
    77 :'EyelashAccessory',
    78 :'MoodAnimation',
    79 :'DynamicHead'
    }

rbx_bundle_types = {
    1 :'Bundle - Character',
    2 :'Bundle - Animations',
    3 :'Bundle - Shoes',
    4 :'Bundle - DynamicHead',
    5 :'Bundle - DynamicHeadAvatar'
    }

### Only when you getting direct assets or LC, not bundles
supported_assets = {
    "Gear"          : [19],
    "Accessory"     : [8,41,42,43,44,45,46,47],
    "Layered Cloth" : [64,65,66,67,68,69,70,71,72],
    "Dynamic Head"  : [79],
    "Body Parts"    : [27,28,29,30,31]
    }

supported_bundles = {
    "Shoes"          : [3],
    "Dynamic Head"   : [4],
    "Character"      : [1]
    }

### If the Asset is actually part of bundle (cannot get data for this item as asset)
part_of_bundle_items = [79,27,28,29,30,31]

### Only when you getting bundled item list of items
supported_bundled_items = {
    70 : 'Left_Shoe',
    71 : 'Right_Shoe',
    79 : 'Dynamic Head',
    27 : 'Torso',
    28 : 'RightArm',
    29 : 'LeftArm',
    30 : 'LeftLeg',
    31 : 'RightLeg',
    }

### Which sets need for the accessory
rbx_asset_sets_rbxm = {
    "Gear"          : ['Obj','texture'],
    "Accessory"     : ['Obj','texture'],
    "Dynamic Head"  : ['Obj','texture'],
    "Character"     : ['Obj','texture'],
    "Torso"         : ['Obj','texture'],
    "RightArm"      : ['Obj','texture'],
    "LeftArm"       : ['Obj','texture'],
    "LeftLeg"       : ['Obj','texture'],
    "RightLeg"      : ['Obj','texture'],
    "Layered Cloth" : ['Obj','base_color','Metallic','Roughness','Normal'],
    "Cages"         : ['inner_cage','outer_cage']
}

### If one of this set is missing - raise error
rbxm_raise_error_if_not_found = {
    "Gear"          : ['Obj','texture'],
    "Accessory"     : ['Obj','texture'],
    "Dynamic Head"  : ['Obj'],
    "Character"     : ['Obj','texture'],
    "Torso"         : ['Obj','texture'],
    "RightArm"      : ['Obj','texture'],
    "LeftArm"       : ['Obj','texture'],
    "LeftLeg"       : ['Obj','texture'],
    "RightLeg"      : ['Obj','texture'],
    "Layered Cloth" : ['Obj','base_color'],
    "Cages"         : ['inner_cage','outer_cage']
}




### Regex finding expressions
regex_values_norm = {
    "Obj"           : r"meshid.*?\W*(prop)",
    "texture"       : r"textureid.*?\W*(prop)",
    "base_color"    : r"colormap.*?\W*(prop)",
    "Metallic"      : r"metalnessmap.*?\W*(prop)",
    "Roughness"     : r"roughnessmap.*?\W*(prop)",
    "Normal"        : r"normalmap.*?\W*(prop)",
    "inner_cage"    : r"referencemeshid.*?\W*(prop)",
    "outer_cage"    : r"cagemeshid.*?\W*(prop)"
}

regex_values_rbx = {
    "Obj"           : r'meshid.*?prop',
    "texture"       : r'textureid.*?prop',
    "base_color"    : r"colormap.*?\W*(prop)",
    "Metallic"      : r"metalnessmap.*?\W*(prop)",
    "Roughness"     : r"roughnessmap.*?\W*(prop)",
    "Normal"        : r"normalmap.*?\W*(prop)",
    "inner_cage"    : r"referencemeshid.*?\W*(prop)",
    "outer_cage"    : r"cagemeshid.*?\W*(prop)"
}

regex_values_rbxmx = {
    "Obj"           : r'"meshid"><url>.*?\W*(<)',
    "texture"       : r'"textureid"><url>.*?\W*(<)',
    "base_color"    : r'"colormap"><url>.*?\W*(<)',
    "Metallic"      : r'"metalnessmap"><url>.*?\W*(<)',
    "Roughness"     : r'"roughnessmap"><url>.*?\W*(<)',
    "Normal"        : r'"normalmap"><url>.*?\W*(<)',
    "inner_cage"    : r'"referencemeshid"><url>.*?\W*(<)',
    "outer_cage"    : r'"cagemeshid"><url>.*?\W*(<)'
}



