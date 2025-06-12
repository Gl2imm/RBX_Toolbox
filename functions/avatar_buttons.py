import bpy
import glob_vars



######### Avatar Buttons ########### 
class RBX_BUTTON_AVA(bpy.types.Operator):
    bl_label = "RBX_BUTTON_AVA"
    bl_idname = "object.rbx_button_ava"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_ava : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        global rbx_anim_error
        global unhide_store
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_ava = self.rbx_ava

        ava_list = [
                    'Blocky_ava',
                    'Round_male',
                    'Anime_ava'
                    ]

        if rbx_ava == 'avatar':     
            for x in range(len(ava_list)):
                if rbx_prefs.rbx_ava_enum == 'OP' + str(x+1):
                    ava_spwn = ava_list[x]   
                                 
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename =ava_spwn)
            
            
            
        if rbx_ava == 'clear':
            selected = bpy.context.selected_objects
            active = bpy.context.view_layer.objects.active
            prop_lst = []
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            
            for item in selected:
                bpy.data.objects[item.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[item.name]
                
                props = bpy.data.objects[item.name].items()
       
                for x in props:
                    prop_lst.append(x[0])
                for prop in prop_lst:
                    bpy.ops.wm.properties_remove(data_path='object', property_name=prop)
                prop_lst.clear()
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                
            for item in selected:
                bpy.data.objects[item.name].select_set(True)
                bpy.context.view_layer.objects.active = active
                
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'rename':
            objects = bpy.context.selected_objects
        
            for item in objects:
                if '.' in item.name:
                     new_name = item.name.split('.')[0]
                     item.name = new_name
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'hide':
            objects = bpy.context.selected_objects
            
            for item in objects:
                if '_Att' in item.name:
                    item.hide_viewport = True
                    unhide_store.append(item)
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'unhide':
           unhide_store.clear()
           bpy.context.view_layer.update()
           
           for item in unhide_store:
               item.hide_viewport = False

           unhide_store.clear()
           bpy.context.view_layer.update()
                   
            
        if rbx_ava == 'export':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', path_mode='COPY', embed_textures=True, use_selection=True, object_types={'MESH', 'OTHER', 'EMPTY', 'ARMATURE'}, use_custom_props=True, add_leaf_bones=False, bake_anim=True, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=False, bake_anim_simplify_factor=0)


        return {'FINISHED'}         