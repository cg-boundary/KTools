# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.utils import register_class, unregister_class
from .view_3d_panel import (
    KT_PT_View3dPanelMesh,
    KT_PT_View3dPanelProcedural,
)


CLASSES = (
    KT_PT_View3dPanelMesh,
    KT_PT_View3dPanelProcedural,
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

