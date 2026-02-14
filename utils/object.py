# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import math
import bmesh
from mathutils import (
    geometry,
    Vector,
    Matrix,
    Euler,
    Quaternion,
)
from bpy.types import (
    Context,
    Object,
    Operator,
    Mesh,
)

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def unparent_object(obj:Object):
    if isinstance(obj, Object) and obj.parent:
        mat = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = mat


def parent_object(child:Object, parent:Object):
    if isinstance(child, Object) and isinstance(parent, Object):
        if child.parent:
            unparent_object(child)
        child.parent = parent
        child.matrix_parent_inverse = parent.matrix_world.inverted_safe()


def duplicate_mesh(context:Context, obj:Object) -> Object | None:
    if isinstance(context, Context) and isinstance(obj, Object) and obj.type == 'MESH':
        if obj.data.is_editmode:
            obj.update_from_editmode()
        copy = obj.copy()
        copy.data = obj.data.copy()
        obj.animation_data_clear()
        return copy
    return None


def any_polygons_shaded_smooth(obj:Object):
    if isinstance(obj, Object) and obj.type == 'MESH':
        if obj.data.is_editmode:
            obj.update_from_editmode()
        for polygon in obj.data.polygons:
            if polygon.use_smooth:
                return True
    return False


def shade_polygons(obj, use_smooth:bool=True):
    if isinstance(obj, Object) and obj.type == 'MESH':
        mesh = obj.data
        if mesh.is_editmode:
            bm = bmesh.from_edit_mesh(mesh)
            for face in bm.faces:
                face.smooth = use_smooth
            bmesh.update_edit_mesh(mesh)
            obj.update_from_editmode()
        else:
            for polygon in obj.data.polygons:
                polygon.use_smooth = use_smooth
