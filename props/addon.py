# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    PointerProperty,
)
from bpy.types import (
    AddonPreferences,
    Context,
)
from .. import utils

# ------------------------------------------------------------------------------- #
# OPERATOR
# ------------------------------------------------------------------------------- #

class KT_OT_Addon(AddonPreferences):
    bl_idname = utils.addon.name()


    def draw(self, context:Context):
        layout = self.layout


