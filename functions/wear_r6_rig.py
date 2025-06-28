import bpy
import os
import asyncio
import requests

from RBX_Toolbox import glob_vars



######### Wear Character ###########    
class BUTTON_WEAR(bpy.types.Operator):
    bl_label = "BUTTON_WEAR"
    bl_idname = "object.button_wear"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_cloth : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        scene = context.scene
        rbx_prefs = scene.rbx_prefs 
        rbx_cloth = self.rbx_cloth
        rbx_face = rbx_prefs.rbx_face
        rbx_shirt = rbx_prefs.rbx_shirt
        rbx_pants = rbx_prefs.rbx_pants
        
        global rbx_face_netw_error
        global rbx_shirt_netw_error
        global rbx_pants_netw_error
        global rbx_face_name 
        global rbx_shirt_name
        global rbx_pants_name
        global rbx_face_filename
        global rbx_shirt_filename
        global rbx_pants_filename
        
        
        rbx_character = None 
        rbx_cloth_error = None
                

        char_list = ['RoBone'] 
        rbx_parts = {
                    0 : ['Head', 'Left Hand', 'Left Leg', 'Right Hand', 'Right Leg', 'Torso']
                    }              
        rbx_clothes = {
                    0 : ['R6 Head', 'R6 Shirt', 'R6 Pants', 'R6 Shirt', 'R6 Pants', 'R6 Torso']
                    }
              
        ##### Create Folders #####
        if rbx_cloth == 'folder':
            if not os.path.exists(glob_vars.addon_path + '/Imported_Clothes'):
                os.makedirs(glob_vars.addon_path + '/Imported_Clothes')
            os.startfile(os.path.dirname(glob_vars.addon_path + '/Imported_Clothes/'))

        ### Check selected objects ###
        if rbx_cloth == 'mod':
            if bpy.context.mode != 'EDIT_MESH':
                rbx_object = bpy.context.selected_objects
                if len(rbx_object) == 1:
                    rbx_object = bpy.context.selected_objects[0]
                    if rbx_object.type == 'ARMATURE':
                        rbx_cloth_error = None
                    else:
                        rbx_cloth_error = "Error: Pls Select Armature"
                else:
                    rbx_cloth_error = "Error: Pls Select 1 Object"
            else:
                rbx_cloth_error = "Error: Pls Exit Edit Mode"


            if rbx_cloth_error == None:
                for x in range(len(char_list)):
                    if char_list[x] in rbx_object.name:
                        rbx_character = x
                        break
                          
            if rbx_character != None:  
                rbx_object.name = f"{rbx_object.name}_cloth_mod"         
                bpy.ops.object.select_grouped(type='COLLECTION')
                rbx_selected = bpy.context.selected_objects
            
                for part in rbx_parts[rbx_character]:
                    for mesh in rbx_selected:
                        if part in mesh.name:
                            bpy.ops.object.select_all(action='DESELECT')
                            bpy.context.view_layer.objects.active = None
                            bpy.data.objects[mesh.name].select_set(True)
                            bpy.context.view_layer.objects.active = bpy.data.objects[mesh.name]
                            
                            mat_index = rbx_parts[rbx_character].index(part)
                            mat_name = rbx_clothes[rbx_character][mat_index]
                            if mesh.material_slots:
                                bpy.ops.object.material_slot_remove()
                                
                                
                            if bpy.data.materials.get(f"{mat_name}_{rbx_object.name}") == None:
                                if bpy.data.materials.get(mat_name) == None:
                                    bpy.ops.wm.append(directory =glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_material, filename =mat_name)
                                    mat = bpy.data.materials.get(mat_name)
                                    mesh.data.materials.append(mat)
                                    mat.name = f"{mat_name}_{rbx_object.name}"
                            else:
                                mat = bpy.data.materials.get(f"{mat_name}_{rbx_object.name}")
                                mesh.data.materials.append(mat)
                                
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                bpy.data.objects[rbx_object.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[rbx_object.name]
        
        def get_id(data):
            error = None
            if "https://www.roblox.com/" in data:
                data = data.lstrip("https://www.roblox.com/catalog/")
                data = data.split("/")[0]
                if not data.isdigit():
                    error = "Error: Invalid URL"
            return data, error
        
        def make_folder(data):
            error = None
            path = os.path.join(glob_vars.addon_path, 'Imported_Clothes' + glob_vars.fbs + data)
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except:
                    error = "Error Making Accessory Folder" 
            return path, error
        
        def write_data(path, data, asset_name):
            error = None
            file = os.path.join(path, asset_name + ".png")
            with open(file, "wb") as f:
                f.write(data)      
            return file, error
        
        def prop_filename(name):
            forb_chars = dict((ord(char), None) for char in '\/*?:"<>|')
            new_name = name.translate(forb_chars)  
            return new_name   
            
        ##### Accessory Import ##### 
        if rbx_cloth == 'face':
            ##### Convert accessory input #####
            rbx_face, rbx_face_netw_error = get_id(rbx_face) 
            
            ### Get face Info ###
            if rbx_face_netw_error == None:        
                rbx_face_name, rbx_face_type, rbx_face_creator, rbx_face_netw_error = asyncio.run(self.get_acc_info(rbx_face))
            
            ### Make folder if dont have ###    
            if rbx_face_netw_error == None: 
                rbx_face_path, rbx_face_netw_error = make_folder("Faces")
            
            ### Get face thumbnail url ###    
            if rbx_face_netw_error == None:
                face_url, rbx_face_netw_error = asyncio.run(self.get_acc_thumb(rbx_face, rbx_cloth))
            
            ### Get face image data from thumbnail url ###     
            if rbx_face_netw_error == None:
                face_data, rbx_face_netw_error = asyncio.run(self.get_url_data(face_url))
            
            ### Write Data ###
            if rbx_face_netw_error == None:
                rbx_face_filename = prop_filename(rbx_face_name) #Remove forbidden characters
                rbx_face_tex, rbx_face_netw_error = write_data(rbx_face_path, face_data, rbx_face_filename)
                   
            ### Import Face ###
            if rbx_face_netw_error == None:
                rbx_object = bpy.context.selected_objects[0]
                rbx_image = bpy.data.images.load(rbx_face_tex)
                rbxtexNode = bpy.data.materials[f"R6 Head_{rbx_object.name}"].node_tree.nodes['Image Texture.001']

                #rbx_cloth_head = bpy.data.materials[f"R6 Head_{rbx_object.name}"].node_tree.nodes['R6 Cloth']
                rbxtexNode.image = rbx_image
 
 
         ##### Accessory Import ##### 
        if rbx_cloth == 'shirt':
            ##### Convert accessory input #####
            rbx_shirt, rbx_shirt_netw_error = get_id(rbx_shirt) 
            
            ### Get shirt Info ###
            if rbx_shirt_netw_error == None:        
                rbx_shirt_name, rbx_shirt_type, rbx_shirt_creator, rbx_shirt_netw_error = asyncio.run(self.get_acc_info(rbx_shirt))
                
            ### Get shirt asset ID ###
            if rbx_shirt_netw_error == None:        
                shirt_data, rbx_shirt_netw_error = asyncio.run(self.get_id_data(rbx_shirt, rbx_cloth))
                shirt_data = str(shirt_data).split("<url>http://www.roblox.com/asset/?id=")[1]
                rbx_shirt = shirt_data.split("</url>")[0] #Actual item ID
                
            ### Get shirt Data ###
            if rbx_shirt_netw_error == None:        
                shirt_data, rbx_shirt_netw_error = asyncio.run(self.get_id_data(rbx_shirt, rbx_cloth))
            
            ### Make folder if dont have ###
            if rbx_shirt_netw_error == None: 
                rbx_shirt_path, rbx_shirt_netw_error = make_folder("Shirts")   

            ### Write Data ###
            if rbx_shirt_netw_error == None:
                rbx_shirt_filename = prop_filename(rbx_shirt_name) #Remove forbidden characters
                rbx_shirt_tex, rbx_shirt_netw_error = write_data(rbx_shirt_path, shirt_data, rbx_shirt_filename)
                
            ### Import Shirt ###
            if rbx_shirt_netw_error == None:
                rbx_object = bpy.context.selected_objects[0]
                rbx_image = bpy.data.images.load(rbx_shirt_tex)
                rbxtexNode = bpy.data.materials[f"R6 Shirt_{rbx_object.name}"].node_tree.nodes['Image Texture.001']
                rbxtexNode2 = bpy.data.materials[f"R6 Torso_{rbx_object.name}"].node_tree.nodes['Image Texture.001']

                rbxtexNode.image = rbx_image 
                rbxtexNode2.image = rbx_image   


        ##### Accessory Import ##### 
        if rbx_cloth == 'pants':
            ##### Convert accessory input #####
            rbx_pants, rbx_pants_netw_error = get_id(rbx_pants) 
            
            ### Get pants Info ###
            if rbx_pants_netw_error == None:        
                rbx_pants_name, rbx_pants_type, rbx_pants_creator, rbx_pants_netw_error = asyncio.run(self.get_acc_info(rbx_pants))
                
            ### Get pants asset ID ###
            if rbx_pants_netw_error == None:        
                pants_data, rbx_pants_netw_error = asyncio.run(self.get_id_data(rbx_pants, rbx_cloth))
                pants_data = str(pants_data).split("<url>http://www.roblox.com/asset/?id=")[1]
                rbx_pants = pants_data.split("</url>")[0] #Actual item ID
                
            ### Get pants Data ###
            if rbx_pants_netw_error == None:        
                pants_data, rbx_pants_netw_error = asyncio.run(self.get_id_data(rbx_pants, rbx_cloth))
            
            ### Make folder if dont have ###
            if rbx_pants_netw_error == None: 
                rbx_pants_path, rbx_pants_netw_error = make_folder("Pants")   

            ### Write Data ###
            if rbx_pants_netw_error == None:
                rbx_pants_filename = prop_filename(rbx_pants_name) #Remove forbidden characters
                rbx_pants_tex, rbx_pants_netw_error = write_data(rbx_pants_path, pants_data, rbx_pants_filename)
                
            ### Import pants ###
            if rbx_pants_netw_error == None:
                rbx_object = bpy.context.selected_objects[0]
                rbx_image = bpy.data.images.load(rbx_pants_tex)
                rbxtexNode = bpy.data.materials[f"R6 Pants_{rbx_object.name}"].node_tree.nodes['Image Texture.001']
                rbxtexNode2 = bpy.data.materials[f"R6 Torso_{rbx_object.name}"].node_tree.nodes['Image Texture.002']

                rbxtexNode.image = rbx_image 
                rbxtexNode2.image = rbx_image 
                
                                       

        return {'FINISHED'} 
    

    ### Get Item info ###
    async def get_acc_info(self, id):                                
        url = f"https://economy.roblox.com/v2/assets/{id}/details"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            name = data['Name']
            type = data['AssetTypeId']
            creator = data['Creator']['Name']
            netw_error = None
        else:
            name = None
            creator = None
            type = None
            netw_error = f"{data.status_code}: Error getting Accessory Info"
        return name, type, creator, netw_error 
    
    ### Get Item Thumbnail ###
    async def get_acc_thumb(self, id, type):
        rbx_size = '250x250'
        rbx_format = 'Png'
        rbx_isCircular = 'false'
        url = f"https://thumbnails.roblox.com/v1/assets?assetIds={id}&returnPolicy=PlaceHolder&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}"     
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
            try:
                img_url = data["data"][0]["imageUrl"]
            except:
                netw_error = f"{data.status_code}: Error, Invalid {type}"
                img_url = None
            else:
                netw_error = None
        else:
            img_url = None
            netw_error = f"{data.status_code}: Error getting {type} IMG URL"
        return img_url, netw_error      
    
    ### Get items Data by URL ###
    async def get_url_data(self, img_url): 
        data = requests.get(img_url)
        if data.status_code == 200:
            image_data = data.content
            netw_error = None
        else:
            netw_error = f"{data.status_code}: Error getting IMG Data"
        return image_data, netw_error
 
    ### Get items Data by ID ###
    async def get_id_data(self, id, type):
        url = f"https://assetdelivery.roblox.com/v1/asset?id={id}" 
        data = requests.get(url)
        if data.status_code == 200:
            data = data.content
            netw_error = None
        else:
            netw_error = f"{data.status_code}: Error getting {type} Data"
        return data, netw_error       