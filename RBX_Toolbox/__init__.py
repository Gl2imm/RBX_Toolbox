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
    "author": "Random Blender Dude",
    "version": (4, 2),
    "blender": (2, 90, 0),
    "location": "Operator",
    "description": "Roblox UGC models toolbox",
    "warning": "Subscribe to NYTV :)",
    "category": "Object"
}


import bpy
import os
from bpy.types import (Scene,Panel,PropertyGroup)
from bpy.props import (BoolProperty,FloatProperty,StringProperty)
import requests
import subprocess
import webbrowser
import sys
import platform
import bmesh
import RBX_Toolbox

import zipfile
import io
import mathutils
from bpy.props import FloatVectorProperty
from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import urllib.request
import bpy.utils.previews
import asyncio
import re


## Toolbox vars ##
ver = "v.4.2"
disp_ver = ver
#disp_ver = "v.3.2 Beta-3" ### TO REMOVE IN 3.2
lts_ver = None


mode = 1 #0 - Test Mode; 1 - Live mode
wh =1   #0 - W; 1 - H


if mode == 0:
    if wh == 1:
        rbx_my_path = ("E:\\G-Drive\\Blender\\Roblox\\0. Addon\\RBX_Toolbox")
        rbx_ast_fldr = ("E:\\G-Drive\\Blender\\Roblox\\UGC\\UGC Files") 
    if wh == 0:
        rbx_my_path = ("D:\\Personal\\G-Drive\\Blender\\Roblox\\0. Addon\\RBX_Toolbox")
        rbx_ast_fldr = ("D:\\Personal\\G-Drive\\Blender\\Roblox\\UGC\\UGC Files")    
else:
    rbx_my_path = (os.path.dirname(os.path.realpath(__file__)))
    
addon_path = os.path.dirname(RBX_Toolbox.__file__)    


       
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
        
rbx_asset_name = None
rbx_asset_type_name = None
rbx_asset_creator = None
rbx_bkd_hair_img = None
rbx_anim_error = None

#https://create.roblox.com/docs/reference/engine/enums/AssetType
rbx_ast_type = {
    'BodyParts' : 'Bundle',
    '2':'T-Shirt',
    '8':'Hat',
    '11':'Shirt',
    '12':'Pants',
    '17':'Head',
    '18':'Face',
    '19':'Gear',
    '25':'Arms',
    '26':'Legs',
    '27':'Torso',
    '28':'RightArm',
    '29':'LeftArm',
    '30':'LeftLeg',
    '31':'RightLeg',
    '41':'HairAccessory',
    '42':'FaceAccessory',
    '43':'NeckAccessory',
    '44':'ShoulderAccessory',
    '45':'FrontAccessory',
    '46':'BackAccessory',
    '47':'WaistAccessory',
    '48':'ClimbAnimation',
    '49':'DeathAnimation',
    '50':'FallAnimation',
    '51':'IdleAnimation',
    '52':'JumpAnimation',
    '53':'RunAnimation',
    '54':'SwimAnimation',
    '55':'WalkAnimation',
    '56':'PoseAnimation',
    '61':'EmoteAnimation',
    '62':'Video',
    '64':'TShirtAccessory',
    '65':'ShirtAccessory',
    '66':'PantsAccessory',
    '67':'JacketAccessory',
    '68':'SweaterAccessory',
    '69':'ShortsAccessory',
    '70':'LeftShoeAccessory',
    '71':'RightShoeAccessory',
    '72':'DressSkirtAccessory',
    '73':'FontFamily',
    '76':'EyebrowAccessory',
    '77':'EyelashAccessory',
    '78':'MoodAnimation',
    '79':'DynamicHead'
    }
accessory = [8,41,42,43,44,45,46,47]
lc = [64,65,66,67,68,69,70,71,72]
#################

print("**********************************************")
print("OS Platform: " + platform.system())
print("**********************************************")    

'''
if sys.platform == 'win32':
    asyncio.get_event_loop().close()
    # On Windows, the default event loop is SelectorEventLoop, which does
    # not support subprocesses. ProactorEventLoop should be used instead.
    # Source: https://docs.python.org/3/library/asyncio-subprocess.html
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    loop.set_default_executor(executor)
    # loop.set_debug(True)      
   
    
try:
    import aiohttp
    import aiodns
except:
    
    def isWindows():
        return os.name == 'nt'

    def isMacOS():
        return os.name == 'posix' and platform.system() == "Darwin"

    def isLinux():
        return os.name == 'posix' and platform.system() == "Linux"

    def python_exec():
        if isWindows():
            return os.path.join(sys.prefix, 'bin', 'python.exe')
        elif isMacOS():
        
            try:
                # 2.92 and older
                path = bpy.app.binary_path_python
            except AttributeError:
                # 2.93 and later
                path = sys.executable
            return os.path.abspath(path)
        elif isLinux():
            return os.path.join(sys.prefix, 'sys.prefix/bin', 'python')
        else:
            print("sorry, still not implemented for ", os.name, " - ", platform.system)


    def installModule(packageName):
        try:
            subprocess.call([python_exe, "import ", packageName])
        except:
            python_exe = python_exec()
           # upgrade pip
            subprocess.call([python_exe, "-m", "ensurepip"])
            subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
           # install required packages
            subprocess.call([python_exe, "-m", "pip", "install", packageName])

    installModule("aiohttp")        
    installModule("aiodns")
''' 


               
    #OPERATOR         
######################################## 
class RBXToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
 
    rbx_asset_folder: bpy.props.StringProperty(name="Folder",
                                        description="Select Assets folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH")
                                                                                                            
    if mode == 0:
        rbx_asset_folder = rbx_ast_fldr
        
             
class PROPERTIES_RBX(bpy.types.PropertyGroup):
    
    name : bpy.props.StringProperty(name= "ver", default="", maxlen=40) #Not in use, key in data            

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
        )
        
    rbx_sky_enum : bpy.props.EnumProperty(
        name = "Sky",
        description = "Set Sky",
        default='OP1',
        items = [('OP1', "Sky 1", ""),
                 ('OP2', "Sky 2", ""),
                 ('OP3', "Sky 3", "") 
                ]
        ) 
    
    ### NORMALS ###    
    rbx_face_enum : bpy.props.EnumProperty(
        name = "Faces",
        description = "Recalculate Faces",
        default='OP1',
        items = [('OP1', "Selected Only", ""),
                 ('OP2', "All Faces", "")
                ]
        )
         

    ## UGC Boundaries: Hide Dummy ##
    rbx_bnds_hide : BoolProperty(
    name="Hide Dummy",
    description="Hide Dummy property",
    default = True
    )  
    
    
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
        )     

    ### Dummies ###    
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
                 ('OP11', "Rthro: Boy", ""),
                 ('OP12', "Rthro: Girl", ""),
                 ('OP13', "Rthro: Normal", ""),
                 ('OP14', "Rthro: Slender", ""),
                 ('OP15', "R6: Blocky", ""),
                ]
        ) 
 
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
        )        


    ### Armatures ###    
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
                 ('OP8', "Rthro: Slender Armature", ""),
                ]
        ) 
                
    ### Layered Cloth Dummies ###    
    rbx_lc_dum_enum : bpy.props.EnumProperty(
        name = "LC Dummies",
        description = "Layered Cloth Dummies",
        default='OP1',
        items = [('OP1', "Default Mannequin", ""),
                 ('OP2', "Roblox Boy", ""),
                 ('OP3', "Roblox Girl", ""),
                 ('OP4', "Roblox Man", ""),
                 ('OP5', "Roblox Woman", ""),
                 ('OP6', "Classic Male", ""),
                 ('OP7', "Classic Female", ""),
                 ('OP8', "Roblox Blocky", "")
                ]
        ) 
        
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
        ) 
        
    ### Layered Cloth Animation Dummies ###    
    rbx_lc_dum_anim_enum : bpy.props.EnumProperty(
        name = "LC Animation Dummies",
        description = "Layered Cloth Dummies",
        default='OP1',
        items = [('OP1', "Roblox Woman", ""),
                 ('OP2', "Roblox Blocky", "")
                ]
        )
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
        )                           
    
    ## Other Functions: Origin to Geometry ##
    rbx_of_orig : BoolProperty(
    name="Origin to Geometry",
    description="Origin to Geometry property",
    default = True
    )
    
    ## Other Functions: Apply all Transforms ##
    rbx_of_trsf : BoolProperty(
    name="Apply all Transforms",
    description="Apply all Transforms property",
    default = True
    ) 
    
    ## Import Character ##
    rbx_username: StringProperty(
        name="Username",
        description="Username of the character to import",
        default="papa_boss332",
        maxlen=100,
    )
    rbx_split : BoolProperty(
    name="Split accessories",
    description="Split accessories property",
    default = False
    )
    rbx_bundle : BoolProperty(
    name="Bundle accessory",
    description="Bundle accessory property",
    default = False
    )    
    
    
    ## Import Accessory ##
    rbx_accessory: StringProperty(
        name="Accessory",
        description="Accessory ID to import",
        default="11996887739",
        maxlen=100,
    ) 
    
    ## Import Face ##
    rbx_face: StringProperty(
        name="Accessory Face",
        description="Accessory Face ID to import",
        default="7987180607",
        maxlen=100,
    )
    
    ## Import Shirt ##
    rbx_shirt: StringProperty(
        name="Accessory Shirt",
        description="Accessory Shirt ID to import",
        default="4047884046",
        maxlen=100,
    ) 
    
    ## Import Pants ##
    rbx_pants: StringProperty(
        name="Accessory Pants",
        description="Accessory Pants ID to import",
        default="398635338",
        maxlen=100,
    )          

    ## not in use just show disabled bones in LC dummies##
    rbx_bn_disabled : BoolProperty(
    name="Bones",
    description="Shows Disabled Bones",
    default = False
    ) 
        
    ## not in use just for display in test mode ##
    recolor_folder: bpy.props.StringProperty(name="Folder",
                                        description="Select Recolor textures folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH")    
    
    ####   Check for update addon  ####
    rbx_url = 'https://github.com/Gl2imm/RBX_Toolbox/releases.atom'
    try:
        full_text = requests.get(rbx_url, allow_redirects=True).text
    except:
        pass
    else:
        global lts_ver
        split_1 = full_text.split('536450223/')[1]
        lts_ver = split_1.split('</id>')[0]                     


############   OPERATORS   ##############    
class RBX_OPERATORS(bpy.types.Operator):
    bl_label = "RBX_OPERATORS"
    bl_idname = "object.rbx_operators"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_operator : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_operator = (self.rbx_operator)
                    
        if rbx_operator == 'exp_fbx':
            if rbx_prefs.rbx_of_trsf == True:
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            if rbx_prefs.rbx_of_orig == True:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', use_selection=True, object_types={'MESH'}, global_scale=0.01, bake_anim=False)
            
        if rbx_operator == 'exp_fbx_lc':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', path_mode='COPY', embed_textures=True, use_selection=True, object_types={'ARMATURE', 'MESH', 'OTHER'}, add_leaf_bones=False, global_scale=0.01, bake_anim=False)            
            
        if rbx_operator == 'set_unit': 
            bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'
            bpy.context.scene.unit_settings.scale_length = 0.01


        return {'FINISHED'}

        
############   URL HANDLER OPERATOR   ##############    
class URL_HANDLER(bpy.types.Operator):
    bl_label = "URL_HANDLER"
    bl_idname = "object.url_handler"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_link : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        rbx_link = (self.rbx_link)
        rbx_guides = ['Credits and Instructions','Version_log','Guide_Armature']
                    
        if rbx_link == "update":
            webbrowser.open_new("https://github.com/Gl2imm/RBX_Toolbox/releases")
            
        if rbx_link == "discord":
            webbrowser.open_new("https://discord.gg/gFa4mY7")   
            
        if rbx_link == "mixamo":
            webbrowser.open_new("https://www.mixamo.com/") 
            
        if rbx_link == "rbx github":
            webbrowser.open_new("https://github.com/Roblox/avatar") 
        
        if rbx_link == "rbx nuke":
            webbrowser.open_new("https://www.youtube.com/watch?v=ggqvqwYQUSc")
                
        if rbx_link == "zeb twitter":
            webbrowser.open_new("https://twitter.com/Zeblyno")
            
        if rbx_link == "buy coffee":
            webbrowser.open_new("https://donate.stripe.com/fZe5op0W1fjg2nC002")                                                 

        for x in range(len(rbx_guides)):
            if rbx_link == rbx_guides[x]:
                texts_exist = bpy.data.texts.get(rbx_guides[x])
                if texts_exist != None:
                    bpy.context.area.ui_type = 'TEXT_EDITOR'
                    bpy.context.space_data.text = bpy.data.texts[rbx_guides[x]]
                else:
                    instructions = rbx_my_path + fbs + rbx_guides[x] + ".txt"
                    with open(instructions) as f:
                        text = f.read()
                    t = bpy.data.texts.new(rbx_guides[x])
                    t.write("To switch back to normal view switch from 'TEXT EDITOR' to '3D Viewport'. Or just press 'Shift+F5' \n \n \n") 
                    t.write(text)          
                    bpy.context.area.ui_type = 'TEXT_EDITOR'
                    bpy.context.space_data.text = bpy.data.texts[rbx_guides[x]]
                    bpy.context.space_data.show_word_wrap = True
                    bpy.ops.text.jump(line=1) 
        
        return {'FINISHED'}


class RBX_BUTTON_HDRI(bpy.types.Operator):
    bl_label = "RBX_BUTTON_HDRIFULL"
    bl_idname = "object.rbx_button_hdrifull"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_hdri : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        rbx_hdri = (self.rbx_hdri)
        
        if rbx_hdri == 'sky':
            if rbx_prefs.rbx_sky_enum == 'OP1':
                rbx_hdri_name = "Sky-1_(From_unsplash).jpg"                    
            if rbx_prefs.rbx_sky_enum == 'OP2':
                rbx_hdri_name = "Sky-2_(From_unsplash).jpg"                  
            if rbx_prefs.rbx_sky_enum == 'OP3':
                rbx_hdri_name = "Sky-3_(From_unsplash).jpg"
                            
            if bpy.data.objects.get("Sky Sphere") == None:
                bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, filename ='Sky Sphere')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects['Sky Sphere'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Sky Sphere']
            sky_img_path = rbx_my_path + fbs + 'img' + fbs + 'sky' + fbs + rbx_hdri_name
            sky_image = bpy.data.images.load(sky_img_path)
            bpy.data.objects['Sky Sphere'].active_material.node_tree.nodes['Image Texture'].image = sky_image 
            
            
        if rbx_hdri == 'hdri':
            if rbx_prefs.rbx_hdri_enum == 'OP1':
                rbx_hdri_name = "World"                    
            if rbx_prefs.rbx_hdri_enum == 'OP2':
                rbx_hdri_name = "City"                  
            if rbx_prefs.rbx_hdri_enum == 'OP3':
                rbx_hdri_name = "Courtyard"
            if rbx_prefs.rbx_hdri_enum == 'OP4':
                rbx_hdri_name = "Forest"
            if rbx_prefs.rbx_hdri_enum == 'OP5':
                rbx_hdri_name = "Interior"
            if rbx_prefs.rbx_hdri_enum == 'OP6':
                rbx_hdri_name = "Night"
            if rbx_prefs.rbx_hdri_enum == 'OP7':
                rbx_hdri_name = "Studio"
            if rbx_prefs.rbx_hdri_enum == 'OP8':
                rbx_hdri_name = "Sunrise"
            if rbx_prefs.rbx_hdri_enum == 'OP9':
                rbx_hdri_name = "Sunset"
                                                                                                                     

            if rbx_hdri_name == 'World':
                try:
                    rbx_hdri = bpy.data.worlds[rbx_hdri_name]
                except:
                    bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_world, filename =rbx_hdri_name)
                    rbx_hdri = bpy.data.worlds[rbx_hdri_name]
                scene.world = rbx_hdri
                print(rbx_hdri_name + " has been Appended and applied to the World")
            else:
                if bpy.context.scene.world != 'HDRI':
                    if 'HDRI' not in bpy.data.worlds:
                        bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_world, filename ='HDRI')
                    rbx_hdri = bpy.data.worlds['HDRI']
                    scene.world = rbx_hdri
                    hdri_img_path = bldr_hdri_path + rbx_hdri_name + '.exr'
                    hdri_image = bpy.data.images.load(hdri_img_path)
                    bpy.data.worlds['HDRI'].node_tree.nodes['Environment Texture'].image = hdri_image 

        return {'FINISHED'}  


############   IMPORT CHARACTERS AND ACCESSORIES   ############## 
class OBJECT_OT_add_object(bpy.types.Operator,AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "object.add_character"
    bl_label = "Add Roblox Character"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_char : bpy.props.StringProperty(name= "Added")

    def execute(self, context): 
        global rbx_char_netw_error
        global rbx_asset_netw_error
        global rbx_asset_name
        global rbx_asset_type_name
        global rbx_asset_creator
        global rbx_username
        global rbx_accessory
        
        scene = context.scene
        rbx_char = self.rbx_char
        rbx_prefs = scene.rbx_prefs
        rbx_bundle = rbx_prefs.rbx_bundle
        rbx_split = rbx_prefs.rbx_split  
        rbx_username = rbx_prefs.rbx_username
        rbx_accessory = rbx_prefs.rbx_accessory
        rbx_username_is = "username"
        
        #rbx_char_path = addon_path + '/Imported_Characters' + fbs + rbx_username        
        
        ##### Convert username input #####
        if "https://www.roblox.com/" in rbx_username:
            rbx_username = rbx_username.lstrip("https://www.roblox.com/users/")
            rbx_username = rbx_username.split("/")[0]
            if not rbx_username.isdigit():
                rbx_char_netw_error = "Error: Invalid URL"
            else:                
                rbx_username_is = "id"
        elif rbx_username.isdigit():
            rbx_username = rbx_username
            rbx_username_is = "id"

        ##### Convert accessory input #####
        if rbx_bundle == False:
            if "https://www.roblox.com/" in rbx_accessory:
                rbx_accessory = rbx_accessory.lstrip("https://www.roblox.com/catalog/")
                rbx_accessory = rbx_accessory.split("/")[0]
                print(rbx_accessory)
                if not rbx_accessory.isdigit():
                    rbx_asset_netw_error = "Error: Invalid URL"
        else:
            if "https://www.roblox.com/" in rbx_accessory:
                rbx_accessory = rbx_accessory.lstrip("https://www.roblox.com/bundles/")
                rbx_accessory = rbx_accessory.split("/")[0]
                if not rbx_accessory.isdigit():
                    rbx_asset_netw_error = "Error: Invalid URL"

                    
        rbx_char_path = os.path.join(addon_path, 'Imported_Characters' + fbs + rbx_username)



        ##### Create Folders #####
        if rbx_char == 'folder':
            if not os.path.exists(addon_path + '/Imported_Characters'):
                os.makedirs(addon_path + '/Imported_Characters')
            os.startfile(os.path.dirname(addon_path + '/Imported_Characters/'))
        if rbx_char == 'folder_accessory':
            if not os.path.exists(addon_path + '/Imported_Accessories'):
                os.makedirs(addon_path + '/Imported_Accessories')
            os.startfile(os.path.dirname(addon_path + '/Imported_Accessories/'))         
        
        
        
        ##### Character Preview #####
        if rbx_char == 'preview': 
            if rbx_char_netw_error == None:
                rbx_usr_avtr, rbx_char_netw_error, rbx_username = asyncio.run(self.preview(rbx_username, rbx_username_is))
            
            if rbx_char_netw_error == None:
                ### Clear Previous Preview ###
                try:
                    rbx_tmp_img = bpy.data.images[rbx_username + '.png']
                except:
                    pass
                else:
                    bpy.data.images.remove(rbx_tmp_img)
                    
                    
                rbx_tmp_filepath = os.path.join(addon_path, 'tmp')
                if not os.path.exists(rbx_tmp_filepath):
                        os.makedirs(rbx_tmp_filepath)
                rbx_tmp_file = os.path.join(rbx_tmp_filepath, rbx_username + ".png")
                
                try:
                    with open(f"{rbx_tmp_file}", "wb") as f:
                        f.write(rbx_usr_avtr) 
                except:
                    print("OS Error")
                    rbx_char_netw_error = "Error saving temp avatar img"
                else:
                    rbx_usr_avtr = bpy.data.images.load(rbx_tmp_file)
                
                
        ##### Accessory Preview #####
        if rbx_char == 'preview_accessory': 
            if rbx_asset_netw_error == None:
                rbx_asset_img, rbx_asset_name, rbx_asset_type, rbx_asset_creator, rbx_asset_netw_error = asyncio.run(self.acc_preview(rbx_accessory, rbx_bundle))
                rbx_asset_type_name = rbx_ast_type.get(str(rbx_asset_type))
            
            if rbx_asset_netw_error == None:
                ### Clear Previous Preview ###
                try:
                    rbx_tmp_img = bpy.data.images[rbx_accessory + '.png']
                except:
                    pass
                else:
                    bpy.data.images.remove(rbx_tmp_img)
                    
                    
                rbx_tmp_filepath = os.path.join(addon_path, 'tmp')
                if not os.path.exists(rbx_tmp_filepath):
                        os.makedirs(rbx_tmp_filepath)
                rbx_tmp_file = os.path.join(rbx_tmp_filepath, rbx_accessory + ".png")
                
                try:
                    with open(f"{rbx_tmp_file}", "wb") as f:
                        f.write(rbx_asset_img) 
                except:
                    print("OS Error")
                    rbx_asset_netw_error = "Error saving temp Accessory img"
                else:
                    rbx_asset_img = bpy.data.images.load(rbx_tmp_file)                
                
        ##### Character Import #####        
        if rbx_char == 'import':
            if not os.path.exists(rbx_char_path):
                os.makedirs(rbx_char_path)               
                
            if rbx_char_netw_error == None:
                rbx_usr_hsh_urls, rbx_char_netw_error, rbx_username = asyncio.run(self.char_import(rbx_username, rbx_username_is))

            if rbx_char_netw_error == None: 
                              
                def get_cdn_url(hash):
                    i = 31
                    for char in hash[:32]:
                        i ^= ord(char)  # i ^= int(char, 16) also works
                    return f"https://t{i%8}.rbxcdn.com/{hash}"
                
                avt_obj_hsh = rbx_usr_hsh_urls['obj']
                avt_mtl_hsh = rbx_usr_hsh_urls['mtl']
                avt_tex_hsh = rbx_usr_hsh_urls['textures']
                
                ### Get All URLs ###
                avt_mtl_url = get_cdn_url(avt_mtl_hsh)
                avt_obj_url = get_cdn_url(avt_obj_hsh)

                avt_tex_url = []
                for i in range(len(avt_tex_hsh)):
                    tmp_tex_url = get_cdn_url(avt_tex_hsh[i])
                    avt_tex_url.append(tmp_tex_url)               
                
                ### Download files ###
                rbx_mtl_file = os.path.join(rbx_char_path, rbx_username + ".mtl")
                rbx_obj_file = os.path.join(rbx_char_path, rbx_username + ".obj")                
                
                def save_to_file(file, url, type):
                    data, rbx_char_netw_error = asyncio.run(self.download(url, type))
                    if rbx_char_netw_error == None:
                        try:
                            with open(file, "wb") as f:
                                f.write(data) 
                        except:
                            print("OS Error")
                            rbx_char_netw_error = f"Error saving {type}"
                            
                save_to_file(rbx_mtl_file, avt_mtl_url, "mtl")
                save_to_file(rbx_obj_file, avt_obj_url, "obj")
                
                for i in range(len(avt_tex_url)):
                    rbx_tex_file = os.path.join(rbx_char_path, rbx_username + '_tex-' + str(i) + ".png")
                    save_to_file(rbx_tex_file, avt_tex_url[i], "png")
                    
                ### Write new Texture names into MTL ###
                if rbx_char_netw_error == None:
                    try:
                        with open(rbx_mtl_file, 'r', encoding='UTF-8') as f:
                            text = f.read()
                    except:
                        rbx_char_netw_error = "Error writing to MTL file"
                    else:
                        with open(rbx_mtl_file, 'w', encoding='UTF-8') as f:
                            for i in range(len(avt_tex_hsh)):
                                text = text.replace(avt_tex_hsh[i], rbx_username + '_tex-' + str(i) + ".png")
                            if "map_d" in text:
                                text = text.replace("map_d","") ## Remove transparency
                            f.write(text)

                        rbx_imp_avat = bpy.ops.import_scene.obj(filepath=rbx_obj_file)
                    
                        ### Selecting Character ###
                        rbx_object = bpy.context.selected_objects[0]
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.context.view_layer.objects.active = None
                        bpy.data.objects[rbx_object.name].select_set(True)
                        bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object.name]
                                                
                        ### Position Character ###
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                        bpy.ops.transform.translate(value=(0, 0, 3.28467), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
                        bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
                        
                        ### Setting up materials ###
                        for rbx_mat_slot in bpy.context.object.material_slots:
                            rbx_mat_slot.material.show_transparent_back = False
                            rbx_mat_slot.material.use_backface_culling = True 
                        
                        ### Setting up materials for New Heads and Skinned characters ###    
                        with open(rbx_mtl_file, 'r', encoding='UTF-8') as f:
                            lines = f.readlines()
                            for i in range(len(lines)):
                                if "newmtl" in lines[i]:
                                    mat_nm = lines[i].split("newmtl")
                                    mat_nm = mat_nm[1].strip()
                                    for x in range(i,i+2):
                                        if "Material Color" in lines[x]:
                                            for n in range(x,len(lines)):
                                                if "Ka" in lines[n]:
                                                    rbx_shade = lines[n].split(" ")
                                                    rbx_shade_r = rbx_shade[1].strip()
                                                    rbx_shade_g = rbx_shade[2].strip()
                                                    rbx_shade_b = rbx_shade[3].strip()
                                                    if (rbx_shade_r, rbx_shade_g, rbx_shade_b) != ('1','1','1'):
                                                        rbx_shade_r = float(rbx_shade_r)
                                                        rbx_shade_g = float(rbx_shade_g)
                                                        rbx_shade_b = float(rbx_shade_b)                                                    
                                                        for rbx_mat_slot in bpy.context.object.material_slots:
                                                            if mat_nm in rbx_mat_slot.name:
                                                                rbx_mat = rbx_mat_slot.material
                                                                rbx_nodes = rbx_mat.node_tree.nodes
                                                                bsdf = rbx_nodes['Principled BSDF']
                                                                
                                                                if float(bldr_fdr) < 3.4:
                                                                    rbx_MixNode = rbx_nodes.new('ShaderNodeMixRGB')
                                                                    rbx_MixNode.inputs[1].default_value = (rbx_shade_r, rbx_shade_g, rbx_shade_b, 1)
                                                                else:
                                                                    rbx_MixNode = rbx_nodes.new('ShaderNodeMix')
                                                                    rbx_MixNode.data_type='RGBA'
                                                                    rbx_MixNode.inputs[6].default_value = (rbx_shade_r, rbx_shade_g, rbx_shade_b, 1)
                                                                rbx_MixNode.location = (-200,300)
                                                                
                                                                rbx_img = rbx_nodes['Image Texture']
                                                                rbx_img.location = (-500,300)
                                                                rbx_img_link = rbx_img.outputs[0].links[0] #existing link to bsdf
                                                                rbx_mat.node_tree.links.remove(rbx_img_link) #remove existing link to bsdf
                                                                
                                                                if float(bldr_fdr) < 3.4:
                                                                    rbx_mat.node_tree.links.new(rbx_img.outputs[1], rbx_MixNode.inputs[0]) #Alpha
                                                                    rbx_mat.node_tree.links.new(rbx_img.outputs[0], rbx_MixNode.inputs[2]) #Color
                                                                    rbx_mat.node_tree.links.new(rbx_MixNode.outputs[0], bsdf.inputs[0])
                                                                else:
                                                                    rbx_mat.node_tree.links.new(rbx_img.outputs[1], rbx_MixNode.inputs[0]) #Alpha
                                                                    rbx_mat.node_tree.links.new(rbx_img.outputs[0], rbx_MixNode.inputs[7]) #Color
                                                                    rbx_mat.node_tree.links.new(rbx_MixNode.outputs[2], bsdf.inputs[0])
                                                    break
 
                        ### Removing doubles ###
                        if bpy.context.mode == 'OBJECT':
                            bpy.ops.object.editmode_toggle()
                            bpy.ops.mesh.select_all(action='SELECT')                
                        elif bpy.context.mode == 'EDIT_MESH':
                            bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.remove_doubles()
                        #bpy.ops.mesh.normals_make_consistent(inside=False)
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.customdata_custom_splitnormals_clear()
                        bpy.context.object.data.use_auto_smooth = False
                              
                if rbx_split == True:
                    if rbx_char_netw_error == None:
                        
                        obj = context.active_object
                        i = 1
            
                        # Check if the selected object has any materials assigned to it
                        if not obj.material_slots:
                            rbx_char_netw_error = "No materials assigned to selected object."
                        else:
                            bpy.ops.object.editmode_toggle()
                            bpy.ops.mesh.select_all(action='SELECT')
                            bpy.ops.mesh.separate(type='MATERIAL')
                            bpy.ops.object.editmode_toggle()
                            for selected in context.selected_objects:
                                if selected.name == obj.name:
                                    # Deselect selected object
                                    obj.select_set(False)
                                else:
                                    # Set the new created object to active
                                    context.view_layer.objects.active = selected
                                    context.active_object.name = f"{obj.name}_Accessory_{i}"
                                    i += 1
                            bpy.ops.object.select_all(action='DESELECT')
            

        ##### Accossory Import #####        
        if rbx_char == 'import_accessory': 
            if rbx_bundle == True:
                rbx_asset_name, rbx_asset_type, rbx_asset_creator, rbx_asset_items, rbx_asset_netw_error = asyncio.run(self.get_acc_bundl_info(rbx_accessory))
                print(rbx_asset_items)    
            else:               
                rbx_asset_name, rbx_asset_type, rbx_asset_creator, rbx_asset_netw_error = asyncio.run(self.get_acc_info(rbx_accessory, rbx_bundle))
            rbx_asset_type_name = rbx_ast_type.get(str(rbx_asset_type))
            
            if rbx_asset_netw_error == None:    
                rbx_char_path = os.path.join(addon_path, 'Imported_Accessories' + fbs + rbx_asset_name)
                if not os.path.exists(rbx_char_path):
                    try:
                        os.makedirs(rbx_char_path)
                    except:
                        print("OS Error")
                        rbx_asset_netw_error = "Error Making Accessory Folder" 
                
            if rbx_asset_netw_error == None:
                asset_data, rbx_asset_netw_error = asyncio.run(self.get_asset_data(rbx_accessory))
                asset_data = str(asset_data)

            if rbx_asset_netw_error == None:
                def get_cdn_url(hash):
                    i = 31
                    for char in hash[:32]:
                        i ^= ord(char)  # i ^= int(char, 16) also works
                    return f"https://t{i%8}.rbxcdn.com/{hash}"
                ############## PARSING RBXM ################
                ### WARNING!!
                ### If you also want to use this parsing method
                ### You can, this is created by me
                ### But you must give a proper credits with links to my socials (e.g. Twitter, Discord)
                def regex(exp,str):
                    clean = r"[0-9]+\W*(PROP)"
                    res = re.search(exp, str, re.MULTILINE)
                    if res == None:
                        pass
                    else:
                        if rbx_asset_type in accessory and rbx_asset_creator == "Roblox":
                            res = res.group()
                            if 'id=' in res:
                                res = res.split("id=")[1]
                            if 'id://' in res:
                                res = res.split("id://")[1]
                            res = res.split("<")[0]
                        else:
                            res = res.group()
                            print(res)
                            res = re.search(clean, res, re.MULTILINE)
                            if res == None:
                                pass
                            else:
                                res = res.group()
                                res = res.split("PROP")[0]
                    return res
             
                if rbx_asset_type in accessory and rbx_asset_creator == "Roblox":
                    expMesh = r'"MeshId"><url>.*?\W*(<)'
                    expTexMap = r'"TextureId"><url>.*?\W*(<)'
                else:
                    expTexMap = r"TextureId.*?\W*(PROP)"
                    expColMap = r"ColorMap.*?\W*(PROP)"
                    expNorMap = r"NormalMap.*?\W*(PROP)"
                    expMetMap = r"MetalnessMap.*?\W*(PROP)"
                    expRoughMap = r"RoughnessMap.*?\W*(PROP)"
                    expMesh = r"MeshId.*?\W*(PROP)"
                    #expOutCage = r"CageMeshId.*?\W*(PROP)"
                    #expInCage = r"ReferenceMeshId.*?\W*(PROP)"        
                
                is_acry = False
                is_lc = False
                if rbx_asset_type in accessory:
                    is_acry = True
                if rbx_asset_type in lc:
                    is_lc = True                    
                    
                ### Getting Accessory Textures ID's (Library ID) ### 
                texMapId = None
                meshId = None 
                colMapId = None
                norMapId = None
                metMapId = None
                roughMapId = None
                if is_acry == True:    
                   texMapId = regex(expTexMap, asset_data)
                   meshId = regex(expMesh, asset_data)
                if is_lc == True:
                    colMapId = regex(expColMap, asset_data)
                    norMapId = regex(expNorMap, asset_data)
                    metMapId = regex(expMetMap, asset_data)
                    roughMapId = regex(expRoughMap, asset_data)
                    meshId = regex(expMesh, asset_data)
                    #outCageId = regex(expOutCage, lines)
                    #inCageId = regex(expInCage, lines)
                print(texMapId)
                print(meshId)
                tex_items = [meshId,texMapId,colMapId,metMapId,roughMapId,norMapId]
                tex_range = ['Obj','Texture','Diffuse','Metallic','Roughness','Normal']

                ### Create Temp files ###
                rbx_mtl_file = os.path.join(rbx_char_path, rbx_asset_name + ".mtl")
                
                ### Get Textures Data and write them to files ###
                n = 0
                for item in tex_items:
                    if rbx_asset_netw_error == None:
                        if item != None:
                            if n == 0:
                                try:
                                    file_data, rbx_asset_netw_error = asyncio.run(self.get_asset_hashes(rbx_accessory)) # Get OBJ Hash
                                except:
                                    rbx_asset_netw_error = "Error Getting OBJ file"
                                else:
                                    acc_obj_hsh = file_data['obj'] # Get OBJ Hash
                                    acc_obj_url = get_cdn_url(acc_obj_hsh) # Convert OBJ Hash to URL
                                    file_data, rbx_asset_netw_error = asyncio.run(self.download(acc_obj_url, 'obj')) # Get OBJ Data
                                if rbx_asset_netw_error == None:
                                    rbx_tmp_file = os.path.join(rbx_char_path, rbx_asset_name + ".obj") # Save OBJ Data
                                    rbx_obj_file = os.path.join(rbx_char_path, rbx_asset_name + ".obj") # For Import OBJ Later
                                else:
                                    rbx_asset_netw_error = f"Error saving {tex_range[n]}" 
                            else:
                                file_data, rbx_asset_netw_error = asyncio.run(self.get_asset_data(item)) # Get all other Textures
                                if rbx_asset_netw_error == None:
                                    rbx_tmp_file = os.path.join(rbx_char_path, rbx_asset_name + f"_{tex_range[n]}.png")
                                else:
                                    rbx_asset_netw_error = f"Error getting {tex_range[n]} Map"
                            if rbx_asset_netw_error == None:
                                try:
                                    #print(f"Writing {tex_range[n]} data")
                                    with open(rbx_tmp_file, "wb") as f:
                                        f.write(file_data) 
                                except:
                                    print("OS Error")
                                    rbx_asset_netw_error = f"Error saving {tex_range[n]}"
                    n += 1
                    
                ### Import Accessory ###    
                if rbx_asset_netw_error == None:
 
                    ### Start Accessory Import ###
                    rbx_imp_acc = bpy.ops.import_scene.obj(filepath=rbx_obj_file)

                    ### Creating new Material ###
                    rbx_obj = bpy.context.selected_objects[0]
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None
                    bpy.data.objects[rbx_obj.name].select_set(True)
                    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_obj.name]
                    
                    if rbx_obj.material_slots:
                        bpy.ops.object.material_slot_remove()
                    mat = bpy.data.materials.new(name=f"{rbx_asset_name}_mat")
                    rbx_obj.data.materials.append(mat) 
                    mat = rbx_obj.material_slots[0].material 
                    mat.use_nodes = True
                    mat.use_backface_culling = True
                    nodes = mat.node_tree.nodes
                    bsdf = nodes.get("Principled BSDF")
                    bsdf.inputs[9].default_value = 1


                    for i in range(len(tex_items)):
                        if tex_items[i] != None:
                            if i == 0:
                                pass
                            else:
                                rbx_tex = os.path.join(rbx_char_path, rbx_asset_name + f"_{tex_range[i]}.png")
                                rbx_image = bpy.data.images.load(rbx_tex)
                                rbxtexNode = nodes.new('ShaderNodeTexImage')
                                rbxtexNode.image = rbx_image
                                rbxtexNode.name = tex_range[i]
                                if i > 1:
                                    loc = i-2
                                else:
                                    loc = i-1
                                rbxtexNode.location = (-500,300-300*loc)
                                if i == 1 or i == 2:
                                    mat.node_tree.links.new(rbxtexNode.outputs[0], bsdf.inputs["Base Color"])
                                else:
                                    if i == 5:
                                        norm_node = nodes.new(type="ShaderNodeNormalMap")
                                        norm_node.location = (-200,300-300*loc)        
                                        mat.node_tree.links.new(rbxtexNode.outputs[0], norm_node.inputs[1])
                                        mat.node_tree.links.new(norm_node.outputs[0], bsdf.inputs[tex_range[i]])
                                        norm_node.space = 'TANGENT'
                                    else:
                                        mat.node_tree.links.new(rbxtexNode.outputs[0], bsdf.inputs[tex_range[i]])
                                    rbx_image.colorspace_settings.name = 'Non-Color'
                                    
                   
                    ### Position Asset ###
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                    bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
                    
                    
                    ### Removing doubles ###
                    if bpy.context.mode == 'OBJECT':
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')                
                    elif bpy.context.mode == 'EDIT_MESH':
                        bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    #bpy.ops.mesh.normals_make_consistent(inside=False)
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    bpy.context.object.data.use_auto_smooth = False

                                        
                           
        return {'FINISHED'}
    



    ###########  MAIN ASYNC FUNCTIONS ###########
    ### Preview for Character ###
    async def preview(self, rbx_username, rbx_username_is):
        result, rbx_char_netw_error, rbx_username = await self.get_user_id(rbx_username, rbx_username_is) #User ID
        if rbx_char_netw_error == None:
            result, rbx_char_netw_error = await self.get_user_avatar_url(result) #User Avatar URL
            if rbx_char_netw_error == None:
                result, rbx_char_netw_error = await self.get_user_avatar_img(result) #User Avatar IMG Data
        return result, rbx_char_netw_error, rbx_username

    ### Preview for Accessory ###
    async def acc_preview(self, rbx_accessory, rbx_bundle):
        rbx_asset_img_url, rbx_asset_netw_error = await self.get_acc_url(rbx_accessory, rbx_bundle) #Accessory IMG URL
        if rbx_asset_netw_error == None:
            result, rbx_asset_netw_error = await self.get_acc_img(rbx_asset_img_url) #Accessory IMG Data
            if rbx_asset_netw_error == None:
                rbx_asset_name, rbx_asset_type, rbx_asset_creator, rbx_asset_netw_error = await self.get_acc_info(rbx_accessory, rbx_bundle) #Accessory Infos
            else:
                result, rbx_asset_name, rbx_asset_type, rbx_asset_creator = None, None, None, None
        else:
            result, rbx_asset_name, rbx_asset_type, rbx_asset_creator = None, None, None, None
            
        return result, rbx_asset_name, rbx_asset_type, rbx_asset_creator, rbx_asset_netw_error
    
    ### Import Character ###
    async def char_import(self, rbx_username, rbx_username_is):
        result, rbx_char_netw_error, rbx_username = await self.get_user_id(rbx_username, rbx_username_is) #User ID
        if rbx_char_netw_error == None:
            result, rbx_char_netw_error = await self.get_user_hashes(result)
        return result, rbx_char_netw_error, rbx_username

        
    ########### INDIVIDUAL FUNCTIONS ###########
    async def get_user_id(self, rbx_username, rbx_username_is):
        if rbx_username_is == "id":
            try:
                data = requests.get(f"https://users.roblox.com/v1/users/{rbx_username}")
            except:
                rbx_char_netw_error = "Get User ID Error, no respose"
                rbx_usr_id = None
            else: 
                if data.status_code == 200:
                    data = data.json()
                    rbx_usr_id = data['id']
                    rbx_username = data['name']
                    rbx_char_netw_error = None
                else:
                    if data.status_code == 404:
                        rbx_username_is = "username"
                    else:
                        rbx_usr_id = None
                        rbx_char_netw_error = f"{data.status_code}: Error getting User ID" 
        if rbx_username_is == "username":
            payload = {
                "usernames": [rbx_username],
                "excludeBannedUsers" : 'true'
                }
            try:
                data = requests.post("https://users.roblox.com/v1/usernames/users", json=payload)
            except:
                rbx_char_netw_error = "Get User ID Error, no respose"
                rbx_usr_id = None
            else:
                if data.status_code == 200:
                    data = data.json()
                    try:
                        rbx_usr_id = data.get('data')[0]['id']
                    except:
                        rbx_usr_id = None
                        rbx_char_netw_error = "Error: Unable to find this user"
                    else:
                        rbx_char_netw_error = None           
                else:
                    rbx_usr_id = None
                    rbx_char_netw_error = f"{data.status_code}: Error getting User ID"
        return rbx_usr_id, rbx_char_netw_error, rbx_username
    
                    
    async def get_user_avatar_url(self, rbx_usr_id):
        rbx_size = '250x250'
        rbx_format = 'Png'
        rbx_isCircular = 'false'                                            
        url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={rbx_usr_id}&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            rbx_usr_img_url = data["data"][0]["imageUrl"]
            rbx_char_netw_error = None
        else:
            rbx_usr_img_url = None
            rbx_char_netw_error = f"{data.status_code}: Error getting Avatar URL"
        return rbx_usr_img_url, rbx_char_netw_error
                
                
    async def get_user_avatar_img(self, rbx_usr_img_url): 
        image_data = requests.get(rbx_usr_img_url)
        if image_data.status_code == 200:
            image_data = image_data.content
            rbx_char_netw_error = None
        else:
            rbx_char_netw_error = f"{image_data.status_code}: Error getting Avatar IMG"
        return image_data, rbx_char_netw_error



    async def get_user_hashes(self, rbx_usr_id): 
        data = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-3d?userId={rbx_usr_id}")                   
        if data.status_code == 200:
            data = data.json()
            rbx_usr_hsh_urls = data['imageUrl']  #Get Link to OBJ and Textures Hashes
            rbx_char_netw_error = None
            rbx_usr_hsh_urls = requests.get(rbx_usr_hsh_urls)
            if rbx_usr_hsh_urls.status_code == 200:
                rbx_usr_hsh_urls = rbx_usr_hsh_urls.json() #Get OBJ and Textures Hashes links
                rbx_char_netw_error = None
            else:
                rbx_usr_hsh_urls = None
                rbx_char_netw_error = f"{rbx_usr_hsh_urls.status_code}: Error getting user hashes"
        else:
            rbx_usr_hsh_urls = None
            rbx_char_netw_error = f"{rbx_usr_hsh_urls.status_code}: Error getting user hashes"
        return rbx_usr_hsh_urls, rbx_char_netw_error


    async def download(self, url, type): 
        data = requests.get(url) 
        if data.status_code == 200:
            data = data.content
            rbx_char_netw_error = None
        else:
            rbx_char_netw_error = f"{data.status_code}: Error downloading {type} file"
        return data, rbx_char_netw_error



    async def get_acc_url(self, rbx_accessory, rbx_bundle):
        rbx_size = '250x250'
        rbx_format = 'Png'
        rbx_isCircular = 'false'
        if rbx_bundle == True:
            rbx_url = f"https://thumbnails.roblox.com/v1/bundles/thumbnails?bundleIds={rbx_accessory}&size=150x150&format={rbx_format}&isCircular={rbx_isCircular}"
        else:
            rbx_url = f"https://thumbnails.roblox.com/v1/assets?assetIds={rbx_accessory}&returnPolicy=PlaceHolder&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}"         
        data = requests.get(rbx_url)
        if data.status_code == 200:
            data = data.json()
            try:
                rbx_asset_img_url = data["data"][0]["imageUrl"]
            except:
                rbx_asset_netw_error = f"{data.status_code}: Error, Invalid accessory"
                rbx_asset_img_url = None
            else:
                rbx_asset_netw_error = None
        else:
            rbx_asset_img_url = None
            rbx_asset_netw_error = f"{data.status_code}: Error getting Accessory IMG URL"
        return rbx_asset_img_url, rbx_asset_netw_error


    async def get_acc_img(self, rbx_asset_img_url): 
        data = requests.get(rbx_asset_img_url)
        if data.status_code == 200:
            image_data = data.content
            rbx_asset_netw_error = None
        else:
            rbx_char_netw_error = f"{data.status_code}: Error getting Accessory IMG Data"
        return image_data, rbx_asset_netw_error

    async def get_acc_info(self, rbx_accessory, rbx_bundle):          
        if rbx_bundle == True:
            url = f"https://catalog.roblox.com/v1/bundles/{rbx_accessory}/details"
            data = requests.get(url)
            if data.status_code == 200:
                data = data.json()
                rbx_asset_name = data['name']
                rbx_asset_type = data['bundleType']
                rbx_asset_creator = data['creator']['name']
                rbx_asset_netw_error = None
            else:
                rbx_asset_name = None
                rbx_asset_creator = None
                rbx_asset_type = None
                rbx_asset_netw_error = f"{data.status_code}: Error getting Accessory Info"
        else:                           
            url = f"https://economy.roblox.com/v2/assets/{rbx_accessory}/details"
            data = requests.get(url)
            if data.status_code == 200:
                data = data.json()
                rbx_asset_name = data['Name']
                rbx_asset_type = data['AssetTypeId']
                rbx_asset_creator = data['Creator']['Name']
                rbx_asset_netw_error = None
            else:
                rbx_asset_name = None
                rbx_asset_creator = None
                rbx_asset_type = None
                rbx_asset_netw_error = f"{data.status_code}: Error getting Accessory Info"
        return rbx_asset_name, rbx_asset_type, rbx_asset_creator, rbx_asset_netw_error





    async def get_acc_bundl_info(self, rbx_accessory):          
        url = f"https://catalog.roblox.com/v1/bundles/{rbx_accessory}/details"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            rbx_asset_name = data['name']
            rbx_asset_type = data['bundleType']
            rbx_asset_creator = data['creator']['name']
            rbx_asset_items = data['items']
            rbx_asset_netw_error = None
        else:
            rbx_asset_name = None
            rbx_asset_creator = None
            rbx_asset_type = None
            rbx_asset_items = None
            rbx_asset_netw_error = f"{data.status_code}: Error getting Accessory Info"
        return rbx_asset_name, rbx_asset_type, rbx_asset_creator, rbx_asset_items, rbx_asset_netw_error
    
    

    async def get_asset_data(self, rbx_accessory):
        url = f"https://assetdelivery.roblox.com/v1/asset?id={rbx_accessory}" 
        data = requests.get(url)
        if data.status_code == 200:
            asset_data = data.content
            rbx_asset_netw_error = None
        else:
            asset_data = None
            rbx_char_netw_error = f"{data.status_code}: Error getting Asset Data"
        return asset_data, rbx_asset_netw_error


    async def get_asset_hashes(self, rbx_accessory):             
        url = f"https://thumbnails.roblox.com/v1/assets-thumbnail-3d?assetId={rbx_accessory}"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            rbx_acc_hsh_urls = data['imageUrl']  #Get Link to OBJ and Textures Hashes
            rbx_asset_netw_error = None
            data = requests.get(rbx_acc_hsh_urls)
            if data.status_code == 200:
                rbx_acc_hsh_urls = data.json() #Get OBJ and Textures Hashes links
                rbx_asset_netw_error = None
            else:
                rbx_acc_hsh_urls = None
                rbx_asset_netw_error = f"{data.status_code}: Error getting Asset hashes"
        else:
            rbx_acc_hsh_urls = None
            rbx_asset_netw_error = f"{data.status_code}: Error getting Asset hashes"
        return rbx_acc_hsh_urls, rbx_asset_netw_error



    
######### Dummy Buttons ###########    
class BUTTON_DMMY(bpy.types.Operator):
    bl_label = "BUTTON_DMMY"
    bl_idname = "object.button_dmmy"
    bl_options = {'REGISTER', 'UNDO'}
    dmy : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs         
        dmy = self.dmy
        dmy_spwn = None
        rbx_mode = None
        
        dum_list = [
                        'R15 Blocky',
                        'R15 Boy',
                        'R15 Girl',
                        'R15 Woman',
                        '4.0 Lin',
                        '4.0 Oakley',
                        '3.0 Man',
                        '3.0 Woman',
                        'Robloxian 2.0',
                        'Neoclassic Skyler',
                        'Rthro Boy',
                        'Rthro Girl',
                        'Rthro Normal',
                        'Rthro Slender',
                        'R6 (1.0)'
                        ] 
                        
        dum_hd_list = [
                        'Classic Head',
                        'Woman Head',
                        'Woman Head v2',
                        'Man Head',
                        'R6 Head'
                        ]  
                        
                        
        if dmy == 'Dummy':    
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects
                
                                
            for x in range(len(dum_list)):
                if rbx_prefs.rbx_dum_enum == 'OP' + str(x+1):
                    dmy_spwn = dum_list[x]                  

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, filename =dmy_spwn)
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print(dmy_spwn + " Dummy Spawned")
            
        if dmy == 'Dummy_head': 
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects
                
                                
            for x in range(len(dum_list)):
                if rbx_prefs.rbx_dum_hd_enum == 'OP' + str(x+1):
                    dmy_spwn = dum_hd_list[x]                  

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, filename =dmy_spwn)
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print(dmy_spwn + " Spawned")

        if dmy == 'rigged_r6': 
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects               

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='Rigged R6')
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print("Rigged R6 Spawned")

        if dmy == 'rigged_r15_blocky': 
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects               

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='R15 Blocky Rig')
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print("Rigged R15 Blocky Spawned")
            
        if dmy == 'rigged_r15_woman': 
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects               

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='R15 Woman Rig')
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print("Rigged R15 Woman Spawned")                                   
        
        return {'FINISHED'} 



######### Wear Character ###########    
class BUTTON_WEAR(bpy.types.Operator):
    bl_label = "BUTTON_WEAR"
    bl_idname = "object.button_wear"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_cloth : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs 
        rbx_cloth = self.rbx_cloth
        rbx_face = rbx_prefs.rbx_face
        rbx_shirt = rbx_prefs.rbx_shirt
        rbx_pants = rbx_prefs.rbx_pants
        
        global rbx_face_netw_error
        global rbx_shirt_netw_error
        global rbx_pants_netw_error
        global rbx_face_name 
        global rbx_shirt_name
        global rbx_pants_name
        global rbx_face_filename
        global rbx_shirt_filename
        global rbx_pants_filename
        
        
        rbx_character = None 
        rbx_cloth_error = None
                

        char_list = ['RoBone'] 
        rbx_parts = {
                    0 : ['Head', 'Left Hand', 'Left Leg', 'Right Hand', 'Right Leg', 'Torso']
                    }              
        rbx_clothes = {
                    0 : ['R6 Head', 'R6 Shirt', 'R6 Pants', 'R6 Shirt', 'R6 Pants', 'R6 Torso']
                    }
              
        ##### Create Folders #####
        if rbx_cloth == 'folder':
            if not os.path.exists(addon_path + '/Imported_Clothes'):
                os.makedirs(addon_path + '/Imported_Clothes')
            os.startfile(os.path.dirname(addon_path + '/Imported_Clothes/'))

        ### Check selected objects ###
        if rbx_cloth == 'mod':
            if bpy.context.mode != 'EDIT_MESH':
                rbx_object = bpy.context.selected_objects
                if len(rbx_object) == 1:
                    rbx_object = bpy.context.selected_objects[0]
                    if rbx_object.type == 'ARMATURE':
                        rbx_cloth_error = None
                    else:
                        rbx_cloth_error = "Error: Pls Select Armature"
                else:
                    rbx_cloth_error = "Error: Pls Select 1 Object"
            else:
                rbx_cloth_error = "Error: Pls Exit Edit Mode"


            if rbx_cloth_error == None:
                for x in range(len(char_list)):
                    if char_list[x] in rbx_object.name:
                        rbx_character = x
                        break
                          
            if rbx_character != None:  
                rbx_object.name = f"{rbx_object.name}_cloth_mod"         
                bpy.ops.object.select_grouped(type='COLLECTION')
                rbx_selected = bpy.context.selected_objects
            
                for part in rbx_parts[rbx_character]:
                    for mesh in rbx_selected:
                        if part in mesh.name:
                            bpy.ops.object.select_all(action='DESELECT')
                            bpy.context.view_layer.objects.active = None
                            bpy.data.objects[mesh.name].select_set(True)
                            bpy.context.view_layer.objects.active = bpy.data.objects[mesh.name]
                            
                            mat_index = rbx_parts[rbx_character].index(part)
                            mat_name = rbx_clothes[rbx_character][mat_index]
                            if mesh.material_slots:
                                bpy.ops.object.material_slot_remove()
                                
                                
                            if bpy.data.materials.get(f"{mat_name}_{rbx_object.name}") == None:
                                if bpy.data.materials.get(mat_name) == None:
                                    bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_material, filename =mat_name)
                                    mat = bpy.data.materials.get(mat_name)
                                    mesh.data.materials.append(mat)
                                    mat.name = f"{mat_name}_{rbx_object.name}"
                            else:
                                mat = bpy.data.materials.get(f"{mat_name}_{rbx_object.name}")
                                mesh.data.materials.append(mat)
                                
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                bpy.data.objects[rbx_object.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object.name]
        
        def get_id(data):
            error = None
            if "https://www.roblox.com/" in data:
                data = data.lstrip("https://www.roblox.com/catalog/")
                data = data.split("/")[0]
                if not data.isdigit():
                    error = "Error: Invalid URL"
            return data, error
        
        def make_folder(data):
            error = None
            path = os.path.join(addon_path, 'Imported_Clothes' + fbs + data)
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except:
                    error = "Error Making Accessory Folder" 
            return path, error
        
        def write_data(path, data, asset_name):
            error = None
            file = os.path.join(path, asset_name + ".png")
            with open(file, "wb") as f:
                f.write(data)      
            return file, error
        
        def prop_filename(name):
            forb_chars = dict((ord(char), None) for char in '\/*?:"<>|')
            new_name = name.translate(forb_chars)  
            return new_name   
            
        ##### Accessory Import ##### 
        if rbx_cloth == 'face':
            ##### Convert accessory input #####
            rbx_face, rbx_face_netw_error = get_id(rbx_face) 
            
            ### Get face Info ###
            if rbx_face_netw_error == None:        
                rbx_face_name, rbx_face_type, rbx_face_creator, rbx_face_netw_error = asyncio.run(self.get_acc_info(rbx_face))
            
            ### Make folder if dont have ###    
            if rbx_face_netw_error == None: 
                rbx_face_path, rbx_face_netw_error = make_folder("Faces")
            
            ### Get face thumbnail url ###    
            if rbx_face_netw_error == None:
                face_url, rbx_face_netw_error = asyncio.run(self.get_acc_thumb(rbx_face, rbx_cloth))
            
            ### Get face image data from thumbnail url ###     
            if rbx_face_netw_error == None:
                face_data, rbx_face_netw_error = asyncio.run(self.get_url_data(face_url))
            
            ### Write Data ###
            if rbx_face_netw_error == None:
                rbx_face_filename = prop_filename(rbx_face_name) #Remove forbidden characters
                rbx_face_tex, rbx_face_netw_error = write_data(rbx_face_path, face_data, rbx_face_filename)
                   
            ### Import Face ###
            if rbx_face_netw_error == None:
                rbx_object = bpy.context.selected_objects[0]
                rbx_image = bpy.data.images.load(rbx_face_tex)
                rbxtexNode = bpy.data.materials[f"R6 Head_{rbx_object.name}"].node_tree.nodes['Image Texture.001']

                #rbx_cloth_head = bpy.data.materials[f"R6 Head_{rbx_object.name}"].node_tree.nodes['R6 Cloth']
                rbxtexNode.image = rbx_image
 
 
         ##### Accessory Import ##### 
        if rbx_cloth == 'shirt':
            ##### Convert accessory input #####
            rbx_shirt, rbx_shirt_netw_error = get_id(rbx_shirt) 
            
            ### Get shirt Info ###
            if rbx_shirt_netw_error == None:        
                rbx_shirt_name, rbx_shirt_type, rbx_shirt_creator, rbx_shirt_netw_error = asyncio.run(self.get_acc_info(rbx_shirt))
                
            ### Get shirt asset ID ###
            if rbx_shirt_netw_error == None:        
                shirt_data, rbx_shirt_netw_error = asyncio.run(self.get_id_data(rbx_shirt, rbx_cloth))
                shirt_data = str(shirt_data).split("<url>http://www.roblox.com/asset/?id=")[1]
                rbx_shirt = shirt_data.split("</url>")[0] #Actual item ID
                
            ### Get shirt Data ###
            if rbx_shirt_netw_error == None:        
                shirt_data, rbx_shirt_netw_error = asyncio.run(self.get_id_data(rbx_shirt, rbx_cloth))
            
            ### Make folder if dont have ###
            if rbx_shirt_netw_error == None: 
                rbx_shirt_path, rbx_shirt_netw_error = make_folder("Shirts")   

            ### Write Data ###
            if rbx_shirt_netw_error == None:
                rbx_shirt_filename = prop_filename(rbx_shirt_name) #Remove forbidden characters
                rbx_shirt_tex, rbx_shirt_netw_error = write_data(rbx_shirt_path, shirt_data, rbx_shirt_filename)
                
            ### Import Shirt ###
            if rbx_shirt_netw_error == None:
                rbx_object = bpy.context.selected_objects[0]
                rbx_image = bpy.data.images.load(rbx_shirt_tex)
                rbxtexNode = bpy.data.materials[f"R6 Shirt_{rbx_object.name}"].node_tree.nodes['Image Texture.001']
                rbxtexNode2 = bpy.data.materials[f"R6 Torso_{rbx_object.name}"].node_tree.nodes['Image Texture.001']

                rbxtexNode.image = rbx_image 
                rbxtexNode2.image = rbx_image   


        ##### Accessory Import ##### 
        if rbx_cloth == 'pants':
            ##### Convert accessory input #####
            rbx_pants, rbx_pants_netw_error = get_id(rbx_pants) 
            
            ### Get pants Info ###
            if rbx_pants_netw_error == None:        
                rbx_pants_name, rbx_pants_type, rbx_pants_creator, rbx_pants_netw_error = asyncio.run(self.get_acc_info(rbx_pants))
                
            ### Get pants asset ID ###
            if rbx_pants_netw_error == None:        
                pants_data, rbx_pants_netw_error = asyncio.run(self.get_id_data(rbx_pants, rbx_cloth))
                pants_data = str(pants_data).split("<url>http://www.roblox.com/asset/?id=")[1]
                rbx_pants = pants_data.split("</url>")[0] #Actual item ID
                
            ### Get pants Data ###
            if rbx_pants_netw_error == None:        
                pants_data, rbx_pants_netw_error = asyncio.run(self.get_id_data(rbx_pants, rbx_cloth))
            
            ### Make folder if dont have ###
            if rbx_pants_netw_error == None: 
                rbx_pants_path, rbx_pants_netw_error = make_folder("Pants")   

            ### Write Data ###
            if rbx_pants_netw_error == None:
                rbx_pants_filename = prop_filename(rbx_pants_name) #Remove forbidden characters
                rbx_pants_tex, rbx_pants_netw_error = write_data(rbx_pants_path, pants_data, rbx_pants_filename)
                
            ### Import pants ###
            if rbx_pants_netw_error == None:
                rbx_object = bpy.context.selected_objects[0]
                rbx_image = bpy.data.images.load(rbx_pants_tex)
                rbxtexNode = bpy.data.materials[f"R6 Pants_{rbx_object.name}"].node_tree.nodes['Image Texture.001']
                rbxtexNode2 = bpy.data.materials[f"R6 Torso_{rbx_object.name}"].node_tree.nodes['Image Texture.002']

                rbxtexNode.image = rbx_image 
                rbxtexNode2.image = rbx_image 
                
                                       

        return {'FINISHED'} 
    

    ### Get Item info ###
    async def get_acc_info(self, id):                                
        url = f"https://economy.roblox.com/v2/assets/{id}/details"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            name = data['Name']
            type = data['AssetTypeId']
            creator = data['Creator']['Name']
            netw_error = None
        else:
            name = None
            creator = None
            type = None
            netw_error = f"{data.status_code}: Error getting Accessory Info"
        return name, type, creator, netw_error 
    
    ### Get Item Thumbnail ###
    async def get_acc_thumb(self, id, type):
        rbx_size = '250x250'
        rbx_format = 'Png'
        rbx_isCircular = 'false'
        url = f"https://thumbnails.roblox.com/v1/assets?assetIds={id}&returnPolicy=PlaceHolder&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}"     
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            try:
                img_url = data["data"][0]["imageUrl"]
            except:
                netw_error = f"{data.status_code}: Error, Invalid {type}"
                img_url = None
            else:
                netw_error = None
        else:
            img_url = None
            netw_error = f"{data.status_code}: Error getting {type} IMG URL"
        return img_url, netw_error      
    
    ### Get items Data by URL ###
    async def get_url_data(self, img_url): 
        data = requests.get(img_url)
        if data.status_code == 200:
            image_data = data.content
            netw_error = None
        else:
            netw_error = f"{data.status_code}: Error getting IMG Data"
        return image_data, netw_error
 
    ### Get items Data by ID ###
    async def get_id_data(self, id, type):
        url = f"https://assetdelivery.roblox.com/v1/asset?id={id}" 
        data = requests.get(url)
        if data.status_code == 200:
            data = data.content
            netw_error = None
        else:
            netw_error = f"{data.status_code}: Error getting {type} Data"
        return data, netw_error       
        
         

######### Hair Buttons ###########    
class BUTTON_HAIR(bpy.types.Operator):
    bl_label = "BUTTON_HAIR"
    bl_idname = "object.button_hair"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_hair : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs         
        rbx_hair = self.rbx_hair
        rbx_mode = None

        global rbx_bkd_hair_img
                               
        if rbx_hair == 'hair_template':    
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects                

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='Hair Template')
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print("Hair Template Spawned")
            
            
        if rbx_hair == 'hair_shader':    
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects 
                               
            if bpy.data.collections.get('Hair Shader') == None:
                bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='Hair Shader')
                
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print("Hair Shader Spawned")            


        if rbx_hair == 'hair_bake':    
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects 
                              
            rbx_bake_hair = bpy.data.objects['Bake']
            
            try:
                rbx_bkd_hair_img = bpy.data.objects['Hair Color'].active_material.node_tree.nodes['Image Texture'].image
            except:
                pass

                
            bpy.ops.object.select_all(action='DESELECT')
            rbx_bake_hair.hide_viewport = False
            rbx_bake_hair.select_set(True)
            bpy.context.view_layer.objects.active = rbx_bake_hair
            
            bpy.context.scene.cycles.samples = 1
            bpy.context.scene.cycles.bake_type = 'DIFFUSE'
            bpy.context.scene.render.bake.use_pass_direct = False
            bpy.context.scene.render.bake.use_pass_indirect = False
            bpy.context.scene.render.engine = 'CYCLES'
            bpy.ops.object.bake(type='DIFFUSE')
            
            rbx_bake_hair.hide_viewport = True
            bpy.ops.object.select_all(action='DESELECT')
            
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print("Hair Texture Baked") 
        
        if rbx_hair == 'hair_save':
            # Call user prefs window
            bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
            # Change area type
            area = bpy.context.window_manager.windows[-1].screen.areas[0]
            area.type = 'IMAGE_EDITOR'
            area.spaces.active.image = rbx_bkd_hair_img
            print(rbx_bkd_hair_img)
            
        '''    
            bpy.ops.image.save_as(filepath="", save_as_render=False, relative_path=False, show_multiview=False, use_multiview=False)    
                        
            #bpy.ops.export_scene.fbx('INVOKE_DEFAULT', use_selection=True, object_types={'MESH'}, global_scale=0.01, bake_anim=False)
            #bpy.ops.image.save_as(save_as_render=False, filepath="C:\\Users\\User\\Downloads\\Hair_diffuse_512.004.png", relative_path=False, show_multiview=False, use_multiview=False)
        '''
                
        return {'FINISHED'} 
    
        

######### Layered Clothing Buttons ###########    
class RBX_BUTTON_LC(bpy.types.Operator):
    bl_label = "RBX_BUTTON_LC"
    bl_idname = "object.rbx_button_lc"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_lc : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_lc = self.rbx_lc
        rbx_lc_spwn = None 
        rbx_mode = None
        
        lc_dum_list = [
                        'Default Mannequin',
                        'Roblox Boy',
                        'Roblox Girl',
                        'Roblox Man',
                        'Roblox Woman',
                        'Classic Male',
                        'Classic Female',
                        'Roblox Blocky'
                        ] 
                        
        lc_spl_list = [
                        'Female Hair',
                        'Hoodie',
                        'Cargo Pants',
                        'Skate',
                        'Tennis'
                        ]                             
        
        
        if bpy.context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
            rbx_mode = 1
            rbx_sel = bpy.context.selected_objects

        if rbx_lc == 'sample':
            for x in range(len(lc_spl_list)):
                if rbx_prefs.rbx_lc_spl_enum == 'OP' + str(x+1):
                    rbx_lc_spwn = lc_spl_list[x]
            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename =rbx_lc_spwn) 
            bpy.data.collections[rbx_lc_spwn].hide_viewport = False
            print(rbx_lc_spwn + " Sample Spawned") 
        else:
            for x in range(len(lc_dum_list)):
                if rbx_prefs.rbx_lc_dum_enum == 'OP' + str(x+1):
                    rbx_lc_spwn = lc_dum_list[x] + rbx_lc     
                           

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename =rbx_lc_spwn)
            
            rbx_lc_spwn_split = rbx_lc_spwn.rsplit('_')
            if rbx_lc == '_Arma':
                print(rbx_lc_spwn_split[0] + " Inner Cage Spawned")
            if rbx_lc == '_Cage':
                print(rbx_lc_spwn_split[0] + " Outer Cage Spawned") 
                
        if rbx_mode == 1:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[rbx_sel[0].name].select_set(True)            
            bpy.ops.object.editmode_toggle()
                           
        
        return {'FINISHED'}              


######### Layered Clothing Animation ########### 
class RBX_BUTTON_LC_ANIM(bpy.types.Operator):
    bl_label = "RBX_BUTTON_LC_ANIM"
    bl_idname = "object.rbx_button_lc_anim"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_lc_anim : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        global rbx_anim_error
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_lc_anim = self.rbx_lc_anim
        rbx_anim_error = None
        
        lc_dum_list = [
                        'R15 Woman Rig',
                        'R15 Blocky Rig'
                        ]
                        
        lc_anim_list_wom = [
                        'No Animation',
                        'Chapa-Giratoria_LC_wom',
                        'Hokey Pokey_LC_wom',
                        'Rumba Dancing_LC_wom'
                        ]

        lc_anim_list_blk = [
                        'No Animation',
                        'Chapa-Giratoria_LC_blk',
                        'Hokey Pokey_LC_blk',
                        'Rumba Dancing_LC_blk'
                        ]
                        
        if rbx_lc_anim == 'add':
            
            ### Check selected objects ###
            if bpy.context.mode != 'EDIT_MESH':
                rbx_object = bpy.context.selected_objects
                if len(rbx_object) == 1:
                    rbx_object = bpy.context.selected_objects[0]
                    if rbx_object.type == 'ARMATURE':
                        rbx_anim_error = None
                    else:
                        rbx_anim_error = "Error: Pls Select Armature"
                else:
                    rbx_anim_error = "Error: Pls Select 1 Object"
            else:
                rbx_anim_error = "Error: Pls Exit Edit Mode"


            if rbx_anim_error == None:
                
                ### Adding Characters ###
                rbx_anim_dum_spwn = 'R15 Woman Rig'
                x = 0
                for dum in lc_dum_list:
                    if rbx_prefs.rbx_lc_dum_anim_enum == f'OP{x+1}':
                        rbx_anim_dum_spwn = dum
                        break
                    x +=1
                
                ### Add rig and move ###
                bpy.ops.view3d.snap_cursor_to_center()
                bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename =rbx_anim_dum_spwn)
                bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                bpy.ops.transform.translate(value=(5, -0, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')

                ### Create new collection ###
                rbx_rig_collection = bpy.context.selected_objects[0].users_collection
                rbx_rig_collection = rbx_rig_collection[0]
                rbx_anim_collection = bpy.data.collections.new("LC_Animation")
                bpy.context.scene.collection.children.link(rbx_anim_collection)                    
                
                ### Clear parent from parts ###
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                for part in rbx_rig_collection.all_objects:
                    if "Geo" in part.name:
                        bpy.data.objects[part.name].select_set(True)
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                
                ### Move parts to new collection and delete rig collection ###
                for obj in bpy.context.selected_objects:
                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                    rbx_anim_collection.objects.link(obj)
                bpy.data.collections.remove(rbx_rig_collection)


                ### Duplicate LC Arma and item ###
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                bpy.data.objects[rbx_object.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object.name]
                rbx_object_collection = bpy.ops.object.select_grouped(type='COLLECTION')
                for item in bpy.context.selected_objects:
                    if "Att" in item.name:
                        bpy.data.objects[item.name].hide_viewport = True
                bpy.data.objects[rbx_object.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object.name]
                bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(5, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 1, 0)), "orient_matrix_type":'GLOBAL'})
                
                ### Move LC Arma and item to new collection ###
                for obj in bpy.context.selected_objects:
                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                    rbx_anim_collection.objects.link(obj)
                
                ### Select Duplicated Arma in new collection ###
                for part in rbx_anim_collection.all_objects:
                    if part.type == 'ARMATURE':
                        rbx_object_copy = part
                                        
                ### Parent parts to LC Arma bones ###
                def parentBone(rig, part):
                    bpy.ops.object.mode_set(mode='EDIT')
                    for bone in rig.data.edit_bones:
                        if bone.name in part.name:
                            bpy.ops.armature.select_all(action='DESELECT')
                            bone.select = True
                            rig.data.edit_bones.active = bone
                            bpy.ops.object.mode_set(mode='OBJECT')
                            bpy.ops.object.select_all(action='DESELECT')
                            bpy.data.objects[part.name].select_set(True)
                            bpy.data.objects[rig.name].select_set(True)
                            bpy.context.view_layer.objects.active = bpy.data.objects[rig.name]
                            bpy.ops.object.parent_set(type='BONE')
                            break

                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None 
                bpy.data.objects[rbx_object_copy.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object_copy.name] 
                for part in rbx_anim_collection.all_objects:
                    parentBone(rbx_object_copy, part)
                bpy.ops.object.mode_set(mode='OBJECT')
                
                ### Select Copy of LC Bones and make active ###
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_object_copy.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object_copy.name]
 
                
                ### Adding Animations ### 
                rbx_anim_spwn = None
                
                if rbx_prefs.rbx_lc_dum_anim_enum == 'OP1':
                    lc_anim_list = lc_anim_list_wom
                if rbx_prefs.rbx_lc_dum_anim_enum == 'OP2':
                    lc_anim_list = lc_anim_list_blk
                    
                x = 0
                for anim in lc_anim_list:
                    if rbx_prefs.rbx_lc_anim_enum == f'OP{x+1}':
                        rbx_anim_spwn = anim
                        break
                    x +=1
                    
                if anim == 'No Animation':
                    pass
                else:
                    ### Append Animation ###
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None 
                    bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, filename =rbx_anim_spwn)
                    rbx_added_anim = bpy.context.selected_objects[0]
                    
                    ### Select Object and animation and link Data ###
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.data.objects[rbx_object_copy.name].select_set(True)
                    bpy.data.objects[rbx_added_anim.name].select_set(True)
                    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_added_anim.name]  
                    bpy.ops.object.make_links_data(type='ANIMATION')
                    
                    ### Select Appended Animation and delete it ###
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.data.objects[rbx_added_anim.name].select_set(True)  
                    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_added_anim.name]  
                    bpy.ops.object.delete(use_global=False)
                    
                    ### Select Copy of LC Bones and make active ###
                    bpy.data.objects[rbx_object_copy.name].select_set(True)
                    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object_copy.name]
                          
                
                           
        
        return {'FINISHED'}   
    
            
        
######### Bounds Buttons ###########    
class BUTTON_BNDS(bpy.types.Operator):
    bl_label = "BUTTON_BNDS"
    bl_idname = "object.button_bnds"
    bl_options = {'REGISTER', 'UNDO'}
    bnds : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        bnds = self.bnds
        bnds_spwn = None
        
        '''        
        if mode == 0:
            rbx_asset_folder = rbx_ast_fldr
        else:
            rbx_asset_folder = bpy.context.preferences.addons['RBX_Toolbox'].preferences.rbx_asset_folder
        '''
        
        rbx_bnds_list = [
                        'Hat',
                        'Hair',
                        'Face Center',
                        'Face Front',
                        'Neck',
                        'Front',
                        'Back',
                        'Shoulder Right',
                        'Shoulder Left',
                        'Shoulder Neck',
                        'Waist Back',
                        'Waist Front',
                        'Waist Center'
                        ] 
                 
                 
        for x in range(len(rbx_bnds_list)):
            if rbx_prefs.rbx_bnds_enum == 'OP' + str(x+1):
                bnds_spwn = rbx_bnds_list[x]
        
        ### Without Dummy ###            
        bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='UGC '+ bnds_spwn + ' Bounds')                            
                             
        ### Add Dummy ###
        if rbx_prefs.rbx_bnds_hide == False:
            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, filename ='R15 Blocky')
            rbx_col_num = len(bpy.data.collections)
            bpy.ops.object.move_to_collection(collection_index=rbx_col_num)
        
        print(bnds_spwn + " Boundary Spawned")

        return {'FINISHED'}      
   

######### Camera Buttons ###########    
class BUTTON_CMR(bpy.types.Operator):
    bl_label = "BUTTON_CMR"
    bl_idname = "object.button_cmr"
    bl_options = {'REGISTER', 'UNDO'}
    cmr : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        cmr = self.cmr
        cmr_spl = cmr.rsplit('_',1)
        
        #### Apend Cameras Stage ####
        if cmr == 'append':               
            if bpy.data.objects.get('Camera_F') == None:
                bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='Cameras')
                bpy.context.scene.render.resolution_x = 1080
                bpy.context.scene.render.resolution_y = 1080
                bpy.context.scene.render.resolution_percentage = 100
                print("Cameras Setup Spawned")
            else:
                print("Cameras Setup Already Exist")

        #### Apend Cameras Stage ####
        if cmr == 'edtr_append':               
            if bpy.data.objects.get('Avatar Editor Camera') == None:
                bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='Avatar Editor Room (New)')
                bpy.context.scene.render.resolution_x = 1080
                bpy.context.scene.render.resolution_y = 1080
                bpy.context.scene.render.resolution_percentage = 100
                print("Avatar Editor Room Setup Spawned")
            else:
                print("Avatar Editor Room Setup Already Exist") 
            if bpy.context.scene.world != 'Avatar Editor Stage (New) World':
                if 'Avatar Editor Stage (New) World' not in bpy.data.worlds:
                    bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_world, filename ='Avatar Editor Stage (New) World')
                rbx_hdri = bpy.data.worlds['Avatar Editor Stage (New) World']
                scene.world = rbx_hdri
            
        
        #### Set Active ####        
        if cmr_spl[-1] == 'active':
            cam = bpy.data.objects[cmr_spl[0]]
            bpy.data.scenes['Scene'].camera = cam
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects[cmr_spl[0]].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[cmr_spl[0]]
            print(cmr_spl[0] + " Set as Active")
            
        #### Preview ####        
        if cmr == 'preview':
            try:
                for i in range(len(cams)):
                    if bpy.context.active_object.name == cams[i]:
                        bpy.ops.view3d.object_as_camera()
            except:
                pass


            
        #### Add Animated Staging ####    
        if cmr == 'staging':
            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename='Staging')
            print("Animated Staging Setup Appended")

        #### Set Active (Staging cam) ####        
        if cmr == 'staging-active':
            cam = bpy.data.objects['Staging Camera']
            bpy.data.scenes['Scene'].camera = cam
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects['Staging Camera'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Staging Camera']
            print("'Staging Camera' Set as Active")
            del cam 
            
        #### Set Active (Avatar Editor Room cam) ####        
        if cmr == 'edtr-active':
            cam = bpy.data.objects['Avatar Editor Camera']
            bpy.data.scenes['Scene'].camera = cam
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects['Avatar Editor Camera'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Avatar Editor Camera']
            print("'Avatar Editor Camera' Set as Active")
            del cam                         


        #### Append Roblox Baseplate ####
        if cmr == 'bsplt_append':               
            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_collection, filename ='RBX Baseplate')
                
                                                                                                                        
        return {'FINISHED'}      

 
######### Armature Buttons ###########    
class BUTTON_BN(bpy.types.Operator):
    bl_label = "BUTTON_BN"
    bl_idname = "object.button_bn"
    bl_options = {'REGISTER', 'UNDO'}
    bn : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        bn = self.bn
        global bn_selection
        global bn_error
        global msh_selection
        global msh_error
        bn_error = None
        msh_error = None


        bn_items = [
                    'Character_bones_blocky',
                    'Character_bones_r15_boy',
                    'Character_bones_r15_girl',
                    'Character_bones_r15_woman',
                    'Character_bones_rth_boy',
                    'Character_bones_rth_girl',
                    'Character_bones_rth_normal',
                    'Character_bones_rth_slender'
                    ] 
      
        
        #### Append Armature ####
        bn_split = bn.rsplit('_')
        
        if bn_split[-1] == 'arma':
            for x in range(len(bn_items)):
                if rbx_prefs.rbx_arma_enum == 'OP' + str(x+1):
                    rbx_arma_spwn = bn_items[x]                  

            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, filename =rbx_arma_spwn)            
            bn_sel = bpy.context.selected_objects[0].name
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects[bn_sel].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[bn_sel]
            print("Armature Appended")

 
        #### Recalculate Normals ####
        if bn == 'normal':
            bn_mesh = 0
            sel = bpy.context.selected_objects
            if len(sel) < 1:
                print("Nothing Selected")
                msh_selection = "Nothing Selected"                
            else:
                for x in sel:
                    if x.type != 'MESH':
                        print(x.type + " Selected. Pls Select Only Mesh")
                        msh_selection = "Pls Select Only Mesh"
                        bn_mesh = 0
                    else:
                        bn_mesh = 1
                        msh_selection = None
                if bn_mesh == 1:
                    if bpy.context.mode == 'OBJECT':
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')                
                    elif bpy.context.mode == 'EDIT_MESH':
                        bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                    bpy.ops.object.editmode_toggle()
                    msh_error = 'done_nml'
                    print("Normals Recalculated")
            
        #### Remove Duplicated Vertices ####
        if bn == 'doubles':
            bn_mesh = 0
            sel = bpy.context.selected_objects
            if len(sel) < 1:
                print("Nothing Selected")
                msh_selection = "Nothing Selected"
            else:
                for x in sel:
                    if x.type != 'MESH':
                        print(x.type + " Selected. Pls Select Only Mesh")
                        msh_selection = "Pls Select Only Mesh"
                        bn_mesh = 0
                    else:
                        bn_mesh = 1
                        msh_selection = None
                if bn_mesh == 1:
                    if bpy.context.mode == 'OBJECT':
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')                
                    elif bpy.context.mode == 'EDIT_MESH':
                        bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                    bpy.ops.object.editmode_toggle()
 
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    bpy.context.object.data.use_auto_smooth = False
                        
                    msh_error = 'done_vts'
                    print("Doubles Removed")
                        
        #### Parent Armature ####
        if bn == 'parent':
            bn_arma = 0
            bn_mesh = 0
            
            sel = bpy.context.selected_objects
            if len(sel) < 1:
                print("Nothing Selected")
                bn_selection = "Nothing Selected"
            else:
                print(sel)
                if len(sel) > 2:
                    print("More than 2 Objects selected")
                    bn_selection = "More than 2 Objects selected"
                else:
                    if len(sel) < 2:
                        print("2 Objects Must be Selected")
                        bn_selection = "Select 2 Objects"
                    else:
                        for x in sel:
                            if x.type == 'ARMATURE':
                                bn_arma = 1
                                break
                        if bn_arma == 0:
                            print("No Bones Selected")
                            bn_selection = "No Bones Selected"
                        for x in sel:
                            if x.type == 'MESH':
                                bn_mesh = 1
                                break
                        if bn_mesh == 0:
                            print("No Mesh Selected")
                            bn_selection = "No Mesh Selected"
                                
            if bn_arma == 1 and bn_mesh == 1:
                bn_selection = None
                bn_active = bpy.context.view_layer.objects.active
                if bn_active.type != 'ARMATURE':
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None
                    for x in sel:
                        if x.type == 'ARMATURE':
                            bpy.data.objects[x.name].select_set(True)
                            bpy.context.view_layer.objects.active = bpy.data.objects[x.name]
                        else:
                            bpy.data.objects[x.name].select_set(True)     
                try:
                    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
                except:
                    bn_error = 1
                else:
                    print("Bones Successfully Parented")
                    bn_error = 2
                    

        return {'FINISHED'}             
                
                
                
                
                                                                                                                    
        return {'FINISHED'}   
    
    
######### Other Functions ###########    
class RBX_BUTTON_OF(bpy.types.Operator):
    bl_label = "RBX_BUTTON_OF"
    bl_idname = "object.rbx_button_of"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_of : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        rbx_of = self.rbx_of
        
        
        if rbx_of == 'inside' or rbx_of == 'outside':
            def rbx_of_recalc():
                if rbx_of == 'outside':
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                if rbx_of == 'inside':
                    bpy.ops.mesh.normals_make_consistent(inside=True)
         
     
            #### Recalculate Normals ####
            rbx_sel = bpy.context.selected_objects
            of_mesh = 0
            if len(rbx_sel) < 1:
                print("Nothing Selected")             
            else:
                for x in rbx_sel:
                    if x.type != 'MESH':
                        print(x.type + " Selected. Pls Select Only Mesh")
                        msh_selection = "Pls Select Only Mesh"
                        of_mesh = 0
                    else:
                        of_mesh = 1
                        msh_selection = None
                if of_mesh == 1:
                    if bpy.context.mode == 'OBJECT':
                        bpy.ops.object.editmode_toggle()
                        if rbx_prefs.rbx_face_enum == 'OP1':
                            rbx_of_recalc()
                        if rbx_prefs.rbx_face_enum == 'OP2':
                            bpy.ops.mesh.select_all(action='SELECT')
                            rbx_of_recalc()
                        bpy.ops.object.editmode_toggle()               
                    elif bpy.context.mode == 'EDIT_MESH':
                        if rbx_prefs.rbx_face_enum == 'OP1':
                            rbx_of_recalc()
                        if rbx_prefs.rbx_face_enum == 'OP2':
                            bpy.ops.mesh.select_all(action='SELECT')
                            rbx_of_recalc()

                print("Normals Recalculated")
           
 
        if rbx_of == 'theme_install':
            file = "Theme/RBXToolbox.xml"
            path = os.path.join(addon_path, file)
            bpy.ops.preferences.theme_install(overwrite=True, filepath=path, filter_folder=True, filter_glob="*.xml")
            #bpy.ops.preferences.reset_default_theme()     
        
        
                                                                                                                           
        return {'FINISHED'}      
 

    
    #PANEL UI
####################################
class TOOLBOX_MENU(bpy.types.Panel):
    bl_label = "Roblox Toolbox (" + disp_ver + ")"
    bl_idname = "RBX_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "RBX Tools"
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        
        
        ######## Update Notifier ########
        try:
            if lts_ver > ver:
                box = layout.box()
                #box.label(text = "Addon Update Available: " + lts_ver, icon='IMPORT') 
                box.operator('object.url_handler', text = "Update Available: " + lts_ver, icon='IMPORT').rbx_link = "update"    
        except:
            pass
            
        ######## Set Correct Units ########
        '''
        rbx_length = bpy.context.scene.unit_settings.scale_length
        rbx_unit = bpy.context.scene.unit_settings.length_unit

        if rbx_length == 1 or rbx_unit == 'METERS':
            box = layout.box()
            box.operator('object.rbx_operators', text = "Set Correct Units", icon='ERROR').rbx_operator = 'set_unit'
            box.label(text = " (Length is 0.01;   Units is 'CM')")
        '''
           
        
        '''       
        ######## ASSETS ########                
        if mode == 0:
            addon_assets = rbx_prefs
            rbx_folder = 'recolor_folder'
        else:
            addon_assets =bpy.context.preferences.addons['RBX_Toolbox'].preferences
            rbx_folder = 'rbx_asset_folder'
        
        ######## Check if Asset Folder installed ######## 
        if mode == 0:
            rbx_asset_folder = rbx_ast_fldr
            rbx_asset_folder_set = rbx_asset_folder
        else:
            rbx_asset_folder_set =bpy.context.preferences.addons['RBX_Toolbox'].preferences.rbx_asset_folder
        rbx_assets_set = 0

        if os.path.exists(rbx_asset_folder_set) == True:
            dir = os.listdir(rbx_asset_folder_set)
            for x in range(len(dir)):
                if "Bounds.blend" in dir[x]:
                    #print("Found UGC 'Bounds.blend' file, related features unlocked")
                    rbx_assets_set = 1
                    break
                else:
                   rbx_assets_set = 2 
        '''  
                        
        ######### Readme ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_readme else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_readme', icon=icon, icon_only=True)
        row.label(text = "Readme", icon= "ASSET_MANAGER")
        # some data on the subpanel
        if context.scene.subpanel_readme:
            box = layout.box()
            box.operator('object.url_handler', text = "Read Instructions, Credits", icon='ARMATURE_DATA').rbx_link = "Credits and Instructions"
            box.operator('object.url_handler', text = "Read Version Log", icon='CON_ARMATURE').rbx_link = "Version_log" 
            
            
            box = layout.box()
            box.label(text = 'R15 rigs are taken from here:')
            box.operator('object.url_handler', text = "Roblox Github", icon='URL').rbx_link = "rbx github"
            box.label(text = 'R6 Rig taken from here:')
            box.operator('object.url_handler', text = "Nuke Youtube", icon='URL').rbx_link = "rbx nuke"
            box.label(text = 'You can see here how to link')
            box.label(text = 'texture to R6 rig')
            
            '''
            if rbx_assets_set != 1:
                box.label(text = "To unlock additional features")
                box.label(text = "Specify folder with UGC")
                box.label(text = "blend file 'Bounds.blend'")
            row = layout.row()
            box.prop(addon_assets, rbx_folder)
            if rbx_assets_set == 1:
                box.label(text = "'Bounds.blend' linked to addon")
            if rbx_assets_set == 2:
                box.label(text = "'Bounds.blend' not found")
            '''

        ######### HDRI ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_hdri else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_hdri', icon=icon, icon_only=True)
        row.label(text = "HDRI & Templates", icon= "WORLD")
        # some data on the subpanel
        if context.scene.subpanel_hdri:
            box = layout.box()
            box.label(text = "Blender built-in HDRIs", icon ='NODE_MATERIAL')
            box.prop(rbx_prefs, 'rbx_hdri_enum')
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text = "")
            split.operator("object.rbx_button_hdrifull", text = "Set as HDRI").rbx_hdri = 'hdri'
            try:
                wrld = bpy.context.scene.world.name
            except:
                pass
            else:
                box.label(text='** Current World Controls: **')
                wrld_0 = bpy.data.worlds[wrld].node_tree.nodes['Background'].inputs['Strength']
                wrld_1 = None
                if wrld == 'HDRI':
                    wrld_1 = bpy.data.worlds[wrld].node_tree.nodes['Mapping'].inputs['Rotation'] 
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(wrld_0, "default_value", text = "")
                if wrld == 'HDRI':
                    split = box.split(factor = 0.5)
                    col = split.column(align = True)
                    col.label(text='Rotationn:')
                    split.prop(wrld_1, "default_value", text = "") 
                    
                    
            #### Set Sky ####  
            box = layout.box()      
            box.label(text = "Simple Skybox", icon ='WORLD_DATA')
            box.prop(rbx_prefs, 'rbx_sky_enum')
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text = "")
            split.operator("object.rbx_button_hdrifull", text = "Set Sky").rbx_hdri = 'sky'
            try:
                sky = bpy.data.objects['Sky Sphere']
            except:
                pass
            else:
                box.label(text='** Skybox Controls: **') 
                sky_0 = bpy.data.objects['Sky Sphere'].active_material.node_tree.nodes['Mapping'].inputs['Location']
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Rotation:')
                split.prop(sky_0, 'default_value', text = "")
            box.label(text='*You may setup your own')
            box.label(text=' Skybox in Shading tab')                  


            ##### Animated Staging #####
            box = layout.box()
            box.operator('object.button_cmr', text = "Add Animated Staging", icon='IMPORT').cmr = 'staging'                        
            try:
                bpy.data.objects['Staging Camera']
            except:
                pass
            else:               
                #box = layout.box()
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Camera:')
                split.operator('object.button_cmr', text = "Set Active").cmr = 'staging-active'
            try:
                bkdrp = bpy.data.objects['Floor Plane']
            except:
                pass
            else:
                bkdrp_0 = bpy.data.objects['Floor Plane'].active_material.node_tree.nodes['Principled BSDF'].inputs['Base Color']
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Backdrop:')
                split.prop(bkdrp_0, 'default_value', text = "")

            ##### Avatar Editor Room (New) #####
            box = layout.box()
            box.operator('object.button_cmr', text = "Add Avatar Editor Room", icon='IMPORT').cmr = 'edtr_append'                        
            try:
                bpy.data.objects['Avatar Editor Camera']
            except:
                pass
            else:               
                #box = layout.box()
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Camera:')
                split.operator('object.button_cmr', text = "Set Active").cmr = 'edtr-active'
                
                
            ##### Roblox Baseplate #####
            box = layout.box()
            box.operator('object.button_cmr', text = "Add Roblox Baseplate", icon='IMPORT').cmr = 'bsplt_append'                        
                
                
                
        ######### Import Characters and Accessories #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_imp_char else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_imp_char', icon=icon, icon_only=True)
        row.label(text='Import From Roblox', icon='IMPORT')
        # some data on the subpanel
        if context.scene.subpanel_imp_char:
            #row = layout.row()
            #row.label(text = 'Take Note!!', icon='ERROR')
            #row = layout.row()
            #row.label(text = 'Often Roblox refuses to share files')
            #row = layout.row()
            #row.label(text = 'So try to get it another time')
            box = layout.box()
            box.label(text = 'Enter ID, URL or Username')
            box.prop(rbx_prefs, 'rbx_username', text ='')
            box.operator('object.add_character', text = "Preview").rbx_char = "preview" 
            box.prop(rbx_prefs, 'rbx_split', text ='Separate Accessories')              
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.operator('object.add_character', text = "Import").rbx_char = "import"
            split.operator('object.add_character', text = "Open Folder").rbx_char = "folder"
            
            try:
                #rbx_avat_img_prev = bpy.data.images[rbx_prefs.rbx_username + '.png']
                rbx_avat_img_prev = bpy.data.images[rbx_username + '.png']
            except:
                box.separator()
                box.separator()
                box.separator()
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
                '''
                try:
                    rbx_avat_img_prev = bpy.data.images['blanc.png'] 
                except:
                    pass
                else:
                    rbx_avat_img_prev.preview_ensure()
                    box.template_icon(rbx_avat_img_prev.preview.icon_id, scale=10.0)
                '''
            else:
                rbx_avat_img_prev.preview_ensure()
                box.template_icon(rbx_avat_img_prev.preview.icon_id, scale=10.0)


            if rbx_char_netw_error:
                box.label(text = rbx_char_netw_error, icon='ERROR')
                try:
                    rbx_asset_img_prev = bpy.data.images[rbx_username + '.png']
                except:
                    pass 
                                                  
            
            ######### Import Accessory #########    
            box = layout.box()
            box.label(text = 'Accessory ID or URL')
            box.prop(rbx_prefs, 'rbx_accessory', text ='')
            #box.prop(rbx_prefs, 'rbx_bundle', text ='Tick for Bundle') 
            box.operator('object.add_character', text = "Preview").rbx_char = "preview_accessory"      
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.operator('object.add_character', text = "Import").rbx_char = "import_accessory"
            split.operator('object.add_character', text = "Open Folder").rbx_char = "folder_accessory"

            try:
                #rbx_asset_img_prev = bpy.data.images[rbx_prefs.rbx_accessory + '.png']
                rbx_asset_img_prev = bpy.data.images[rbx_accessory + '.png']
            except:
                box.separator()
                box.separator()
                box.separator()
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
                box.label(text = '')
            else:
                rbx_asset_img_prev.preview_ensure()
                box.template_icon(rbx_asset_img_prev.preview.icon_id, scale=10.0)
            
                if rbx_asset_name:
                    if rbx_prefs.rbx_accessory:
                        box.label(text = 'Name: ' + rbx_asset_name)
                        box.label(text = 'Type: ' + rbx_asset_type_name)
                        box.label(text = 'Creator: ' + rbx_asset_creator)
                    
            if rbx_asset_netw_error:
                box.label(text = rbx_asset_netw_error, icon='ERROR')
                try:
                    rbx_asset_img_prev = bpy.data.images[rbx_accessory + '.png']
                except:
                    pass 
                                           
                                        
        ######### Bounds #########
        #if rbx_assets_set == 1:
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_bounds else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_bounds', icon=icon, icon_only=True)
        row.label(text='Accessory Bounds', icon='CUBE')
        # some data on the subpanel
        if context.scene.subpanel_bounds:
            box = layout.box()
            box.prop(rbx_prefs, 'rbx_bnds_enum', text ='Bounds')
            box.prop(rbx_prefs, 'rbx_bnds_hide')                
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")
            split.operator('object.button_bnds', text = "Spawn")
                

        
        ######### Dummies #########
        row = layout.row()     
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_dummy else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_dummy', icon=icon, icon_only=True)
        row.label(text='Dummy', icon='OUTLINER_OB_ARMATURE')
        # some data on the subpanel
        if context.scene.subpanel_dummy:
            box = layout.box()
            box.label(text = 'Dummies')
            box.prop(rbx_prefs, 'rbx_dum_enum', text ='')
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")            
            split.operator('object.button_dmmy', text = "Spawn").dmy = 'Dummy'
            
            box.separator()
            box.operator('object.button_dmmy', text = "Add Rigged R6").dmy = 'rigged_r6'
            box.operator('object.button_dmmy', text = "R15 Blocky Rig").dmy = 'rigged_r15_blocky'
            box.operator('object.button_dmmy', text = "R15 Woman Rig").dmy = 'rigged_r15_woman'
            
            
            
            
            
            ######### Wear Clothing #########
            box = layout.box()
            box.label(text = 'Wear Character (Select Armature)')
            box.label(text = 'Currently Only R6 Rig is supported')
            box.operator('object.button_wear', text = "Modify Character").rbx_cloth = 'mod'
            
            cloth_panel = False
            try:
                rbx_object = bpy.context.selected_objects
                if len(rbx_object) == 1:
                    rbx_object = bpy.context.selected_objects[0]
                    if rbx_object.type == 'ARMATURE':
                        if 'cloth_mod' in rbx_object.name:
                            cloth_panel = True
                        else:
                            cloth_panel = False
                    else:
                        cloth_panel = False
                else:
                    cloth_panel = False
            except:
                pass 
            if cloth_panel == True:
                box = layout.box()
                box.label(text = '- - - - - - - - - - - HEAD - - - - - - - - - - -')
                #box.label(text = 'Head')
                rbx_cloth_head = bpy.data.materials[f"R6 Head_{rbx_object.name}"].node_tree.nodes['R6 Cloth']
                cloth_head = rbx_cloth_head.inputs['Skin Tone']
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Skin Tone:')
                split.prop(cloth_head, "default_value", text = "")
                if rbx_face_filename == None:
                    box.label(text = 'Loaded Face: None')
                else:
                    box.label(text = f'Loaded Face: {rbx_face_name}')
                box.label(text = 'Enter Face ID or URL')
                box.prop(rbx_prefs, 'rbx_face', text ='')
                box.operator('object.button_wear', text = "Import").rbx_cloth = 'face'
                if rbx_face_netw_error != None:
                    box.label(text = rbx_face_netw_error, icon='ERROR') 
                #box.label(text = '')
                
                
                box = layout.box()
                box.label(text = '- - - - - - - - - - - SHIRT - - - - - - - - - - -')
                #box.label(text = 'Shirt')
                rbx_cloth_shirt = bpy.data.materials[f"R6 Shirt_{rbx_object.name}"].node_tree.nodes['R6 Cloth']
                cloth_shirt = rbx_cloth_shirt.inputs['Skin Tone']
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Skin Tone:')
                split.prop(cloth_shirt, "default_value", text = "")
                if rbx_shirt_filename == None:
                    box.label(text = 'Loaded Shirt: None')
                else:
                    box.label(text = f'Loaded Shirt: {rbx_shirt_name}')
                box.label(text = 'Enter Shirt ID or URL')
                box.prop(rbx_prefs, 'rbx_shirt', text ='')
                box.operator('object.button_wear', text = "Import").rbx_cloth = 'shirt'
                if rbx_shirt_netw_error != None:
                    box.label(text = rbx_shirt_netw_error, icon='ERROR') 
                #box.label(text = '')
                
                
                box = layout.box()
                box.label(text = '- - - - - - - - - - - TORSO - - - - - - - - - -')
                #box.label(text = 'Torso')
                rbx_cloth_torso = bpy.data.materials[f"R6 Torso_{rbx_object.name}"].node_tree.nodes['R6 Cloth']
                cloth_torso = rbx_cloth_torso.inputs['Skin Tone']
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Skin Tone:')
                split.prop(cloth_torso, "default_value", text = "")
                if rbx_shirt_filename == None:
                    box.label(text = 'Loaded Shirt: None')
                else:
                    box.label(text = f'Loaded Shirt: {rbx_shirt_name}')
                if rbx_pants_filename == None:
                    box.label(text = 'Loaded Pants: None')
                else:
                    box.label(text = f'Loaded Pants: {rbx_pants_name}')
                #box.label(text = '')
                
                
                box = layout.box()
                box.label(text = '- - - - - - - - - - - PANTS - - - - - - - - - - -')
                #box.label(text = 'Pants')
                rbx_cloth_pants = bpy.data.materials[f"R6 Pants_{rbx_object.name}"].node_tree.nodes['R6 Cloth']
                cloth_pants = rbx_cloth_pants.inputs['Skin Tone']
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Skin Tone:')
                split.prop(cloth_pants, "default_value", text = "")
                if rbx_pants_filename == None:
                    box.label(text = 'Loaded Pants: None')
                else:
                    box.label(text = f'Loaded Pants: {rbx_pants_name}')
                box.label(text = 'Enter Pants ID or URL')
                box.prop(rbx_prefs, 'rbx_pants', text ='')
                box.operator('object.button_wear', text = "Import").rbx_cloth = 'pants'
                if rbx_pants_netw_error != None:
                    box.label(text = rbx_pants_netw_error, icon='ERROR') 
                
                box.label(text = '')
                box.operator('object.button_wear', text = "Textures Folder").rbx_cloth = "folder"

                
                
                                  

        ######### Hairs #########
        row = layout.row()     
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_hair else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_hair', icon=icon, icon_only=True)
        row.label(text='Hairs', icon='OUTLINER_OB_FORCE_FIELD')
        # some data on the subpanel
        if context.scene.subpanel_hair:
            box = layout.box()
            box.label(text = 'Dummie Heads Only')
            box.prop(rbx_prefs, 'rbx_dum_hd_enum', text ='')
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")            
            split.operator('object.button_dmmy', text = "Spawn").dmy = 'Dummy_head' 
            
            box.separator()
            split = box.split(factor = 0.7)
            col = split.column(align = True)
            col.label(text='Starter Hair Template:')
            split.operator('object.button_hair', text = "Add").rbx_hair = 'hair_template'
            
            box = layout.box() 
            box.label(text = 'Bake Hair Texture')
            box.operator('object.button_hair', text = "Add Hair Shader").rbx_hair = 'hair_shader'


            try:
                rbx_hair_color = bpy.data.objects['Hair Color']
            except:
                pass
            else:
                rbx_hair_cntrl = rbx_hair_color.active_material.node_tree.nodes['Hair shader v.2.0']
                box.label(text='** Hair Color Controls: **')
                hrs_0 = rbx_hair_cntrl.inputs['Hair Color']
                hrs_1 = rbx_hair_cntrl.inputs['Hair Strands']
                hrs_2 = rbx_hair_cntrl.inputs['Strands Color']
                hrs_3 = rbx_hair_cntrl.inputs['Highlight Color']
                hrs_4 = rbx_hair_cntrl.inputs['Highlight Scale']
                hrs_5 = rbx_hair_cntrl.inputs['Top Position']
                hrs_6 = rbx_hair_cntrl.inputs['Bottom Position']
                hrs_7 = rbx_hair_cntrl.inputs['Bumps']
                
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Hair Color:')
                split.prop(hrs_0, "default_value", text = "")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Hair Strands:')
                split.prop(hrs_1, "default_value", text = "")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Strands Color:')
                split.prop(hrs_2, "default_value", text = "")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Highlight Color:')
                split.prop(hrs_3, "default_value", text = "")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Highlight Scale:')
                split.prop(hrs_4, "default_value", text = "")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Top Position:')
                split.prop(hrs_5, "default_value", text = "")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Bottom Position:')
                split.prop(hrs_6, "default_value", text = "")
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Bumps:')
                split.prop(hrs_7, "default_value", text = "")
            
                box.separator()
                split = box.split(factor = 0.3)
                col = split.column(align = True)
                col.label(text='')
                split.operator('object.button_hair', text = "Bake Texture").rbx_hair = 'hair_bake'

                box.operator('object.button_hair', text = "View Image").rbx_hair = 'hair_save'
                    
                                
                   

        ######### Layered Cloth Dummies #########
        row = layout.row()   
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_lc else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_lc', icon=icon, icon_only=True)
        row.label(text='Layered Cloth', icon='MATCLOTH')
        # some data on the subpanel
        if context.scene.subpanel_lc:
            box = layout.box()
            box.label(text = 'Cages')
            box.prop(rbx_prefs, 'rbx_lc_dum_enum', text ='')
            split = box.split(factor = 0.5)
            col = split.column(align = True) 
            col.operator('object.rbx_button_lc', text = "Cages").rbx_lc = "_Cage"           
            split.operator('object.rbx_button_lc', text = "Armature").rbx_lc = "_Arma"


            box = layout.box()
            try:
                if len(bpy.context.selected_objects) == 1: 
                    for i in bpy.context.selected_objects:
                        if i.type == 'ARMATURE':
                            box.prop(bpy.context.object, 'show_in_front', text ='Show Bones Infront')
                            box.prop(bpy.context.object.data, 'show_names', text ='Show Bone Names')
                else:
                    box.enabled=False
                    box.prop(rbx_prefs, 'rbx_bn_disabled', text ='Show Bones Infront')
                    box.prop(rbx_prefs, 'rbx_bn_disabled', text ='Show Bone Names')  
            except:
                box.enabled=False
                box.prop(rbx_prefs, 'rbx_bn_disabled', text ='Show Bones Infront')
                box.prop(rbx_prefs, 'rbx_bn_disabled', text ='Show Bone Names')   
                
            
            ###### ADD LC ANIMATION ######               
            box = layout.box()
            ### Check selected objects ###
            if bpy.context.mode != 'EDIT_MESH':
                rbx_object = bpy.context.selected_objects
                if len(rbx_object) == 1:
                    rbx_object = bpy.context.selected_objects[0]
                    if rbx_object.type == 'ARMATURE':
                        rbx_anim_error = None
                    else:
                        rbx_anim_error = "Error: Pls Select Armature"
                else:
                    rbx_anim_error = "Error: Pls Select 1 Object"
            else:
                rbx_anim_error = "Error: Pls Exit Edit Mode"
                
                
            if rbx_anim_error != None:
                box.enabled=False
            else:
                box.enabled=True        
            box.label(text = 'LC Animation Check')
            box.label(text = '1. Select LC Armature')
            box.label(text = '2. Select Character to add')
            box.prop(rbx_prefs, 'rbx_lc_dum_anim_enum', text ='')
            box.label(text = '3. Select Animation to add')
            box.label(text = '(Provided by Mixamo.com)')
            box.prop(rbx_prefs, 'rbx_lc_anim_enum', text ='')
            box.label(text = "")
            box.operator('object.rbx_button_lc_anim', text = "Make RIG", icon='RESTRICT_COLOR_ON').rbx_lc_anim = "add"

            
            if rbx_anim_error != None:
                box.label(text = rbx_anim_error, icon='ERROR') 
            else:
                box.label(text = "No Errors", icon='ERROR')             
            
    
    


        ######### Layered Cloth Samples #########
            box = layout.box()
            box.label(text = 'Roblox Samples from Github')
            box.prop(rbx_prefs, 'rbx_lc_spl_enum', text ='')
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")
            split.operator('object.rbx_button_lc', text = "Spawn").rbx_lc = "sample" 
            
            box = layout.box()
            box.operator('object.url_handler', text = "Roblox Github", icon='URL').rbx_link = "rbx github"                         
            
                    
        ######### Cameras #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_cams else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_cams', icon=icon, icon_only=True)
        row.label(text='Cameras and Lights', icon='CAMERA_DATA')
        # some data on the subpanel
        if context.scene.subpanel_cams: 
            box = layout.box()                  
            box.operator('object.button_cmr', text = "Add 4 Cameras Setup", icon='IMPORT').cmr = 'append' 
            try:
                bpy.data.objects['Camera_F']
            except:
                pass
            else:               
                #box = layout.box()
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Camera Front:')
                split.operator('object.button_cmr', text = "Set Active").cmr = 'Camera_F_active'
                
            try:
                bpy.data.objects['Camera_B']
            except:
                pass
            else:                       
                #box = layout.box()
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Camera Back:')
                split.operator('object.button_cmr', text = "Set Active").cmr = 'Camera_B_active'
            try:
                bpy.data.objects['Camera_L']
            except:
                pass
            else:                           
                #box = layout.box()
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='  Camera Left:')
                split.operator('object.button_cmr', text = "Set Active").cmr = 'Camera_L_active'
            try:
                bpy.data.objects['Camera_R']
            except:
                pass
            else:                           
                #box = layout.box()
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Camera Right:')
                split.operator('object.button_cmr', text = "Set Active").cmr = 'Camera_R_active' 
            try:
                bpy.context.active_object.name
            except:
                pass
            else:
                for i in range(len(cams)):
                    if bpy.context.active_object.name == cams[i]:                            
                        #row = layout.row()
                        split = box.split(factor = 0.4)
                        col = split.column(align = True)
                        col.label(text='')
                        split.operator('object.button_cmr', text = "Preview", icon='HIDE_OFF').cmr = 'preview'
            try:
                 bpy.context.active_object.name
            except:
                pass
            else:
                for i in range(len(cams)):
                    if bpy.context.active_object.name == cams[i]:                                
                        #row = layout.row()
                        box.prop(bpy.context.scene.render, "film_transparent", text = "Transparent background")                        
                        split = box.split(factor = 0.4)
                        col = split.column(align = True)
                        col.label(text='')
                        split.operator('render.render', text = "Render", icon='RENDER_STILL')
                

        ######### Armature #########
        row = layout.row()
        bn_icon = 'HANDLETYPE_AUTO_CLAMP_VEC'
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_bn else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_bn', icon=icon, icon_only=True)
        row.label(text='Animation (Advanced)', icon='OUTLINER_DATA_ARMATURE')
        # some data on the subpanel
        if context.scene.subpanel_bn:
            box = layout.box()
            box.operator('object.url_handler', text = "How to Use", icon='HELP').rbx_link = "Guide_Armature"
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_bn_st1 else 'RIGHTARROW'
            box.prop(context.scene, 'subpanel_bn_st1', icon=icon, icon_only=False, text='Step-1 (Add Armature)')
            # some data on the subpanel
            if context.scene.subpanel_bn_st1:               
                ##### STEP-1 #####  
                bn_exist = 0 
                try:
                    for i in bpy.context.selected_objects:
                        if i.type == 'ARMATURE':
                            bn_exist = 1
                            break
                except:
                    pass

                box.prop(rbx_prefs, 'rbx_arma_enum', text ='')
                split = box.split(factor = 0.5)
                col = split.column(align = True)            
                col.label(text = "")            
                split.operator('object.button_bn', text = "Add Armature").bn = 'arma'

                if bn_exist == 1:             
                    #box = layout.box()
                    split = box.split(factor = 0.5)
                    col = split.column(align = True)
                    col.label(text='Show Bones:')
                    split.prop(context.object,'show_in_front')
                box.label(text='          -------------------------------------  ')
                box.label(text='You may try from Step-4')
                box.label(text='If no work - back to Step-2')
            
            ##### STEP-2 #####    
            box = layout.box()
            box.label(text='Step-2 (Prepare Mesh):', icon=bn_icon)
            box.operator('object.button_bn', text = "Recalculate Normals", icon='NORMALS_FACE').bn = 'normal'
            if msh_selection:
                box.label(text=msh_selection, icon='ERROR')
            if msh_error == 'done_nml':
                box.label(text='Recalucalting Done!', icon='CHECKMARK')             
            
            ##### STEP-3 #####
            #CALCULATE DOUBLES
            box = layout.box()
            box.label(text='Step-3 (Double Vertices):', icon=bn_icon)            
            msh_exist = 0 
            dbls_msg = None
            try:
                if len(bpy.context.selected_objects) != 1:
                    dbls_msg = 'Select 1 Object'
                else:
                    if bpy.context.selected_objects[0].type != 'MESH':
                        dbls_msg = 'Object Must be a Mesh'
                    else:
                        msh_exist = 1
                        dbls_msg = None
            except:
                pass    
            if msh_exist == 1:
                try:
                    # Get the active mesh
                    me = bpy.context.object.data
                except:
                    pass #dbls_msg = 'No Mesh Selected'
                else:
                    dbls_msg = None
                    distance = 0.0001 # remove doubles tolerance
                    # Get a BMesh representation
                    bm = bmesh.new()   # create an empty BMesh
                    bm.from_mesh(me)   # fill it in from a Mesh
                    len_bef = len(bm.verts)
                    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist = distance)
                    len_af = len(bm.verts)
                    doubles = len_bef - len_af
                    bm.clear()
                    bm.free()  # free and prevent further access
                    box.label(text='Doubles Found: ' + str(doubles), icon='INFO')
            if dbls_msg:
                box.label(text=dbls_msg, icon='ERROR')
                box.label(text='Doubles Found: ERROR!', icon='INFO')                     
                 
            box.operator('object.button_bn', text = "Remove Double Vertices", icon='VERTEXSEL').bn = 'doubles'
            if msh_selection:
                box.label(text=msh_selection, icon='ERROR')
            if msh_error == 'done_vts':  
                box.label(text='Remove Doubles Done!', icon='CHECKMARK')
            # MESH SMOOTHING #
            msh_exist = 0 
            try:
                for i in bpy.context.selected_objects:
                    if i.type == 'MESH':
                        msh_exist = 1
                        break
            except:
                pass                     
            if msh_exist == 1:
                box.label(text='(Optional, Might help look better):')             
                split = box.split(factor = 0.6)
                col = split.column(align = True)
                col.label(text='Mesh Smoothing:')
                try:
                    split.prop(context.object.data,'use_auto_smooth', text='Auto') 
                except:
                    pass               
            
            ##### STEP-4 #####       
            box = layout.box() 
            box.label(text='Step-4:', icon=bn_icon)            
            box.label(text="Adjust Bones in 'Edit Mode'")
            box.label(text="If needed")
            
            ##### STEP-5 #####
            box = layout.box()
            box.label(text='Step-5:', icon=bn_icon)
            box.label(text='Select Mesh + Bones, then Parent')
            box.operator('object.button_bn', text = "Parent Bones and Mesh", icon='BONE_DATA').bn = 'parent'

            if bn_selection:
                box.label(text=bn_selection, icon='ERROR')
            if bn_error:
                if bn_error == 1:
                    box.label(text='Error, need rectify Mesh', icon='ERROR')
                    bn_error == None
                if bn_error == 2:
                    bn_error == None
                    box.label(text='Parenting Done!', icon='CHECKMARK')
                    box.label(text='Step-6 (Optional):', icon=bn_icon)
                    box.label(text='You can also now export this')
                    box.label(text='Model as .fbx to Mixamo for')
                    box.label(text='animation. (No need redo bones)')
                    box.operator('object.url_handler', text = "Go to Mixamo", icon='URL').rbx_link = "mixamo"
        
        #### Other Functions ####
        row = layout.row()
        row = layout.row()
        row = layout.row()

                
        ######### Other Functions #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_other else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_other', icon=icon, icon_only=True)
        row.label(text='Quick Functions:', icon='COLLAPSEMENU')
        # some data on the subpanel
        if context.scene.subpanel_other:

            box = layout.box()
            try:
                if len(bpy.context.selected_objects) == 1: 
                    box.prop(bpy.context.object.active_material, 'use_backface_culling', text='Backface Culling', icon='FACESEL')
                    #box.prop(bpy.context.space_data, 'lock_camera', text='Lock Camera to View', icon='OUTLINER_DATA_CAMERA') 
                else:
                    box.label(text='Select obj for Culling Option', icon='ERROR')                    
            except:
                box.label(text='Culling: No Material Found', icon='ERROR') 
            

            #box = layout.box()
            box.label(text='')
            box.prop(bpy.context.space_data.overlay, 'show_face_orientation', text='Show Face Orientation', icon='NORMALS_FACE')  
            box.prop(rbx_prefs, 'rbx_face_enum')
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.operator("object.rbx_button_of", text = "Recalc Outside").rbx_of = 'outside'
            split.operator("object.rbx_button_of", text = "Recalc Inside").rbx_of = 'inside'  


        ######### Export Functions #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_export else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_export', icon=icon, icon_only=True)
        row.label(text='File Export:', icon='COLLAPSEMENU')
        # some data on the subpanel
        if context.scene.subpanel_export:
                        
            #### Export FBX UGC ####
            row = layout.row()
            row = layout.row()
            box = layout.box()
            box.label(text='UGC Item Export:')
            try:
                if len(bpy.context.selected_objects) == 1: 
                    box.prop(rbx_prefs, 'rbx_of_orig', text = "Set Origin to Geometry") 
                    box.prop(rbx_prefs, 'rbx_of_trsf', text = "Apply All Transforms")  
                    box.operator('object.rbx_operators', text = "Export FBX", icon='EXPORT').rbx_operator = 'exp_fbx'
                else:
                    box.label(text='Select obj for FBX Export', icon='ERROR')
            except:
                box.label(text='Select obj for FBX Export', icon='ERROR')                                          


            #### Export FBX LC ####
            row = layout.row()
            box = layout.box()
            box.label(text='Layered Cloth Export:')
            box.label(text='Make sure you select these:')
            box.label(text='1. Armature')
            box.label(text='2. YourItem in Armature')
            box.label(text='3. ItemName_OuterCage')
            box.label(text='4. ItemName_InnerCage')
            try:
                if len(bpy.context.selected_objects) >= 4:  
                    box.operator('object.rbx_operators', text = "Export FBX", icon='EXPORT').rbx_operator = 'exp_fbx_lc'
                else:
                    box.label(text='Some items not selected', icon='ERROR')
            except:
                box.label(text='Some items not selected', icon='ERROR')    
                
                        
        #### Discord Support Server ####                
        row = layout.row()
        row.label(text='          -------------------------------------  ') 
        row = layout.row() 
        row.operator("object.rbx_button_of", text = "Install Cool Theme", icon='BRUSHES_ALL').rbx_of = 'theme_install'
        row = layout.row()  
        row.operator('object.url_handler', text = "Discord Support Server", icon='URL').rbx_link = "discord"
        row = layout.row() 
        row.operator('object.url_handler', text = "Buy me a Coffee! ;)", icon='URL').rbx_link = "buy coffee" 



    #CLASS REGISTER 
##########################################
classes = (
        RBXToolsPreferences,
        RBX_OPERATORS,
        PROPERTIES_RBX, 
        URL_HANDLER,
        RBX_BUTTON_HDRI,
        OBJECT_OT_add_object,
        BUTTON_DMMY,
        BUTTON_WEAR,
        BUTTON_HAIR, 
        RBX_BUTTON_LC,
        RBX_BUTTON_LC_ANIM,
        BUTTON_BNDS,
        BUTTON_CMR,
        BUTTON_BN, 
        RBX_BUTTON_OF,
        TOOLBOX_MENU
        )  
             

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.rbx_prefs = bpy.props.PointerProperty(type= PROPERTIES_RBX)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_hdri = BoolProperty(default=False)
    Scene.subpanel_imp_char = BoolProperty(default=False)
    Scene.subpanel_imp_char = BoolProperty(default=False)
    Scene.subpanel_bounds = BoolProperty(default=False)
    Scene.subpanel_dummy = BoolProperty(default=False)
    Scene.subpanel_hair = BoolProperty(default=False)
    Scene.subpanel_lc = BoolProperty(default=False)
    Scene.subpanel_cams = BoolProperty(default=False)
    Scene.subpanel_bn = BoolProperty(default=False)
    Scene.subpanel_bn_st1 = BoolProperty(default=False)
    Scene.subpanel_other = BoolProperty(default=False)
    Scene.subpanel_export = BoolProperty(default=False)
    
    
def unregister():
    rbx_tmp_path = os.path.join(addon_path, 'tmp')
    rbx_tmp_list = os.listdir(rbx_tmp_path)
    for i in rbx_tmp_list:
        os.remove(os.path.join(rbx_tmp_path, i))
    
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.rbx_prefs
    del Scene.subpanel_readme
    del Scene.subpanel_hdri
    del Scene.subpanel_imp_char
    del Scene.subpanel_imp_char
    del Scene.subpanel_bounds
    del Scene.subpanel_dummy
    del Scene.subpanel_hair
    del Scene.subpanel_lc
    del Scene.subpanel_cams
    del Scene.subpanel_bn
    del Scene.subpanel_bn_st1
    del Scene.subpanel_other
    del Scene.subpanel_export    
        

if __name__ == "__main__":
    register()
