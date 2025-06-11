import bpy
import glob_vars


######### Layered Clothing Buttons ###########    
class RBX_BUTTON_LC(bpy.types.Operator):
    bl_label = "RBX_BUTTON_LC"
    bl_idname = "object.rbx_button_lc"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_lc : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_lc = self.rbx_lc
        rbx_lc_spwn = None 
        rbx_mode = None
        
        lc_dum_list = [
                        'Default Mannequin',
                        'Default Mannequin (separated)',
                        'Roblox Boy',
                        'Roblox Girl',
                        'Roblox Man',
                        'Roblox Woman',
                        'Classic Male',
                        'Classic Female',
                        'Roblox Blocky',
                        'Roblox Korblox',
                        'Roblox Deathwalker'
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
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename =rbx_lc_spwn) 
            bpy.data.collections[rbx_lc_spwn].hide_viewport = False
            print(rbx_lc_spwn + " Sample Spawned") 
        else:
            for x in range(len(lc_dum_list)):
                if rbx_prefs.rbx_lc_dum_enum == 'OP' + str(x+1):
                    rbx_lc_spwn = lc_dum_list[x] + rbx_lc     
                           

            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename =rbx_lc_spwn)
            
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