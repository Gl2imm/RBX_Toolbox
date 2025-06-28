import bpy
import os
from RBX_Toolbox import glob_vars



######### Other Functions ###########    
class RBX_BUTTON_OF(bpy.types.Operator):
    bl_label = "RBX_BUTTON_OF"
    bl_idname = "object.rbx_button_of"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_of : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        rbx_of = self.rbx_of
        
        
        if rbx_of == 'orig_to_geo':
            try:
                sel = bpy.context.selected_objects
            except:
                pass
            else:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')


        if rbx_of == 'orig_to_3d':
            try:
                sel = bpy.context.selected_objects
            except:
                pass
            else:
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')


        if rbx_of == 'shd_flat':
            try:
                sel = bpy.context.selected_objects
            except:
                pass
            else:
                bpy.ops.object.shade_flat()
                

        if rbx_of == 'shd_smooth':
            try:
                sel = bpy.context.selected_objects
            except:
                pass
            else:
                #bpy.ops.object.shade_smooth(use_auto_smooth=False, auto_smooth_angle=0.523599)
                bpy.ops.object.shade_smooth()

                

        if rbx_of == 'shd_aut_smooth':
            try:
                sel = bpy.context.selected_objects
            except:
                pass
            else:
                #bpy.ops.object.shade_smooth(use_auto_smooth=True, auto_smooth_angle=0.523599)
                bpy.ops.object.shade_auto_smooth()

                                                
                            
        if rbx_of == 'inside' or rbx_of == 'outside' or rbx_of == 'flip':
            def rbx_of_recalc():
                if rbx_of == 'outside':
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                if rbx_of == 'inside':
                    bpy.ops.mesh.normals_make_consistent(inside=True)
                if rbx_of == 'flip':
                    bpy.ops.mesh.flip_normals()
                

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
        
        
        
        if rbx_of == 'glow':
            try:
                sel = bpy.context.selected_objects
            except:
                pass
            else:
                if bpy.context.mode == 'OBJECT':
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.point_normals(target_location=(0, 0, 99999))
                    bpy.ops.object.editmode_toggle() 
                elif bpy.context.mode == 'EDIT_MESH':
                    bpy.ops.mesh.point_normals(target_location=(0, 0, 99999))
                else:
                    return {'FINISHED'}


        if rbx_of == 'unglow':
            try:
                sel = bpy.context.selected_objects
            except:
                pass
            else:
                if bpy.context.mode == 'OBJECT':
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                elif bpy.context.mode == 'EDIT_MESH':
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    bpy.ops.object.editmode_toggle()
                else:
                    return {'FINISHED'}
 
 
        if rbx_of == 'make_outline':
            obj = bpy.context.selected_objects[0]
            
            if 'RBX_Outline' not in obj.modifiers:
                obj.modifiers.new("RBX_Outline","SOLIDIFY")
                solidify = obj.modifiers["RBX_Outline"]
                solidify.use_flip_normals = True
                solidify.thickness = -0.1
                solidify.material_offset = 999
            
            
            mat = bpy.data.materials.get("RBX_Outline_mat")
            if mat == None:
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_material, filename ='RBX_Outline_mat')
                mat = bpy.data.materials.get("RBX_Outline_mat") 
                
            mat.node_tree.nodes["RGB"].outputs[0].default_value = (0, 0, 0, 1)
            if mat.use_backface_culling != True:
                mat.use_backface_culling = True

            if "RBX_Outline_mat" not in obj.material_slots:
                obj.data.materials.append(mat)
            

        if rbx_of == 'apply_outline':
            obj = bpy.context.selected_objects[0]
                        
            bpy.ops.object.modifier_apply(modifier="RBX_Outline")
            obj.active_material_index = 1
            
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.material_slot_select() #Select all faces from the outline material
            bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=False) #UV unwrap
            
            original_area = bpy.context.area.type
            bpy.context.area.ui_type = 'UV'
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.transform.translate(value=(1, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False)) #Move Unwrapped UV
            bpy.context.area.type = original_area # return to the original mode where the script was run
            bpy.ops.object.editmode_toggle()
            
            bpy.ops.object.material_slot_remove()
            bpy.context.object.active_material.use_backface_culling = True




       
        
        #### Recalculate Normals (Pie Menu)####
        if rbx_of == 'pie_inside' or rbx_of == 'pie_outside' or rbx_of == 'pie_flip' or rbx_of == 'pie_inside_all' or rbx_of == 'pie_outside_all' or rbx_of == 'pie_flip_all':
            def rbx_of_recalc():
                if rbx_of == 'pie_outside' or rbx_of == 'pie_outside_all':
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                if rbx_of == 'pie_inside' or rbx_of == 'pie_inside_all':
                    bpy.ops.mesh.normals_make_consistent(inside=True)
                if rbx_of == 'pie_flip' or rbx_of == 'pie_flip_all':
                    bpy.ops.mesh.flip_normals()
                

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
                        if rbx_of == 'pie_inside' or rbx_of == 'pie_outside' or rbx_of == 'pie_flip':
                            rbx_of_recalc()
                        if rbx_of == 'pie_inside_all' or rbx_of == 'pie_outside_all' or rbx_of == 'pie_flip_all':
                            bpy.ops.mesh.select_all(action='SELECT')
                            rbx_of_recalc()
                        bpy.ops.object.editmode_toggle()               
                    elif bpy.context.mode == 'EDIT_MESH':
                        if rbx_of == 'pie_inside' or rbx_of == 'pie_outside' or rbx_of == 'pie_flip':
                            rbx_of_recalc()
                        if rbx_of == 'pie_inside_all' or rbx_of == 'pie_outside_all' or rbx_of == 'pie_flip_all':
                            bpy.ops.mesh.select_all(action='SELECT')
                            rbx_of_recalc()

                print("Normals Recalculated")
                           
 
        if rbx_of == 'theme_install':
            file = "Theme/RBXToolbox.xml"
            path = os.path.join(glob_vars.addon_path, file)
            bpy.ops.preferences.theme_install(overwrite=True, filepath=path, filter_folder=True, filter_glob="*.xml")
            #bpy.ops.preferences.reset_default_theme()     
        
        
                                                                                                                           
        return {'FINISHED'}      