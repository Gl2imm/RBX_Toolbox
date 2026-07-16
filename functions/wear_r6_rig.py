import bpy
import os
import asyncio
import requests

from .. import glob_vars



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
            forb_chars = dict((ord(char), None) for char in '/*?:"<>|')
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

            ### Get authorized session (Roblox OAuth) ###
            if rbx_shirt_netw_error == None:
                auth_headers, rbx_shirt_netw_error = self.get_auth_headers(context)

            ### Get shirt Info ###
            if rbx_shirt_netw_error == None:
                rbx_shirt_name, rbx_shirt_type, rbx_shirt_creator, rbx_shirt_netw_error = asyncio.run(self.get_acc_info(rbx_shirt))

            ### Get shirt asset ID (parse classic Shirt for its ShirtTemplate texture) ###
            if rbx_shirt_netw_error == None:
                shirt_asset, rbx_shirt_netw_error = self.get_auth_asset_data(rbx_shirt, auth_headers)
            if rbx_shirt_netw_error == None:
                rbx_shirt, rbx_shirt_netw_error = self.get_classic_texture_id(shirt_asset, rbx_cloth) #Actual item ID

            ### Get shirt Data ###
            if rbx_shirt_netw_error == None:
                shirt_data, rbx_shirt_netw_error = self.get_auth_asset_data(rbx_shirt, auth_headers)
            
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

            ### Get authorized session (Roblox OAuth) ###
            if rbx_pants_netw_error == None:
                auth_headers, rbx_pants_netw_error = self.get_auth_headers(context)

            ### Get pants Info ###
            if rbx_pants_netw_error == None:
                rbx_pants_name, rbx_pants_type, rbx_pants_creator, rbx_pants_netw_error = asyncio.run(self.get_acc_info(rbx_pants))

            ### Get pants asset ID (parse classic Pants for its PantsTemplate texture) ###
            if rbx_pants_netw_error == None:
                pants_asset, rbx_pants_netw_error = self.get_auth_asset_data(rbx_pants, auth_headers)
            if rbx_pants_netw_error == None:
                rbx_pants, rbx_pants_netw_error = self.get_classic_texture_id(pants_asset, rbx_cloth) #Actual item ID

            ### Get pants Data ###
            if rbx_pants_netw_error == None:
                pants_data, rbx_pants_netw_error = self.get_auth_asset_data(rbx_pants, auth_headers)
            
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
 
    ### Build authorized request headers (Roblox OAuth Bearer token) ###
    def get_auth_headers(self, context):
        """Refreshes the Roblox OAuth token and returns ({"Authorization": ...}, error).
        Returns (None, error) when the user is not logged in or the refresh fails."""
        from ..func_import_v2 import func_rbx_other
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        try:
            access_token = loop.run_until_complete(func_rbx_other.renew_token(context))
        except Exception:
            return None, "Roblox login required. Please log in above."
        return {"Authorization": f"Bearer {access_token}"}, None

    ### Get item Data by ID via the authorized Cloud asset-delivery API ###
    def get_auth_asset_data(self, id, headers):
        """Downloads asset bytes using the authenticated session. Returns (data, error)."""
        from ..func_import_v2 import func_rbx_cloud_api
        return func_rbx_cloud_api.get_asset_data(id, headers)

    ### Resolve the texture asset ID from a classic Shirt/Pants asset ###
    def get_classic_texture_id(self, asset_bytes, type):
        """Parses a classic Shirt/Pants asset (XML or binary rbxm) and returns
        (texture_id, error). Never raises - returns a friendly error on bad data."""
        from ..func_import_v2 import func_rbx_other
        from ..func_import_v2.readers import rbxm_reader

        tex_id = None
        error = None
        if not asset_bytes:
            return None, f"Error: Empty {type} data"

        class_name = "Shirt" if type == "shirt" else "Pants"
        prop_name = "ShirtTemplate" if type == "shirt" else "PantsTemplate"

        tmp_dir = os.path.join(glob_vars.addon_path, 'Imported_Clothes', 'tmp')
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        tmp_file = os.path.join(tmp_dir, f"classic_{type}.rbxm")
        try:
            with open(tmp_file, "wb") as f:
                f.write(asset_bytes)
            model = rbxm_reader.parse(tmp_file)
            node = model.FindFirstChildOfClass(class_name)
            if node is None:
                matches = model.FindAll(class_name)
                node = matches[0] if matches else None
            if node is None:
                error = f"Error: Not a classic {type}"
            else:
                template_raw = node.get(prop_name)
                template_id_val = func_rbx_other.resolve_content_uri(template_raw)
                if template_id_val:
                    tex_id = func_rbx_other.strip_rbxassetid(template_id_val)
                else:
                    error = f"Error: No texture found in {type}"
        except Exception:
            error = f"Error reading {type} data"
        return tex_id, error