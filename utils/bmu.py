# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import bmesh
import math
from mathutils import (
    geometry,
    Vector,
    Matrix,
    Euler,
    Quaternion,
)
from bmesh.types import (
    BMesh,
    BMVert,
    BMEdge,
    BMFace,
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

def open_bmesh(mesh:Mesh):
    bm = None
    if isinstance(mesh, Mesh):
        # Edit Mode
        if mesh.is_editmode:
            bm = bmesh.from_edit_mesh(mesh)
        # Object Mode
        else:
            bm = bmesh.new(use_operators=True)
            bm.from_mesh(mesh)
    return bm


def close_bmesh(bm:BMesh, mesh:Mesh):
    if isinstance(bm, BMesh):
        if isinstance(mesh, Mesh):
            if bm.is_valid:
                update_bmesh(bm, mesh)
                # Object Mode
                if not bm.is_wrapped:
                    bm.free()
    bm = None


def update_bmesh(bm:BMesh, mesh:Mesh):
    # Ensure
    ensure_bmesh(bm)
    # Edit Mode
    if bm.is_wrapped:
        bmesh.update_edit_mesh(mesh, loop_triangles=True, destructive=True)
    # Object Mode
    else:
        bm.to_mesh(mesh)


def ensure_bmesh(bm:BMesh):
    if isinstance(bm, BMesh):
        if bm.is_valid:
            tool_sel_mode = bpy.context.tool_settings.mesh_select_mode
            bm.select_mode = {mode for mode, sel in zip(['VERT', 'EDGE', 'FACE'], tool_sel_mode) if sel}
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            bm.verts.index_update()
            bm.edges.index_update()
            bm.faces.index_update()
            bm.select_history.validate()
            bm.select_flush_mode()
            bm.normal_update()


def simple_bisect(bm:BMesh, axis:str='+X'):
    plane_no = Vector((0,0,1))
    if axis == '+X':
        plane_no = Vector((-1,0,0))
    elif axis == '-X':
        plane_no = Vector((1,0,0))
    elif axis == '+Y':
        plane_no = Vector((0,-1,0))
    elif axis == '-Y':
       plane_no = Vector((0,1,0))
    elif axis == '+Z':
        plane_no = Vector((0,0,-1))
    elif axis == '-Z':
       plane_no = Vector((0,0,1))
    bmesh.ops.bisect_plane(
        bm,
        geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
        dist=0.005,
        plane_co=Vector((0,0,0)),
        plane_no=plane_no,
        use_snap_center=False,
        clear_outer=True,
        clear_inner=False
    )
