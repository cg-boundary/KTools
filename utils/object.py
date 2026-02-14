# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import math
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

