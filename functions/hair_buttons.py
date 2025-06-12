import bpy
import glob_vars


######### Hair Buttons ###########    
class BUTTON_HAIR(bpy.types.Operator):
    bl_label = "BUTTON_HAIR"
    bl_idname = "object.button_hair"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_hair : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs         
        rbx_hair = self.rbx_hair
        rbx_mode = None

        global rbx_bkd_hair_img

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
                        
        dum_hd_list = [
                        'Classic Head',
                        'Woman Head',
                        'Woman Head v2',
                        'Man Head',
                        'R6 Head'
                        ] 
        
        if rbx_hair == 'Dummy_head': 
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects
                
                                
            for x in range(len(dum_list)):
                if rbx_prefs.rbx_dum_hd_enum == 'OP' + str(x+1):
                    dmy_spwn = dum_hd_list[x]                  

            bpy.ops.wm.append(directory =glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_object, filename =dmy_spwn)
            
            if rbx_mode == 1:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[rbx_sel[0].name].select_set(True)            
                bpy.ops.object.editmode_toggle()
            
            print(dmy_spwn + " Spawned")

                               
        if rbx_hair == 'hair_template':    
            if bpy.context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
                rbx_mode = 1
                rbx_sel = bpy.context.selected_objects                

            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename ='Hair Template')
            
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
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename ='Hair Shader')
                
            
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