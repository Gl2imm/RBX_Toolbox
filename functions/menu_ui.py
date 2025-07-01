import traceback
import bpy
import os
import glob
import bmesh
from RBX_Toolbox import glob_vars
from glob_vars import addon_path
from . import menu_pie
from RBX_Toolbox import update
from RBX_Toolbox import update_aepbr
from RBX_Toolbox import props



addon_version = "v.6.2"
#to update in __init__ as well
#clean public lib, pycache and imports folder
#set debug to false



def get_aepbr_cur_ver():
    rbx_aepbr_fldr_path = os.path.join(addon_path, glob_vars.rbx_aepbr_fldr)
    try:
        rbx_aepbr_blend = os.listdir(rbx_aepbr_fldr_path)[0]
        rbx_aepbr_filename = rbx_aepbr_blend.split(".bl")[0]    #split away .blend extension
        aepbr_cur_ver = rbx_aepbr_filename.split("v.")[1]
    except:
        aepbr_cur_ver = "0" #leave it at 0, will not trigger error during update of AEPBR
    return aepbr_cur_ver


    #PANEL UI
####################################
class TOOLBOX_MENU(bpy.types.Panel):
    bl_label = f"Roblox Toolbox (" + addon_version + ")"
    bl_idname = "RBX_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "RBX Tools"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rbx_prefs = scene.rbx_prefs

        #print(glob_vars.get_login_info())
        ######## Update Notifier ########
        #print("lts_ver: ", glob_vars.lts_ver)
        #print("addon_version: ", addon_version)
        if glob_vars.lts_ver is not None:
            if glob_vars.lts_ver > addon_version:
                box = layout.box()
                box.label(text = "Update Available: " + glob_vars.lts_ver)
                box.operator('object.url_handler', text = "Release Notes " + glob_vars.lts_ver, icon='DOCUMENTS').rbx_link = "update"
                if update.operator_state == "IDLE" and not glob_vars.need_restart_blender:
                    box.operator("wm.install_update", text="Install Update", icon='IMPORT')
                    '''elif update.operator_state == "DOWNLOADING":
                    box.label(text=f"Downloading... {update.download_progress:.2f}%")'''
                elif update.operator_state == "DOWNLOADING":
                    # Display the progress bar
                    box.prop(update.current_operator, "progress", text="Downloading", slider=True)
                elif update.operator_state == "INSTALLING":
                    box.label(text="Installing...")
                elif update.operator_state == "FINISHED":
                    box = layout.box()
                    box.alert = True  # 🔴 Makes the button red
                    box.operator("wm.install_update", text="Restart Blender")
                elif update.operator_state == "ERROR":
                    box = layout.box()
                    box.alert = True  # 🔴 Makes the button red
                    box.label(text=f"Error: {update.error_message}", icon='ERROR')
                if glob_vars.need_restart_blender:
                    box.row().label(text="Logging out complete!", icon="CHECKMARK")
                    box.alert = True  # 🔴 Makes the button red
                    box.operator("wm.install_update", text="Restart Blender").restart_only = True





        ######## oAuth Login ########
        row = layout.row()
        row.label(text = "Roblox Authorization", icon= "USER")
        box = layout.box()
        rbx = context.window_manager.rbx
        rbx_installed_dependencies = False

        # 2. Dependency Installation
        from oauth.lib import install_dependencies  # Local import
        if not rbx.is_finished_installing_dependencies:
            box.row().label(
                text=f"This plugin requires installation of",
                icon="INFO",
            )
            box.row().label(
                text=f"dependencies the first time it is run.",
            )
            box.row().operator(
                install_dependencies.RBX_OT_install_dependencies.bl_idname,
                text="Installing..." if rbx.is_installing_dependencies else "Install Dependencies",
            )
            #return
        else:
            rbx_installed_dependencies = True

        if rbx.needs_restart:
            box.row().label(text="Installation complete!", icon="CHECKMARK")
            box.alert = True  # 🔴 Makes the button red
            box.operator("wm.install_update", text="Restart Blender").restart_only = True
            #layout.row().label(text="Restart Blender to continue.")
            #return

        if rbx_installed_dependencies == True and not rbx.needs_restart:
            # 3. Load Creator Details (if not done)
            # Blender does not provide an API for us to hook into to read the creator details when
            # the plugin loads. Instead, we will fetch this information on the first draw of the
            # main panel
            if not rbx.has_called_load_creator:
                from oauth.lib import creator_details  # Local import
                creator_details.load_creator_details(
                    context.window_manager, context.preferences)

            # 4. Main UI Content: Login or Creator/Upload sections
            if not rbx.is_logged_in:
                # Login UI Section
                from oauth.lib import oauth2_login_operators  # Local import

                button_text_login = "Logging in..." if rbx.is_processing_login_or_logout else "Log in"
                box.row().operator(
                    oauth2_login_operators.RBX_OT_oauth2_login.bl_idname, text=button_text_login)

                # This cancel button renders for logins requiring the browser, but not for automatic logins via refreshing a remembered token
                if bpy.ops.rbx.oauth2_cancel_login.poll():  # poll() is a classmethod of the operator
                    box.row().operator(oauth2_login_operators.RBX_OT_oauth2_cancel_login.bl_idname)
            else:
                # Logged In State: Creator Section
                #creator_section_box = layout.box()

                top_row_creator = box.row(align=True)
                try:
                    from oauth.lib.oauth2_client import RbxOAuth2Client  # Local import
                    oauth2_client = RbxOAuth2Client(rbx)  # rbx is already defined
                    top_row_creator.label(text=f"Hello, {rbx.name}!")
                except Exception as exception:
                    self.report(
                        {"ERROR"}, f"Failed to display user name: {str(exception)}\n{traceback.format_exc()}")
                    top_row_creator.label(
                        text="Hello, User (Error)", icon="ERROR")  # Fallback

                from oauth.lib import oauth2_login_operators  # Local import
                button_text_logout = "Working..." if rbx.is_processing_login_or_logout else "Log out"
                top_row_creator.operator(
                    oauth2_login_operators.RBX_OT_oauth2_logout.bl_idname, text=button_text_logout)





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
        if rbx.is_logged_in:
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_imp_char else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_imp_char', icon=icon, icon_only=True)
            row.label(text='Import From Roblox', icon='IMPORT')
            # some data on the subpanel
            if context.scene.subpanel_imp_char:
                box = layout.box()
                box.label(text = 'Enter ID, URL or Username')
                box.prop(rbx_prefs, 'rbx_username_entered', text ='')
                box.operator('object.add_character', text = "Preview").rbx_char = "preview_avatar"
                box.prop(rbx_prefs, 'rbx_split', text ='Separate Accessories')
                split = box.split(factor = 0.5)
                col = split.column(align = True)            
                col.operator('object.add_character', text = "Import").rbx_char = "import"
                split.operator('object.add_character', text = "Open Folder").rbx_char = "folder_character"
                rbx_cur_usr = glob_vars.get_login_info()["user_name"]
                box.operator('object.add_character', text = f"Import My avatar ({rbx_cur_usr})", icon = 'TRACKING_REFINE_BACKWARDS').rbx_char = "my_avatar"
                
                 

                ### Set preview
                try:
                    rbx_avat_img_prev = bpy.data.images[glob_vars.rbx_user_name_clean + '.png']
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
                    rbx_avat_img_prev.preview_ensure()
                    box.template_icon(rbx_avat_img_prev.preview.icon_id, scale=10.0)


                if glob_vars.rbx_char_error:
                    box.label(text = glob_vars.rbx_char_error, icon='ERROR')
                    try:
                        rbx_asset_img_prev = bpy.data.images[glob_vars.rbx_user_name_clean + '.png']
                    except:
                        pass 



                ######### Import Accessory #########    
                box = layout.box()
                box.label(text = 'Accessory ID or URL')
                box.prop(rbx_prefs, 'rbx_accessory_entered', text ='')
                box.operator('object.add_character', text = "Check Item (must)").rbx_char = "preview_accessory"  
                if glob_vars.rbx_supported_type_category == "Layered Cloth" or glob_vars.rbx_supported_type_category == "Shoes":
                    box.prop(rbx_prefs, 'rbx_incl_cages', text =' Include Cages in Import (take longer)')    
                split = box.split(factor = 0.5)
                col = split.column(align = True) 
                col.enabled = glob_vars.rbx_supported_type          
                col.operator('object.add_character', text = "Import").rbx_char = "import_accessory"
                split.operator('object.add_character', text = "Open Folder").rbx_char = "folder_accessory"

                '''# --- Top conditional row: Include Cages checkbox ---
                if glob_vars.rbx_supported_type_category == "Layered Cloth":
                    box.prop(rbx_prefs, 'rbx_incl_cages', text=' Include Cages in Import')
                # --- Second row: Check + Import buttons ---
                split = box.split(factor=0.5)
                col_left = split.column(align=True)
                col_left.operator('object.add_character', text="Check Item").rbx_char = "preview_accessory"
                col_right = split.column(align=True)
                col_right.enabled = glob_vars.rbx_supported_type
                col_right.operator('object.add_character', text="Import").rbx_char = "import_accessory"
                # --- Third row: empty left, Open Folder button on right ---
                split = box.split(factor=0.5)
                col_left = split.column(align=True)
                col_right = split.column(align=True)
                col_right.operator('object.add_character', text="Open Folder").rbx_char = "folder_accessory"'''

                try:
                    rbx_asset_img_prev = bpy.data.images[glob_vars.rbx_asset_name_clean + '.png']
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
                

                box.label(text = f'Name: {glob_vars.rbx_asset_name if glob_vars.rbx_asset_name else ""}')
                box.label(text = f'Creator: {glob_vars.rbx_asset_creator if glob_vars.rbx_asset_creator else ""}')
                box.label(text = f'Type: {glob_vars.rbx_asset_type if glob_vars.rbx_asset_type else ""}')
                box.label(text = f'Import: {"Supported" if glob_vars.rbx_supported_type else "Not Supported"}')

                        
                if glob_vars.rbx_asset_error:
                    box.label(text = glob_vars.rbx_asset_error, icon='ERROR')
                    try:
                        rbx_asset_img_prev = bpy.data.images[glob_vars.rbx_asset_name_clean + '.png']
                    except:
                        pass 
                
                box = layout.box()
                row = box.row()
                icon = 'DISCLOSURE_TRI_DOWN' if context.scene.subpanel_supported else 'DISCLOSURE_TRI_RIGHT'
                row.prop(context.scene, 'subpanel_supported', icon=icon, icon_only=True)
                row.label(text='Supported Accessories:', icon='CHECKMARK')
                # some data on the subpanel
                if context.scene.subpanel_supported:
                    row = box.row()
                    #row.label(text='', icon='BLANK1')  # Small indent
                    row.label(text='Avatar Accessories', icon='DOT')
                    row = box.row()
                    row.label(text='Layered Clothing', icon='DOT')
                    row = box.row()
                    row.label(text='Cages', icon='DOT')
                    row = box.row()
                    row.label(text='Gears', icon='DOT')
                    row = box.row()
                    row.label(text='Bundle Items:', icon='PACKAGE')
                    row = box.row()
                    row.label(text='Characters', icon='DOT')
                    row = box.row()
                    row.label(text='Body Parts (import whole bundle)', icon='DOT') 
                    row = box.row()
                    row.label(text='Dynamic Heads', icon='DOT') 
                    row = box.row()
                    row.label(text='Shoes', icon='DOT') 






        ######### Bounds #########
        #if rbx_assets_set == 1:
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_bounds else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_bounds', icon=icon, icon_only=True)
        row.label(text='Accessory Bounds', icon='CUBE')
        # some data on the subpanel
        if context.scene.subpanel_bounds:
            box = layout.box()
            box.prop(rbx_prefs, 'rbx_bnds_enum', text ='UGC')
            box.prop(rbx_prefs, 'rbx_bnds_hide')                
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")
            split.operator('object.button_bnds', text = "Spawn").bnds = "UGC"
            
            box = layout.box()
            box.prop(rbx_prefs, 'rbx_bnds_avatar_enum', text ='Avatars')             
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")
            split.operator('object.button_bnds', text = "Spawn").bnds = "AVA"
            
            box = layout.box()
            box.prop(rbx_prefs, 'rbx_bnds_lc_enum', text ='LC')              
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")
            split.operator('object.button_bnds', text = "Spawn").bnds = "LC"




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
            





        ######### Rigs #########
        row = layout.row()     
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_rigs else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_rigs', icon=icon, icon_only=True)
        row.label(text='Rigs', icon='OUTLINER_DATA_ARMATURE')
        # some data on the subpanel
        if context.scene.subpanel_rigs:
            box = layout.box()
            box.label(text = 'Roblox Rigged Models')
            box.operator('object.button_dmmy', text = "R15 Blocky Rig").dmy = 'R15 Blocky Rig'
            box.operator('object.button_dmmy', text = "R15 Woman Rig").dmy = 'R15 Woman Rig'
            box.operator('object.button_dmmy', text = "Plushie Template").dmy = 'Plushie Template'
            
            
            ######### iiXenix Rigs #########
            box = layout.box()
            box.label(text = 'iiXenix Rigs')
            box.operator('object.button_dmmy', text = "Multirig").dmy = 'Multirig'
            box.operator('object.button_dmmy', text = "Multirig Faceless").dmy = 'Multirig_faceless'



            ######### Paribes Rigs #########
            box = layout.box()
            box.label(text = 'Paribes Rig')

            # Check if folder exists
            #addon_path = os.path.dirname(os.path.abspath(__file__))
            #addon_path = os.path.dirname(os.path.realpath(__file__))
            aepbr_path = os.path.join(addon_path, glob_vars.rbx_aepbr_fldr)
            folder_exists = os.path.exists(aepbr_path)
            blend_files = glob.glob(os.path.join(aepbr_path, "*.blend"))
            if folder_exists and blend_files:
                #insert dummy operator
                box.operator('object.button_dmmy', text = "AEPBR").dmy = 'aepbr'
                ######## Update Notifier ########
                if glob_vars.aepbr_lts_ver is not None:
                    aepbr_cur_ver = get_aepbr_cur_ver()
                    if glob_vars.aepbr_lts_ver > aepbr_cur_ver:
                        box.label(text = '')
                        box.label(text = '- - - - - - - ')
                        box.label(text = f"Update Available:  ({aepbr_cur_ver} -> {glob_vars.aepbr_lts_ver})")
                        box.label(text = glob_vars.aepbr_lts_title)
                        #box.operator('object.url_handler', text = "Release Notes " + glob_vars.lts_ver, icon='DOCUMENTS').rbx_link = "update"
                        if update_aepbr.aepbr_operator_state == "IDLE":
                            box.operator("wm.update_aepbr", text="Install Update", icon='IMPORT')
                            box.operator('object.url_handler', text = f"Release Notes v.{glob_vars.aepbr_lts_ver}", icon='DOCUMENTS').rbx_link = "aepbr notes"
                        elif update_aepbr.aepbr_operator_state == "DOWNLOADING":
                            # Display the progress bar
                            box.prop(update_aepbr.aepbr_current_operator, "progress", text="Downloading", slider=True)
                        elif update_aepbr.aepbr_operator_state == "INSTALLING":
                            box.label(text="Installing...")
                        elif update_aepbr.aepbr_operator_state == "ERROR":
                            box = layout.box()
                            box.alert = True  # 🔴 Makes the button red
                            box.label(text=f"Error: {update_aepbr.aepbr_error_message}", icon='ERROR')
            ### download rig if not installed
            else:
                if update_aepbr.aepbr_operator_state == "IDLE":
                    if glob_vars.aepbr_lts_ver is None:
                        box.enabled = False
                        box.operator("wm.update_aepbr", text=f"Dowload rig (v.{glob_vars.aepbr_lts_ver})", icon='IMPORT')
                        box.label(text="No inernet Connection", icon='ERROR')
                    else:
                        box.operator("wm.update_aepbr", text=f"Dowload rig (v.{glob_vars.aepbr_lts_ver})", icon='IMPORT')
                elif update_aepbr.aepbr_operator_state == "DOWNLOADING":
                    # Display the progress bar
                    box.prop(update_aepbr.aepbr_current_operator, "progress", text="Downloading", slider=True)
                elif update_aepbr.aepbr_operator_state == "INSTALLING":
                    box.label(text="Installing...")
                elif update_aepbr.aepbr_operator_state == "ERROR":
                    box = layout.box()
                    box.alert = True  # 🔴 Makes the button red
                    box.label(text=f"Error: {update_aepbr.aepbr_error_message}", icon='ERROR')

            box = layout.box()    
            box.operator('object.url_handler', text = "AEPBR Discord", icon='URL').rbx_link = "aepbr discord"
                






            ######### R6 Rig #########
            box = layout.box()
            box.label(text = 'R6 from Nuke (YT)')
            box.operator('object.button_dmmy', text = "Rigged R6").dmy = 'Rigged R6'
            ######### Wear Clothing #########
            box.label(text = '')
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
                if glob_vars.rbx_face_filename == None:
                    box.label(text = 'Loaded Face: None')
                else:
                    box.label(text = f'Loaded Face: {glob_vars.rbx_face_name}')
                box.label(text = 'Enter Face ID or URL')
                box.prop(rbx_prefs, 'rbx_face', text ='')
                box.operator('object.button_wear', text = "Import").rbx_cloth = 'face'
                if glob_vars.rbx_face_netw_error != None:
                    box.label(text = glob_vars.rbx_face_netw_error, icon='ERROR') 
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
                if glob_vars.rbx_shirt_filename == None:
                    box.label(text = 'Loaded Shirt: None')
                else:
                    box.label(text = f'Loaded Shirt: {glob_vars.rbx_shirt_name}')
                box.label(text = 'Enter Shirt ID or URL')
                box.prop(rbx_prefs, 'rbx_shirt', text ='')
                box.operator('object.button_wear', text = "Import").rbx_cloth = 'shirt'
                if glob_vars.rbx_shirt_netw_error != None:
                    box.label(text = glob_vars.rbx_shirt_netw_error, icon='ERROR') 
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
                if glob_vars.rbx_shirt_filename == None:
                    box.label(text = 'Loaded Shirt: None')
                else:
                    box.label(text = f'Loaded Shirt: {glob_vars.rbx_shirt_name}')
                if glob_vars.rbx_pants_filename == None:
                    box.label(text = 'Loaded Pants: None')
                else:
                    box.label(text = f'Loaded Pants: {glob_vars.rbx_pants_name}')
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
                if glob_vars.rbx_pants_filename == None:
                    box.label(text = 'Loaded Pants: None')
                else:
                    box.label(text = f'Loaded Pants: {glob_vars.rbx_pants_name}')
                box.label(text = 'Enter Pants ID or URL')
                box.prop(rbx_prefs, 'rbx_pants', text ='')
                box.operator('object.button_wear', text = "Import").rbx_cloth = 'pants'
                if glob_vars.rbx_pants_netw_error != None:
                    box.label(text = glob_vars.rbx_pants_netw_error, icon='ERROR') 
                
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
            split.operator('object.button_hair', text = "Spawn").rbx_hair = 'Dummy_head' 
            
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





        ######### Avatars #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_ava else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_ava', icon=icon, icon_only=True)
        row.label(text='Avatars', icon='COMMUNITY')
        # some data on the subpanel
        if context.scene.subpanel_ava:
            # Avatar templates:
            box = layout.box()
            box.label(text = 'Avatar Templates')
            box.prop(rbx_prefs, 'rbx_ava_enum', text ='')
            split = box.split(factor = 0.5)
            col = split.column(align = True)            
            col.label(text = "")            
            split.operator('object.rbx_button_ava', text = "Spawn").rbx_ava = 'avatar'
                
            # Clean props:
            box = layout.box()                  
            box.label(text = "Clear All Custom Props in selected")
            box.operator('object.rbx_button_ava', text="Clean Up").rbx_ava = "clear" 
            
            # Renamer:
            box = layout.box()
            box.label(text = "Select Objects to remove .000")
            box.label(text = "ps: not always works")
            box.operator('object.rbx_button_ava', text="Rename All").rbx_ava = "rename" 

            # Hide Att:
            box = layout.box()
            box.label(text = "Hide all Att in selected:")
            box.operator('object.rbx_button_ava', text="Hide All").rbx_ava = "hide" 
            box.operator('object.rbx_button_ava', text="UnHide Them").rbx_ava = "unhide" 
            box.label(text = "(only the ones you hide before)")





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
                for i in range(len(glob_vars.cams)):
                    if bpy.context.active_object.name == glob_vars.cams[i]:                            
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
                for i in range(len(glob_vars.cams)):
                    if bpy.context.active_object.name == glob_vars.cams[i]:                                
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
            if glob_vars.msh_selection:
                box.label(text=glob_vars.msh_selection, icon='ERROR')
            if glob_vars.msh_error == 'done_nml':
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
            if glob_vars.msh_selection:
                box.label(text=glob_vars.msh_selection, icon='ERROR')
            if glob_vars.msh_error == 'done_vts':  
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

            if glob_vars.bn_selection:
                box.label(text=glob_vars.bn_selection, icon='ERROR')
            if glob_vars.bn_error:
                if glob_vars.bn_error == 1:
                    box.label(text='Error, need rectify Mesh', icon='ERROR')
                    glob_vars.bn_error == None
                if glob_vars.bn_error == 2:
                    glob_vars.bn_error == None
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





        ######## Upload to Roblox ########
        if rbx.is_logged_in:
            row = layout.row()
            icon = 'DOWNARROW_HLT' if context.scene.subpanel_upload else 'RIGHTARROW'
            row.prop(context.scene, 'subpanel_upload', icon=icon, icon_only=True)
            row.label(text='Upload to Roblox', icon='COLLAPSEMENU')
            # some data on the subpanel
            if context.scene.subpanel_upload:
                upload_section_box = layout.box()
                upload_section_box.prop(rbx, "creator")  # Creator dropdown
                # Logged In State & Not Processing Login/Logout: Upload Section
                if not rbx.is_processing_login_or_logout:
                    from oauth.lib.upload_operator import RBX_OT_upload  # Local import
                    upload_section_box.row().operator(RBX_OT_upload.bl_idname)
                else:
                    upload_section_box.label(text="Refreshing Login. Please wait", icon='ERROR')

                from oauth.lib.get_selected_objects import get_selected_objects  # Local import
                selected_text = ", ".join(
                    obj.name for obj in get_selected_objects(context))
                if selected_text:
                    upload_section_box.row().label(text="Selected Objects:", icon="RESTRICT_SELECT_OFF")
                    selected_objects_display_box = upload_section_box.box()  # Sub-box for the list
                    selected_objects_display_box.label(text=selected_text)

                from oauth.lib import status_indicators  # Local import
                # Pass the layout of the upload_section_box for drawing statuses
                status_indicators.draw_statuses(
                    context.window_manager, upload_section_box)

                        



        ######### Other Functions #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_other else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_other', icon=icon, icon_only=True)
        row.label(text='Quick Functions:', icon='COLLAPSEMENU')
        # some data on the subpanel
        if context.scene.subpanel_other:

            box = layout.box()
            objs = None
            mat = None
            try:
                objs = bpy.context.selected_objects
                try:
                    mat = bpy.context.object.active_material
                except:
                    pass
            except:
                pass

            if objs:
                if len(objs) == 1: 
                    if mat:
                        box.label(text='Culling Option', icon='HIDE_ON') 
                        box.label(text='(Hide flipped faces, like in Roblox)') 
                        box.prop(bpy.context.object.active_material, 'use_backface_culling', text='Backface Culling', icon='FACESEL')
                    else:
                        box.enabled=False
                        box.label(text='Culling Option (Add Material)', icon='HIDE_ON')
                        box.label(text='(Hide flipped faces, like in Roblox)') 
                        box.operator("object.rbx_button_of", text = "Backface Culling",  icon='FACESEL') #Fake button 
                else:
                    box.enabled=False
                    box.label(text='Culling Option (Select 1 Object)', icon='HIDE_ON')
                    box.label(text='(Hide flipped faces, like in Roblox)') 
                    box.operator("object.rbx_button_of", text = "Backface Culling",  icon='FACESEL') #Fake button
            else:
                box.enabled=False
                box.label(text='Culling Option (Select Object)', icon='HIDE_ON')
                box.label(text='(Hide flipped faces, like in Roblox)') 
                box.operator("object.rbx_button_of", text = "Backface Culling",  icon='FACESEL') #Fake button    
            

            box = layout.box()
            box.label(text='Normals', icon='ORIENTATION_NORMAL')
            box.prop(bpy.context.space_data.overlay, 'show_face_orientation', text='Show Face Orientation', icon='NORMALS_FACE')  
            box.prop(rbx_prefs, 'rbx_face_enum')
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.operator("object.rbx_button_of", text = "Recalc Outside").rbx_of = 'outside'
            split.operator("object.rbx_button_of", text = "Recalc Inside").rbx_of = 'inside' 
            box.operator("object.rbx_button_of", text = "Flip Normals").rbx_of = 'flip' 
            
            box = layout.box()
            try:
                if len(bpy.context.selected_objects) == 1: 
                    box.label(text='Glowing UGC', icon='SHADING_SOLID')
                    box.operator("object.rbx_button_of", text = "Make Item Glow").rbx_of = 'glow'
                    box.operator("object.rbx_button_of", text = "Remove Glowing").rbx_of = 'unglow'            
                else:
                    box.enabled=False
                    box.label(text='Glowing UGC (Select Object)', icon='SHADING_SOLID')
                    box.operator("object.rbx_button_of", text = "Make Item Glow").rbx_of = 'glow'
                    box.operator("object.rbx_button_of", text = "Remove Glowing").rbx_of = 'unglow'
            except:
                pass


            #### Make Outline ####
            box = layout.box()
            if objs:
                if len(objs) == 1: 
                    if mat:
                        box.label(text='UGC Outline ', icon='HIDE_ON') 
                        box.operator("object.rbx_button_of", text = "Make Outline").rbx_of = 'make_outline'
                        
                        if 'RBX_Outline_mat' in objs[0].material_slots and 'RBX_Outline' in objs[0].modifiers:
                            mat = bpy.data.materials.get("RBX_Outline_mat")
                            color = mat.node_tree.nodes['RGB']
                            box.label(text='** Outline Controls: **')
                            col_0 = color.outputs[0]
                            
                            split = box.split(factor = 0.5)
                            col = split.column(align = True)
                            col.label(text='Preview Color:')
                            split.prop(col_0, "default_value", text = "")
                            
                            box.prop(bpy.context.object.modifiers["RBX_Outline"], 'thickness', text='Outline Thickness:')
                            
                            box.label(text='')
                            box.label(text='** Add Outline to UGC: **')
                            box.operator("object.rbx_button_of", text = "Apply Outline").rbx_of = 'apply_outline'
                            box.label(text='*Outline faces will be added to your')
                            box.label(text='object and UV moved outside.')
                            box.label(text='Just move that UV to the color')
                            box.label(text='that you need or re-unwrap it')
                    else:
                        box.enabled=False
                        box.label(text='UGC Outline (Add Material)', icon='HIDE_ON')
                        box.operator("object.rbx_button_of", text = "Make Outline").rbx_of = 'make_outline'
                else:
                    box.enabled=False
                    box.label(text='UGC Outline (Select 1 Object)', icon='HIDE_ON')
                    box.operator("object.rbx_button_of", text = "Make Outline").rbx_of = 'make_outline'
            else:
                box.enabled=False
                box.label(text='UGC Outline (Select Object)', icon='HIDE_ON')
                box.operator("object.rbx_button_of", text = "Make Outline").rbx_of = 'make_outline' 





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
            
            
            #### Export Avatar ####
            row = layout.row()
            box = layout.box()
            box.label(text='Avatar Export:')
            box.label(text='Select all parts 1st')
            box.operator('object.rbx_button_ava', text="Export Avatar").rbx_ava = 'export'

        
                

        ######### Pie Menu #########
        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_pie else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_pie', icon=icon, icon_only=True)
        row.label(text='Pie Menu:', icon='COLLAPSEMENU')
        # some data on the subpanel
        if context.scene.subpanel_pie:
                        
            #### Export FBX UGC ####
            box = layout.box()
            box.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            
            split = box.split(factor = 0.5)
            col = split.column(align = True)
            col.label(text='Shortcut:', icon_value=672)
            try:
                split.prop(menu_pie.find_user_keyconfig('F85A6'), 'type', text='', full_event=True)
            except:
                split.label(text='Shortcut not found')
            box.label(text='1. Wont work if shortcut exist') 
            box.label(text='2. Work in Obj mode only')            





        #### Discord Support Server ####                
        row = layout.row()
        row.label(text='          -------------------------------------  ') 
        row = layout.row() 
        row.operator("object.rbx_button_of", text = "Install Cool Theme", icon='BRUSHES_ALL').rbx_of = 'theme_install'
        row = layout.row()  
        row.operator('object.url_handler', text = "Discord Support Server", icon='URL').rbx_link = "discord"
        row = layout.row() 
        row.operator('object.url_handler', text = "Buy me a Coffee! ;)", icon='URL').rbx_link = "buy coffee"

        row = layout.row()
        icon = 'DOWNARROW_HLT' if context.scene.subpanel_support else 'RIGHTARROW'
        row.prop(context.scene, 'subpanel_support', icon=icon, icon_only=True)
        row.label(text='Support with Robux', icon='FUND')
        # some data on the subpanel
        if context.scene.subpanel_support:
            box = layout.box()
            split_sup = box.split(factor = 0.2)
            col_sup = split_sup.column(align = True)       
            col_sup.label(text="", icon="LAYERGROUP_COLOR_04")
            split_sup.operator("object.url_handler", text = "Supporter (10 Bobuc)").rbx_link = 'tips 10'
            split_sup = box.split(factor = 0.2)
            col_sup = split_sup.column(align = True)       
            col_sup.label(text="", icon="LAYERGROUP_COLOR_03")
            split_sup.operator("object.url_handler", text = "Hero (50 Bobuc)").rbx_link = 'tips 50'
            split_sup = box.split(factor = 0.2)
            col_sup = split_sup.column(align = True)       
            col_sup.label(text="", icon="LAYERGROUP_COLOR_06")
            split_sup.operator("object.url_handler", text = "Legend (500 Bobuc)").rbx_link = 'tips 500'
            split_sup = box.split(factor = 0.2)
            col_sup = split_sup.column(align = True)       
            col_sup.label(text="", icon="LAYERGROUP_COLOR_07")
            split_sup.operator("object.url_handler", text = "Epic (1000 Bobuc)").rbx_link = 'tips 1000'
        
    