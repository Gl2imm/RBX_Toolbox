import bpy


    #OPERATOR         
######################################## 
class RBXToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
 
    rbx_asset_folder: bpy.props.StringProperty(name="Folder",
        description="Select Assets folder",
        default="",
        maxlen=1024,
        subtype="DIR_PATH") # type: ignore
                                                                                                            
        
             
