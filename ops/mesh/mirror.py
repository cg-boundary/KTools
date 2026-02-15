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
# OPERATOR
# ------------------------------------------------------------------------------- #

class KT_OT_Mirror(Operator):
    bl_idname      = "kt.mirror"
    bl_label       = "KT Mirror"
    bl_description = "KTools - Mirror"
    bl_options     = {'REGISTER', 'UNDO'}

    axis_opts = (
        ('+X' ,"+X", ""),
        ('-X', "-X", ""),
        ('+Y', "+Y", ""),
        ('-Y', "-Y", ""),
        ('+Z', "+Z", ""),
        ('-Z', "-Z", ""),
    )
    axis: EnumProperty(name="Axis", items=axis_opts, default='+X') # type:ignore

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
                    obj = context.active_object
        if not isinstance(obj, Object):
            return {'CANCELLED'}

        # Slice
        mesh = obj.data
        bm = utils.bmu.open_bmesh(mesh)
        utils.bmu.simple_bisect(bm, axis=self.axis)
        utils.bmu.close_bmesh(bm, mesh)

        # Modifier
        mirror = obj.modifiers.new(name="Mirror", type='MIRROR')
        if 'X' in self.axis:
            mirror.use_axis = (True, False, False)
        elif 'Y' in self.axis:
            mirror.use_axis = (False, True, False)
        elif 'Z' in self.axis:
            mirror.use_axis = (False, False, True)
        mirror.use_clip = True

        context.area.tag_redraw()
        return {'FINISHED'}


    def draw(self, context:Context):
        layout = self.layout
        layout.prop(self, 'axis')


