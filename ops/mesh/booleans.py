# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import bmesh
import math
from mathutils import (
    geometry,
    Vector,
    Matrix,
    Euler,
    Quaternion,
)
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    PointerProperty,
)
from bpy.types import (
    Context,
    Object,
    Operator,
    Mesh,
)
from ... import utils

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def get_target_and_booleans(context:Context) -> tuple[Object, list[Object]] | tuple[None, None]:
    if isinstance(context.active_object, Object) and context.active_object.type == 'MESH':
        target = context.active_object
        booleans = [obj for obj in context.selected_editable_objects if obj.type == 'MESH' and obj != target]
        if booleans:
            return target, booleans
    return None, None



# ------------------------------------------------------------------------------- #
# OPERATOR
# ------------------------------------------------------------------------------- #

class KT_OT_Boolean(Operator):
    bl_idname      = "kt.boolean"
    bl_label       = "KT Boolean"
    bl_description = "KTools - Boolean"
    bl_options     = {'REGISTER', 'UNDO'}

    boolean_opts = (
        ('DIFFERENCE', "Difference", ""),
        ('UNION'     , "Union"     , ""),
        ('INTERSECT' , "Intersect" , ""),
        ('SLICE'     , "Slice"     , ""),
    )
    boolean_type: EnumProperty(name="Booleans", items=boolean_opts, default='DIFFERENCE') # type:ignore

    @classmethod
    def poll(cls, context:Context):
        target, booleans = get_target_and_booleans(context)
        if target is None or booleans is None:
            return False
        return True


    def execute(self, context:Context):
        target, booleans = get_target_and_booleans(context)

        for mod in target.modifiers:
            if mod.type == 'BOOLEAN':
                if mod.object in booleans:
                    booleans.remove(mod.object)
        if not booleans:
            return {'CANCELLED'}

        scene = context.scene
        collection = utils.collection.ensure_collection_in_scene_by_name(scene, name="Booleans")
        utils.collection.color_tag_collection(collection, color=utils.collection.COLORS.COLOR_01)

        shade_smooth = utils.object.any_polygons_shaded_smooth(target)

        for boolean in booleans:
            utils.collection.remove_object_from_scene_collections(boolean, scene)
            utils.collection.append_object_to_collection(boolean, collection)
            utils.object.parent_object(boolean, target)
            boolean.display_type = 'WIRE'

            if shade_smooth:
                utils.object.shade_polygons(boolean, use_smooth=True)

            if self.boolean_type == 'SLICE':
                target_collection = utils.collection.get_probable_collection_from_object(context, target)
                if not target_collection:
                    target_collection = context.scene.collection
                copy = utils.object.duplicate_mesh(context, obj=target)
                utils.object.parent_object(copy, target)
                utils.collection.append_object_to_collection(copy, collection=target_collection)
                copy_mod = copy.modifiers.new(name="Slice", type='BOOLEAN')
                copy_mod.show_expanded = False
                copy_mod.show_in_editmode = True
                copy_mod.object = boolean
                copy_mod.operation = 'INTERSECT'
                mod = target.modifiers.new(name="Boolean", type='BOOLEAN')
                mod.show_expanded = False
                mod.show_in_editmode = True
                mod.object = boolean
                mod.operation = 'DIFFERENCE'
            else:
                mod = target.modifiers.new(name="Boolean", type='BOOLEAN')
                mod.show_expanded = False
                mod.show_in_editmode = True
                mod.object = boolean
                mod.operation = self.boolean_type

        context.area.tag_redraw()
        return {'FINISHED'}


    def draw(self, context:Context):
        layout = self.layout

