# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import Panel
from .. import utils

# ------------------------------------------------------------------------------- #
# PANELS
# ------------------------------------------------------------------------------- #

class KT_PT_View3dPanelMesh(Panel):
    bl_label       = "KTools - Mesh"
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


class KT_PT_View3dPanelProcedural(Panel):
    bl_label       = "KTools - Procedural"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "KTools"
    bl_options     = {'HEADER_LAYOUT_EXPAND'}

    @classmethod
    def poll(cls, context):
        return True


    def draw(self, context):
        layout = self.layout

        layout.label(text="Voxel")
        layout.operator("kt.voxel_gen_v1", text="Voxel Gen V1")
