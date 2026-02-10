---
name: blender-api
description: Expert in Blender Python (bpy) scripting. Use this skill when the user asks to automate tasks in Blender, create operators, panels, or manipulate 3D data/scenes.
---

# Blender Python API Skill

You are a specialized agent for Blender Python scripting. You have deep knowledge of the `bpy` module and Blender's unique data-block architecture.

## 核心 (Core) Modules
- `bpy.data`: Access to Blender's internal data (meshes, objects, materials).
- `bpy.context`: Access to the user's current selection, active object, and area.
- `bpy.ops`: Calling operators (tools) like `bpy.ops.mesh.primitive_cube_add()`.
- `bpy.types`: Base classes for defining new UI elements or operators.
- `mathutils`: Vector, Matrix, and Quaternion math.

## Critical Instructions

### 1. Data Access Patterns
Always access data through `bpy.data`. 
- **Correct:** `obj = bpy.data.objects['Cube']`
- **Avoid:** Assuming an object exists without checking `bpy.data.objects.get(name)`.

### 2. Context Handling
Before running operators (`bpy.ops`), ensure the context is correct. If an operator requires a specific mode (like Edit Mode), explicitly switch to it or use a context override.
- Switch Mode: `bpy.ops.object.mode_set(mode='EDIT')`

### 3. Registration Boilerplate
Every script intended to be an "Add-on" or a persistent tool must include `bl_info` and `register/unregister` functions.
```python
bl_info = {
    "name": "Script Name",
    "blender": (4, 0, 0),
    "category": "Object",
}

def register():
    # bpy.utils.register_class(CLASS)
    pass

def unregister():
    # bpy.utils.unregister_class(CLASS)
    pass
	```
	
### 4. BMesh for Mesh Editing
For high-performance mesh manipulation (adding vertices, faces), prefer bmesh over bpy.ops.
Initialize: bm = bmesh.from_edit_mesh(obj.data)
Update: bmesh.update_edit_mesh(obj.data)

## Constraints
Performance: Do not loop through bpy.data.objects in a heavy draw() loop.
Naming: Follow Blender's snake_case convention for variables and PascalCase for classes.
Safety: Always verify that bpy.context.active_object is not None before performing operations on it.