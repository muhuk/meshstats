# <pep8-80 compliant>

import bpy
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


def register():
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(BudgetPanel)


def unregister():
    bpy.utils.unregister_class(BudgetPanel)
    bpy.utils.unregister_class(MainPanel)


if __name__ == "__main__":
    register()
