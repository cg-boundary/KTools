# ------------------------------------------------------------------------------- #
# ADDON
# ------------------------------------------------------------------------------- #

bl_info = {
    "name": "KTools",
    "description": "Blender Workflow Utilities",
    "author": "KenzoCG",
    "version": (1, 0, 0),
    "blender": (5, 0, 2),
    "location": "View3D",
    "category": "3D View"
}

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    from . import utils
    utils.register()
    from . import ops
    ops.register()


def unregister():
    from . import ops
    ops.unregister()
    from . import utils
    utils.unregister()
