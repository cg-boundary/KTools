# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
import bmesh
import math
import random
from mathutils import (
    geometry,
    Vector,
    Matrix,
    Euler,
    Quaternion,
)
from bpy.types import (
    Context,
    Object,
    Operator,
    Mesh,
    SpaceView3D,
    Scene,
)
from ... import utils

# ------------------------------------------------------------------------------- #
# OPERATOR
# ------------------------------------------------------------------------------- #

class Voxel:
    def __init__(self, co:Vector, index:int):
        self.co = co
        self.index = index
        self.active = False
        self.pos_x = None
        self.neg_x = None
        self.pos_y = None
        self.neg_y = None
        self.pos_z = None
        self.neg_z = None


    def total_neighbors_active(self, voxels):
        total = 0
        if voxels[self.pos_x].active: total += 1
        if voxels[self.neg_x].active: total += 1
        if voxels[self.pos_y].active: total += 1
        if voxels[self.neg_y].active: total += 1
        if voxels[self.pos_z].active: total += 1
        if voxels[self.neg_z].active: total += 1
        return total


    def activate_neighbors(self, voxels):
        voxels[self.pos_x].active = True
        voxels[self.neg_x].active = True
        voxels[self.pos_y].active = True
        voxels[self.neg_y].active = True
        voxels[self.pos_z].active = True
        voxels[self.neg_z].active = True


    def deactivate_neighbors(self, voxels):
        voxels[self.pos_x].active = False
        voxels[self.neg_x].active = False
        voxels[self.pos_y].active = False
        voxels[self.neg_y].active = False
        voxels[self.pos_z].active = False
        voxels[self.neg_z].active = False


    def random_neighbor(self):
        choice = random.choice([self.pos_x, self.neg_x, self.pos_y, self.neg_y, self.pos_z, self.neg_z])
        return choice


class GEN:
    REGISTERED = False
    HANDLE_POST_VIEW = None
    HANDLE_POST_PIXEL = None
    GRID = 25
    VOXELS: list[Voxel] = []
    COORDS: list[Vector] = []
    POINTS_BATCH = None

    @classmethod
    def remove(cls):
        cls.REGISTERED = False
        if cls.HANDLE_POST_VIEW:
            SpaceView3D.draw_handler_remove(cls.HANDLE_POST_VIEW, 'WINDOW')
            cls.HANDLE_POST_VIEW = None
        if cls.HANDLE_POST_PIXEL:
            SpaceView3D.draw_handler_remove(cls.HANDLE_POST_PIXEL, 'WINDOW')
            cls.HANDLE_POST_PIXEL = None
        if cls.frame_change_pre in bpy.app.handlers.frame_change_pre:
            bpy.app.handlers.frame_change_pre.remove(cls.frame_change_pre)


    @classmethod
    def setup(cls, context:Context):
        # Flag
        cls.REGISTERED = True

        # Handles
        args = (context,)
        cls.HANDLE_POST_VIEW = SpaceView3D.draw_handler_add(cls.draw_post_view, args, 'WINDOW', 'POST_VIEW')
        cls.HANDLE_POST_PIXEL = SpaceView3D.draw_handler_add(cls.draw_post_pixel, args, 'WINDOW', 'POST_PIXEL')
        bpy.app.handlers.frame_change_pre.append(cls.frame_change_pre)

        # Grid
        cls.COORDS = []
        for x in range(cls.GRID):
            for y in range(cls.GRID):
                for z in range(cls.GRID):
                    point = Vector((x,y,z))
                    cls.COORDS.append(point)

        # Graphics
        cls.POINTS_BATCH = utils.graphics.create_points_batch(cls.COORDS)

        # Voxels
        cls.VOXELS = []
        for index, coord in enumerate(cls.COORDS):
            voxel = Voxel(coord, index)
            cls.VOXELS.append(voxel)
            x, y, z = cls.from_index(index)
            g = cls.GRID
            voxel.pos_x = cls.to_index((x + 1) % g, y, z)
            voxel.neg_x = cls.to_index((x - 1) % g, y, z)
            voxel.pos_y = cls.to_index(x, (y + 1) % g, z)
            voxel.neg_y = cls.to_index(x, (y - 1) % g, z)
            voxel.pos_z = cls.to_index(x, y, (z + 1) % g)
            voxel.neg_z = cls.to_index(x, y, (z - 1) % g)

        # Seed
        index = random.randint(0, len(cls.VOXELS))
        voxel = cls.VOXELS[index]
        voxel.active = True
        cls.VOXELS[voxel.random_neighbor()].active = True
        cls.VOXELS[voxel.random_neighbor()].active = True
        cls.VOXELS[voxel.random_neighbor()].active = True


    @classmethod
    def to_index(cls, x, y, z):
        return x * cls.GRID * cls.GRID + y * cls.GRID + z


    @classmethod
    def from_index(cls, index):
        g = cls.GRID
        x = index // (g * g)
        y = (index // g) % g
        z = index % g
        return x, y, z


    @classmethod
    def frame_change_pre(cls, scene:Scene, deps):
        frame = scene.frame_current
        end = scene.frame_end
        fps = scene.render.fps

        voxels = cls.VOXELS

        for voxel in cls.VOXELS:
            if voxel.active:
                count = voxel.total_neighbors_active(voxels)
                if count > 4:
                    continue
                elif count > 3:
                    voxel.active = False
                    voxel.deactivate_neighbors(voxels)
                    break
                elif count > 2:
                    voxels[voxel.random_neighbor()].active = True
                    voxels[voxel.random_neighbor()].active = True
                else:
                    voxels[voxel.random_neighbor()].active = True

    @classmethod
    def draw_post_view(cls, context:Context):
        if cls.POINTS_BATCH:
            utils.graphics.draw_points_batch(cls.POINTS_BATCH, color=(0,1,0,1), size=1)

        points = []
        for voxel in cls.VOXELS:
            if voxel.active:
                points.append(voxel.co)
        batch = utils.graphics.create_points_batch(points)
        utils.graphics.draw_points_batch(batch, color=(1,1,0,1), size=10)


    @classmethod
    def draw_post_pixel(cls, context:Context):
        return
        coords = utils.ray.cast_points_to_screen_space(context, cls.COORDS)
        for index, coord in enumerate(coords):
            utils.graphics.draw_text(text=str(index), postion=coord, size=10, color=(1,1,1,1))


class KT_OT_VoxelGenV1(Operator):
    bl_idname      = "kt.voxel_gen_v1"
    bl_label       = "KT Voxel Gen V1"
    bl_description = "KTools - Voxel Gen V1"
    bl_options     = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context:Context):
        return True


    def execute(self, context:Context):
        # Stop
        if GEN.REGISTERED:
            GEN.remove()
        # Start
        else:
            GEN.setup(context)
        # Redraw
        context.area.tag_redraw()
        return {'FINISHED'}
