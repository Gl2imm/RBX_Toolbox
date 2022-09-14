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
    "version": (1, 1),
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

## Toolbox vars ##
ver = "v.1.1"
lts_ver = ver

mode = 1 #0 - Test Mode; 1 - Live mode
wh =1   #0 - W; 1 - H


if mode == 0:
    if wh == 1:
        my_path = ("E:\\G-Drive\\Blender\\Roblox\\0. Addon\\RBX_Toolbox")
        ast_fldr = ("E:\\G-Drive\\Blender\\Roblox\\UGC\\UGC Files") 
    if wh == 0:
        my_path = ("D:\\Personal\\G-Drive\\Blender\\Roblox\\0. Addon\\RBX_Toolbox")
        ast_fldr = ("D:\\Personal\\G-Drive\\Blender\\Roblox\\UGC\\UGC Files")    
else:
    my_path = (os.path.dirname(os.path.realpath(__file__)))

### For Blender HDRI ### 
bldr_path = (os.path.dirname(bpy.app.binary_path))
bldr_ver = bpy.app.version_string.split('.')
bldr_fdr = bldr_ver[0] + '.' + bldr_ver[1]
    
if platform.system() == 'Windows':
    fbs = '\\'
    blend_file = ("\\RBX_Templates.blend")
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
    blend_file = ("/RBX_Templates.blend")
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



print("**********************************************")
print("OS Platform: " + platform.system())
print("**********************************************")


    
    #OPERATOR         
######################################## 
class RBXToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
 
    asset_folder: bpy.props.StringProperty(name="Folder",
                                        description="Select Assets folder",
                                        default="",
                                        maxlen=1024,
                                        subtype="DIR_PATH")
                                                                              
                                                                        
                                        
    if mode == 0:
        asset_folder = ast_fldr
        
             
class PROPERTIES_RBX(bpy.types.PropertyGroup):
    
    name : bpy.props.StringProperty(name= "ver", default="", maxlen=40) #Not in use, key in data            

    cust_enum_hdri : bpy.props.EnumProperty(
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
    url = 'https://github.com/Gl2imm/RBX_Toolbox/releases.atom'
    try:
        full_text = requests.get(url, allow_redirects=True).text
    except:
        pass
    else:
        global lts_ver
        split_1 = full_text.split('536450223/')[1]
        lts_ver = split_1.split('</id>')[0]                     
            
    
############   URL HANDLER OPERATOR   ##############    
class URL_HANDLER(bpy.types.Operator):
    bl_label = "BUTTON CUSTOM"
    bl_idname = "object.lgndtranslate_url"
    bl_options = {'REGISTER', 'UNDO'}
    link : bpy.props.StringProperty(name= "Added")


    def execute(self, context):
        link = (self.link)
                    
        if link == "update":
            webbrowser.open_new("https://github.com/Gl2imm/RBX_Toolbox/releases")
            
        if link == "discord":
            webbrowser.open_new("https://discord.gg/gFa4mY7")            
            
        if link == "instructions":
            instructions = my_path + fbs + "Credits and Instructions.txt"
            with open(instructions) as f:
                text = f.read()
            t = bpy.data.texts.new("Instructions")
            t.write("To switch back to normal view switch from 'TEXT EDITOR' to '3D Viewport'. Or just press 'Shift+F5' \n \n \n")
            t.write(text)
            bpy.context.area.ui_type = 'TEXT_EDITOR'
            bpy.context.space_data.text = bpy.data.texts['Instructions']
            bpy.ops.text.jump(line=1)            
            
        if link == "version":
            instructions = my_path + fbs + "Version_log.txt"
            with open(instructions) as f:
                text = f.read()
            t = bpy.data.texts.new("Version_log")
            t.write("To switch back to normal view switch from 'TEXT EDITOR' to '3D Viewport'. Or just press 'Shift+F5' \n \n \n")
            t.write(text)
            bpy.context.area.ui_type = 'TEXT_EDITOR'
            bpy.context.space_data.text = bpy.data.texts['Version_log']
            bpy.ops.text.jump(line=1)  
            

        return {'FINISHED'}


class BUTTON_HDRI(bpy.types.Operator):
    bl_label = "BUTTON_HDRIFULL"
    bl_idname = "object.button_hdrifull"
    bl_options = {'REGISTER', 'UNDO'}
    hdri : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        scene = context.scene
        prefs = scene.my_prefs
        hdri = (self.hdri)
        
 
 
        if prefs.cust_enum_hdri == 'OP1':
            hdri_name = "World"                    
        if prefs.cust_enum_hdri == 'OP2':
            hdri_name = "City"                  
        if prefs.cust_enum_hdri == 'OP3':
            hdri_name = "Courtyard"
        if prefs.cust_enum_hdri == 'OP4':
            hdri_name = "Forest"
        if prefs.cust_enum_hdri == 'OP5':
            hdri_name = "Interior"
        if prefs.cust_enum_hdri == 'OP6':
            hdri_name = "Night"
        if prefs.cust_enum_hdri == 'OP7':
            hdri_name = "Studio"
        if prefs.cust_enum_hdri == 'OP8':
            hdri_name = "Sunrise"
        if prefs.cust_enum_hdri == 'OP9':
            hdri_name = "Sunset"
                                                                                                                 


        if hdri_name == 'World':
            try:
                hdri = bpy.data.worlds[hdri_name]
            except:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_world, filename =hdri_name)
                hdri = bpy.data.worlds[hdri_name]
            scene.world = hdri
            print(hdri_name + " has been Appended and applied to the World")
        else:
            if bpy.context.scene.world != 'HDRI':
                if 'HDRI' not in bpy.data.worlds:
                    bpy.ops.wm.append(directory =my_path + blend_file + ap_world, filename ='HDRI')
                hdri = bpy.data.worlds['HDRI']
                scene.world = hdri
                hdri_img_path = bldr_hdri_path + hdri_name + '.exr'
                hdri_image = bpy.data.images.load(hdri_img_path)
                bpy.data.worlds['HDRI'].node_tree.nodes['Environment Texture'].image = hdri_image 
                print(hdri_img_path)

        return {'FINISHED'}  


######### Dummy Buttons ###########    
class BUTTON_DMMY(bpy.types.Operator):
    bl_label = "BUTTON_DMMY"
    bl_idname = "object.button_dmmy"
    bl_options = {'REGISTER', 'UNDO'}
    dmy : bpy.props.StringProperty(name= "Added")

    def execute(self, context):
        dmy = self.dmy
        
        dmy_items = {
            'R15 Blocky': [
                {'name': 'Dummy R15'}          
            ]
            }  
            

        bpy.ops.wm.append(directory =my_path + blend_file + ap_object, files =dmy_items.get(dmy))
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
            asset_folder = ast_fldr
        else:
            asset_folder = bpy.context.preferences.addons['RBX_Toolbox'].preferences.asset_folder
            
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
            bpy.ops.wm.append(directory =asset_folder + ugc_bound_file + ap_object, files =bnds_items.get(bnds))
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
        prefs = scene.my_prefs
        cmr = self.cmr
        cmr_spl = cmr.rsplit('_',1)
        
        #### Apend Cameras ####
        if cmr == 'append':               
            if bpy.data.objects.get('Camera_F') == None:
                bpy.ops.wm.append(directory =my_path + blend_file + ap_collection, filename ='Cameras')
                bpy.context.scene.render.resolution_x = 1080
                bpy.context.scene.render.resolution_y = 1080
                bpy.context.scene.render.resolution_percentage = 100
                print("Cameras Setup Spawned")
            else:
                print("Cameras Setup Already Exist")
                
        
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
        prefs = scene.my_prefs 
        
        
        ######## Update Notifier ########
        if lts_ver > ver:
            box = layout.box()
            #box.label(text = "Addon Update Available: " + lts_ver, icon='IMPORT') 
            box.operator('object.lgndtranslate_url', text = "Update Available: " + lts_ver, icon='IMPORT').link = "update"         
               
        ######## ASSETS ########                
        if mode == 0:
            addon_assets = prefs
            folder = 'recolor_folder'
        else:
            addon_assets =bpy.context.preferences.addons['RBX_Toolbox'].preferences
            folder = 'asset_folder'
        
        ######## Check if Asset Folder installed ######## 
        if mode == 0:
            asset_folder = ast_fldr
            asset_folder_set = asset_folder
        else:
            asset_folder_set =bpy.context.preferences.addons['RBX_Toolbox'].preferences.asset_folder
        assets_set = 0

        if os.path.exists(asset_folder_set) == True:
            dir = os.listdir(asset_folder_set)
            for x in range(len(dir)):
                if "Bounds.blend" in dir[x]:
                    #print("Found UGC 'Bounds.blend' file, related features unlocked")
                    assets_set = 1
                    break
                else:
                   assets_set = 2 
          
                        
        ######### Roblox UGC Files ###########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_readme else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_readme', icon=icon, icon_only=True)
        row.label(text = "Roblox UGC Files", icon= "ASSET_MANAGER")
        # some data on the subpanel
        if context.scene.subpanel_readme:
            box = layout.box()
            box.operator('object.lgndtranslate_url', text = "Read Instructions, Credits", icon='ARMATURE_DATA').link = "instructions"
            box.operator('object.lgndtranslate_url', text = "Read Version Log", icon='CON_ARMATURE').link = "version" 
            if assets_set != 1:
                box.label(text = "To unlock additional features")
                box.label(text = "Specify folder with UGC")
                box.label(text = "blend file 'Bounds.blend'")
            row = layout.row()
            box.prop(addon_assets, folder)
            if assets_set == 1:
                box.label(text = "'Bounds.blend' linked to addon")
            if assets_set == 2:
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
            box.label(text = "Blender built-in HDRIs")
            box.prop(prefs, 'cust_enum_hdri')
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text = "")
            split.operator("object.button_hdrifull", text = "Set as HDRI")
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

                                        
        ######### Bounds #########
        if assets_set == 1:
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
            # Bounds
            box.operator('object.button_dmmy', text = "R15 Blocky Dummy").dmy = "R15 Blocky"
                        
        
        ######### Cameras #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_cams else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_cams', icon=icon, icon_only=True)
        row.label(text='Cameras', icon='CAMERA_DATA')
        # some data on the subpanel
        if context.scene.subpanel_cams: 
            box = layout.box()                  
            box.operator('object.button_cmr', text = "Add Cameras Setup", icon='OUTLINER_DATA_CAMERA').cmr = 'append' 
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
                        
                        
        row = layout.row()
        row.label(text='          -------------------------------------  ') 
        row = layout.row()  
        row.operator('object.lgndtranslate_url', text = "Discord Support Server", icon='URL').link = "discord"  


    #CLASS REGISTER 
##########################################
classes = (
        RBXToolsPreferences,
        PROPERTIES_RBX, 
        URL_HANDLER,
        BUTTON_HDRI,
        BUTTON_DMMY, 
        BUTTON_BNDS,
        BUTTON_CMR, 
        TOOLBOX_MENU
        )
        

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.my_prefs = bpy.props.PointerProperty(type= PROPERTIES_RBX)
    Scene.subpanel_readme = BoolProperty(default=False)
    Scene.subpanel_hdri = BoolProperty(default=False)
    Scene.subpanel_bounds = BoolProperty(default=False)
    Scene.subpanel_dummy = BoolProperty(default=False)
    Scene.subpanel_cams = BoolProperty(default=False)



def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.my_prefs
    del Scene.subpanel_readme
    del Scene.subpanel_hdri
    del Scene.subpanel_bounds
    del Scene.subpanel_dummy
    del Scene.subpanel_cams

        

if __name__ == "__main__":
    register()
