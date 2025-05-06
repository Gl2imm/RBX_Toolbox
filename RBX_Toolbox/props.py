import bpy
import requests
import glob_vars
import xml.etree.ElementTree as ET



def has_internet_connection(test_url="https://github.com", timeout=5):
    try:
        requests.get(test_url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False
    

def get_name_and_ver(url): 
    try:
        full_xml = requests.get(url, allow_redirects=True).text
    except:
        print(f"ERROR getting info from: {url}")
        return None
    else:
        # Parse the XML data
        namespace = {"atom": "http://www.w3.org/2005/Atom"}  # Namespace mapping
        root = ET.fromstring(full_xml)
        # Get the latest entry (first one)
        latest_entry = root.find("atom:entry", namespace)
        # Extract title
        latest_title = latest_entry.find("atom:title", namespace).text
        # Extract tag from the link URL
        link = latest_entry.find("atom:link", namespace).attrib["href"]
        latest_tag = link.split("/")[-1]  # Extract last part of URL
    return latest_title, latest_tag



class PROPERTIES_RBX(bpy.types.PropertyGroup):

    name : bpy.props.StringProperty(name= "ver", default="", maxlen=40) #Not in use, key in data      # type: ignore        



    ##### HDRI & SKY #####
    rbx_hdri_enum : bpy.props.EnumProperty(
        name = "HDRI",
        description = "Set HDRI",
        default='OP1',
        items = [('OP1', "Blender Default", ""),
                 ('OP2', "City", ""),
                 ('OP3', "Courtyard", ""),
                 ('OP4', "Forest", ""),
                 ('OP5', "Interior", ""),
                 ('OP6', "Night", ""),
                 ('OP7', "Studio", ""),
                 ('OP8', "Sunrise", ""),
                 ('OP9', "Sunset", "")   
                ]
        )  # type: ignore
        
    rbx_sky_enum : bpy.props.EnumProperty(
        name = "Sky",
        description = "Set Sky",
        default='OP1',
        items = [('OP1', "Sky 1", ""),
                 ('OP2', "Sky 2", ""),
                 ('OP3', "Sky 3", "") 
                ]
        )  # type: ignore







    ##### BOUNDS #####
    ## UGC Boundaries: Hide Dummy ##
    rbx_bnds_hide : bpy.props.BoolProperty(
    name="Hide Dummy",
    description="Hide Dummy property",
    default = True
    )  # type: ignore
    
    ### UGC Boundaries ###    
    rbx_bnds_enum : bpy.props.EnumProperty(
        name = "Boundaries",
        description = "Boundaries spawn",
        default='OP1',
        items = [('OP1', "Hat", ""),
                 ('OP2', "Hair", ""),
                 ('OP3', "Face Center", ""),
                 ('OP4', "Face Front", ""),
                 ('OP5', "Neck", ""),
                 ('OP6', "Front", ""),
                 ('OP7', "Back", ""),
                 ('OP8', "Shoulder Right", ""),
                 ('OP9', "Shoulder Left", ""),
                 ('OP10', "Shoulder Neck", ""),
                 ('OP11', "Waist Back", ""),
                 ('OP12', "Waist Front", ""),
                 ('OP13', "Waist Center", "")
                ]
        )  # type: ignore
        
    ### Avatars Boundaries ###    
    rbx_bnds_avatar_enum : bpy.props.EnumProperty(
        name = "Avatars Boundaries",
        description = "Boundaries spawn",
        default='OP1',
        items = [('OP1', "Classic Avatars", ""),
                 ('OP2', "Rthro Avatars", ""),
                 ('OP3', "Slender Avatars", ""),
                 ('OP4', "Minimum Sizes", "")
                ]
        )     # type: ignore

    ### LC Boundaries ###    
    rbx_bnds_lc_enum : bpy.props.EnumProperty(
        name = "LC Boundaries",
        description = "Boundaries spawn",
        default='OP1',
        items = [('OP1', "LC Max Sizes", "")
                ]
        )  # type: ignore





    ##### DUMMIES #####
    rbx_dum_enum : bpy.props.EnumProperty(
        name = "Dummies",
        description = "Dummies",
        default='OP1',
        items = [('OP1', "R15: Blocky", ""),
                 ('OP2', "R15: Boy", ""),
                 ('OP3', "R15: Girl", ""),
                 ('OP4', "R15: Woman", ""),
                 ('OP5', "4.0: Lin", ""),
                 ('OP6', "4.0: Oakley", ""),
                 ('OP7', "3.0: Man", ""),
                 ('OP8', "3.0: Woman", ""),
                 ('OP9', "2.0: Robloxian 2.0", ""),
                 ('OP10', "Neoclassic: Skyler", ""),
                 ('OP11', "R6: Blocky", ""),
                 ('OP12', "Anime", "")
                ]
        )  # type: ignore

    ### WEAR R6 RIG ###
    ## Import Face ##
    rbx_face: bpy.props.StringProperty( 
        name="Accessory Face",
        description="Accessory Face ID to import",
        default="7987180607",
        maxlen=100,
    ) # type: ignore
    
    ## Import Shirt ##
    rbx_shirt: bpy.props.StringProperty(
        name="Accessory Shirt",
        description="Accessory Shirt ID to import",
        default="4047884046",
        maxlen=100,
    ) # type: ignore

    ## Import Pants ##
    rbx_pants: bpy.props.StringProperty(
        name="Accessory Pants",
        description="Accessory Pants ID to import",
        default="398635338",
        maxlen=100,
    )  # type: ignore





    ##### HAIRS #####
    ### Dummies Heads ###    
    rbx_dum_hd_enum : bpy.props.EnumProperty(
        name = "Dummies Heads",
        description = "Dummies Heads",
        default='OP1',
        items = [('OP1', "Classic Head", ""),
                 ('OP2', "Woman Head", ""),
                 ('OP3', "Woman Head v2", ""),
                 ('OP4', "Man Head", ""),
                 ('OP5', "R6 Head", "")
                ]
        )   # type: ignore
    




    ##### LC #####
    ### Layered Cloth Dummies ###    
    rbx_lc_dum_enum : bpy.props.EnumProperty(
        name = "LC Dummies",
        description = "Layered Cloth Dummies",
        default='OP1',
        items = [('OP1', "Default Mannequin", ""),
                 ('OP2', "Default Mannequin (separated)", ""),
                 ('OP3', "Roblox Boy", ""),
                 ('OP4', "Roblox Girl", ""),
                 ('OP5', "Roblox Man", ""),
                 ('OP6', "Roblox Woman", ""),
                 ('OP7', "Classic Male", ""),
                 ('OP8', "Classic Female", ""),
                 ('OP9', "Roblox Blocky", ""),
                 ('OP10', "Roblox Korblox", ""),
                 ('OP11', "Roblox Deathwalker", "")
                ]
        ) # type: ignore
        
    ### Layered Cloth Samples ###    
    rbx_lc_spl_enum : bpy.props.EnumProperty(
        name = "LC Samples",
        description = "Layered Cloth Samples",
        default='OP1',
        items = [('OP1', "Hair: Female Hair", ""),
                 ('OP2', "Jacket: Hoodie", ""),
                 ('OP3', "Pants: Cargo Pants", ""),
                 ('OP4', "Shoe: Skate", ""),
                 ('OP5', "Skirt: Tennis", "")
                ]
        ) # type: ignore
        
    ### Layered Cloth Animation Dummies ###    
    rbx_lc_dum_anim_enum : bpy.props.EnumProperty(
        name = "LC Animation Dummies",
        description = "Layered Cloth Dummies",
        default='OP1',
        items = [('OP1', "Roblox Woman", ""),
                 ('OP2', "Roblox Blocky", "")
                ]
        ) # type: ignore
    ### Layered Cloth Animations ###    
    rbx_lc_anim_enum : bpy.props.EnumProperty(
        name = "LC Animations",
        description = "Layered Cloth Animations",
        default='OP1',
        items = [('OP1', "No Animation", ""),
                 ('OP2', "Chapa-Giratoria", ""),
                 ('OP3', "Hokey Pokey", ""),
                 ('OP4', "Rumba Dancing", "")
                ]
        ) # type: ignore                     





    ##### AVATARS #####   
    rbx_ava_enum : bpy.props.EnumProperty(
        name = "Avatars",
        description = "Avatars",
        default='OP1',
        items = [('OP1', "Blocky", ""),
                 ('OP2', "Round Male", ""),
                 ('OP3', "Anime", "")
                ]
        ) # type: ignore
    



    ##### ARMATURES #####    
    rbx_arma_enum : bpy.props.EnumProperty(
        name = "Armatures",
        description = "Armatures",
        default='OP1',
        items = [('OP1', "R15: Blocky Armature", ""),
                 ('OP2', "R15: Boy Armature", ""),
                 ('OP3', "R15: Girl Armature", ""),
                 ('OP4', "R15: Woman Armature", ""),
                 ('OP5', "Rthro: Boy Armature", ""),
                 ('OP6', "Rthro: Girl Armature", ""),
                 ('OP7', "Rthro: Normal Armature", ""),
                ]
        ) # type: ignore




    ##### OTHER FUNCTIONS ##### 
    ### NORMALS ###    
    rbx_face_enum : bpy.props.EnumProperty(
        name = "Faces",
        description = "Recalculate Faces",
        default='OP1',
        items = [('OP1', "Selected Only", ""),
                 ('OP2', "All Faces", "")
                ]
        ) # type: ignore
    
        ## Other Functions: Origin to Geometry ##
    rbx_of_orig : bpy.props.BoolProperty(
    name="Origin to Geometry",
    description="Origin to Geometry property",
    default = True
    ) # type: ignore
    
    ## Other Functions: Apply all Transforms ##
    rbx_of_trsf : bpy.props.BoolProperty(
    name="Apply all Transforms",
    description="Apply all Transforms property",
    default = True
    )  # type: ignore





    ####   Check for update addon  ####
    '''rbx_url = 'https://github.com/Gl2imm/RBX_Toolbox/releases.atom'
    try:
        full_text = requests.get(rbx_url, allow_redirects=True).text
    except:
        pass
    else:
        split_1 = full_text.split('536450223/')[1]
        glob_vars.lts_ver = split_1.split('</id>')[0]'''

    if has_internet_connection():
        rbx_url = 'https://github.com/Gl2imm/RBX_Toolbox/releases.atom'
        rbx_result = get_name_and_ver(rbx_url)
        if rbx_result is not None:
            rbx_latest_title, rbx_latest_tag = rbx_result
            #latest_tag = rbx_latest_tag.split("v.")[1]
            if glob_vars.update_test == True:
                glob_vars.lts_ver = "v.999.0"
                glob_vars.lts_title = rbx_latest_title
            else:
                glob_vars.lts_ver = rbx_latest_tag
                glob_vars.lts_title = rbx_latest_title
    else:
        print("No internet connection. Skipping RBX Toolbox update check.")




    ####   Check for update AEPBR  ####
    if has_internet_connection():
        aepbr_url = 'https://github.com/paribeshere/AEPBR/releases.atom'
        result = get_name_and_ver(aepbr_url)
        if result is not None:
            latest_title, latest_tag = result
            latest_tag = latest_tag.split("v.")[1]
            glob_vars.aepbr_lts_ver = latest_tag
            glob_vars.aepbr_lts_title = latest_title
    else:
        print("No internet connection. Skipping AEPBR update check.")




    ## not in use just show disabled bones in LC dummies##
    rbx_bn_disabled : bpy.props.BoolProperty(
    name="Bones",
    description="Shows Disabled Bones",
    default = False
    ) # type: ignore
        
    ## not in use just for display in test mode ##
    recolor_folder: bpy.props.StringProperty(name="Folder",
                                        description="Select Recolor textures folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH") # type: ignore
    