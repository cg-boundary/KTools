# ------------------------------------------------------------------------------- #
# IMPORTS
# ------------------------------------------------------------------------------- #

import bpy
from bpy.types import (
    Collection,
    Context,
    Object,
    Operator,
    Mesh,
    Scene,
)
from enum import Enum

# ------------------------------------------------------------------------------- #
# TYPES
# ------------------------------------------------------------------------------- #

class COLORS(Enum):
    COLOR_01 = 1 # RED
    COLOR_02 = 2 # ORANGE
    COLOR_03 = 3 # YELLOW
    COLOR_04 = 4 # GREEN
    COLOR_05 = 5 # BLUE
    COLOR_06 = 6 # PURPLE
    COLOR_07 = 7 # PINK
    COLOR_08 = 8 # BROWN

# ------------------------------------------------------------------------------- #
# FUNCTIONS
# ------------------------------------------------------------------------------- #

def color_tag_collection(collection:Collection, color:COLORS):
    if isinstance(collection, Collection) and isinstance(color, COLORS):
        collection.color_tag = color.name


def create_collection(name:str="Collection") -> Collection:
    collection = bpy.data.collections.new(name=name)
    return collection


def get_collection_from_scene_by_name(scene:Scene, name:str="Collection") -> Collection | None:
    if isinstance(scene, Scene):
        for collection in scene.collection.children_recursive:
            if collection.name.startswith(name):
                return collection
    return None


def link_collection_to_scene(collection:Collection, scene:Scene):
    if isinstance(collection, Collection) and isinstance(scene, Scene):
        if collection not in scene.collection.children_recursive:
            scene.collection.children.link(collection)


def ensure_collection_in_scene_by_name(scene:Scene, name:str="Collection") -> Collection:
    collection = get_collection_from_scene_by_name(scene, name)
    if isinstance(collection, Collection):
        return collection
    collection = create_collection(name)
    link_collection_to_scene(collection, scene)
    return collection


def remove_object_from_scene_collections(obj:Object, scene:Scene):
    if isinstance(obj, Object) and isinstance(scene, Scene):
        if obj.name in scene.collection.objects:
            scene.collection.objects.unlink(obj)
        scene_collections = scene.collection.children_recursive
        for collection in obj.users_collection:
            if collection in scene_collections:
                collection.objects.unlink(obj)


def append_object_to_collection(obj:Object, collection:Collection) -> bool:
    if isinstance(obj, Object) and isinstance(collection, Collection):
        if obj.name not in collection.objects:
            collection.objects.link(obj)
        return True
    return False


def get_probable_collection_from_object(context:Context, obj:Object) -> Collection | None:
    if isinstance(context, Context) and isinstance(obj, Object):
        scene = context.scene
        if obj.name in scene.collection.objects:
            return scene.collection
        for collection in obj.users_collection:
            if collection in scene.collection.children_recursive:
                if collection == context.view_layer.layer_collection.collection:
                    return collection
                for layer in context.view_layer.layer_collection.children:
                    if not layer.exclude and layer.collection == collection:
                        return collection
        return None
