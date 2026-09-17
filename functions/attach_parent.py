import re
import bpy
from mathutils import Matrix


### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


# ---------------------------------------------------------------------------
# Name helpers
#
# The importer names accessory attachments "<Name>_att" (see
# func_blndr_api.blender_api_add_attachments, which rewrites "Attachment" ->
# "_att" for accessories) and leaves body attachments as "<Name>Attachment".
# Motor6D joints are "<Name>RigAttachment" and are never an accessory attach
# point, so they are filtered out of an item's own candidates.
# ---------------------------------------------------------------------------

_BLENDER_SUFFIX = re.compile(r"\.\d{3}$")


def strip_blender_suffix(name):
    """'BodyBack_att.001' -> 'BodyBack_att'."""
    return _BLENDER_SUFFIX.sub("", name or "")


def is_attachment_name(name):
    n = strip_blender_suffix(name).lower()
    return n.endswith("_att") or n.endswith("attachment")


def is_motor6d_name(name):
    return "rigattachment" in strip_blender_suffix(name).lower()


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def _attachment_collections_for(item):
    """
    Collections that hold this item's attachments.

    The importer does NOT parent attachments to their mesh, it drops them into
    a sibling collection ("<Item>_Attachments" for accessories, "<Prefix>
    Attachments NN" for layered cloth / face parts). So a name-only or
    children-only search would miss them.
    """
    cols = []
    own_cols = list(item.users_collection)
    base = strip_blender_suffix(item.name).lower()

    for col in bpy.data.collections:
        cname = col.name.lower()
        if "attachment" not in cname:
            continue
        if "motor6d" in cname:
            continue

        # a) nested directly under one of the collections the item lives in
        if any(col.name in oc.children for oc in own_cols):
            cols.append(col)
            continue

        # b) named after the item, e.g. "Classic_Swordpack_Throwback_Attachments"
        if base and strip_blender_suffix(col.name).lower().startswith(base):
            cols.append(col)

    return cols


def find_item_attachments(item):
    """Attachments belonging to *item*: parented children plus collection mates."""
    found = {}

    for child in item.children:
        if is_attachment_name(child.name) and not is_motor6d_name(child.name):
            found[child.name] = child

    for col in _attachment_collections_for(item):
        for obj in col.objects:
            if is_attachment_name(obj.name) and not is_motor6d_name(obj.name):
                found[obj.name] = obj

    return sorted(found.values(), key=lambda o: o.name)


def _creates_loop(child, new_parent):
    """True if parenting *child* to *new_parent* would build a parent cycle."""
    node = new_parent
    guard = 0
    while node is not None and guard < 1000:
        if node is child:
            return True
        node = node.parent
        guard += 1
    return False


# ---------------------------------------------------------------------------
# Transform helpers
#
# Parenting is done by assigning matrices, never with bpy.ops.object.parent_set:
# the operator works off the selection and, on Blender 5.x, transform operators
# that walk a hierarchy treat parented children individually.
# ---------------------------------------------------------------------------

def parent_keep_transform(child, parent, context):
    """Parent *child* to *parent*, leaving its world transform untouched."""
    world = child.matrix_world.copy()
    child.parent = parent
    child.parent_type = 'OBJECT'
    child.matrix_parent_inverse = parent.matrix_world.inverted()
    context.view_layer.update()
    child.matrix_world = world


def unparent_keep_transform(child, context):
    world = child.matrix_world.copy()
    child.parent = None
    context.view_layer.update()
    child.matrix_world = world


def parent_to_bone_keep_transform(child, armature, bone_name, context):
    """Bone-parent *child* without moving it.

    Blender anchors a bone parent at the bone TAIL, so matrix_world has to be
    re-applied after the parent is in place and the depsgraph has caught up.
    """
    world = child.matrix_world.copy()
    child.parent = armature
    child.parent_type = 'BONE'
    child.parent_bone = bone_name
    child.matrix_parent_inverse.identity()
    context.view_layer.update()
    child.matrix_world = world


def snap_to(obj, target, context):
    """Put obj exactly where target is (location + rotation), keeping obj's own scale."""
    loc, rot, _ = target.matrix_world.decompose()
    _, _, own_scale = obj.matrix_world.decompose()
    obj.matrix_world = Matrix.LocRotScale(loc, rot, own_scale)
    context.view_layer.update()


# ---------------------------------------------------------------------------
# Checks
#
# Every check returns (ok, label, payload). The panel uses `label` as the button
# text and `ok` as its enabled state; the operator re-runs the same check before
# doing anything, so a stale panel can never trigger a bad edit.
# ---------------------------------------------------------------------------

def get_source(context):
    """The item to attach: exactly one selected object, or None."""
    sel = list(context.selected_objects)
    if len(sel) == 1:
        return sel[0]
    return None


def _common_source(context):
    """(source, error_label) shared by all three buttons."""
    sel = list(context.selected_objects)
    if not sel:
        return None, "Select item to attach"
    if len(sel) > 1:
        return None, "Select only 1 item"
    return sel[0], None


def check_attach_to_attachment(context):
    rbx_prefs = context.scene.rbx_prefs
    src, err = _common_source(context)
    if err:
        return False, err, {}

    target = rbx_prefs.rbx_attach_target
    if target is None:
        return False, "Select target attachment", {}
    if target is src:
        return False, "Target is the item itself", {}
    if not is_attachment_name(target.name):
        return False, "Target is not an attachment", {}

    atts = find_item_attachments(src)
    if not atts:
        return False, "No attachment on item", {}
    if len(atts) > 1:
        return False, f"{len(atts)} attachments, need 1", {}

    att = atts[0]
    if att is target:
        return False, "Target is the item's own att", {}
    if _creates_loop(att, target):
        return False, "Would create a parent loop", {}

    return True, "Attach to Attachment", {"source": src, "target": target, "attachment": att}


def check_attach_to_mesh(context):
    rbx_prefs = context.scene.rbx_prefs
    src, err = _common_source(context)
    if err:
        return False, err, {}

    target = rbx_prefs.rbx_attach_target
    if target is None:
        return False, "Select target mesh", {}
    if target is src:
        return False, "Target is the item itself", {}
    if is_attachment_name(target.name):
        return False, "Target is an attachment", {}
    if target.type != 'MESH':
        return False, "Target is not a mesh", {}
    if _creates_loop(src, target):
        return False, "Would create a parent loop", {}

    return True, "Attach to Mesh", {"source": src, "target": target}


def check_attach_to_bone(context):
    rbx_prefs = context.scene.rbx_prefs
    src, err = _common_source(context)
    if err:
        return False, err, {}

    target = rbx_prefs.rbx_attach_target
    if target is None:
        return False, "Select target armature", {}
    if target is src:
        return False, "Target is the item itself", {}
    if target.type != 'ARMATURE':
        return False, "Target is not an armature", {}

    bone_name = rbx_prefs.rbx_attach_bone
    if not bone_name:
        return False, "Select a bone", {}
    if bone_name not in target.data.bones:
        return False, "Bone not in armature", {}

    if rbx_prefs.rbx_attach_bone_mode == 'WEIGHTS' and src.type != 'MESH':
        return False, "Weights need a mesh item", {}
    if _creates_loop(src, target):
        return False, "Would create a parent loop", {}

    return True, "Attach to Bone", {"source": src, "target": target, "bone": bone_name}


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------

class RBX_OT_attach_to_attachment(bpy.types.Operator):
    """Parent the item to its own attachment, then snap and parent that attachment to the target attachment"""
    bl_idname = "object.rbx_attach_to_attachment"
    bl_label = "Attach to Attachment"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ok, msg, data = check_attach_to_attachment(context)
        if not ok:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}

        item = data["source"]
        att = data["attachment"]
        target = data["target"]

        # 1. Free the attachment first -- it is usually a child of the item, and
        #    parenting the item under it while that holds would be a cycle.
        if att.parent is not None:
            unparent_keep_transform(att, context)

        # 2. The item now hangs off its own attachment, so moving the attachment
        #    carries the item with it.
        parent_keep_transform(item, att, context)

        # 3. Snap the attachment onto the target (location + rotation), item follows.
        snap_to(att, target, context)

        # 4. Hook it under the target attachment so it keeps following.
        parent_keep_transform(att, target, context)

        dprint(f"Attached {item.name} via {att.name} -> {target.name}")
        self.report({'INFO'}, f"{item.name} attached to {target.name} via {att.name}")
        return {'FINISHED'}


class RBX_OT_attach_to_mesh(bpy.types.Operator):
    """Parent the item to the target mesh without moving it"""
    bl_idname = "object.rbx_attach_to_mesh"
    bl_label = "Attach to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ok, msg, data = check_attach_to_mesh(context)
        if not ok:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}

        item = data["source"]
        target = data["target"]
        parent_keep_transform(item, target, context)

        self.report({'INFO'}, f"{item.name} parented to {target.name}")
        return {'FINISHED'}


class RBX_OT_attach_to_bone(bpy.types.Operator):
    """Parent the item to a bone of the target armature without moving it"""
    bl_idname = "object.rbx_attach_to_bone"
    bl_label = "Attach to Bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ok, msg, data = check_attach_to_bone(context)
        if not ok:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}

        rbx_prefs = context.scene.rbx_prefs
        item = data["source"]
        arm = data["target"]
        bone = data["bone"]

        if rbx_prefs.rbx_attach_bone_mode == 'OBJECT':
            parent_to_bone_keep_transform(item, arm, bone, context)
            self.report({'INFO'}, f"{item.name} parented to bone {bone}")
            return {'FINISHED'}

        # Weight mode: rigid bind -- armature modifier + one full-weight group.
        world = item.matrix_world.copy()

        mod = next((m for m in item.modifiers
                    if m.type == 'ARMATURE' and m.object == arm), None)
        if mod is None:
            mod = item.modifiers.new(name="Armature", type='ARMATURE')
            mod.object = arm

        other_groups = [vg.name for vg in item.vertex_groups if vg.name != bone]

        vg = item.vertex_groups.get(bone)
        if vg is None:
            vg = item.vertex_groups.new(name=bone)
        vg.add(range(len(item.data.vertices)), 1.0, 'REPLACE')

        item.parent = arm
        item.parent_type = 'OBJECT'
        item.matrix_parent_inverse = arm.matrix_world.inverted()
        context.view_layer.update()
        item.matrix_world = world

        if other_groups:
            self.report({'WARNING'},
                        f"{item.name} bound to {bone}, but it still has other "
                        f"vertex groups ({len(other_groups)}) that will also deform it")
        else:
            self.report({'INFO'}, f"{item.name} weight-bound to {bone}")
        return {'FINISHED'}


# ---------------------------------------------------------------------------
# Panel drawing
# ---------------------------------------------------------------------------

_TYPE_ICONS = {
    'MESH': 'OUTLINER_OB_MESH',
    'ARMATURE': 'OUTLINER_OB_ARMATURE',
    'EMPTY': 'OUTLINER_OB_EMPTY',
    'CURVE': 'OUTLINER_OB_CURVE',
}


def _action_button(col, ok, label, operator_id):
    """A button whose text IS its status, greyed out until the checks pass."""
    btn = col.row(align=True)
    btn.enabled = ok
    btn.scale_y = 1.1
    btn.operator(operator_id, text=label, icon='CHECKMARK' if ok else 'BLANK1')


def _action_row(box, title, check_result, operator_id, icon):
    """Title label sitting directly on its status button."""
    ok, label, _ = check_result
    col = box.column(align=True)
    col.label(text=title, icon=icon)
    _action_button(col, ok, label, operator_id)
    return ok


def draw_attach_parent(layout, context):
    """Draws the 'Attach & Parent' section. Called from menu_ui's Dummy tab."""
    scene = context.scene
    rbx_prefs = scene.rbx_prefs

    box = layout.box()

    header = box.row(align=True)
    icon = 'DOWNARROW_HLT' if scene.subpanel_attach else 'RIGHTARROW'
    header.prop(scene, 'subpanel_attach', icon=icon, icon_only=True, emboss=False)
    header.label(text='Attach & Parent', icon='CON_CHILDOF')

    if not scene.subpanel_attach:
        return

    # --- Item to attach (viewport selection) + target, as one tight block ----
    sel = list(context.selected_objects)

    item_col = box.column(align=True)
    item_col.label(text="Item to attach:")

    src_row = item_col.row(align=True)
    if len(sel) == 1:
        obj = sel[0]
        src_row.label(text=obj.name, icon=_TYPE_ICONS.get(obj.type, 'OBJECT_DATA'))
    elif not sel:
        src_row.alert = True
        src_row.label(text="Nothing selected", icon='ERROR')
    else:
        src_row.alert = True
        src_row.label(text=f"{len(sel)} objects selected", icon='ERROR')

    # Keep each label glued to its own value, but part the two groups so the
    # selected name does not run straight into the target picker.
    box.separator(factor=0.5)

    target_col = box.column(align=True)
    target_col.label(text="Attach to:")
    target_col.prop(rbx_prefs, 'rbx_attach_target', text="")

    # --- Actions -------------------------------------------------------------
    box.separator(type='LINE')

    _action_row(box, "Attach to Attachment",
                check_attach_to_attachment(context),
                'object.rbx_attach_to_attachment', 'EMPTY_ARROWS')

    box.separator(factor=0.35)

    _action_row(box, "Attach to Mesh",
                check_attach_to_mesh(context),
                'object.rbx_attach_to_mesh', 'OUTLINER_OB_MESH')

    box.separator(factor=0.35)

    # Bone needs its own two inputs before the button can mean anything.
    bone_col = box.column(align=True)
    bone_col.label(text="Attach to Bone", icon='BONE_DATA')

    target = rbx_prefs.rbx_attach_target
    bone_row = bone_col.row(align=True)
    if target is not None and target.type == 'ARMATURE':
        # While the armature sits in Edit Mode its `bones` collection is the
        # pre-edit copy -- `edit_bones` is the live one. Searching the wrong
        # collection there lists a stale set (or none at all).
        source = 'edit_bones' if target.mode == 'EDIT' else 'bones'
        bone_row.prop_search(rbx_prefs, 'rbx_attach_bone',
                             target.data, source, text="", icon='BONE_DATA')
    else:
        # A greyed-out text field reads like a dropdown that lost its entries.
        # Say why it is empty instead.
        bone_row.enabled = False
        bone_row.label(text="Pick an armature above", icon='BONE_DATA')

    mode_row = bone_col.row(align=True)
    mode_row.prop(rbx_prefs, 'rbx_attach_bone_mode', expand=True)

    ok, label, _ = check_attach_to_bone(context)
    _action_button(bone_col, ok, label, 'object.rbx_attach_to_bone')
