import bpy
from RBX_Toolbox import glob_vars



class RBX_BUTTON_HDRI(bpy.types.Operator):
    bl_label = "RBX_BUTTON_HDRIFULL"
    bl_idname = "object.rbx_button_hdrifull"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_hdri : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        rbx_hdri = (self.rbx_hdri)
        
        if rbx_hdri == 'sky':
            if rbx_prefs.rbx_sky_enum == 'OP1':
                rbx_hdri_name = "Sky-1_(From_unsplash).jpg"                    
            if rbx_prefs.rbx_sky_enum == 'OP2':
                rbx_hdri_name = "Sky-2_(From_unsplash).jpg"                  
            if rbx_prefs.rbx_sky_enum == 'OP3':
                rbx_hdri_name = "Sky-3_(From_unsplash).jpg"
                            
            if bpy.data.objects.get("Sky Sphere") == None:
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_object, filename ='Sky Sphere')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects['Sky Sphere'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Sky Sphere']
            sky_img_path = glob_vars.addon_path + glob_vars.fbs + 'img' + glob_vars.fbs + 'sky' + glob_vars.fbs + rbx_hdri_name
            sky_image = bpy.data.images.load(sky_img_path)
            bpy.data.objects['Sky Sphere'].active_material.node_tree.nodes['Image Texture'].image = sky_image 
            
            
        if rbx_hdri == 'hdri':
            if rbx_prefs.rbx_hdri_enum == 'OP1':
                rbx_hdri_name = "World"                    
            if rbx_prefs.rbx_hdri_enum == 'OP2':
                rbx_hdri_name = "City"                  
            if rbx_prefs.rbx_hdri_enum == 'OP3':
                rbx_hdri_name = "Courtyard"
            if rbx_prefs.rbx_hdri_enum == 'OP4':
                rbx_hdri_name = "Forest"
            if rbx_prefs.rbx_hdri_enum == 'OP5':
                rbx_hdri_name = "Interior"
            if rbx_prefs.rbx_hdri_enum == 'OP6':
                rbx_hdri_name = "Night"
            if rbx_prefs.rbx_hdri_enum == 'OP7':
                rbx_hdri_name = "Studio"
            if rbx_prefs.rbx_hdri_enum == 'OP8':
                rbx_hdri_name = "Sunrise"
            if rbx_prefs.rbx_hdri_enum == 'OP9':
                rbx_hdri_name = "Sunset"
                                                                                                                     

            if rbx_hdri_name == 'World':
                try:
                    rbx_hdri = bpy.data.worlds[rbx_hdri_name]
                except:
                    bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_world, filename =rbx_hdri_name)
                    rbx_hdri = bpy.data.worlds[rbx_hdri_name]
                scene.world = rbx_hdri
                print(rbx_hdri_name + " has been Appended and applied to the World")
            else:
                if bpy.context.scene.world != 'HDRI':
                    if 'HDRI' not in bpy.data.worlds:
                        bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_world, filename ='HDRI')
                    rbx_hdri = bpy.data.worlds['HDRI']
                    scene.world = rbx_hdri
                    hdri_img_path = glob_vars.bldr_hdri_path + rbx_hdri_name + '.exr'
                    hdri_image = bpy.data.images.load(hdri_img_path)
                    bpy.data.worlds['HDRI'].node_tree.nodes['Environment Texture'].image = hdri_image 

        return {'FINISHED'}  