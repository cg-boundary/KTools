# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.utils import register_class, unregister_class
# Mesh
from .mesh.booleans import KT_OT_Boolean
from .mesh.mirror import KT_OT_Mirror
# Procedural
from .procedural import voxel_gen_v1


CLASSES = (
    # Mesh
    KT_OT_Boolean,
    KT_OT_Mirror,
    # Procedural
    voxel_gen_v1.KT_OT_VoxelGenV1,
)

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    for cls in CLASSES:
        register_class(cls)


def unregister():
    # Procedural
    voxel_gen_v1.GEN.remove()

    for cls in reversed(CLASSES):
        unregister_class(cls)

