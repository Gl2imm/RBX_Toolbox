import bpy
from bpy_extras.object_utils import AddObjectHelper
import sys
import os
import asyncio
import requests
import json
import mathutils
import importlib
from RBX_Toolbox import glob_vars
from glob_vars import addon_path


#394650 - bundle with dynamic head (User)
#192 - korblox bundle, head is accessory (Roblox)
#306 - pirate bundle, no head (Roblox)


# Get the folder where this script (__file__) lives and add subfolders so PythonNET can find dependencies
net_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rbxm_net_lib")
robloxfile_dll_name = "RobloxFileFormat.dll"
robloxfile_dll = os.path.join(net_lib_dir, robloxfile_dll_name)
# code here runs only in editor
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from rbx_import_bundle_char import *


### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


def is_dotnet_installed() -> bool:
	"""Check if 4.7.1 .NET Framework version is installed."""
	version = "4.7.1"
	try:
		# Registry path for .NET Framework
		key_path = r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full"
		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
			release, _ = winreg.QueryValueEx(key, "Release")
			
			# Map release key numbers to versions
			version_map = {
				461808: "4.7.1",
				528040: "4.8"
			}
			
			for rel, ver in version_map.items():
				if release >= rel:
					return True
	except FileNotFoundError:
		return False


## Remove restricted characters from string ##
def replace_restricted_char(str: str = None):
	'''Replace restricted characters in string with underscores'''
	if str is None:
		return
	restricted_chars = '\/*?:"<>|.,'
	replace_map = dict((ord(char), '_') for char in restricted_chars)
	new_str = str.translate(replace_map)
	return new_str


## Remove rbxassetid:// part
def strip_rbxassetid(asset_str):
	""" Removes the 'rbxassetid://' prefix if present """
	asset_str = str(asset_str)
	prefix = "rbxassetid://"
	if asset_str.startswith(prefix):
		return asset_str[len(prefix):]
	else:
		asset_str = asset_str.split("=")[-1]
	return asset_str


# This asynchronous method is invoked as a separate coroutine from the main thread
async def renew_token(context):
	"""Refreshes Auth Token"""
	from oauth.lib.oauth2_client import RbxOAuth2Client
	window_manager = context.window_manager
	rbx = window_manager.rbx
	oauth2_client = RbxOAuth2Client(rbx)
	await oauth2_client.refresh_login_if_needed()
	access_token = oauth2_client.token_data["access_token"]
	dprint("Auth Token refresh after: " , oauth2_client.token_data["refresh_after"])
	return access_token



##### Create Folders #####
def create_and_open_folders(folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
	os.startfile(folder)
	return


def cleanup_tmp_files(filenames:list, extension:str):
	"""
	Deletes files from folder_path whose names match the list, with the given extension.
	"""
	rbx_tmp_rbxm_filepath = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp_rbxm')
	# make sure extension starts with "."
	if not extension.startswith("."):
		extension = "." + extension

	missing = []
	for name in filenames:
		file_path = os.path.join(rbx_tmp_rbxm_filepath, str(name) + extension)

		if os.path.exists(file_path):
			try:
				os.remove(file_path)
			except Exception as e:
				pass
				#dprint(f"❌ Could not delete {file_path}: {e}")
		else:
			missing.append(file_path)

	return



### Save Downloaded files
def save_to_file(file, data):
	"""Saving files."""
	rbx_imp_error = None
	try:
		with open(file, "wb") as f:
			f.write(data) 
	except Exception as e:
		rbx_imp_error = f"Error saving file. {e}"
		glob_vars.rbx_imp_error = rbx_imp_error
	return rbx_imp_error




##### Extract ID #####
def item_field_extract_id(rbx_item_field_entry):
	dprint("rbx_item_field_entry: ", rbx_item_field_entry)
	rbx_asset_id = None
	rbx_imp_error = None

	if ("https://www.roblox.com/bundles/" in rbx_item_field_entry
	or "https://roblox.com/bundles/" in rbx_item_field_entry):
	
		# Extract the ID correctly
		# Remove any known prefix
		full_url = rbx_item_field_entry
		for prefix in [f"https://www.roblox.com/bundles/",
					f"https://roblox.com/bundles/"]:
			if full_url.startswith(prefix):
				right_part_url = full_url[len(prefix):]
				break
		rbx_asset_id = right_part_url.split("/")[0]
		if not rbx_asset_id.isdigit():
			rbx_imp_error = "Error: Invalid item URL"  
			glob_vars.rbx_imp_error = rbx_imp_error          

	elif rbx_item_field_entry.isdigit():
		rbx_asset_id = rbx_item_field_entry

	return rbx_asset_id, rbx_imp_error




### Get User ID from Username
def get_user_id(rbx_user_name, headers):
	rbx_user_id = None
	rbx_imp_error = None
	glob_vars.rbx_imp_error = None
	payload = {
				"usernames": [rbx_user_name],
				"excludeBannedUsers" : 'true'
				}
	try:
		data = requests.post("https://users.roblox.com/v1/usernames/users", json=payload, headers=headers)
	except:
		rbx_imp_error = "Get User ID Error, no respose"
		glob_vars.rbx_imp_error = rbx_imp_error
	else:
		if data.status_code == 200:
			data = data.json()
			try:
				rbx_user_id = data.get('data')[0]['id']
			except:
				rbx_imp_error = "Error: Unable to find this user" 
				glob_vars.rbx_imp_error = rbx_imp_error       
		else:
			rbx_imp_error = f"{data.status_code}: Error getting User ID"
			glob_vars.rbx_imp_error = rbx_imp_error   
	return rbx_user_id, rbx_imp_error



### Get Data from Assetdelivery API
def get_asset_data(rbx_asset_id, headers, RobloxAssetFormat:str = None):
	asset_data = None
	rbx_imp_error = None
	glob_vars.rbx_imp_error = None
	if RobloxAssetFormat:
		local_headers = headers.copy() 
		local_headers["Roblox-AssetFormat"] = RobloxAssetFormat
	url = f"https://apis.roblox.com/asset-delivery-api/v1/assetId/{rbx_asset_id}"
	dprint("Downloading Asset:")
	dprint("url: ", url)
	try:
		response = requests.get(url, headers=local_headers if RobloxAssetFormat else headers)
	except:     
		rbx_imp_error = "Error Connecting to Assetdelivery API"
		glob_vars.rbx_imp_error = rbx_imp_error
	else:
		if response.status_code == 200:
			json_data = json.loads(response.content)
			dprint("Asset json_data: " , json_data)
			asset_url = json_data.get("location")
			if asset_url:
				try:
					asset_response = requests.get(asset_url)
				except:     
					rbx_imp_error = "Error Connecting to Auth Asset Data URL"
					glob_vars.rbx_imp_error = rbx_imp_error
				else:
					if asset_response.status_code == 200:
						asset_data = asset_response.content
					else:
						rbx_imp_error = f"{response.status_code}: Error getting Asset Data"
						glob_vars.rbx_imp_error = rbx_imp_error
		elif response.status_code == 401:
			rbx_imp_error = f"{response.status_code}: Access Denied"
			glob_vars.rbx_imp_error = rbx_imp_error  
		else:
			rbx_imp_error = f"{response.status_code}: Error getting Asset Data URL"
			glob_vars.rbx_imp_error = rbx_imp_error  
	dprint("rbx_imp_error: ", rbx_imp_error)
	dprint("")   
	return asset_data, rbx_imp_error









######################################
##### Bundles Specific functions #####
######################################

### Get Catalog information for Bundles
def get_catalog_bundle_data(rbx_asset_id, headers):
	rbx_bundledItems = None
	rbx_asset_name = None
	rbx_asset_type_id = None
	rbx_asset_creator = None
	rbx_imp_error = None
	glob_vars.rbx_asset_error = None
	url = f"https://catalog.roblox.com/v1/catalog/items/{rbx_asset_id}/details?itemType=Bundle"
	try:
		data = requests.get(url, headers=headers)
	except:     
		rbx_imp_error = "Error Getting Catalog Bundle Data"
		glob_vars.rbx_imp_error = rbx_imp_error
	else:
		if data.status_code == 200:
			data = data.json()
			rbx_bundledItems = data["bundledItems"] # will get list of dictionaries with items
			rbx_asset_name = data["name"]
			rbx_asset_type_id = data["bundleType"] 
			rbx_asset_creator = data["creatorName"]
		else:
			if data.status_code == 404:
				rbx_imp_error = f"{data.status_code}: Invalid Bundle ID"
			else:
				rbx_imp_error = f"{data.status_code}: Error getting Catalog Bundle Data"
			glob_vars.rbx_imp_error = rbx_imp_error   
	return rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, rbx_bundledItems, rbx_imp_error




#################################
##### Blender API functions #####
#################################

def blender_api_import_obj(obj_filepath):
	if glob_vars.bldr_ver[0] < '4':
		bpy.ops.import_scene.obj(filepath=obj_filepath)
	else:
		bpy.ops.wm.obj_import(filepath=obj_filepath)
	return




def blender_api_add_meshes_as_obj(bundle_own_folder, mesh_part, mesh_data, cframe, cframe_pivot, rbx_choice_at_origin, mesh_reader, funct, mesh_name=None):
	if mesh_name:
		true_name = mesh_name
	else:
		true_name = mesh_part.Name

	obj_file_path = os.path.join(bundle_own_folder, true_name + ".obj")
	mesh_reader.write_obj_from_mesh_json(mesh_data, obj_file_path, lod_index=0, object_name=true_name)

	blender_api_import_obj(obj_file_path)
	rbx_obj = bpy.context.selected_objects[0]
	rbx_obj.name = true_name
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.view_layer.objects.active = None
	bpy.data.objects[rbx_obj.name].select_set(True)
	bpy.context.view_layer.objects.active = bpy.data.objects[rbx_obj.name]

	blender_matrix = funct.cframe_to_blender_matrix(cframe)
	oriented_blender_matrix = funct.blender_matrix_axis_conversion(blender_matrix)

	# Apply the matrix to object (world transform)
	rbx_obj.matrix_world = oriented_blender_matrix
	### Spawn at origin
	if rbx_choice_at_origin:
		blender_matrix = funct.cframe_to_blender_matrix(cframe_pivot)
		oriented_blender_vector = funct.blender_matrix_axis_conversion(blender_matrix,loc_vector_only=True)
		rbx_obj.matrix_world.translation = -oriented_blender_vector

	return rbx_obj



def blender_api_add_attachments(mesh_part_attachment, mesh_part_attachment_cframe, part_cframe, part_cframe_pivot, rbx_bndl_char_choice_at_origin, funct):
	bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.15, 0.15, 0.15))
	bpy.ops.object.shade_smooth()
	mesh_part_attachment_obj = bpy.context.selected_objects[0]
	mesh_part_attachment_obj.name = f"{str(mesh_part_attachment.Name)}"
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.view_layer.objects.active = None 
	bpy.data.objects[mesh_part_attachment_obj.name].select_set(True)
	bpy.context.view_layer.objects.active = bpy.data.objects[mesh_part_attachment_obj.name]

	# Get main mesh location
	blender_matrix_parent = funct.cframe_to_blender_matrix(part_cframe)
	oriented_blender_matrix_parent = funct.blender_matrix_axis_conversion(blender_matrix_parent)
	
	# Apply mesh matrix to attachment (world transform)
	mesh_part_attachment_obj.matrix_world = oriented_blender_matrix_parent

	# Apply mesh matrix to attachment if spawn at origin
	if rbx_bndl_char_choice_at_origin:
		blender_matrix_parent = funct.cframe_to_blender_matrix(part_cframe_pivot)
		oriented_blender_matrix_parent = funct.blender_matrix_axis_conversion(blender_matrix_parent,loc_vector_only=True)
		mesh_part_attachment_obj.matrix_world.translation = -oriented_blender_matrix_parent 

	# Add in attachment own offset
	blender_matrix_attachment = funct.cframe_to_blender_matrix(mesh_part_attachment_cframe)
	oriented_blender_matrix_attachment = funct.blender_matrix_axis_conversion(blender_matrix_attachment)

	# Apply the matrix to object (world transform)
	mesh_part_attachment_obj.matrix_world.translation = mesh_part_attachment_obj.matrix_world.translation + oriented_blender_matrix_attachment.translation
										



def blender_api_add_ver_col(rbx_obj, mesh_data):
	## Adding Vertex Colors
	obj_mesh = rbx_obj.data
	# Ensure a vertex color layer
	vcol_layer = obj_mesh.vertex_colors.get("Col")
	if not vcol_layer:
		vcol_layer = obj_mesh.vertex_colors.new(name="Col")
	# Access mesh polygons and loops
	colors_flat = mesh_data["vertexColors"]  # [255,255,255, ...]
	# Normalize colors to 0.0–1.0 and assign to each loop's vertex
	for loop in obj_mesh.loops:
		idx = loop.vertex_index * 4  # 4 numbers per vertex (RGBA)
		r = colors_flat[idx + 0] / 255.0
		g = colors_flat[idx + 1] / 255.0
		b = colors_flat[idx + 2] / 255.0
		a = colors_flat[idx + 3] / 255.0
		vcol_layer.data[loop.index].color = (r, g, b, a)




def blender_api_create_collection(name, parent_name=None):
	""" Create or get a collection by name."""
	# Get or create the collection
	if name in bpy.data.collections:
		coll = bpy.data.collections[name]
	else:
		coll = bpy.data.collections.new(name)
	
	# Find parent collection
	if parent_name is None:
		parent = bpy.context.scene.collection
	else:
		parent = bpy.data.collections.get(parent_name)
		if parent is None:
			# auto-create parent if it doesn't exist
			parent = bpy.data.collections.new(parent_name)
			bpy.context.scene.collection.children.link(parent)
	
	# Link collection to parent if not already linked
	if coll.name not in parent.children:
		parent.children.link(coll)

	# Set it as the active collection so new objects go inside
	def find_layer_collection(layer_collection, coll_name):
		"""Recursively find a LayerCollection by name."""
		if layer_collection.collection.name == coll_name:
			return layer_collection
		for child in layer_collection.children:
			found = find_layer_collection(child, coll_name)
			if found:
				return found
		return None

	layer_coll = find_layer_collection(bpy.context.view_layer.layer_collection, coll.name)
	if layer_coll:
		bpy.context.view_layer.active_layer_collection = layer_coll
	
	return coll



def blender_api_assets_new_material(rbx_obj, mesh_part, rbx_textures, rbx_asset_name_clean, rbx_SurfaceAppearance):
	### Creating new Material ###
	
	if rbx_obj.material_slots:
		bpy.ops.object.material_slot_remove()
	mat = bpy.data.materials.new(name=f"{rbx_asset_name_clean}_{mesh_part.Name}_mat")
	rbx_obj.data.materials.append(mat) 
	mat = rbx_obj.material_slots[0].material 
	mat.use_nodes = True
	mat.use_backface_culling = True
	nodes = mat.node_tree.nodes
	bsdf = nodes.get("Principled BSDF")
	# Set Roughness
	if float(glob_vars.bldr_fdr) < 4.0:
		bsdf.inputs[9].default_value = 1
	else:
		bsdf.inputs[2].default_value = 1
	
	node_y_index = 0
	for tex_name, tex_path in rbx_textures.items():
		rbx_image = bpy.data.images.load(tex_path)
		rbxtexNode = nodes.new('ShaderNodeTexImage')
		rbxtexNode.image = rbx_image
		rbxtexNode.name = tex_name
		rbxtexNode.location = (-700,300-300 * node_y_index)
		if tex_name == "Color":
			mat.node_tree.links.new(rbxtexNode.outputs[0], bsdf.inputs["Base Color"])	
			if not rbx_SurfaceAppearance:
				blender_api_transparent_textures()
				return
	
		elif tex_name == "Normal":
			norm_node = nodes.new(type="ShaderNodeNormalMap")
			norm_node.location = (-400,300-300 * node_y_index)        
			mat.node_tree.links.new(rbxtexNode.outputs[0], norm_node.inputs[1])
			mat.node_tree.links.new(norm_node.outputs[0], bsdf.inputs[tex_name])
			norm_node.space = 'TANGENT'
			rbx_image.colorspace_settings.name = 'Non-Color'
		else:
			mat.node_tree.links.new(rbxtexNode.outputs[0], bsdf.inputs[tex_name])
			rbx_image.colorspace_settings.name = 'Non-Color'
		blender_api_transparent_textures()
		node_y_index += 1



### remove alpha textures and add a mix node to properly display transparency
def blender_api_transparent_textures():
	if float(glob_vars.bldr_fdr) < 3.4:
		obj = bpy.context.selected_objects[0]
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.view_layer.objects.active = None
		bpy.data.objects[obj.name].select_set(True)
		bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]
	else:
		obj = bpy.context.active_object

	if obj is None or obj.type != 'MESH':
		print("Please select a mesh object.")
	else:
		for slot in obj.material_slots:
			mat = slot.material
			if mat is None or not mat.use_nodes:
				print(f"Skipping empty or non-node material in slot: {slot.name}")
				continue
			
			# Setup backface culling
			mat.show_transparent_back = False
			mat.use_backface_culling = True 

			nodes = mat.node_tree.nodes
			links = mat.node_tree.links

			# Find the Principled BSDF node
			bsdf_node = None
			for node in nodes:
				if node.type == 'BSDF_PRINCIPLED':
					bsdf_node = node
					break

			if bsdf_node is None:
				print(f"No Principled BSDF found in material: {mat.name}")
				continue

			base_color_input = bsdf_node.inputs[0]
			alpha_input = bsdf_node.inputs[4]

			# Get base color image texture
			base_color_link = base_color_input.links[0] if base_color_input.is_linked else None
			base_color_tex = base_color_link.from_node if base_color_link else None

			# Remove transparency node connected to alpha input (if exists)
			if alpha_input.is_linked:
				alpha_link = alpha_input.links[0]
				alpha_node = alpha_link.from_node
				links.remove(alpha_link)
				nodes.remove(alpha_node)
				#print(f"Removed transparency texture node in material: {mat.name}")
			else:
				print(f"No alpha texture to remove in material: {mat.name}")

			if not base_color_tex or base_color_tex.type != 'TEX_IMAGE':
				#print(f"Material {mat.name}: Base color is not connected to an image texture.")
				continue

			# Remove link from base color texture to BSDF base color
			links.remove(base_color_link)

			# Create MixRGB node
			mix_node = nodes.new(type='ShaderNodeMixRGB')
			mix_node.blend_type = 'MIX'
			mix_node.label = 'Alpha Mix'
			rbx_shade_r = 0.361304
			rbx_shade_g = 0.3564
			rbx_shade_b = 0.371238
			mix_node.inputs[1].default_value = (rbx_shade_r, rbx_shade_g, rbx_shade_b, 1)  # fallback color
			#mix_node.location = ((base_color_tex.location.x + bsdf_node.location.x) / 8 * 5, base_color_tex.location.y - 0)
			mix_node.location = (bsdf_node.location.x - 200, base_color_tex.location.y - 0)

			# Connect image color → Mix input 2
			links.new(base_color_tex.outputs['Color'], mix_node.inputs[2])

			# Connect image alpha → Mix Fac
			if 'Alpha' in base_color_tex.outputs:
				links.new(base_color_tex.outputs['Alpha'], mix_node.inputs[0])
			else:
				print(f"Material {mat.name}: Texture has no Alpha output.")

			# Connect Mix → BSDF base color
			links.new(mix_node.outputs['Color'], bsdf_node.inputs[0])


















class RBX_IMPORT_V2(bpy.types.Operator,AddObjectHelper): # type: ignore
	"""Import Mesh from Roblox"""
	bl_idname = "object.add_character_v2"
	bl_label = "Add Roblox Character (v2)"
	bl_options = {'REGISTER', 'UNDO'}
	rbx_imp : bpy.props.StringProperty(name= "Added") # type: ignore


	def execute(self, context): 
		from pythonnet import load
		load('coreclr')
		import clr
		from System.Reflection import Assembly # type: ignore
		clr.AddReference(robloxfile_dll) # type: ignore
		# this is import from dll in runtime
		if not TYPE_CHECKING:
			from RobloxFiles import RobloxFile, Folder, MeshPart, Part, WrapTarget, Attachment, SpecialMesh, SurfaceAppearance, Shirt, Pants, Accessory   # type: ignore
			from RobloxFiles.DataTypes import Vector3, CFrame
		from . import mesh_reader
		importlib.reload(mesh_reader)
		from . import conversion_funct as funct
		importlib.reload(funct)

		
		# Run async function from sync context and refresh Auth Token if need
		try:
			loop = asyncio.get_event_loop()
		except RuntimeError:
			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)

		access_token = loop.run_until_complete(renew_token(context))
		headers = {
			"Authorization": f"Bearer {access_token}"
		}


		scene = context.scene
		rbx_imp = self.rbx_imp
		rbx_prefs = scene.rbx_prefs
		rbx_item_field_entry = rbx_prefs.rbx_item_field_entry
		rbx_bndl_char_choice_at_origin = rbx_prefs.rbx_bndl_char_choice_at_origin
		rbx_bndl_char_choice_add_meshes = rbx_prefs.rbx_bndl_char_choice_add_meshes
		rbx_bndl_char_choice_add_textures = rbx_prefs.rbx_bndl_char_choice_add_textures
		rbx_bndl_char_choice_add_cages = rbx_prefs.rbx_bndl_char_choice_add_cages
		rbx_bndl_char_choice_add_attachment = rbx_prefs.rbx_bndl_char_choice_add_attachment
		rbx_bndl_char_choice_add_motor6d_attachment = rbx_prefs.rbx_bndl_char_choice_add_motor6d_attachment
		rbx_bndl_char_choice_add_bones = rbx_prefs.rbx_bndl_char_choice_add_bones
		rbx_bndl_char_choice_add_ver_col = rbx_prefs.rbx_bndl_char_choice_add_ver_col
		rbx_bndl_char_choice_clean_tmp_meshes = rbx_prefs.rbx_bndl_char_choice_clean_tmp_meshes

		bundles_folder = os.path.join(addon_path, glob_vars.rbx_import_main_folder, glob_vars.rbx_import_v2_bundles)
		rbx_meshes_to_clean_up_lst = []

		if rbx_imp == "open_imp_folder":
			create_and_open_folders(bundles_folder)
			return {'FINISHED'}
		
		rbx_tmp_rbxm_filepath = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp_rbxm')
		if not os.path.exists(rbx_tmp_rbxm_filepath):
			os.makedirs(rbx_tmp_rbxm_filepath)

		################
		################

		
		rbx_asset_id, rbx_imp_error = item_field_extract_id(rbx_item_field_entry)
		dprint("rbx_asset_id: ", rbx_asset_id)
		dprint("rbx_imp_error: ", rbx_imp_error)
		
		if not rbx_imp_error:
			rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, rbx_bundledItems, rbx_imp_error = get_catalog_bundle_data(rbx_asset_id, headers)
			rbx_asset_name_clean = replace_restricted_char(rbx_asset_name)
			dprint("rbx_bundledItems: ", rbx_bundledItems)



			if not rbx_imp_error:     
				rbx_filtered_assets_id_only = []

				### Filter out bundled items to assets only
				for asset in rbx_bundledItems:
					asset_id = asset.get("id")
					asset_type = asset.get("type")
					asset_name = asset.get("name")
					if asset_type != "Asset":
						continue
					if asset_name == "Default Mood":    #skip animation
						continue
					rbx_tmp_rbxm_file = os.path.join(rbx_tmp_rbxm_filepath, str(asset_id) + ".rbxm")
					rbx_filtered_assets_id_only.append(asset_id)
					
					### Get rbxm files and save them
					if not rbx_imp_error:
						asset_data, rbx_imp_error = get_asset_data(asset_id, headers)
						try:
							with open(f"{rbx_tmp_rbxm_file}", "wb") as f:
								f.write(asset_data) 
						except:
							rbx_imp_error = "Error saving temp RBXM file"
							glob_vars.rbx_imp_error = rbx_imp_error
							return


				### iterate all rbxm files and get all data from them
				all_bones_data = {}
				all_mesh_skin_data = []  # list of dicts per mesh

				if not rbx_imp_error:
					for rbxm_id in rbx_filtered_assets_id_only:
						mesh_parts_to_process = []	#should resets every rbxm file loop
						is_body_part = False
						is_dynamic_head = False
						is_accessory = False
						is_classic_pants = False
						is_classic_shirt = False
						mesh_name = ""
						class_accessory = None
						special_mesh = None

						rbxm_file_path = os.path.join(rbx_tmp_rbxm_filepath, str(rbxm_id) + ".rbxm")
						rbxm_file = RobloxFile.Open(rbxm_file_path)

						R15Fixed = rbxm_file.FindFirstChild[Folder]("R15Fixed")
						special_mesh_part = rbxm_file.FindFirstChild[SpecialMesh]("Mesh")
						class_shirt = rbxm_file.FindFirstChildOfClass[Shirt]()
						class_pants = rbxm_file.FindFirstChildOfClass[Pants]()
						class_accessory = rbxm_file.FindFirstChildOfClass[Accessory]()

						### Body parts
						if R15Fixed:
							is_body_part = True
							rbx_avatar_bundle_parts = [
									"LeftUpperArm", "LeftLowerArm", "LeftHand",
									"RightUpperArm", "RightLowerArm", "RightHand",
									"LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
									"RightUpperLeg", "RightLowerLeg", "RightFoot",
									"UpperTorso", "LowerTorso"
								]
							
							### iterate all mesh parts found in rbxm
							for mesh_name in rbx_avatar_bundle_parts:
								dprint(f"Checking mesh_name: {mesh_name} in RBXM ID: {rbxm_id}")
								mesh_part = R15Fixed.FindFirstChild[MeshPart](mesh_name)
								dprint("mesh_part: ", mesh_part)
								if mesh_part:
									mesh_parts_to_process.append((mesh_part, mesh_name, False, None))
							
								if mesh_part:
									mesh_parts_to_process.append((mesh_part, mesh_name, False, None))
							
								if mesh_part:
									mesh_parts_to_process.append((mesh_part, mesh_name, False, None))
							
							# Also check for Head in R15Fixed
							mesh_name = "Head"
							mesh_part = R15Fixed.FindFirstChild[MeshPart](mesh_name)
							if mesh_part:
								dprint(f"Found Standard Head in R15Fixed")
								mesh_parts_to_process.append((mesh_part, mesh_name, False, None))
							
							dprint("mesh_parts_to_process: ", mesh_parts_to_process)


						### Dynamic Head
						if special_mesh_part:
							is_dynamic_head = True
							dprint("Special Mesh exist, mesh is a dynamic head")
							dprint("")
							mesh_name = "Head"
							### need to download separate head rbxm, its not in the bundle
							asset_data, rbx_imp_error = get_asset_data(rbxm_id, headers, RobloxAssetFormat="avatar_meshpart_head")
							if not rbx_imp_error:
								with open(f"{rbxm_file_path}", "wb") as f:
									f.write(asset_data)
								rbxm_file = RobloxFile.Open(rbxm_file_path) 
								mesh_part = rbxm_file.FindFirstChild[MeshPart](mesh_name)
								if mesh_part:
									mesh_parts_to_process.append((mesh_part, mesh_name, False, None))
							else:
								dprint("Failed to download avatar_meshpart_head, returning...")
								return {'FINISHED'}
							
						
						### Classic Shirt
						elif class_shirt:
							is_classic_shirt = True
							dprint("CLASSIC SHIRT FOUND")

						
						### Classic pants
						elif class_pants:
							is_classic_pants = True
							dprint("CLASSIC PANTS FOUND")


						### Accessory
						elif class_accessory:
							is_accessory = True
							dprint("Accessory FOUND")
							
							# Check for initial MeshPart Handle
							mesh_part = class_accessory.FindFirstChild[MeshPart]("Handle")

							# If MeshPart Handle is missing, try to fetch the optimized usage "avatar_meshpart_accessory"
							if not mesh_part:
								dprint(f"MeshPart Handle not found for Accessory. Attempting to fetch avatar_meshpart_accessory version...")
								# Attempt to download with special header
								# We use a temporary error var to avoid clobbering the main one if this optional step fails
								asset_data_acc, rbx_acc_error = get_asset_data(rbxm_id, headers, RobloxAssetFormat="avatar_meshpart_accessory")
								
								if not rbx_acc_error and asset_data_acc:
									try:
										with open(f"{rbxm_file_path}", "wb") as f:
											f.write(asset_data_acc)
										# Reload the file and re-find the accessory
										rbxm_file = RobloxFile.Open(rbxm_file_path)
										class_accessory = rbxm_file.FindFirstChildOfClass[Accessory]()
										if class_accessory:
											mesh_part = class_accessory.FindFirstChild[MeshPart]("Handle")
											if mesh_part:
												dprint("Successfully upgraded Accessory to MeshPart!")
									except Exception as e:
										dprint(f"Error processing upgraded accessory file: {e}")
										# If reloading fails, we might be in trouble since we overwrote the file. 
										# But this is a risk we optimize for.
										pass
								else:
									dprint("Failed to fetch avatar_meshpart_accessory version or no data returned. Falling back.")

							if not class_accessory:
								dprint("Error: Accessory missing after attempt to upgrade/reload! Skipping.")
								continue

							mesh_name = str(class_accessory.Name) # Use Accessory Name
							# DEBUG: Trace mesh_name origin
							dprint(f"DEBUG: Processing Accessory {class_accessory.Name}")
							dprint(f"DEBUG: Current mesh_name variable: {mesh_name}")
							dprint("MESH NAME: ", mesh_name)
							dprint(f"Accessory Children: {[c.Name + ' (' + str(c.ClassName) + ')' for c in class_accessory.GetChildren()]}")
							if mesh_part:
								mesh_parts_to_process.append((mesh_part, mesh_name, True, class_accessory))
								dprint(f"Added {mesh_name} to processing list.")
							else:
								dprint(f"WARNING: Handle (MeshPart) not found in {mesh_name}!")
								part_handle = class_accessory.FindFirstChild("Handle", False)
								if part_handle and part_handle.ClassName == "Part":
									dprint(f"Fnoud Handle with ClassName: {part_handle.ClassName}")
									mesh_parts_to_process.append((part_handle, mesh_name, True, class_accessory))
								else:
									dprint("Handle completely missing!")




						for mesh_part, mesh_name, is_acc, acc_obj in mesh_parts_to_process:
							dprint(f"Processing mesh: {mesh_name}")
							rbx_textures = {}
							part_TextureID = ""
							
							rbx_SurfaceAppearance = mesh_part.FindFirstChild[SurfaceAppearance]("SurfaceAppearance")
							dprint(f"Checked SurfaceAppearance for {mesh_name}")
							try:
								special_mesh = None
								if mesh_part.ClassName == "Part":
									special_mesh = mesh_part.FindFirstChildOfClass[SpecialMesh]()
									if not special_mesh:
										dprint(f"Skip: Part {mesh_name} has no SpecialMesh")
										continue
									part_MeshId = strip_rbxassetid(special_mesh.Properties["MeshId"].Value)
								else:
									part_MeshId = strip_rbxassetid(mesh_part.Properties["MeshId"].Value)
								
								dprint(f"Got MeshId for {mesh_name}: {part_MeshId}")
							except Exception as e:
								dprint(f"Error getting MeshId for {mesh_name}: {e}")
								continue
							if rbx_SurfaceAppearance:
								for tex_name in glob_vars.rbx_pbr_materials:
									part_TextureID = strip_rbxassetid(rbx_SurfaceAppearance.Properties[tex_name].Value)
									if part_TextureID == "":
										continue
									if tex_name == "MetalnessMap":
										tex_name = "MetallicMap"
									rbx_textures[tex_name.removesuffix("Map")] = part_TextureID
							else:
								if special_mesh:
									rbx_tex_id_value = special_mesh.Properties["TextureId"].Value
								else:
									rbx_tex_id_value = mesh_part.Properties["TextureID"].Value
								if not rbx_tex_id_value or str(rbx_tex_id_value) == "":
									rbx_textures = None
								else:
									part_TextureID = strip_rbxassetid(rbx_tex_id_value)
									rbx_textures["Color"] = part_TextureID
							part_cframe = mesh_part.Properties["CFrame"].Value
							# Apply Accessory Grip (AttachmentPoint) inverse if available and this is an accessory handle
							if is_acc and acc_obj and "AttachmentPoint" in acc_obj.Properties:
								grip = acc_obj.Properties["AttachmentPoint"]
								if grip.Value != CFrame():
									part_cframe = part_cframe * grip.Value.Inverse()
									dprint(f"DEBUG: Applied Grip Inverse. New CFrame: {part_cframe}")
								else:
									dprint("DEBUG: Grip is Identity or None")
							
							# Apply SpecialMesh Offset if available
							if special_mesh and "Offset" in special_mesh.Properties:
								offset = special_mesh.Properties["Offset"]
								if offset.Value != Vector3(0,0,0):
									dprint(f"DEBUG: Found SpecialMesh Offset: {offset.Value}")
									part_cframe = part_cframe + offset.Value
									dprint(f"DEBUG: Applied Offset. New CFrame: {part_cframe}")
									
							part_cframe_pivot = mesh_part.Properties["PivotOffset"].Value
							dprint("part_MeshId: ", part_MeshId)
							dprint("part_TextureID: ", part_TextureID)
							dprint("")

							bundle_own_folder = os.path.join(bundles_folder, rbx_asset_name_clean)
							if not os.path.exists(bundle_own_folder):
								os.makedirs(bundle_own_folder)

								
							### download mesh file
							if not rbx_imp_error:
								dprint("Downloading mesh")
								dprint("part_MeshId: ", part_MeshId)
								dprint("rbx_imp_error: ", rbx_imp_error)
								mesh_file_path = os.path.join(rbx_tmp_rbxm_filepath, mesh_part.Name + ".mesh")
								asset_data, rbx_imp_error = get_asset_data(part_MeshId, headers)
								dprint("")
							if not rbx_imp_error:
								rbx_imp_error = save_to_file(mesh_file_path, asset_data)
								### add to list meshes to clean up
								rbx_meshes_to_clean_up_lst.append(mesh_part.Name)




						
							if not rbx_imp_error:
								with open(mesh_file_path, "rb") as f:
									data = f.read()
								mesh_data = mesh_reader.RBXMeshParser.parse(data)
								

								blender_api_create_collection(rbx_asset_name_clean)

								### In case textures selected but meshes are not
								if rbx_bndl_char_choice_add_textures and not rbx_bndl_char_choice_add_meshes:
									rbx_bndl_char_choice_add_meshes = True

								if rbx_bndl_char_choice_add_meshes:
									rbx_obj = blender_api_add_meshes_as_obj(bundle_own_folder, mesh_part, mesh_data, part_cframe, part_cframe_pivot, rbx_bndl_char_choice_at_origin, mesh_reader, funct, mesh_name=mesh_name)



									### Add vertex colors
									if rbx_bndl_char_choice_add_ver_col:
										dprint("Adding Vertex Color for Meshes, OBJ: ", rbx_obj)
										dprint("")
										blender_api_add_ver_col(rbx_obj, mesh_data)



									### Download textures and set material
									if rbx_bndl_char_choice_add_textures:
										dprint("Downloading Textures")
										if not rbx_textures:
											dprint("rbx_textures is empty, skipping")
											dprint("")
											pass
										else:
											### download tex file
											if not rbx_imp_error:
												dprint("rbx_textures: ", rbx_textures)
												dprint("")
												new_rbx_textures = rbx_textures.copy()
												for tex_name, tex_id in rbx_textures.items():
													tex_file_path = os.path.join(bundle_own_folder, mesh_part.Name + "_" + tex_name + ".png")
													asset_data, rbx_imp_error = get_asset_data(tex_id, headers)
													if not rbx_imp_error:
														rbx_imp_error = save_to_file(tex_file_path, asset_data)
														if not rbx_imp_error:
															new_rbx_textures[tex_name] = tex_file_path
												rbx_textures = new_rbx_textures

											if not rbx_imp_error:
												blender_api_assets_new_material(rbx_obj, mesh_part, rbx_textures, rbx_asset_name_clean, rbx_SurfaceAppearance)


								
								if rbx_bndl_char_choice_add_cages:
									cage_part = mesh_part.FindFirstChild[WrapTarget](mesh_name + "WrapTarget")
									### Accessories dont have cages, so skip
									if cage_part:
										blender_api_create_collection("Cages", rbx_asset_name_clean)
										if cage_part:
											dprint("cage_part: ", cage_part)
											cage_inner_MeshId = strip_rbxassetid(cage_part.Properties["CageMeshId"].Value)
											cage_cframe = cage_part.Properties["CageOrigin"].Value
											cage_cframe_pivot = cage_part.Properties["ImportOrigin"].Value
											dprint("cage_inner_MeshId: ", cage_inner_MeshId)

											bundle_own_folder = os.path.join(bundles_folder, rbx_asset_name_clean)
											if not os.path.exists(bundle_own_folder):
												os.makedirs(bundle_own_folder)
												
											### download mesh file
											if not rbx_imp_error:
												cage_mesh_file_path = os.path.join(rbx_tmp_rbxm_filepath, cage_part.Name + ".mesh")
												asset_data, rbx_imp_error = get_asset_data(cage_inner_MeshId, headers)
											if not rbx_imp_error:
												rbx_imp_error = save_to_file(cage_mesh_file_path, asset_data)
												### add to list meshes to clean up
												rbx_meshes_to_clean_up_lst.append(cage_part.Name)


										### read meshes
										with open(cage_mesh_file_path, "rb") as f:
											data = f.read()
										cage_data = mesh_reader.RBXMeshParser.parse(data)

										### add obj to blender
										rbx_obj = blender_api_add_meshes_as_obj(bundle_own_folder, cage_part, cage_data, cage_cframe, cage_cframe_pivot, rbx_bndl_char_choice_at_origin, mesh_reader, funct)

										### Add vertex colors
										if rbx_bndl_char_choice_add_ver_col:
											dprint("Adding Vertex Color for Cages, OBJ: ", rbx_obj)
											dprint("")
											blender_api_add_ver_col(rbx_obj, cage_data)


								if rbx_bndl_char_choice_add_attachment:
									blender_api_create_collection("Accessory Attachments", rbx_asset_name_clean)
									mesh_part_children = mesh_part.GetChildren()
									for child in mesh_part_children:
										if str(child.ClassName) == "Attachment":
											if not "RigAttachment" in str(child.Name):
												mesh_part_attachment = child
												dprint("mesh_part_attachment: ", mesh_part_attachment)
												mesh_part_attachment_cframe = mesh_part_attachment.Properties["CFrame"].Value

												blender_api_add_attachments(mesh_part_attachment, mesh_part_attachment_cframe, part_cframe, part_cframe_pivot, rbx_bndl_char_choice_at_origin, funct)
												
					

		


								if rbx_bndl_char_choice_add_motor6d_attachment:
									blender_api_create_collection("Motor6D Attachments", rbx_asset_name_clean)
									mesh_part_children = mesh_part.GetChildren()
									for child in mesh_part_children:
										if str(child.ClassName) == "Attachment":
											if "RigAttachment" in str(child.Name):
												mesh_part_motor6d_attachment = child
												dprint("mesh_part_motor6d_attachment: ", mesh_part_motor6d_attachment)
												mesh_part_motor6d_attachment_cframe = mesh_part_motor6d_attachment.Properties["CFrame"].Value

												blender_api_add_attachments(mesh_part_motor6d_attachment, mesh_part_motor6d_attachment_cframe, part_cframe, part_cframe_pivot, rbx_bndl_char_choice_at_origin, funct)




								if rbx_bndl_char_choice_add_bones:
									mesh_bones_array = mesh_data["bones"]
									# Collect bones into global dict
									for bone in mesh_bones_array:
										if bone["name"] not in all_bones_data:
											all_bones_data[bone["name"]] = bone


									if rbx_bndl_char_choice_add_meshes:
										# Collect vertex/weight info for this mesh
										skin_info = []
										for vert_idx, (si, w) in enumerate(zip(mesh_data["skinIndices"], mesh_data["skinWeights"])):
											bone_name = mesh_bones_array[si]["name"]
											skin_info.append((vert_idx, bone_name, w))

										all_mesh_skin_data.append({
											"object": rbx_obj,
											"skin_info": skin_info
										})


					if rbx_bndl_char_choice_add_bones:
						## bones here join
						'''import json
						print(json.dumps(all_bones_data, indent=4))'''

						# Add single armature
						#bpy.ops.object.mode_set(mode='OBJECT')

						bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
						arm_obj = bpy.context.object
						arm = arm_obj.data
						arm_obj.name = "R15_Armature"

						# --- PASS 1: create all bones ---
						for bone_name, bd in all_bones_data.items():
							print("BONE: ", bone_name)
							if bone_name not in arm.edit_bones.keys():
								eb = arm.edit_bones.new(bone_name)

								# Use cframe translation as placeholder head
								cframe = bd.get("cframe")
								print(cframe)
								if cframe:
									blender_matrix = funct.cframe_to_blender_matrix(cframe)
									oriented_blender_matrix = funct.blender_matrix_axis_conversion(blender_matrix)
									head, tail = funct.matrix_to_bone_positions(blender_matrix)
									eb.head = head
									eb.tail = tail
								else:
									# fallback if no cframe
									eb.head = mathutils.Vector((0, 0, 0))
									eb.tail = mathutils.Vector((0, 0.1, 0))

						# --- PASS 2: set parents (still in Edit Mode) ---
						for bone_name, bd in all_bones_data.items():
							parent = bd.get("parent")  # dict or None
							parent_name = parent["name"] if parent else None

							if parent_name and parent_name in arm.edit_bones.keys():
								child_bone = arm.edit_bones[bone_name]
								parent_bone = arm.edit_bones[parent_name]
								child_bone.parent = parent_bone
								child_bone.use_connect = False  # keep world-space head/tail
							else:
								print(f"[INFO] Bone {bone_name} has no parent")
						
						bpy.ops.object.mode_set(mode='OBJECT')




						'''Mapping Subsets and Skinning together
						The weight value of each bone on a given vertex can be worked out through the following pseudocode:

						for (subset in subsets) {
							vertsBegin = subset.vertsBegin
							vertsEnd = vertsBegin + subset.vertsLength

							for (i = vertsBegin; i < vertsEnd; i++) {
								vert = mesh.Verts[i]
								skinning = mesh.Skinning[i]
								
								for (j = 0; j < 4; j++) {
									subsetIndex = skinning.subsetIndices[j]
									boneWeight = skinning.boneWeights[j]

									if (boneWeight > 0) {
										boneIndex = subset.boneIndices[subsetIndex]
										bone = bones[boneIndex]
										
										// Apply the bone weight to the vertex
										vert.Weights[bone] = boneWeight;
									}
								}
							}
							}'''




						if rbx_bndl_char_choice_add_meshes:
							for mesh_skin in all_mesh_skin_data:
								obj = mesh_skin["object"]

								# Create vertex groups for all bones used by this mesh
								used_bones = set(bone_name for _, bone_name, _ in mesh_skin["skin_info"])
								for bone_name in used_bones:
									if bone_name not in obj.vertex_groups:
										obj.vertex_groups.new(name=bone_name)

								# Assign weights
								for vert_idx, bone_name, weight in mesh_skin["skin_info"]:
									obj.vertex_groups[bone_name].add([vert_idx], weight, 'REPLACE')

								# Add armature modifier
								mod = obj.modifiers.new(name="ArmatureMod", type='ARMATURE')
								mod.object = arm_obj



						#cleanup_tmp_files(rbx_filtered_assets_id_only, ".rbxm")
						#cleanup_tmp_files(rbx_meshes_to_clean_up_lst, ".mesh")





						
						
						
						
			

		return {'FINISHED'}


