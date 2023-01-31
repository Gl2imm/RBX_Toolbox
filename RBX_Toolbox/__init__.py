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
    "version": (3, 0),
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
from urllib import request
import bpy.utils.previews


## Toolbox vars ##
ver = "v.3.0"
lts_ver = ver

mode = 1 #0 - Test Mode; 1 - Live mode
wh =0   #0 - W; 1 - H


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
rbx_char_error = None
rbx_asset_error = None
rbx_network_error = None
rbx_asset_name = None
rbx_asset_creator = None
rbx_bkd_hair_img = None

print("**********************************************")
print("OS Platform: " + platform.system())
print("**********************************************")    

 
                
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
    
    ## Import Accessory ##
    rbx_accessory: StringProperty(
        name="Accessory",
        description="Accessory ID to import",
        default="11996887739",
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
        scene = context.scene
        rbx_char = self.rbx_char
        rbx_prefs = scene.rbx_prefs        
        rbx_username = rbx_prefs.rbx_username
        rbx_accessory = rbx_prefs.rbx_accessory
        rbx_char_path = os.path.join(addon_path, 'Imported_Characters' + fbs + rbx_username)
        #rbx_char_path = addon_path + '/Imported_Characters' + fbs + rbx_username
        
        global rbx_char_error
        global rbx_asset_error
        global rbx_asset_name
        global rbx_asset_creator
        global rbx_network_error

        if rbx_char == 'folder':
            if not os.path.exists(addon_path + '/Imported_Characters'):
                os.makedirs(addon_path + '/Imported_Characters')
            os.startfile(os.path.dirname(addon_path + '/Imported_Characters/'))
            
         
                
        if rbx_char == 'preview':                
            ### Clear Previous Preview ###
            try:
                rbx_tmp_img = bpy.data.images[rbx_username + '.png']
            except:
                pass
            else:
                bpy.data.images.remove(rbx_tmp_img)
                
            ### Find userID ###
            #rbx_username = 'papa_boss332'  # User ID
            rbx_req_usr_id = requests.post("https://users.roblox.com/v1/usernames/users", json={
                "usernames": [rbx_username],
                "excludeBannedUsers": 'true'
            })
            
            try:
                rbx_usr_nm_data = rbx_req_usr_id.json()
            except:
                rbx_network_error = 1
            else:
                rbx_network_error = 0
                
                
            try:
                rbx_usr_id = rbx_usr_nm_data.get('data')[0]['id']
            except:
                rbx_char_error = 1
            else:
                rbx_char_error = 0
                #print("ID:", rbx_usr_nm_data.get('data')[0]['id'])

                ### Get user Thumbnail ###
                rbx_size = '250x250'
                rbx_format = 'Png'
                rbx_isCircular = 'false'
                
                rbx_req_usr_img = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={rbx_usr_id}&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}")
                
                try:
                    user_img = rbx_req_usr_img.json()
                except:
                    rbx_network_error = 1
                else:
                    rbx_network_error = 0
                
                    rbx_usr_img_url = user_img.get('data')[0]['imageUrl']
                    #print('User Image:', user_img.get('data')[0]['imageUrl'])
                
                
                rbx_tmp_filepath = os.path.join(addon_path, 'tmp')
                
                if not os.path.exists(rbx_tmp_filepath):
                    os.makedirs(rbx_tmp_filepath)
                

                rbx_tmp_file = os.path.join(rbx_tmp_filepath, rbx_username + ".png")               
                
                try:
                    rbx_usr_avtr = bpy.data.images[rbx_username + ".png"]
                except:
                    try:
                        request.urlretrieve(rbx_usr_img_url, rbx_tmp_file)
                    except:
                        rbx_network_error = 1
                    else:
                        rbx_network_error = 0
                        rbx_usr_avtr = bpy.data.images.load(rbx_tmp_file)
                        #os.remove(rbx_tmp_file)



        if rbx_char == 'import':
            if not os.path.exists(rbx_char_path):
                os.makedirs(rbx_char_path)
                
            ### Find userID ###
            rbx_req_usr_id = requests.post("https://users.roblox.com/v1/usernames/users", json={
                "usernames": [rbx_username],
                "excludeBannedUsers": 'true'
            })
            
            try:
                rbx_usr_nm_data = rbx_req_usr_id.json()
            except:
                rbx_network_error = 1
            else:
                rbx_network_error = 0
                
                
            try:
                rbx_usr_id = rbx_usr_nm_data.get('data')[0]['id']
            except:
                rbx_char_error = 1
            else:
                rbx_char_error = 0
                ### Get Avatar Hashes ###
                rbx_req_usr_hsh = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-3d?userId={rbx_usr_id}")
                rbx_usr_hsh = rbx_req_usr_hsh.json()
                rbx_usr_hsh2 = requests.get(rbx_usr_hsh['imageUrl']) #Get OBJ and Textures Hashes
                rbx_usr_hsh2 = rbx_usr_hsh2.json()
                
                def get_cdn_url(hash):
                    i = 31
                    for char in hash[:32]:
                        i ^= ord(char)  # i ^= int(char, 16) also works
                    return f"https://t{i%8}.rbxcdn.com/{hash}"
                
                avt_obj_hsh = rbx_usr_hsh2['obj']
                avt_mtl_hsh = rbx_usr_hsh2['mtl']
                avt_tex_hsh = rbx_usr_hsh2['textures']
                
                
                ### Get All URLs ###
                try:
                    avt_mtl_url = get_cdn_url(avt_mtl_hsh)
                    avt_obj_url = get_cdn_url(avt_obj_hsh)
                except:
                    rbx_network_error = 1
                else:
                    rbx_network_error = 0
                
                    avt_tex_url = []
                    for i in range(len(avt_tex_hsh)):
                        tmp_tex_url = get_cdn_url(avt_tex_hsh[i])
                        avt_tex_url.append(tmp_tex_url)
                    
                    
                    ### Download files ###
                    rbx_mtl_file = os.path.join(rbx_char_path, rbx_username + ".mtl")
                    rbx_obj_file = os.path.join(rbx_char_path, rbx_username + ".obj")
                    
                    try:
                        request.urlretrieve(avt_mtl_url, rbx_mtl_file)
                        request.urlretrieve(avt_obj_url, rbx_obj_file)


                        for i in range(len(avt_tex_url)):
                            rbx_tex_file = os.path.join(rbx_char_path, rbx_username + '_tex-' + str(i) + ".png")
                            request.urlretrieve(avt_tex_url[i], rbx_tex_file)
                    except:
                        rbx_network_error = 1
                    else:
                        rbx_network_error = 0

                        ### Write new Texture names into MTL ###
                        try:
                            with open(rbx_mtl_file) as f:
                                text = f.read()
                        except:
                            rbx_network_error = 1
                        else:
                            rbx_network_error = 0
                            for i in range(len(avt_tex_hsh)):
                                text = text.replace(avt_tex_hsh[i], rbx_username + '_tex-' + str(i) + ".png")
                            f.close()
                            test = open(rbx_mtl_file,'w')
                            test.write(text)
                            test.close()
                            
                            
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
                            
                            

        if rbx_char == 'folder_accessory':
            if not os.path.exists(addon_path + '/Imported_Accessories'):
                os.makedirs(addon_path + '/Imported_Accessories')
            os.startfile(os.path.dirname(addon_path + '/Imported_Accessories/'))   

        if rbx_char == 'preview_accessory': 
            ### Clear Previous Preview ###
            try:
                rbx_tmp_img = bpy.data.images[rbx_accessory + '.png']    
            except:
                pass
            else:
                bpy.data.images.remove(rbx_tmp_img)
                              
            #11996887739 - noob
            ### Get Asset Thumbnail ###
            rbx_size = '150x150'
            rbx_format = 'Png'
            rbx_isCircular = 'false'
            
            
            try:
                rbx_req_acs_img = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={rbx_accessory}&returnPolicy=PlaceHolder&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}") 
                asset_img = rbx_req_acs_img.json()
                
                rbx_req_acs_info = requests.get(f"https://economy.roblox.com/v2/assets/{rbx_accessory}/details") 
                asset_info = rbx_req_acs_info.json()
            except:
                rbx_network_error = 1
            else:
                rbx_network_error = 0

                try:
                    rbx_asset_img_url = asset_img.get('data')[0]['imageUrl']
                    #print('User Image:', user_img.get('data')[0]['imageUrl'])
                except:
                    rbx_asset_error = 1
                else:
                    rbx_asset_error = 0
                    
                    rbx_asset_name = asset_info['Name']
                    rbx_asset_creator = asset_info['Creator']['Name']
                    print(rbx_asset_creator)
                    
                    rbx_tmp_filepath = os.path.join(addon_path, "tmp")
                    
                    if not os.path.exists(rbx_tmp_filepath):
                        os.makedirs(rbx_tmp_filepath)
                    
                    rbx_tmp_file = os.path.join(rbx_tmp_filepath, rbx_accessory + ".png")              
                    
                    try:
                        rbx_asset_img = bpy.data.images[rbx_accessory + ".png"]
                    except:
                        try:
                            request.urlretrieve(rbx_asset_img_url, rbx_tmp_file)
                        except:
                            rbx_network_error = 1
                        else:
                            rbx_network_error = 0
                            rbx_asset_img = bpy.data.images.load(rbx_tmp_file)
                            #os.remove(rbx_tmp_file)


        if rbx_char == 'import_accessory':
            ### Get Asset Name ###
            try:
                rbx_req_acs_info = requests.get(f"https://economy.roblox.com/v2/assets/{rbx_accessory}/details") 
                asset_info = rbx_req_acs_info.json()
            except:
                rbx_network_error = 1
            else:
                rbx_network_error = 0
                try:
                    rbx_asset_name = asset_info['Name']
                except:
                    pass
                else:
                    rbx_char_path = os.path.join(addon_path, 'Imported_Accessories' + fbs + rbx_asset_name)
                    
                    if not os.path.exists(rbx_char_path):
                        os.makedirs(rbx_char_path)
                    
                    ### Get Hashes ###
                    try:
                        rbx_req_asset_hsh = requests.get(f"https://thumbnails.roblox.com/v1/assets-thumbnail-3d?assetId={rbx_accessory}")
                        rbx_asset_hsh = rbx_req_asset_hsh.json()
                        rbx_asset_hsh2 = requests.get(rbx_asset_hsh['imageUrl']) #Get OBJ and Textures Hashes
                        rbx_asset_hsh2 = rbx_asset_hsh2.json()
                    except:
                        rbx_network_error = 1
                    else:
                        rbx_network_error = 0
                    
                        def get_cdn_url(hash):
                            i = 31
                            for char in hash[:32]:
                                i ^= ord(char)  # i ^= int(char, 16) also works
                            return f"https://t{i%8}.rbxcdn.com/{hash}"
                        
                        asset_obj_hsh = rbx_asset_hsh2['obj']
                        asset_mtl_hsh = rbx_asset_hsh2['mtl']
                        asset_tex_hsh = rbx_asset_hsh2['textures']
                        
                        
                        ### Get All URLs ###
                        try:
                            asset_mtl_url = get_cdn_url(asset_mtl_hsh)
                            asset_obj_url = get_cdn_url(asset_obj_hsh)
                        except:
                            rbx_network_error = 1
                        else:
                            rbx_network_error = 0
                            asset_tex_url = []
                            for i in range(len(asset_tex_hsh)):
                                tmp_tex_url = get_cdn_url(asset_tex_hsh[i])
                                asset_tex_url.append(tmp_tex_url)
                            
                            
                            ### Download files ###
                            rbx_mtl_file = os.path.join(rbx_char_path, rbx_asset_name + ".mtl")
                            rbx_obj_file = os.path.join(rbx_char_path, rbx_asset_name + ".obj")
                            
                            try:
                                request.urlretrieve(asset_mtl_url, rbx_mtl_file)
                                request.urlretrieve(asset_obj_url, rbx_obj_file)
                                
                                
                                for i in range(len(asset_tex_url)):
                                    rbx_tex_file = os.path.join(rbx_char_path, rbx_asset_name + '_tex-' + str(i) + ".png")
                                    request.urlretrieve(asset_tex_url[i], rbx_tex_file)
                            except:
                                rbx_network_error = 1
                            else:
                                rbx_network_error = 0
                        
                                ### Write new Texture names into MTL ###
                                try:
                                    with open(rbx_mtl_file) as f:
                                        text = f.read()
                                except:
                                    rbx_network_error = 1
                                else:
                                    rbx_network_error = 0
                                    for i in range(len(asset_tex_hsh)):
                                        text = text.replace(asset_tex_hsh[i], rbx_asset_name + '_tex-' + str(i) + ".png")
                                    f.close()
                                    f = open(rbx_mtl_file,'w')
                                    f.write(text)
                                    f.close()
                                    
                                    
                                    rbx_imp_asset = bpy.ops.import_scene.obj(filepath=rbx_obj_file)
                                    ### Selecting Asset ###
                                    rbx_object = bpy.context.selected_objects[0]
                                    bpy.ops.object.select_all(action='DESELECT')
                                    bpy.context.view_layer.objects.active = None
                                    bpy.data.objects[rbx_object.name].select_set(True)
                                    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object.name]
                                    
                                                            
                                    ### Position Asset ###
                                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                                    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                                    '''
                                    bpy.ops.transform.translate(value=(0, 0, 3.28467), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
                                    bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
                                    '''
                                    ### Setting up materials ###
                                    for rbx_mat_slot in bpy.context.object.material_slots:
                                        rbx_mat_slot.material.show_transparent_back = False
                                        rbx_mat_slot.material.use_backface_culling = True                  


        return {'FINISHED'}
    
    
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
        
                
        if mode == 0:
            rbx_asset_folder = rbx_ast_fldr
        else:
            rbx_asset_folder = bpy.context.preferences.addons['RBX_Toolbox'].preferences.rbx_asset_folder
        
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
                                                                                                                    
        return {'FINISHED'}      
 

    
    #PANEL UI
####################################
class TOOLBOX_MENU(bpy.types.Panel):
    bl_label = "Roblox Toolbox (" + ver + ")"
    bl_idname = "RBX_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "RBX Tools"
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        
        
        ######## Update Notifier ########
        if lts_ver > ver:
            box = layout.box()
            #box.label(text = "Addon Update Available: " + lts_ver, icon='IMPORT') 
            box.operator('object.url_handler', text = "Update Available: " + lts_ver, icon='IMPORT').rbx_link = "update"    
            
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
            row = layout.row()
            row.label(text = 'Take Note!!', icon='ERROR')
            row = layout.row()
            row.label(text = 'Often Roblox refuses to share files')
            row = layout.row()
            row.label(text = 'So try to get it another time')
            box = layout.box()
            box.label(text = 'RBX Username (not Display Name)')
            box.prop(rbx_prefs, 'rbx_username', text ='')
            box.operator('object.add_character', text = "Preview").rbx_char = "preview"               
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.operator('object.add_character', text = "Import").rbx_char = "import"
            split.operator('object.add_character', text = "Open Folder").rbx_char = "folder"
            
            try:
                rbx_avat_img_prev = bpy.data.images[rbx_prefs.rbx_username + '.png']
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

            
            
            if rbx_char_error:
                try:
                    rbx_avat_img_prev = bpy.data.images[rbx_prefs.rbx_username + '.png']
                except:
                    box.label(text = 'Error. No Such Character!!', icon='ERROR')

            if rbx_network_error:
                try:
                    rbx_asset_img_prev = bpy.data.images[rbx_prefs.rbx_accessory + '.png']
                except:
                    box.label(text = 'Network Error, or Roblox is Busy', icon='ERROR')             
            
            ######### Import Accessory #########    
            box = layout.box()
            box.label(text = 'Accessory ID')
            box.prop(rbx_prefs, 'rbx_accessory', text ='')
            box.operator('object.add_character', text = "Preview").rbx_char = "preview_accessory"               
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.operator('object.add_character', text = "Import").rbx_char = "import_accessory"
            split.operator('object.add_character', text = "Open Folder").rbx_char = "folder_accessory"
            
            try:
                rbx_asset_img_prev = bpy.data.images[rbx_prefs.rbx_accessory + '.png']
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
                        box.label(text = 'Creator: ' + rbx_asset_creator)
                    
            if rbx_asset_error:
                try:
                    rbx_asset_img_prev = bpy.data.images[rbx_prefs.rbx_accessory + '.png']
                except:
                    box.label(text = 'Error. No Such Accessory!!', icon='ERROR') 
    
            if rbx_network_error:
                try:
                    rbx_asset_img_prev = bpy.data.images[rbx_prefs.rbx_accessory + '.png']
                except:
                    box.label(text = 'Network Error, or Roblox is Busy', icon='ERROR') 
                                           
                                        
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
        BUTTON_HAIR, 
        RBX_BUTTON_LC,
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
