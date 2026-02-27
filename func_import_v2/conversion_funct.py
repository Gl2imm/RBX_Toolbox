import bpy
import bpy_extras
import mathutils

'''
Blender Matrix
matrix = | m[0][0]  m[0][1]  m[0][2] |	# X axis vector
         | m[1][0]  m[1][1]  m[1][2] |	# Y axis vector
         | m[2][0]  m[2][1]  m[2][2] |	# Z axis vector
Rows are where the vector is pointing to in world space (X Y Z)
'''

def cframe_identity():
	"""Return an identity CFrame dict (replaces RbxCFrame() from .NET)."""
	return {"position": (0.0, 0.0, 0.0), "rotation": ("matrix", (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))}


def cframe_get_components(cframe):
	"""Extract a 12-tuple (px,py,pz, r00..r22) from any CFrame format.
	Supports dicts from rbxm_reader, lists, and legacy .NET objects.
	"""
	if isinstance(cframe, dict):
		pos = cframe.get("position", (0, 0, 0))
		rot_type, rot_data = cframe.get("rotation", ("matrix", (1,0,0, 0,1,0, 0,0,1)))
		return (*pos, *rot_data)
	elif isinstance(cframe, (list, tuple)):
		return tuple(cframe)
	elif hasattr(cframe, "GetComponents"):
		return cframe.GetComponents()
	else:
		raise TypeError(f"Unsupported CFrame type: {type(cframe)}")

def cframe_to_blender_matrix(cframe):
	"""Convert Roblox CFrame to Blender 4x4 matrix. (no swapping Y/Z)
	Supports:
	  - list of 12 floats [px, py, pz, r00..r22]
	  - dict from rbxm_reader: {"position": (x,y,z), "rotation": ("matrix", (9 floats))}
	  - .NET CFrame objects with .GetComponents() (legacy, if still used)
	"""
	if isinstance(cframe, list):
		if len(cframe) != 12:
			raise ValueError("CFrame must have exactly 12 components")
		px, py, pz, r00, r01, r02, r10, r11, r12, r20, r21, r22 = cframe
	elif isinstance(cframe, dict):
		# rbxm_reader dict format: {"position": (x,y,z), "rotation": ("matrix", (r00..r22))}
		pos = cframe.get("position", (0, 0, 0))
		px, py, pz = pos
		rot_type, rot_data = cframe.get("rotation", ("matrix", (1,0,0, 0,1,0, 0,0,1)))
		r00, r01, r02, r10, r11, r12, r20, r21, r22 = rot_data
	elif hasattr(cframe, "GetComponents"):
		# Legacy .NET CFrame object
		px, py, pz, r00, r01, r02, r10, r11, r12, r20, r21, r22 = cframe.GetComponents()
	else:
		raise TypeError(f"Unsupported CFrame type: {type(cframe)}")

	# Build a 4x4 matrix
	matrix = mathutils.Matrix((
		(r00, r01, r02, px),
		(r10, r11, r12, py),
		(r20, r21, r22, pz),
		(0.0, 0.0, 0.0, 1.0)
	))

	return matrix


def blender_matrix_axis_conversion(matrix: mathutils.Matrix, loc_vector_only: bool = False):
	"""Takes blender 4x4 matrix and transfoming it from Roblox orientation into blender orientation"""
	print("ORIGINAL MATRIX")
	print(matrix)
	identity_matrix = mathutils.Matrix.Identity(4)	#creates no rotations 4x4 matrix
	## transform from roblox -Z forward to blender Y forward and from Y up to Z up
	### transformation pattern
	transform_to_blender = bpy_extras.io_utils.axis_conversion(from_forward='-Z', from_up='Y', to_forward='-Y', to_up='Z').to_4x4()

	### conversion of blender matrix to new pattern
	transformed_blender_matrix = transform_to_blender @ matrix
	print("TRANSFORMED MATRIX")
	print(transformed_blender_matrix)

	if loc_vector_only:
		transformed_blender_matrix = transformed_blender_matrix.to_translation()
		print("PIVOT MATRIX")
		print(transformed_blender_matrix)

	return transformed_blender_matrix



def matrix_to_bone_positions(matrix, length=0.2):
	"""Return head and tail vectors from a 4x4 matrix (list of lists)."""
	# Head = translation of the matrix
	head = matrix.to_translation()

	# Tail = along local Y axis (Blender bone direction)
	# m.col[1] is the 2nd column = local Y axis in Blender
	y_axis = matrix.col[1].to_3d().normalized()
	tail = head + (y_axis * length)

	return head, tail