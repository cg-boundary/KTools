# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Panel
from .. import utils

# ------------------------------------------------------------------------------- #
# PANELS
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

        box = layout.box()
        box.label(text="Booleans")
        prop = box.operator("kt.boolean", text="Difference")
        prop.boolean_type = 'DIFFERENCE'
        prop = box.operator("kt.boolean", text="Union")
        prop.boolean_type = 'UNION'
        prop = box.operator("kt.boolean", text="Intersect")
        prop.boolean_type = 'INTERSECT'
        prop = box.operator("kt.boolean", text="Slice")
        prop.boolean_type = 'SLICE'
