import bpy
import glob_vars


######### Camera Buttons ###########    
class BUTTON_CMR(bpy.types.Operator):
    bl_label = "BUTTON_CMR"
    bl_idname = "object.button_cmr"
    bl_options = {'REGISTER', 'UNDO'}
    cmr : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        cmr = self.cmr
        cmr_spl = cmr.rsplit('_',1)
        
        #### Apend Cameras Stage ####
        if cmr == 'append':               
            if bpy.data.objects.get('Camera_F') == None:
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename ='Cameras')
                bpy.context.scene.render.resolution_x = 1080
                bpy.context.scene.render.resolution_y = 1080
                bpy.context.scene.render.resolution_percentage = 100
                print("Cameras Setup Spawned")
            else:
                print("Cameras Setup Already Exist")

        #### Apend Cameras Stage ####
        if cmr == 'edtr_append':               
            if bpy.data.objects.get('Avatar Editor Camera') == None:
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename ='Avatar Editor Room (New)')
                bpy.context.scene.render.resolution_x = 1080
                bpy.context.scene.render.resolution_y = 1080
                bpy.context.scene.render.resolution_percentage = 100
                print("Avatar Editor Room Setup Spawned")
            else:
                print("Avatar Editor Room Setup Already Exist") 
            if bpy.context.scene.world != 'Avatar Editor Stage (New) World':
                if 'Avatar Editor Stage (New) World' not in bpy.data.worlds:
                    bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_world, filename ='Avatar Editor Stage (New) World')
                rbx_hdri = bpy.data.worlds['Avatar Editor Stage (New) World']
                scene.world = rbx_hdri
            
        
        #### Set Active ####        
        if cmr_spl[-1] == 'active':
            cam = bpy.data.objects[cmr_spl[0]]
            bpy.data.scenes['Scene'].camera = cam
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects[cmr_spl[0]].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[cmr_spl[0]]
            print(cmr_spl[0] + " Set as Active")
            
        #### Preview ####        
        if cmr == 'preview':
            try:
                for i in range(len(glob_vars.cams)):
                    if bpy.context.active_object.name == glob_vars.cams[i]:
                        bpy.ops.view3d.object_as_camera()
            except:
                pass


            
        #### Add Animated Staging ####    
        if cmr == 'staging':
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename='Staging')
            print("Animated Staging Setup Appended")

        #### Set Active (Staging cam) ####        
        if cmr == 'staging-active':
            cam = bpy.data.objects['Staging Camera']
            bpy.data.scenes['Scene'].camera = cam
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects['Staging Camera'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Staging Camera']
            print("'Staging Camera' Set as Active")
            del cam 
            
        #### Set Active (Avatar Editor Room cam) ####        
        if cmr == 'edtr-active':
            cam = bpy.data.objects['Avatar Editor Camera']
            bpy.data.scenes['Scene'].camera = cam
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects['Avatar Editor Camera'].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects['Avatar Editor Camera']
            print("'Avatar Editor Camera' Set as Active")
            del cam                         


        #### Append Roblox Baseplate ####
        if cmr == 'bsplt_append':               
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename ='RBX Baseplate')
                
                                                                                                                        
        return {'FINISHED'}      