import bpy
import os
from RBX_Toolbox import glob_vars
from mathutils import Matrix, Vector


#################################
##### Blender API functions #####
#################################

def blender_api_import_obj(obj_filepath):
	if glob_vars.bldr_ver[0] < '4':
		bpy.ops.import_scene.obj(filepath=obj_filepath)
	else:
		bpy.ops.wm.obj_import(filepath=obj_filepath)
	return



def blender_api_add_meshes_as_obj(bundle_own_folder, mesh_part, mesh_data, cframe, part_cframe_pivot, actual_at_origin, mesh_reader, funct, mesh_name=None, special_mesh_scale=None):
    if mesh_name:
        true_name = mesh_name
    else:
        true_name = mesh_part.Name

    obj_file_path = os.path.join(bundle_own_folder, true_name + ".obj")
    mesh_reader.write_obj_from_mesh_json(mesh_data, obj_file_path, lod_index=0, object_name=true_name)

    blender_api_import_obj(obj_file_path)
    rbx_obj = bpy.context.selected_objects[0]
    rbx_obj.name = true_name
    
    # Deselect and Select only the new object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    bpy.data.objects[rbx_obj.name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_obj.name]

    # Apply Scale if provided (e.g. SpecialMesh)
    if special_mesh_scale:
        try:
             # SpecialMesh.Scale is Vector3
             rbx_obj.scale = (special_mesh_scale.X, special_mesh_scale.Y, special_mesh_scale.Z)
        except Exception as e:
             print(f"Error applying special mesh scale: {e}")

    # Standard Matrix Logic for CFrame / Pivot
    if cframe and part_cframe_pivot:
        blender_matrix = funct.cframe_to_blender_matrix(cframe)
        oriented_blender_matrix = funct.blender_matrix_axis_conversion(blender_matrix)


        print(f"DEBUG_ORIGIN: Name={true_name}")
        print(f"  CFrame (Roblox): {cframe}")
        print(f"  PivotOffset (Roblox): {part_cframe_pivot}")
		
        # Calculate Pivot Offset Vector (Raw Local Space)
        blender_matrix_pivot = funct.cframe_to_blender_matrix(part_cframe_pivot)
        raw_local_pivot = blender_matrix_pivot.translation

        # Shift Mesh Data so that Origin is at Pivot Point
        # We move vertices by -PivotOffset (in Local Space)
        rbx_obj.data.transform(Matrix.Translation(-raw_local_pivot))
        
        # Rotate the Pivot Vector by Object Rotation to get World Space Offset
        rot_mat = oriented_blender_matrix.to_3x3()
        rotated_pivot_vector = rot_mat @ raw_local_pivot
        
        # Adjust Object Matrix to be at World Pivot Location
        # New Pos = Old Pos + Rotated Pivot Offset
        oriented_blender_matrix.translation += rotated_pivot_vector

        # Apply the matrix to object (world transform)
        rbx_obj.matrix_world = oriented_blender_matrix
        
        ### Spawn at origin
        if actual_at_origin:
            # Simply reset translation to 0,0,0
            # If pivot logic worked, 0,0,0 is now the Pivot point in World Space.
            rbx_obj.matrix_world.translation = (0.0, 0.0, 0.0)
            
    return rbx_obj


def blender_api_add_attachments(mesh_part_attachment, mesh_part_attachment_cframe, part_cframe, part_cframe_pivot, rbx_bndl_char_choice_at_origin, funct, is_accessory=False):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.15, 0.15, 0.15))
    bpy.ops.object.shade_smooth()
    mesh_part_attachment_obj = bpy.context.selected_objects[0]
    mesh_part_attachment_name = str(mesh_part_attachment.Name)
    if is_accessory and "Attachment" in mesh_part_attachment_name:
        mesh_part_attachment_name = mesh_part_attachment_name.replace("Attachment", "_att")
    mesh_part_attachment_obj.name = f"{mesh_part_attachment_name}"
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None 
    bpy.data.objects[mesh_part_attachment_obj.name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[mesh_part_attachment_obj.name]

    # Get main mesh location
    blender_matrix_parent = funct.cframe_to_blender_matrix(part_cframe)
    oriented_blender_matrix_parent = funct.blender_matrix_axis_conversion(blender_matrix_parent)
    
    # Apply mesh matrix to attachment (world transform)
    # NOTE: Mesh Origin is now at Pivot Point! 
    # So 'oriented_blender_matrix_parent' (derived from Part CFrame Center) is NOT where the Mesh Object Origin is.
    # We need to construct the matrix of the Mesh Object (at Pivot).
    
    blender_matrix_pivot = funct.cframe_to_blender_matrix(part_cframe_pivot)
    raw_local_pivot = blender_matrix_pivot.translation
    
    rot_mat = oriented_blender_matrix_parent.to_3x3()
    rotated_pivot_vector = rot_mat @ raw_local_pivot
    
    # Shift Parent Matrix to Pivot Location
    oriented_blender_matrix_parent.translation += rotated_pivot_vector
    
    # Apply final parent matrix to attachment object temporarily (as base)
    mesh_part_attachment_obj.matrix_world = oriented_blender_matrix_parent

    # Apply mesh matrix to attachment if spawn at origin
    if rbx_bndl_char_choice_at_origin:
        # Reset Parent Translation to (0,0,0)
        oriented_blender_matrix_parent.translation = (0.0, 0.0, 0.0)
        mesh_part_attachment_obj.matrix_world.translation = (0.0, 0.0, 0.0)

    # Calculate Attachment Offset relative to Pivot
    # Attachment World Matrix = Parent(at Pivot) @ Translation(-PivotOffset) @ AttachmentLocal
    # PivotOffset here must be RAW LOCAL because it's applied in Local Space of the Parent.
    
    offset_matrix = Matrix.Translation(-raw_local_pivot)
    
    # Get Attachment Local Matrix
    blender_matrix_att = funct.cframe_to_blender_matrix(mesh_part_attachment_cframe)
    oriented_blender_matrix_att = funct.blender_matrix_axis_conversion(blender_matrix_att)
    
    # Combine Matrices: Parent(at Pivot) @ Offset(to Center) @ Attachment(from Center)
    final_matrix = oriented_blender_matrix_parent @ offset_matrix @ oriented_blender_matrix_att

    # Apply the matrix to object (world transform)
    mesh_part_attachment_obj.matrix_world = final_matrix
										



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
		try:
			parent.children.link(coll)
		except RuntimeError:
			pass

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