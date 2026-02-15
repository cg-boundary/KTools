# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from mathutils import (
    Vector,
    Matrix,
    Quaternion,
)
from mathutils.geometry import (
    intersect_line_plane,
)
from bpy_extras.view3d_utils import (
    region_2d_to_vector_3d,
    region_2d_to_origin_3d,
    region_2d_to_location_3d,
    location_3d_to_region_2d
)
from bpy.types import (
    Context,
    Event,
)
import math

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def mouse_ray(context:Context, event:Event) -> tuple:
    mouse = Vector((event.mouse_region_x, event.mouse_region_y))
    ray_org = region_2d_to_origin_3d(context.region, context.region_data, mouse)
    ray_nor = region_2d_to_vector_3d(context.region, context.region_data, mouse)
    ray_end = ray_org + (ray_nor * context.space_data.clip_end)
    return mouse, ray_org, ray_nor, ray_end


def cast_to_view_plane(context:Context, event:Event) -> Vector:
    mouse, ray_org, ray_nor, ray_end = mouse_ray(context, event)
    plane_co = context.region_data.view_location
    plane_no = context.region_data.view_rotation @ Vector((0,0,1))
    hit_point = intersect_line_plane(ray_org, ray_end, plane_co, plane_no)
    if hit_point is None:
        return Vector((0,0,0))
    return hit_point


def cast_points_to_screen_space(context:Context, points:list[Vector]=[]) -> list[Vector]:
    hw = context.area.width / 2
    hh = context.area.height / 2
    perp_mat = context.region_data.perspective_matrix
    casted_points = []
    for point in points:
        prj = perp_mat @ Vector((point[0], point[1], point[2], 1.0))
        if prj.w > 0.0:
            casted_points.append(Vector((hw + hw * (prj.x / prj.w), hh + hh * (prj.y / prj.w))))
    return casted_points
