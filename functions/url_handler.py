import bpy
import webbrowser
from RBX_Toolbox import glob_vars



############   URL HANDLER OPERATOR   ##############    
class URL_HANDLER(bpy.types.Operator):
    bl_label = "URL_HANDLER"
    bl_idname = "object.url_handler"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_link : bpy.props.StringProperty(name= "Added") # type: ignore


    def execute(self, context):
        rbx_link = (self.rbx_link)
        rbx_guides = ['Credits and Instructions','Version_log','Guide_Armature']
                    
        if rbx_link == "update":
            webbrowser.open_new("https://github.com/Gl2imm/RBX_Toolbox/releases")
            
        if rbx_link == "discord":
            webbrowser.open_new("https://discord.gg/gFa4mY7")   
            
        if rbx_link == "mixamo":
            webbrowser.open_new("https://www.mixamo.com/") 
            
        if rbx_link == "rbx github":
            webbrowser.open_new("https://github.com/Roblox/avatar") 
        
        if rbx_link == "rbx nuke":
            webbrowser.open_new("https://www.youtube.com/watch?v=ggqvqwYQUSc")
                
        if rbx_link == "zeb twitter":
            webbrowser.open_new("https://twitter.com/Zeblyno")
            
        if rbx_link == "buy coffee":
            webbrowser.open_new("https://donate.stripe.com/fZe5op0W1fjg2nC002") 

        if rbx_link == "tips 10":
            webbrowser.open_new("https://www.roblox.com/game-pass/1292957634/RBX-Toolbox-Tips-Supporter")   

        if rbx_link == "tips 50":
            webbrowser.open_new("https://www.roblox.com/game-pass/132720885/RBX-Toolbox-tips-Hero") 

        if rbx_link == "tips 500":
            webbrowser.open_new("https://www.roblox.com/game-pass/132688311/RBX-Toolbox-Tips-Legend") 

        if rbx_link == "tips 1000":
            webbrowser.open_new("https://www.roblox.com/game-pass/1292117937/RBX-Toolbox-Tips-Epic")                                              

        for x in range(len(rbx_guides)):
            if rbx_link == rbx_guides[x]:
                texts_exist = bpy.data.texts.get(rbx_guides[x])
                if texts_exist != None:
                    bpy.context.area.ui_type = 'TEXT_EDITOR'
                    bpy.context.space_data.text = bpy.data.texts[rbx_guides[x]]
                else:
                    instructions = glob_vars.addon_path + glob_vars.fbs + glob_vars.info + glob_vars.fbs + rbx_guides[x] + ".txt"
                    with open(instructions) as f:
                        text = f.read()
                    t = bpy.data.texts.new(rbx_guides[x])
                    t.write("To switch back to normal view switch from 'TEXT EDITOR' to '3D Viewport'. Or just press 'Shift+F5' \n \n \n") 
                    t.write(text)          
                    bpy.context.area.ui_type = 'TEXT_EDITOR'
                    bpy.context.space_data.text = bpy.data.texts[rbx_guides[x]]
                    bpy.context.space_data.show_word_wrap = True
                    bpy.ops.text.jump(line=1)


        if rbx_link == "aepbr discord":
            webbrowser.open_new("https://discord.gg/qSuEemywG2")
        if rbx_link == "aepbr notes":
            rbx_aepbr_notes_url = "https://github.com/paribeshere/AEPBR/releases/tag/v." + glob_vars.aepbr_lts_ver
            webbrowser.open_new(rbx_aepbr_notes_url)
        
        
        return {'FINISHED'}