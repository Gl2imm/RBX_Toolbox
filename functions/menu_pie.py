import bpy
from RBX_Toolbox import glob_vars




#### RBX PIE MENU ####
def find_user_keyconfig(key):
    km, kmi = glob_vars.addon_keymaps[key]
    for item in bpy.context.window_manager.keyconfigs.user.keymaps[km.name].keymap_items:
        found_item = False
        if kmi.idname == item.idname:
            found_item = True
            for name in dir(kmi.properties):
                if not name in ["bl_rna", "rna_type"] and not name[0] == "_":
                    if not kmi.properties[name] == item.properties[name]:
                        found_item = False
        if found_item:
            return item
    print(f"Couldn't find keymap item for {key}, using addon keymap instead. This won't be saved across sessions!")
    return kmi


#### MAIN MENU ####
class RBX_MT_MENU(bpy.types.Menu):
    bl_idname = "RBX_MT_MENU"
    bl_label = "RBX Toolbox Menu"

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        layout = self.layout.menu_pie()
        op = layout.prop(bpy.context.space_data.overlay, 'show_face_orientation', text='Show Face Orientation', icon='NORMALS_FACE') 
        layout.menu('RBX_MT_MENU3', text='Set Origin', icon='LAYER_ACTIVE')
        layout.menu('RBX_MT_MENU2', text='Recalculate Normals', icon='FACESEL')
        layout.menu('RBX_MT_MENU4', text='Shading', icon='SHADING_TEXTURE')
        

           
#### Recalculate MENU ####        
class RBX_MT_MENU2(bpy.types.Menu):
    bl_idname = "RBX_MT_MENU2"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        layout.menu('RBX_MT_MENU2_1', text='Recalc Outside', icon_value=0)
        layout.menu('RBX_MT_MENU2_2', text='Recalc Inside', icon_value=0)
        layout.menu('RBX_MT_MENU2_3', text='Flip Normals', icon_value=0)


#### Recalculate SUBMENU Recalc Outside ####        
class RBX_MT_MENU2_1(bpy.types.Menu):
    bl_idname = "RBX_MT_MENU2_1"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        op = layout.operator("object.rbx_button_of", text = "All Faces").rbx_of = 'pie_outside_all'
        op = layout.operator("object.rbx_button_of", text = "Selected Faces").rbx_of = 'pie_outside'


#### Recalculate SUBMENU Recalc Inside ####        
class RBX_MT_MENU2_2(bpy.types.Menu):
    bl_idname = "RBX_MT_MENU2_2"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        op = layout.operator("object.rbx_button_of", text = "All Faces").rbx_of = 'pie_inside_all'
        op = layout.operator("object.rbx_button_of", text = "Selected Faces").rbx_of = 'pie_inside'
        

#### Recalculate SUBMENU Recalc Flip Normals ####        
class RBX_MT_MENU2_3(bpy.types.Menu):
    bl_idname = "RBX_MT_MENU2_3"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        op = layout.operator("object.rbx_button_of", text = "All Faces").rbx_of = 'pie_flip_all'
        op = layout.operator("object.rbx_button_of", text = "Selected Faces").rbx_of = 'pie_flip'
        

#### Origin MENU #### 
class RBX_MT_MENU3(bpy.types.Menu):
    bl_idname = "RBX_MT_MENU3"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        op = layout.operator("object.rbx_button_of", text = "To Geometry").rbx_of = 'orig_to_geo'
        op = layout.operator("object.rbx_button_of", text = "To 3D Cursor").rbx_of = 'orig_to_3d'

        
#### Shading MENU #### 
class RBX_MT_MENU4(bpy.types.Menu):
    bl_idname = "RBX_MT_MENU4"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        op = layout.operator("object.rbx_button_of", text = "Shade Flat").rbx_of = 'shd_flat'
        op = layout.operator("object.rbx_button_of", text = "Shade Smooth").rbx_of = 'shd_smooth'
        op = layout.operator("object.rbx_button_of", text = "Shade Auto Smooth").rbx_of = 'shd_aut_smooth'
        #op = layout.prop(bpy.context.object.data.auto_smooth_angle,"default_value", text = "")