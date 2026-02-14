# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Panel
from .. import utils

# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

class KT_PT_View3dPanel(Panel):
    bl_label       = "KTools"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "KTools"
    bl_options     = {'HEADER_LAYOUT_EXPAND'}

    @classmethod
    def poll(cls, context):
        return True


    def draw(self, context):
        layout = self.layout
        layout.operator("kt.mirror")
