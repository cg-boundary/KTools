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

# ------------------------------------------------------------------------------- #
# OPERATOR
# ------------------------------------------------------------------------------- #

class KT_OT_Mirror(Operator):
    bl_idname      = "kt.mirror"
    bl_label       = "KT Mirror"
    bl_description = "KTools - Mirror"
    bl_options     = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context:Context):
        if context.mode == 'EDIT_MESH':
            return True
        elif context.mode == 'OBJECT':
            if isinstance(context.active_object, bpy.types.Object):
                if context.active_object.type == 'MESH':
                    return True
        return False


    def execute(self, context:Context):
        obj = None
        if context.mode == 'EDIT_MESH':
            obj = context.edit_object
        elif context.mode == 'OBJECT':
            if isinstance(context.active_object, bpy.types.Object):
                if context.active_object.type == 'MESH':
                    obj = context.active_operator

        if not isinstance(obj, bpy.types.Object):
            return {'CANCELLED'}


        return {'FINISHED'}




    def draw(self, context:Context):
        layout = self.layout


