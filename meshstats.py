# <pep8-80 compliant>

import bpy
import bmesh
import time


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

    @classmethod
    def poll(cls, context):
        return  context.mode == 'OBJECT' \
            and context.selected_objects \
            and context.active_object.type == 'MESH'

    def draw(self, context):
        obj = context.active_object
        self.layout.label(text="Selected object: {}".format(obj.name))
        data = {}
        self._calculate_stats(data, obj)
        self._draw_summary_table(self.layout, data)

    @staticmethod
    def _draw_summary_table(layout, data):
        j = layout.grid_flow(columns = 3)
        j.label(text="")
        j.label(text="Tris")
        j.label(text="Quads")
        j.label(text="Ngons")

        j.label(text="count")
        j.label(text="{}".format(data['tris_count']))
        j.label(text="{}".format(data['quads_count']))
        j.label(text="{}".format(data['ngons_count']))

        j.label(text="percentage")
        j.label(text="???")
        j.label(text="???")
        j.label(text="???")

    @staticmethod
    def _calculate_stats(d, obj):
        start_time = time.time()
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        tris = [f for f in bm.faces if len(f.loops) == 3]
        quads = [f for f in bm.faces if len(f.loops) == 4]
        ngons = [f for f in bm.faces if len(f.loops) > 4]

        d['tris_count'] = len(tris)
        d['quads_count'] = len(quads)
        d['ngons_count'] = len(ngons)

        bm.free()
        duration = time.time() - start_time
        print("calculated stats for '{}' in {:.4f} seconds".format(obj.name, duration))


def register():
    bpy.utils.register_class(MeshstatsPanel)


def unregister():
    bpy.utils.unregister_class(MeshstatsPanel)


if __name__ == "__main__":
    register()
