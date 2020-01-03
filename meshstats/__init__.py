# <pep8-80 compliant>

import bpy

from meshstats.overlay import draw_callback
from meshstats.props import MeshstatsProperties
from meshstats.ui import MainPanel, BudgetPanel


bl_info = {
    "name": "meshstats",
    "description": "Mesh statistics.",
    "author": "Atamert Ölçgen",
    "version": (0, 1),
    "blender": (2, 81, 0),
    "location": "View3D > Meshstats panel",
    "tracker_url": "https://github.com/muhuk",  # TODO: Fix this
    "support": "COMMUNITY",
    "category": "Mesh"
}


draw_handler = None


def register():
    global draw_handler

    bpy.utils.register_class(MeshstatsProperties)
    bpy.types.Scene.meshstats = bpy.props.PointerProperty(
        type=MeshstatsProperties
    )

    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(BudgetPanel)

    draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        draw_callback,
        (),
        'WINDOW',
        'POST_VIEW'
    )


def unregister():
    bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')

    bpy.utils.unregister_class(BudgetPanel)
    bpy.utils.unregister_class(MainPanel)

    del bpy.types.Scene.meshstats
    bpy.utils.unregister_class(MeshstatsProperties)


if __name__ == "__main__":
    register()
