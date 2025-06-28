import bpy
from RBX_Toolbox import glob_vars



######### Armature Buttons ###########    
class BUTTON_BN(bpy.types.Operator):
    bl_label = "BUTTON_BN"
    bl_idname = "object.button_bn"
    bl_options = {'REGISTER', 'UNDO'}
    bn : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        bn = self.bn
        global bn_selection
        global bn_error
        global msh_selection
        global msh_error
        bn_error = None
        msh_error = None


        bn_items = [
                    'Character_bones_blocky',
                    'Character_bones_r15_boy',
                    'Character_bones_r15_girl',
                    'Character_bones_r15_woman',
                    ] 
      
        
        #### Append Armature ####
        bn_split = bn.rsplit('_')
        
        if bn_split[-1] == 'arma':
            for x in range(len(bn_items)):
                if rbx_prefs.rbx_arma_enum == 'OP' + str(x+1):
                    rbx_arma_spwn = bn_items[x]                  

            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_object, filename =rbx_arma_spwn)            
            bn_sel = bpy.context.selected_objects[0].name
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.data.objects[bn_sel].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[bn_sel]
            print("Armature Appended")

 
        #### Recalculate Normals ####
        if bn == 'normal':
            bn_mesh = 0
            sel = bpy.context.selected_objects
            if len(sel) < 1:
                print("Nothing Selected")
                msh_selection = "Nothing Selected"                
            else:
                for x in sel:
                    if x.type != 'MESH':
                        print(x.type + " Selected. Pls Select Only Mesh")
                        msh_selection = "Pls Select Only Mesh"
                        bn_mesh = 0
                    else:
                        bn_mesh = 1
                        msh_selection = None
                if bn_mesh == 1:
                    if bpy.context.mode == 'OBJECT':
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')                
                    elif bpy.context.mode == 'EDIT_MESH':
                        bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                    bpy.ops.object.editmode_toggle()
                    msh_error = 'done_nml'
                    print("Normals Recalculated")
            
        #### Remove Duplicated Vertices ####
        if bn == 'doubles':
            bn_mesh = 0
            sel = bpy.context.selected_objects
            if len(sel) < 1:
                print("Nothing Selected")
                msh_selection = "Nothing Selected"
            else:
                for x in sel:
                    if x.type != 'MESH':
                        print(x.type + " Selected. Pls Select Only Mesh")
                        msh_selection = "Pls Select Only Mesh"
                        bn_mesh = 0
                    else:
                        bn_mesh = 1
                        msh_selection = None
                if bn_mesh == 1:
                    if bpy.context.mode == 'OBJECT':
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')                
                    elif bpy.context.mode == 'EDIT_MESH':
                        bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.mesh.normals_make_consistent(inside=False)
                    bpy.ops.object.editmode_toggle()
 
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    bpy.context.object.data.use_auto_smooth = False
                        
                    msh_error = 'done_vts'
                    print("Doubles Removed")
                        
        #### Parent Armature ####
        if bn == 'parent':
            bn_arma = 0
            bn_mesh = 0
            
            sel = bpy.context.selected_objects
            if len(sel) < 1:
                print("Nothing Selected")
                bn_selection = "Nothing Selected"
            else:
                print(sel)
                if len(sel) > 2:
                    print("More than 2 Objects selected")
                    bn_selection = "More than 2 Objects selected"
                else:
                    if len(sel) < 2:
                        print("2 Objects Must be Selected")
                        bn_selection = "Select 2 Objects"
                    else:
                        for x in sel:
                            if x.type == 'ARMATURE':
                                bn_arma = 1
                                break
                        if bn_arma == 0:
                            print("No Bones Selected")
                            bn_selection = "No Bones Selected"
                        for x in sel:
                            if x.type == 'MESH':
                                bn_mesh = 1
                                break
                        if bn_mesh == 0:
                            print("No Mesh Selected")
                            bn_selection = "No Mesh Selected"
                                
            if bn_arma == 1 and bn_mesh == 1:
                bn_selection = None
                bn_active = bpy.context.view_layer.objects.active
                if bn_active.type != 'ARMATURE':
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = None
                    for x in sel:
                        if x.type == 'ARMATURE':
                            bpy.data.objects[x.name].select_set(True)
                            bpy.context.view_layer.objects.active = bpy.data.objects[x.name]
                        else:
                            bpy.data.objects[x.name].select_set(True)     
                try:
                    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
                except:
                    bn_error = 1
                else:
                    print("Bones Successfully Parented")
                    bn_error = 2
                    

        return {'FINISHED'}