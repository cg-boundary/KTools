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
from .. import utils

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

        for boolean in booleans:
            mod = target.modifiers.new(name="Boolean", type='BOOLEAN')
            mod.show_expanded = False
            mod.object = boolean
            boolean.display_type = 'WIRE'
            utils.object.parent_object(child=boolean, parent=target)
            mod.operation = self.boolean_type


        context.area.tag_redraw()
        return {'FINISHED'}


    def draw(self, context:Context):
        layout = self.layout

