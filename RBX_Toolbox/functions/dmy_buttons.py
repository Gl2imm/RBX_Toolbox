import bpy
import os
import glob_vars


######### Dummy Buttons ###########    
class BUTTON_DMMY(bpy.types.Operator):
    bl_label = "BUTTON_DMMY"
    bl_idname = "object.button_dmmy"
    bl_options = {'REGISTER', 'UNDO'}
    dmy : bpy.props.StringProperty(name= "Added")  # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs         
        dmy = self.dmy
        dmy_spwn = None
        
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
                        'R6 (1.0)',
                        'SKN Anime'
                        ] 
                        

        def selected_object():  #if in edit mode
            rbx_selected = None
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_selected = bpy.context.selected_objects
                return rbx_selected

        def back_to_edit_mode(rbx_selected):    
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[rbx_selected[0].name].select_set(True)
            bpy.ops.object.editmode_toggle()


        if dmy == 'Dummy':    
            rbx_selected = selected_object()
            for x in range(len(dum_list)):
                if rbx_prefs.rbx_dum_enum == 'OP' + str(x+1):
                    dmy_spwn = dum_list[x]             
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_object, filename = dmy_spwn)
            if rbx_selected:
                back_to_edit_mode(rbx_selected)
            print(f"{dmy_spwn} Dummy Spawned")
            return {'FINISHED'} 

        
        if dmy == 'aepbr':    
            rbx_selected = selected_object()
            rbx_aepbr_fldr_path = os.path.join(glob_vars.addon_path, glob_vars.rbx_aepbr_fldr)
            rbx_aepbr_blend = os.listdir(rbx_aepbr_fldr_path)[0]
            rbx_aepbr_blend_path = os.path.join(rbx_aepbr_fldr_path, rbx_aepbr_blend)
            bpy.ops.wm.append(directory = rbx_aepbr_blend_path + glob_vars.ap_collection, filename = glob_vars.rbx_aepbr_collection)
            if rbx_selected:
                back_to_edit_mode(rbx_selected)
            print(f"{dmy_spwn} Dummy Spawned")
            return {'FINISHED'} 

            
        ### Rigs
        else:
            rbx_selected = selected_object() 
            bpy.ops.wm.append(directory =glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename = dmy)
            if rbx_selected:
                back_to_edit_mode(rbx_selected)
            print(f"{dmy} Spawned")
            return {'FINISHED'} 


        