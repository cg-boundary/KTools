# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.utils import register_class, unregister_class
from .addon import KT_OT_Addon


CLASSES = (
    KT_OT_Addon,
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

