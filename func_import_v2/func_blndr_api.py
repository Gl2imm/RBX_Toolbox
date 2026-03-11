import bpy
import os
from RBX_Toolbox import glob_vars
from mathutils import Matrix, Vector

### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


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
        true_name = mesh_part.name

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
             # SpecialMesh.Scale comes as a tuple (x, y, z) from rbxm reader
             rbx_obj.scale = (special_mesh_scale[0], special_mesh_scale[1], special_mesh_scale[2])
        except Exception as e:
             print(f"Error applying special mesh scale: {e}")

    # Standard Matrix Logic for CFrame / Pivot
    if cframe and part_cframe_pivot:
        blender_matrix = funct.cframe_to_blender_matrix(cframe)
        oriented_blender_matrix = funct.blender_matrix_axis_conversion(blender_matrix)


        dprint(f"DEBUG_ORIGIN: Name={true_name}")
        dprint(f"  CFrame (Roblox): {cframe}")
        dprint(f"  PivotOffset (Roblox): {part_cframe_pivot}")
		
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
        
        ### Spawn at origin tracker
        if actual_at_origin:
            from RBX_Toolbox import glob_vars
            if rbx_obj not in glob_vars.rbx_spawn_tracker:
                glob_vars.rbx_spawn_tracker.append(rbx_obj)
            
    return rbx_obj


def blender_api_add_attachments(mesh_part_attachment, mesh_part_attachment_cframe, part_cframe, part_cframe_pivot, rbx_bndl_char_choice_at_origin, funct, is_accessory=False):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.15, 0.15, 0.15))
    bpy.ops.object.shade_smooth()
    mesh_part_attachment_obj = bpy.context.selected_objects[0]
    mesh_part_attachment_name = str(mesh_part_attachment.name)
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
        from RBX_Toolbox import glob_vars
        if mesh_part_attachment_obj not in glob_vars.rbx_spawn_tracker:
            glob_vars.rbx_spawn_tracker.append(mesh_part_attachment_obj)

    # Calculate Attachment Offset relative to Pivot
    # Attachment World Matrix = Parent(at Pivot) @ Translation(-PivotOffset) @ AttachmentLocal
    # PivotOffset here must be RAW LOCAL because it's applied in Local Space of the Parent.
    
    offset_matrix = Matrix.Translation(-raw_local_pivot)
    
    # Get Attachment Local Matrix
    blender_matrix_att = funct.cframe_to_blender_matrix(mesh_part_attachment_cframe)
    # oriented_blender_matrix_att = funct.blender_matrix_axis_conversion(blender_matrix_att)
    oriented_blender_matrix_att = blender_matrix_att
    
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



def blender_api_collapse_outliner():
    """Collapse all collections in the outliner for a clean view.
    Uses a deferred timer so the UI has time to register new collections."""
    
    def _do_collapse():
        try:
            for area in bpy.context.screen.areas:
                if area.type == 'OUTLINER':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            with bpy.context.temp_override(window=bpy.context.window, area=area, region=region):
                                bpy.ops.outliner.select_all(action='SELECT')
                                for _ in range(10):
                                    bpy.ops.outliner.show_one_level(open=False)
                                bpy.ops.outliner.select_all(action='DESELECT')
                            return None
        except Exception as e:
            dprint(f"Could not collapse outliner: {e}")
        return None
    
    bpy.app.timers.register(_do_collapse, first_interval=0.1)


def blender_api_assets_new_material(rbx_obj, mesh_part, rbx_textures, rbx_asset_name_clean, rbx_SurfaceAppearance):
	### Creating new Material ###
	
	if rbx_obj.material_slots:
		bpy.ops.object.material_slot_remove()
	mat = bpy.data.materials.new(name=f"{rbx_asset_name_clean}_{mesh_part.name}_mat")
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
				#dprint(f"Removed transparency texture node in material: {mat.name}")
			else:
				print(f"No alpha texture to remove in material: {mat.name}")

			if not base_color_tex or base_color_tex.type != 'TEX_IMAGE':
				#dprint(f"Material {mat.name}: Base color is not connected to an image texture.")
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


#################################
##### Animation Functions #####
#################################

# Threshold for animated position (Roblox units).
# Bones whose position delta (after mean subtraction) stays below this
# are rotation-only — their position is just the baked anatomical joint offset.
POSITION_THRESHOLD = 0.002

def _apply_face_front_quat(qw, qx, qy, qz):
	"""180° rotation around the physical up axis (Arm Y = World Z)."""
	return (qw, -qx, qy, -qz)

def _apply_face_front_pos(rx, ry, rz):
	"""180° mirror for position to match FACE_FRONT rotation."""
	return (-rx, ry, -rz)

def _compute_position_info(keyframes_by_track):
	"""
	Roblox Pose positions are ABSOLUTE joint positions in parent-bone space
	(anatomical rest offset + animated delta). Blender pose_bone.location
	expects only the delta from the armature rest pose.

	Solution: subtract the per-bone mean position (which approximates the
	rest offset) to extract only the animated oscillation.
	"""
	info = {}
	for track, kfs in keyframes_by_track.items():
		xs = [k["pos"][0] for k in kfs]
		ys = [k["pos"][1] for k in kfs]
		zs = [k["pos"][2] for k in kfs]
		n  = len(kfs)
		mx, my, mz = sum(xs)/n, sum(ys)/n, sum(zs)/n
		max_delta = max(
			max(abs(x - mx) for x in xs),
			max(abs(y - my) for y in ys),
			max(abs(z - mz) for z in zs),
		)
		info[track] = {
			"mean":     (mx, my, mz),
			"animated": max_delta > POSITION_THRESHOLD,
		}
	return info


def _detect_armature_type(armature):
	"""Auto-detect whether an armature uses 'standard' or 'imported' bone orientations.

	Standard armatures (e.g. manually created rigs):
	  - Bone local Y axis ≈ Blender +Y in armature space (identity bone axes)
	  - Armature object has a 90° X rotation for Roblox→Blender conversion

	Imported armatures (from Import Beta):
	  - Bone local Y axis ≈ Blender +Z in armature space (conversion baked into bones)
	  - Armature object has identity world rotation

	Returns:
	  'standard'  – animation quaternions can be applied directly
	  'imported'  – quaternions need rest-pose compensation
	"""
	from mathutils import Vector as Vec

	# Check a reference bone (LowerTorso, UpperTorso, or Head — any spine bone)
	ref_names = ["LowerTorso", "UpperTorso", "Head"]
	for ref_name in ref_names:
		bone = armature.data.bones.get(ref_name)
		if bone is None:
			continue

		# bone.matrix_local is the bone's rest pose matrix in armature space
		# Column 1 (index 1) is the bone's local Y axis direction
		local_y = bone.matrix_local.col[1].to_3d().normalized()

		# Standard: bone local Y ≈ armature +Y (0, 1, 0)
		# Imported: bone local Y ≈ armature +Z (0, 0, 1)
		dot_y = abs(local_y.dot(Vec((0, 1, 0))))
		dot_z = abs(local_y.dot(Vec((0, 0, 1))))

		if dot_y > 0.9:
			dprint(f"[Animation] Armature type: STANDARD (bone '{ref_name}' Y-axis ≈ armature +Y)")
			return "standard"
		elif dot_z > 0.9:
			dprint(f"[Animation] Armature type: IMPORTED (bone '{ref_name}' Y-axis ≈ armature +Z)")
			return "imported"

	# Fallback: assume standard
	dprint("[Animation] Armature type: STANDARD (fallback, no reference bone found)")
	return "standard"


def _convert_roblox_quat_for_imported_bone(pose_bone, qw, qx, qy, qz, face_front=True):
	"""Convert a Roblox animation quaternion for a bone with non-identity rest pose.

	For imported armatures, the Roblox→Blender axis conversion (90° around X)
	is baked into each bone's rest orientation instead of the armature object.

	Roblox animation data is expressed in Roblox bone-local space:
	  X = right, Y = up, Z = backward

	Blender's pose_bone.rotation_quaternion is a delta FROM the bone's rest pose,
	expressed in the bone's local coordinate system.

	We need to:
	  1. Apply face_front 180° correction in Roblox space (if enabled)
	  2. Convert from Roblox space to Blender world space
	  3. Transform into bone-local space using the bone's rest rotation
	"""
	from mathutils import Quaternion as Quat

	# Apply face_front in Roblox space (180° around Roblox Y = up axis)
	# Same as _apply_face_front_quat but done before axis conversion
	if face_front:
		qw, qx, qy, qz = qw, -qx, qy, -qz

	q_roblox = Quat((qw, qx, qy, qz))

	# Roblox→Blender axis conversion: 90° rotation around X
	# This is the same transform as blender_matrix_axis_conversion:
	#   from_forward='-Z', from_up='Y' → to_forward='-Y', to_up='Z'
	ROT_X_90 = Quat((0.7071068, 0.7071068, 0, 0))  # 90° around X

	# The Roblox quaternion in Blender world space
	q_blender_world = ROT_X_90 @ q_roblox @ ROT_X_90.conjugated()

	# Get bone rest rotation in armature space
	rest_rot = pose_bone.bone.matrix_local.to_quaternion()

	# Convert world-space rotation to bone-local delta:
	# pose_quat = rest_inv @ world_rotation
	q_pose = rest_rot.conjugated() @ q_blender_world @ rest_rot

	return q_pose.w, q_pose.x, q_pose.y, q_pose.z


def _convert_roblox_pos_for_imported_bone(pose_bone, dx, dy, dz, face_front=True):
	"""Convert a Roblox position delta for a bone with non-identity rest pose.

	Same logic as quaternion conversion — transform from Roblox bone-local space
	into the Blender bone's local coordinate system.
	"""
	from mathutils import Vector as Vec

	# Apply face_front mirror in Roblox space first
	if face_front:
		dx, dy, dz = -dx, dy, -dz

	pos_roblox = Vec((dx, dy, dz))

	# Roblox→Blender axis conversion for positions:
	# Blender X = Roblox X, Blender Y = Roblox -Z, Blender Z = Roblox Y
	pos_blender = Vec((pos_roblox.x, -pos_roblox.z, pos_roblox.y))

	# Rotate into bone-local space
	rest_rot = pose_bone.bone.matrix_local.to_quaternion()
	pos_local = rest_rot.conjugated() @ pos_blender

	return pos_local.x, pos_local.y, pos_local.z


def blender_api_apply_animation(armature, anim_data, action_name=None, speed=1.0, reverse=False, face_front=True):
	"""Apply parsed Roblox animation data to a Blender armature.

	Automatically detects whether the armature uses standard bone orientations
	(identity axes, armature-level rotation) or imported bone orientations
	(Roblox→Blender conversion baked into bone rest poses) and applies the
	correct transformation.

	Args:
		armature:    Blender armature object (bpy.types.Object with type='ARMATURE')
		anim_data:   Dict from animation_reader.read_animation(ks)
		action_name: Optional custom action name (defaults to anim_data['name'])
		speed:       Playback speed multiplier (default 1.0)
		reverse:     If True, reverse the animation timeline
		face_front:  If True, apply 180° rotation so character faces Blender +Y
	"""
	from mathutils import Quaternion as Quat, Vector as Vec

	if armature is None or armature.type != "ARMATURE":
		print("[Animation] ERROR: No valid armature provided.")
		return None

	# Must be 60 — Roblox keyframes are at 1/60s intervals
	FPS = 60

	length     = anim_data["length"]
	keyframes  = anim_data["keyframes"]

	if not keyframes:
		print("[Animation] WARNING: No keyframe tracks found.")
		return None

	# Auto-detect armature type for correct quaternion handling
	arm_type = _detect_armature_type(armature)
	is_imported = (arm_type == "imported")

	pos_info = _compute_position_info(keyframes)

	# Setup scene timing
	bpy.context.scene.render.fps = FPS
	bpy.context.scene.frame_start = 1
	bpy.context.scene.frame_end   = int((length / speed) * FPS) + 1

	# Create action
	name = action_name or anim_data.get("name") or "RobloxAnim"
	action = bpy.data.actions.new(name=name)
	armature.animation_data_create()
	armature.animation_data.action = action

	skipped = set()

	for track, track_kfs in keyframes.items():
		bone_name = track.split(".")[1] if "." in track else track
		pose_bone = armature.pose.bones.get(bone_name)
		if not pose_bone:
			skipped.add(f"{track} → '{bone_name}'")
			continue

		pose_bone.rotation_mode = "QUATERNION"
		pinfo      = pos_info[track]
		apply_loc  = pinfo["animated"]
		mx, my, mz = pinfo["mean"]

		for kf in track_kfs:
			t     = length - kf["time"] if reverse else kf["time"]
			frame = (t / speed) * FPS + 1

			qw, qx, qy, qz = kf["rot"]
			# Position delta: subtract mean to remove baked anatomical offset
			dx = kf["pos"][0] - mx
			dy = kf["pos"][1] - my
			dz = kf["pos"][2] - mz

			if is_imported:
				# Imported armature: compensate for bone rest-pose orientation
				qw, qx, qy, qz = _convert_roblox_quat_for_imported_bone(
					pose_bone, qw, qx, qy, qz, face_front=face_front
				)
				if apply_loc:
					dx, dy, dz = _convert_roblox_pos_for_imported_bone(
						pose_bone, dx, dy, dz, face_front=face_front
					)
			else:
				# Standard armature: direct assignment with optional face-front
				if face_front:
					qw, qx, qy, qz = _apply_face_front_quat(qw, qx, qy, qz)
					dx, dy, dz      = _apply_face_front_pos(dx, dy, dz)

			pose_bone.rotation_quaternion = Quat((qw, qx, qy, qz))
			pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)

			if apply_loc:
				pose_bone.location = Vec((dx, dy, dz))
				pose_bone.keyframe_insert(data_path="location", frame=frame)

	if skipped:
		print(f"[Animation] Skipped {len(skipped)} tracks (no matching bone):")
		for s in sorted(skipped):
			print(f"  {s}")

	print(f"[Animation] Applied '{action.name}' to '{armature.name}' ({arm_type}) — Frames: 1 → {bpy.context.scene.frame_end}")
	return action


def blender_api_apply_curve_animation(armature, anim_data, action_name=None, speed=1.0, reverse=False, face_front=True):
	"""Apply parsed CurveAnimation data to a Blender armature.

	Separate function from blender_api_apply_animation to avoid breaking
	the working KeyframeSequence pipeline. CurveAnimation data may have
	different length/timing characteristics that need special handling.

	Args:
		armature:    Blender armature object (bpy.types.Object with type='ARMATURE')
		anim_data:   Dict from curve_animation_reader.read_curve_animation(ca)
		action_name: Optional custom action name (defaults to anim_data['name'])
		speed:       Playback speed multiplier (default 1.0)
		reverse:     If True, reverse the animation timeline
		face_front:  If True, apply 180° rotation so character faces Blender +Y
	"""
	from mathutils import Quaternion as Quat, Vector as Vec

	if armature is None or armature.type != "ARMATURE":
		print("[CurveAnim] ERROR: No valid armature provided.")
		return None

	FPS = 60

	length    = anim_data.get("length", 0.0)
	keyframes = anim_data.get("keyframes", {})

	if not keyframes:
		print("[CurveAnim] WARNING: No keyframe tracks found.")
		return None

	# Guard against invalid length values (NaN, inf, negative, or absurdly large)
	if not isinstance(length, (int, float)) or length != length:  # NaN check
		print(f"[CurveAnim] WARNING: Invalid length ({length}), defaulting to 1.0s")
		length = 1.0
	elif length <= 0:
		# Static pose: compute length from the max keyframe time across all tracks
		max_time = 0.0
		for track_kfs in keyframes.values():
			for kf in track_kfs:
				t = kf.get("time", 0.0)
				if isinstance(t, (int, float)) and t == t and t > max_time:
					max_time = t
		length = max(max_time, 1.0 / FPS)  # At least one frame
		dprint(f"[CurveAnim] Computed length from keyframes: {length:.4f}s")

	# Cap frame_end to a safe int32 range
	raw_frame_end = (length / max(speed, 0.001)) * FPS + 1
	frame_end = min(int(raw_frame_end), 2_000_000)  # ~9 hours at 60fps should be plenty

	# Auto-detect armature type for correct quaternion handling
	arm_type = _detect_armature_type(armature)
	is_imported = (arm_type == "imported")

	pos_info = _compute_position_info(keyframes)

	# Setup scene timing
	bpy.context.scene.render.fps = FPS
	bpy.context.scene.frame_start = 1
	bpy.context.scene.frame_end   = frame_end

	# Create action
	name = action_name or anim_data.get("name") or "CurveAnimation"
	action = bpy.data.actions.new(name=name)
	armature.animation_data_create()
	armature.animation_data.action = action

	skipped = set()

	for track, track_kfs in keyframes.items():
		bone_name = track.split(".")[1] if "." in track else track
		pose_bone = armature.pose.bones.get(bone_name)
		if not pose_bone:
			skipped.add(f"{track} → '{bone_name}'")
			continue

		pose_bone.rotation_mode = "QUATERNION"
		pinfo      = pos_info[track]
		apply_loc  = pinfo["animated"]
		mx, my, mz = pinfo["mean"]

		for kf in track_kfs:
			t     = length - kf["time"] if reverse else kf["time"]
			frame = (t / max(speed, 0.001)) * FPS + 1

			qw, qx, qy, qz = kf["rot"]
			# Position delta: subtract mean to remove baked anatomical offset
			dx = kf["pos"][0] - mx
			dy = kf["pos"][1] - my
			dz = kf["pos"][2] - mz

			if is_imported:
				# Imported armature: compensate for bone rest-pose orientation
				qw, qx, qy, qz = _convert_roblox_quat_for_imported_bone(
					pose_bone, qw, qx, qy, qz, face_front=face_front
				)
				if apply_loc:
					dx, dy, dz = _convert_roblox_pos_for_imported_bone(
						pose_bone, dx, dy, dz, face_front=face_front
					)
			else:
				# Standard armature: direct assignment with optional face-front
				if face_front:
					qw, qx, qy, qz = _apply_face_front_quat(qw, qx, qy, qz)
					dx, dy, dz      = _apply_face_front_pos(dx, dy, dz)

			pose_bone.rotation_quaternion = Quat((qw, qx, qy, qz))
			pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)

			if apply_loc:
				pose_bone.location = Vec((dx, dy, dz))
				pose_bone.keyframe_insert(data_path="location", frame=frame)

	if skipped:
		dprint(f"[CurveAnim] Skipped {len(skipped)} tracks (no matching bone):")
		for s in sorted(skipped):
			dprint(f"  {s}")

	dprint(f"[CurveAnim] Applied '{action.name}' to '{armature.name}' ({arm_type}) — Frames: 1 → {frame_end}")
	return action
