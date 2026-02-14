# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.utils import register_class, unregister_class
from .booleans import KT_OT_Boolean
from .mirror import KT_OT_Mirror


CLASSES = (
    KT_OT_Boolean,
    KT_OT_Mirror,
)

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    for cls in CLASSES:
        register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        unregister_class(cls)

