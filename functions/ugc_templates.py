import bpy
import mathutils
from RBX_Toolbox import glob_vars

# Name given to the fur particle system added to a mesh, used to detect/convert it.
FUR_PS_NAME = "RBX Fur"


def fluff_update(self, context):
    """Update callback for Object.rbx_fluff.

    Rotates the fur template mesh on X by the *change* in the slider and bakes it
    straight into the geometry (mesh.transform == applied rotation), so the fur
    particle instances pick it up. A plain object rotation has no effect unless
    applied, which is exactly what this avoids."""
    obj = self
    if obj is None or obj.type != 'MESH' or obj.data is None:
        return
    last = obj.get("_rbx_fluff_last", 0.0)
    delta = obj.rbx_fluff - last
    if abs(delta) < 1e-7:
        return
    try:
        obj.data.transform(mathutils.Matrix.Rotation(delta, 4, 'X'))
        obj.data.update()
        obj["_rbx_fluff_last"] = obj.rbx_fluff
    except Exception:
        pass


def _blend_path():
    return glob_vars.addon_path + glob_vars.rbx_blend_file


def _ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass


def fur_ps_of(obj):
    """Return the RBX fur particle system of a mesh object, or None."""
    if obj is None or obj.type != 'MESH':
        return None
    return obj.particle_systems.get(FUR_PS_NAME)


######### UGC Templates Button ###########
class RBX_OT_ugc_template(bpy.types.Operator):
    bl_label = "RBX UGC Template"
    bl_idname = "object.rbx_ugc_template"
    bl_options = {'REGISTER', 'UNDO'}
    action: bpy.props.StringProperty(name="Action")  # type: ignore

    def execute(self, context):
        action = self.action
        if action == 'chain':
            return self._spawn_collection('Chain template', "Chain Template")
        if action == 'fur_sample':
            return self._spawn_collection('Fur template', "Fur Sample")
        if action == 'apply_fur':
            return self._apply_fur(context)
        if action == 'convert_fur':
            return self._convert_fur(context, combined=False)
        if action == 'convert_fur_combined':
            return self._convert_fur(context, combined=True)
        return {'CANCELLED'}

    def _spawn_collection(self, datablock, label):
        _ensure_object_mode()
        bpy.ops.wm.append(
            directory=_blend_path() + glob_vars.ap_collection,
            filename=datablock,
        )
        self.report({'INFO'}, f"{label} spawned")
        return {'FINISHED'}

    def _apply_fur(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh first")
            return {'CANCELLED'}
        _ensure_object_mode()
        blend = _blend_path()

        # Fresh particle-settings preset so each mesh keeps independent values.
        with bpy.data.libraries.load(blend, link=False) as (_from, _to):
            _to.particles = ["FurParticleSettings"]
        settings = _to.particles[0]

        # Fresh fur template object (the instance source), linked so it is visible.
        with bpy.data.libraries.load(blend, link=False) as (_from, _to2):
            _to2.objects = ["fur_template"]
        fur_tmpl = _to2.objects[0]
        context.collection.objects.link(fur_tmpl)

        # Add a particle system to the mesh and wire it to the preset + template.
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.particle_system_add()
        ps = obj.particle_systems[-1]
        ps.name = FUR_PS_NAME
        ps.settings = settings
        settings.render_type = 'OBJECT'
        settings.instance_object = fur_tmpl
        settings.use_rotations = True

        self.report({'INFO'}, "Fur applied to mesh")
        return {'FINISHED'}

    def _convert_fur(self, context, combined):
        obj = context.active_object
        ps = fur_ps_of(obj)
        if ps is None:
            self.report({'ERROR'}, "Active mesh has no fur to convert")
            return {'CANCELLED'}
        _ensure_object_mode()
        fur_tmpl = ps.settings.instance_object if ps.settings else None

        # Make the particle instances real (one mesh per fur strand).
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        context.view_layer.update()

        before = set(bpy.data.objects)
        bpy.ops.object.duplicates_make_real()
        new_objs = [o for o in bpy.data.objects
                    if o not in before and o is not fur_tmpl and o is not obj and o.type == 'MESH']

        # Remove the particle system so the fur isn't displayed twice.
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        for i, p in enumerate(obj.particle_systems):
            if p.name == FUR_PS_NAME:
                obj.particle_systems.active_index = i
                bpy.ops.object.particle_system_remove()
                break

        if combined and new_objs:
            bpy.ops.object.select_all(action='DESELECT')
            for o in new_objs:
                o.select_set(True)
            target = new_objs[0]
            context.view_layer.objects.active = target
            bpy.ops.object.join()
            target.name = obj.name + "_Fur"
            msg = "Fur converted to a single mesh"
        else:
            msg = f"Fur converted to {len(new_objs)} meshes"

        # The template instance is only a source for the fur; remove it either way.
        if fur_tmpl is not None and fur_tmpl.name in bpy.data.objects:
            bpy.data.objects.remove(fur_tmpl, do_unlink=True)

        self.report({'INFO'}, msg)
        return {'FINISHED'}
