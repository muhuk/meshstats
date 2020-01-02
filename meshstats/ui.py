# <pep8-80 compliant>

import time

import bgl
import bpy
import bmesh
import gpu
import gpu_extras.batch
import mathutils

from meshstats.face import (FaceTri, FaceNgon)


class MeshstatsPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    bl_idname = "VIEW3D_PT_meshstats"
    bl_label = "Meshstats"

    _draw_handler = None
    _data = {}

    @classmethod
    def poll(cls, context):
        should_draw = context.mode == 'OBJECT' \
            and context.selected_objects \
            and context.active_object.type == 'MESH'
        if not should_draw and cls._draw_handler is not None:
            print("removing handler")
            bpy.types.SpaceView3D.draw_handler_remove(
                cls._draw_handler,
                'WINDOW'
            )
            cls._draw_handler = None
        elif should_draw and cls._draw_handler is None:
            print("adding handler")
            color_tri = context.preferences.themes[0].view_3d.extra_face_area
            color_ngon = context.preferences.themes[0].view_3d.extra_face_angle
            cls._draw_handler = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback,
                (cls, color_tri, color_ngon),
                'WINDOW',
                'POST_VIEW'
            )
        return should_draw

    def draw(self, context):
        obj = context.active_object
        self.layout.label(text="Selected object: {}".format(obj.name))
        self._calculate_stats(self._data, obj)
        self._draw_summary_table(self.layout, self._data)

    @staticmethod
    def _calculate_stats(d, obj):
        start_time = time.time()
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        m = mathutils.Matrix(obj.matrix_world)

        d['tris'] = []
        d['ngons'] = []
        for face in bm.faces:
            if len(face.loops) == 3:
                d['tris'].append(
                    FaceTri(*[(m @ l.vert.co) for l in face.loops])
                )
            elif len(face.loops) > 4:
                d['ngons'].append(
                    FaceNgon([(m @ l.vert.co) for l in face.loops])
                )
        d['tris_count'] = len(d['tris'])
        d['ngons_count'] = len(d['ngons'])
        d['quads_count'] = len(bm.faces) - d['tris_count'] - d['ngons_count']

        bm.free()
        duration = time.time() - start_time
        d['_update_duration'] = duration
        print("calculated stats for '{}' in {:.4f} seconds".format(
            obj.name,
            duration
        ))

    @staticmethod
    def _draw_summary_table(layout, data):
        j = layout.grid_flow(columns=3)
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


def draw_callback(panel, color_tri, color_ngon):
    shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    shader.bind()
    bgl.glLineWidth(3)

    shader.uniform_float("color", (color_tri.r, color_tri.g, color_tri.b, 1.0))
    for tri in panel._data['tris']:
        batch = gpu_extras.batch.batch_for_shader(
            shader,
            'LINE_LOOP',
            {"pos": tri.to_list()}
        )
        batch.draw(shader)

    shader.uniform_float(
        "color",
        (color_ngon.r, color_ngon.g, color_ngon.b, 1.0)
    )
    for ngon in panel._data['ngons']:
        batch = gpu_extras.batch.batch_for_shader(
            shader,
            'LINE_LOOP',
            {"pos": ngon.to_list()}
        )
        batch.draw(shader)

    # Reset defaults
    bgl.glLineWidth(1)
