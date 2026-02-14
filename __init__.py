# ------------------------------------------------------------------------------- #
# ADDON
# ------------------------------------------------------------------------------- #

bl_info = {
    "name": "KTools",
    "description": "Blender Workflow Utilities",
    "author": "KenzoCG",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D",
    "category": "3D View"
}

# ------------------------------------------------------------------------------- #
# REGISTER
# ------------------------------------------------------------------------------- #

def register():
    from . import utils
    utils.register()
    from . import props
    props.register()
    from . import ops
    ops.register()
    from . import interfaces
    interfaces.register()
    register_hotkeys()


def unregister():
    unregister_hotkeys()
    from . import interfaces
    interfaces.unregister()
    from . import ops
    ops.unregister()
    from . import props
    props.unregister()
    from . import utils
    utils.unregister()

# ------------------------------------------------------------------------------- #
# HOTKEYS
# ------------------------------------------------------------------------------- #

import bpy

KEYS = []


def register_hotkeys():

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="Object Mode", space_type='EMPTY')

    kmi = km.keymap_items.new("kt.boolean", 'NUMPAD_MINUS', 'PRESS', ctrl=True, shift=False, alt=False)
    kmi.properties.boolean_type = 'DIFFERENCE'
    KEYS.append((km, kmi))

    kmi = km.keymap_items.new("kt.boolean", 'NUMPAD_PLUS', 'PRESS', ctrl=True, shift=False, alt=False)
    kmi.properties.boolean_type = 'UNION'
    KEYS.append((km, kmi))

    kmi = km.keymap_items.new("kt.boolean", 'NUMPAD_ASTERIX', 'PRESS', ctrl=True, shift=False, alt=False)
    kmi.properties.boolean_type = 'INTERSECT'
    KEYS.append((km, kmi))

    kmi = km.keymap_items.new("kt.boolean", 'NUMPAD_SLASH', 'PRESS', ctrl=True, shift=False, alt=False)
    kmi.properties.boolean_type = 'SLICE'
    KEYS.append((km, kmi))


def unregister_hotkeys():
    for km, kmi in KEYS:
        km.keymap_items.remove(kmi)
    KEYS.clear()



