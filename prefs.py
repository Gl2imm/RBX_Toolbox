import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty
import platform
from . import glob_vars



print("**********************************************")
print("RBX Toolbox Log")
print("OS Platform: " + platform.system())
print("Blender ver:", glob_vars.bldr_ver)
print("Addon path:", glob_vars.addon_path)
print("**********************************************")

# OPERATOR
########################################
class RBXToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    bl_idname = "RBX_Toolbox"



    rbx_asset_folder: bpy.props.StringProperty(name="Folder",
                                               description="Select Assets folder",
                                               default="",
                                               maxlen=1024,
                                               subtype="DIR_PATH")  # type: ignore
    




    ### OAuth ###
    # The identifier of the selected creator (e.g., "U12345" or "G67890")
    creator: StringProperty(
        name="Selected Creator ID",
        description="The last used Creator ID for uploads",
        default="",
    ) # type: ignore

    # Simple flag to know if the user was logged in
    is_logged_in: BoolProperty(
        name="Is Logged In",
        description="Whether there is an active login session saved",
        default=False,
    ) # type: ignore

    # The entire token dictionary (access, refresh, expiry) stored as a JSON string
    saved_token_data_json: StringProperty(
        name="Saved Token Data (JSON)",
        description="Stores the OAuth token data as a JSON string",
        default="",
    ) # type: ignore

    # The list of available creators (User + Groups) stored as a JSON string
    saved_creators_json: StringProperty(
        name="Saved Creators (JSON)",
        description="Stores the list of available creators as a JSON string",
        default="",
    ) # type: ignore

    # These properties are not editable via preferences UI, they get reflected to and from properties in memory.
    # The only token we need to persist is the refresh token, since it gives all new tokens in the next session
    refresh_token: StringProperty() # type: ignore
    selected_creator_enum_index: IntProperty() # type: ignore





    ### Upload to Roblox ###
    # export_scale is configurable via the Add-on preferences menu in Blender
    DEFAULT_EXPORT_SCALE = 0.01  # Blender Meters are 100:1 to Studio Studs

    export_scale: FloatProperty(
        name="Export Scale",
        default=DEFAULT_EXPORT_SCALE,
        soft_max=1000,
        soft_min=0.001,
        step=0.01,
        description=f"Global scale applied to objects during export for upload.\nDEFAULT: {DEFAULT_EXPORT_SCALE} (Blender Meters are 100:1 to Studio Studs)",
    ) # type: ignore
    bake_anim: BoolProperty(
        name="Baked Animation",
        description="Export baked keyframe animation",
        default=True,
    ) # type: ignore
    bake_anim_use_all_bones: BoolProperty(
        name="Key All Bones",
        description="Force exporting at least one key of animation for all bones "
        "(needed with some target applications, like UE4)",
        default=True,
    ) # type: ignore
    bake_anim_use_nla_strips: BoolProperty(
        name="NLA Strips",
        description="Export each non-muted NLA strip as a separated FBX's AnimStack, if any, "
        "instead of global scene animation",
        default=True,
    ) # type: ignore
    bake_anim_use_all_actions: BoolProperty(
        name="All Actions",
        description="Export each action as a separated FBX's AnimStack, instead of global scene animation "
        "(note that animated objects will get all actions compatible with them, "
        "others will get no animation at all)",
        default=True,
    ) # type: ignore
    bake_anim_force_startend_keying: BoolProperty(
        name="Force Start/End Keying",
        description="Always add a keyframe at start and end of actions for animated channels",
        default=True,
    ) # type: ignore
    bake_anim_step: FloatProperty(
        name="Sampling Rate",
        description="How often to evaluate animated values (in frames)",
        min=0.01,
        max=100.0,
        soft_min=0.1,
        soft_max=10.0,
        default=1.0,
    ) # type: ignore
    bake_anim_simplify_factor: FloatProperty(
        name="Simplify",
        description="How much to simplify baked values (0.0 to disable, the higher the more simplified)",
        min=0.0,
        # No simplification to up to 10% of current magnitude tolerance.
        max=100.0,
        soft_min=0.0,
        soft_max=10.0,
        default=1.0,  # default: min slope: 0.005, max frame step: 10.
    ) # type: ignore
    add_leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)",
        default=True,
    ) # type: ignore
    use_custom_props: BoolProperty(
        name="Custom Properties",
        description="Export Custom Properties",
        default=True,
    ) # type: ignore

    def draw(self, context):
        self.layout.label(text="Include")
        include_box = self.layout.box()
        include_box.prop(self, "use_custom_props")

        self.layout.label(text="Transform")
        transform_box = self.layout.box()
        transform_box.prop(self, "export_scale")

        self.layout.label(text="Armature")
        armature_box = self.layout.box()
        armature_box.prop(self, "add_leaf_bones")

        self.layout.prop(self, "bake_anim", text="Bake Animation")
        bake_anim_box = self.layout.box()
        bake_anim_box.use_property_split = True
        bake_anim_box.enabled = self.bake_anim
        bake_anim_box.prop(self, "bake_anim_use_all_bones")
        bake_anim_box.prop(self, "bake_anim_use_nla_strips")
        bake_anim_box.prop(self, "bake_anim_use_all_actions")
        bake_anim_box.prop(self, "bake_anim_force_startend_keying")
        bake_anim_box.prop(self, "bake_anim_step")
        bake_anim_box.prop(self, "bake_anim_simplify_factor")
                                                                                                            
        
             
