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
    "version": (1, 6),
    "blender": (2, 90, 0),
    "location": "Operator",
    "description": "Roblox UGC models toolbox",
    "warning": "Subscribe to NYTV :)",
    "category": "Object"
}


import bpy
import os
from bpy.types import Scene
from bpy.props import (BoolProperty,FloatProperty)
import requests
import webbrowser
import sys
import platform
import bmesh

## Toolbox vars ##
ver = "v.1.6"
lts_ver = ver

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
    
    ## not in use ##
    bool : BoolProperty(
    name="World Transparency",
    description="World Transparency property",
    default = False
    )
    
    ## not in use just for display in test mode##
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
        rbx_operator = (self.rbx_operator)
        
        if rbx_operator == 'exp_fbx':
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', use_selection=True, object_types={'MESH'}, global_scale=0.01, bake_anim=False)


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


######### Dummy Buttons ###########    
class BUTTON_DMMY(bpy.types.Operator):
    bl_label = "BUTTON_DMMY"
    bl_idname = "object.button_dmmy"
    bl_options = {'REGISTER', 'UNDO'}
    dmy : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        dmy = self.dmy

        bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, filename =dmy)
        print(dmy + " Spawned")
           
        
        return {'FINISHED'}          
        
        
######### Bounds Buttons ###########    
class BUTTON_BNDS(bpy.types.Operator):
    bl_label = "BUTTON_BNDS"
    bl_idname = "object.button_bnds"
    bl_options = {'REGISTER', 'UNDO'}
    bnds : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        bnds = self.bnds
        if mode == 0:
            rbx_asset_folder = rbx_ast_fldr
        else:
            rbx_asset_folder = bpy.context.preferences.addons['RBX_Toolbox'].preferences.rbx_asset_folder
            
        bnds_items = {
            'Hat': [
                {'name': 'All_bounds.013'},
                {'name': 'Hat'}            
            ],
            'Hair': [
                {'name': 'All_bounds.012'},
                {'name': 'Hair'}            
            ], 
            'FaceCenter': [
                {'name': 'All_bounds.011'},
                {'name': 'Face Center'}            
            ], 
            'FaceFront': [
                {'name': 'All_bounds.010'},
                {'name': 'Face Front'}            
            ], 
            'Neck': [
                {'name': 'All_bounds.009'},
                {'name': 'Neck'}            
            ], 
            'Front': [
                {'name': 'All_bounds.008'},
                {'name': 'Front'}            
            ], 
            'Back': [
                {'name': 'All_bounds.007'},
                {'name': 'Back'}            
            ], 
            'ShoulderRight': [
                {'name': 'All_bounds.005'},
                {'name': 'Should Right'}            
            ], 
            'ShoulderLeft': [
                {'name': 'All_bounds.006'},
                {'name': 'Shoulder Left'}            
            ], 
            'ShoulderNeck': [
                {'name': 'All_bounds.001'},
                {'name': 'Shoulder Neck'}            
            ], 
            'WaistBack': [
                {'name': 'All_bounds.004'},
                {'name': 'Waist Back'}            
            ], 
            'WaistFront': [
                {'name': 'All_bounds.003'},
                {'name': 'Waist Front'}            
            ], 
            'WaistCenter': [
                {'name': 'All_bounds.002'},
                {'name': 'Waist Center'}            
            ]                                                                                                                                                                   
            }  
               
        if bpy.data.objects.get(bnds) == None:
            bpy.ops.wm.append(directory =rbx_asset_folder + ugc_bound_file + ap_object, files =bnds_items.get(bnds))
            print(bnds + " Boundary Spawned")
        else:
            print(bnds + " Boundary Already Exist")
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

        bn_items = {
            'R15 Blocky': [
                {'name': 'Character_bones_blocky'}       
            ],
            'R15 Boy': [
                {'name': 'Character_bones_r15_boy'}         
            ], 
            'R15 Girl': [
                {'name': 'Character_bones_r15_girl'}         
            ], 
            'R15 Woman': [
                {'name': 'Character_bones_r15_woman'}        
            ], 
            'Rthro Boy': [
                {'name': 'Character_bones_rth_boy'}    
            ],
            'Rthro Girl': [
                {'name': 'Character_bones_rth_girl'}         
            ], 
            'Rthro Normal': [
                {'name': 'Character_bones_rth_normal'}          
            ], 
            'Rthro Slender': [
                {'name': 'Character_bones_rth_slender'}          
            ]                                                                                                                                                          
            }          
        
        #### Apend Armature ####
        bn_split = bn.rsplit('_')
        print(bn_split)
        
        if bn_split[-1] == 'arma':
            bpy.ops.wm.append(directory =rbx_my_path + rbx_blend_file + ap_object, files =bn_items.get(bn_split[0]))
            bn_sel = bpy.context.selected_objects[0].name
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects[bn_sel].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[bn_sel]
            print(bn_split[0] + " Armature Appended")
 
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
          
                        
        ######### Roblox UGC Files ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_readme else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_readme', icon=icon, icon_only=True)
        row.label(text = "Roblox UGC Files", icon= "ASSET_MANAGER")
        # some data on the subpanel
        if context.scene.subpanel_readme:
            box = layout.box()
            box.operator('object.url_handler', text = "Read Instructions, Credits", icon='ARMATURE_DATA').rbx_link = "Credits and Instructions"
            box.operator('object.url_handler', text = "Read Version Log", icon='CON_ARMATURE').rbx_link = "Version_log" 
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

        ######### HDRI ###########
        # subpanel
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_hdri else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_hdri', icon=icon, icon_only=True)
        row.label(text = "Set HDRI (Lights)", icon= "WORLD")
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
                if wrld != 'World':
                    wrld_1 = bpy.data.worlds[wrld].node_tree.nodes['Mapping'].inputs['Rotation'] 
                split = box.split(factor = 0.5)
                col = split.column(align = True)
                col.label(text='Brightness:')
                split.prop(wrld_0, "default_value", text = "")
                if wrld != 'World':
                    split = box.split(factor = 0.5)
                    col = split.column(align = True)
                    col.label(text='Rotation:')
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

                                        
        ######### Bounds #########
        if rbx_assets_set == 1:
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_bounds else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_bounds', icon=icon, icon_only=True)
            row.label(text='Accessory Bounds', icon='CUBE')
            # some data on the subpanel
            if context.scene.subpanel_bounds:
                box = layout.box()
                # Bounds
                box.operator('object.button_bnds', text = "Hat").bnds = "Hat"
                box.operator('object.button_bnds', text = "Hair").bnds = "Hair"
                box.operator('object.button_bnds', text = "Face Center").bnds = "FaceCenter"
                box.operator('object.button_bnds', text = "Face Front").bnds = "FaceFront"
                box.operator('object.button_bnds', text = "Neck").bnds = "Neck"
                box.operator('object.button_bnds', text = "Front").bnds = "Front"
                box.operator('object.button_bnds', text = "Back").bnds = "Back"
                box.operator('object.button_bnds', text = "Shoulder Right").bnds = "ShoulderRight"
                box.operator('object.button_bnds', text = "Shoulder Left").bnds = "ShoulderLeft"
                box.operator('object.button_bnds', text = "Shoulder Neck").bnds = "ShoulderNeck"
                box.operator('object.button_bnds', text = "Waist Back").bnds = "WaistBack"
                box.operator('object.button_bnds', text = "Waist Front").bnds = "WaistFront"
                box.operator('object.button_bnds', text = "Waist Center").bnds = "WaistCenter"

        
        ######### Dummies #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_dummy else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_dummy', icon=icon, icon_only=True)
        row.label(text='Dummy', icon='GHOST_DISABLED')
        # some data on the subpanel
        if context.scene.subpanel_dummy:
            box = layout.box()
            # Dummies
            box.label(text='R15 Dummies')
            box.operator('object.button_dmmy', text = "R15 Blocky").dmy = "R15 Blocky"
            box.operator('object.button_dmmy', text = "R15 Boy").dmy = "R15 Boy"
            box.operator('object.button_dmmy', text = "R15 Girl").dmy = "R15 Girl"
            box.operator('object.button_dmmy', text = "R15 Woman").dmy = "R15 Woman"
            box.label(text='4.0 Dummies')
            box.operator('object.button_dmmy', text = "Lin").dmy = "4.0 Lin"
            box.operator('object.button_dmmy', text = "Oakley").dmy = "4.0 Oakley"
            box.label(text='3.0 Dummies')
            box.operator('object.button_dmmy', text = "Man").dmy = "3.0 Man"
            box.operator('object.button_dmmy', text = "Woman").dmy = "3.0 Woman"
            box.label(text='2.0 Dummies')
            box.operator('object.button_dmmy', text = "Robloxian 2.0").dmy = "Robloxian 2.0"
            box.label(text='Neoclassic Dummies')
            box.operator('object.button_dmmy', text = "Neoclassic Skyler").dmy = "Neoclassic Skyler"
            box.label(text='Rthro Dummies')
            box.operator('object.button_dmmy', text = "Rthro Boy").dmy = "Rthro Boy"
            box.operator('object.button_dmmy', text = "Rthro Girl").dmy = "Rthro Girl"
            box.operator('object.button_dmmy', text = "Rthro Normal").dmy = "Rthro Normal"
            box.operator('object.button_dmmy', text = "Rthro Slender").dmy = "Rthro Slender"
            box.label(text='R6 Dummies (1.0)')
            box.operator('object.button_dmmy', text = "R6 Blocky").dmy = "R6 (1.0)"
                        
        
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

            ##### Animated Staging #####
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
                arma_names = ['R15 Blocky','R15 Boy','R15 Girl','R15 Woman','Rthro Boy','Rthro Girl','Rthro Normal','Rthro Slender'] 
                for x in range(len(arma_names)):
                    split = box.split(factor = 0.08)
                    col = split.column(align = True)
                    col.label(text='')
                    split.operator('object.button_bn', text = arma_names[x] + " Armature", icon='IMPORT').bn = arma_names[x] + '_arma'

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
        row.label(text='Other Functions:', icon='COLLAPSEMENU')
        # some data on the subpanel
        if context.scene.subpanel_other:

            #### Export FBX ####
            box = layout.box()

            try:
                if len(bpy.context.selected_objects) == 1:        
                    box.operator('object.rbx_operators', text = "Export FBX", icon='EXPORT').rbx_operator = 'exp_fbx'
                    box.label(text='What it does:')
                    box.label(text='1. Apply all transforms')
                    box.label(text='2. Set Origin to Geometry')
                    box.label(text='3. Preset Export Settings')
                else:
                    box.label(text='Select one object', icon='ERROR')
            except:
                box.label(text='Select one object', icon='ERROR')
            
            box.label(text='')
            box.label(text='Camera', icon='OUTLINER_DATA_CAMERA')
            box.prop(bpy.context.space_data, 'lock_camera', text='Lock active Camera to View')
        
        #### Discord Support Server ####                
        row = layout.row()
        row.label(text='          -------------------------------------  ') 
        row = layout.row()  
        row.operator('object.url_handler', text = "Discord Support Server", icon='URL').rbx_link = "discord"  


    #CLASS REGISTER 
##########################################
classes = (
        RBXToolsPreferences,
        RBX_OPERATORS,
        PROPERTIES_RBX, 
        URL_HANDLER,
        RBX_BUTTON_HDRI,
        BUTTON_DMMY, 
        BUTTON_BNDS,
        BUTTON_CMR,
        BUTTON_BN, 
        TOOLBOX_MENU
        )
        

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.rbx_prefs = bpy.props.PointerProperty(type= PROPERTIES_RBX)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_hdri = BoolProperty(default=False)
    Scene.subpanel_bounds = BoolProperty(default=False)
    Scene.subpanel_dummy = BoolProperty(default=False)
    Scene.subpanel_cams = BoolProperty(default=False)
    Scene.subpanel_bn = BoolProperty(default=False)
    Scene.subpanel_bn_st1 = BoolProperty(default=False)
    Scene.subpanel_other = BoolProperty(default=False)



def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.rbx_prefs
    del Scene.subpanel_readme
    del Scene.subpanel_hdri
    del Scene.subpanel_bounds
    del Scene.subpanel_dummy
    del Scene.subpanel_cams
    del Scene.subpanel_bn
    del Scene.subpanel_bn_st1
    del Scene.subpanel_other

        

if __name__ == "__main__":
    register()
