# <pep8-80 compliant>

import bpy
from meshstats.ui import MeshstatsPanel


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
    bpy.utils.register_class(MeshstatsPanel)


def unregister():
    bpy.utils.unregister_class(MeshstatsPanel)


if __name__ == "__main__":
    register()
