import bpy
import glob_vars


######### Layered Clothing Animation ########### 
class RBX_BUTTON_LC_ANIM(bpy.types.Operator):
    bl_label = "RBX_BUTTON_LC_ANIM"
    bl_idname = "object.rbx_button_lc_anim"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_lc_anim : bpy.props.StringProperty(name= "Added") # type: ignore

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
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename =rbx_anim_dum_spwn)
                bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
                #bpy.ops.transform.translate(value=(5, -0, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL') #old
                bpy.ops.transform.translate(value=(5, -0, -0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
                #bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))
                
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
                #bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(5, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 1, 0)), "orient_matrix_type":'GLOBAL'}) #Old
                bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(5, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True)})
                
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
                    bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_object, filename =rbx_anim_spwn)
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
                    
                    '''''' 
                          
        return {'FINISHED'}   