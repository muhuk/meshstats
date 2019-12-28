# <pep8-80 compliant>

import bpy.utils
import bpy.types


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


class MeshstatsPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    bl_idname = "VIEW3D_PT_meshstats"
    bl_label = "Meshstats"

    def draw(self, context):
        self.layout.label(text="test")


def register():
    bpy.utils.register_class(MeshstatsPanel)


def unregister():
    bpy.utils.unregister_class(MeshstatsPanel)


if __name__ == "__main__":
    register()
