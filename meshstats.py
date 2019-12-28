# <pep8-80 compliant>

import bpy.utils
import bpy.types
import bmesh


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
        obj = context.active_object
        self.layout.label(text="Selected object: {}".format(obj.name))

        bm = bmesh.new()
        bm.from_mesh(obj.data)

        self.layout.label(text="# of faces = {}".format(len(bm.faces)))

        tris = [f for f in bm.faces if len(f.loops) == 3]
        quads = [f for f in bm.faces if len(f.loops) == 4]
        ngons = [f for f in bm.faces if len(f.loops) > 4]
        self.layout.label(text="# of tris = {}".format(len(tris)))
        self.layout.label(text="# of quads = {}".format(len(quads)))
        self.layout.label(text="# of ngons = {}".format(len(ngons)))

        bm.free()

    @classmethod
    def poll(cls, context):
        return  context.mode == 'OBJECT' \
            and context.selected_objects \
            and context.active_object.type == 'MESH'


def register():
    bpy.utils.register_class(MeshstatsPanel)


def unregister():
    bpy.utils.unregister_class(MeshstatsPanel)


if __name__ == "__main__":
    register()
