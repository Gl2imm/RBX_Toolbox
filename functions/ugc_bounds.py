import bpy
from RBX_Toolbox import glob_vars



######### Bounds Buttons ###########    
class BUTTON_BNDS(bpy.types.Operator):
    bl_label = "BUTTON_BNDS"
    bl_idname = "object.button_bnds"
    bl_options = {'REGISTER', 'UNDO'}
    bnds : bpy.props.StringProperty(name= "Added") # type: ignore

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

        rbx_bnds_avatar_list = [
                        'Classic Avatars',
                        'Rthro Avatars',
                        'Slender Avatars',
                        'Minimum Sizes'
                        ]   
                        
        rbx_bnds_lc_list = [
                        'LC Max Sizes'
                       ]             
        
        ### UGC Boundary ###
        if bnds == "UGC":         
            for x in range(len(rbx_bnds_list)):
                if rbx_prefs.rbx_bnds_enum == 'OP' + str(x+1):
                    bnds_spwn = rbx_bnds_list[x]
            
            ### Without Dummy ###            
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename ='UGC '+ bnds_spwn + ' Bounds')                            
                                 
            ### Add Dummy ###
            if rbx_prefs.rbx_bnds_hide == False:
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_object, filename ='R15 Blocky')
                rbx_col_num = len(bpy.data.collections)
                bpy.ops.object.move_to_collection(collection_index=rbx_col_num)

        ### Avatar Boundary ###
        if bnds == "AVA":         
            for x in range(len(rbx_bnds_avatar_list)):
                if rbx_prefs.rbx_bnds_avatar_enum == 'OP' + str(x+1):
                    bnds_spwn = rbx_bnds_avatar_list[x]
            
            ### Without Dummy ###            
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename ='Avatar '+ bnds_spwn + ' Bounds') 

        ### LC Boundary ###
        if bnds == "LC":         
            for x in range(len(rbx_bnds_lc_list)):
                if rbx_prefs.rbx_bnds_lc_enum == 'OP' + str(x+1):
                    bnds_spwn = rbx_bnds_lc_list[x]
            
            ### Without Dummy ###            
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename =bnds_spwn + ' Bounds') 
                        
        print(bnds_spwn + " Boundary Spawned")

        return {'FINISHED'}     