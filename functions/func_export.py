import bpy


############   OPERATORS   ##############    
class RBX_OPERATORS(bpy.types.Operator):
    bl_label = "RBX_OPERATORS"
    bl_idname = "object.rbx_operators"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_operator : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_operator = (self.rbx_operator)
                    
        if rbx_operator == 'exp_fbx':
            if rbx_prefs.rbx_of_trsf == True:
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            if rbx_prefs.rbx_of_orig == True:
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', use_selection=True, object_types={'MESH'}, global_scale=0.01, bake_anim=False)
            
        if rbx_operator == 'exp_fbx_lc':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', path_mode='COPY', embed_textures=True, use_selection=True, object_types={'ARMATURE', 'MESH', 'OTHER'}, add_leaf_bones=False, global_scale=0.01, bake_anim=False)            
            
        if rbx_operator == 'set_unit': 
            bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'
            bpy.context.scene.unit_settings.scale_length = 0.01

        return {'FINISHED'}