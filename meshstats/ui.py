# <pep8-80 compliant>

import time

import bgl
import bpy
import gpu
import gpu_extras.batch

from meshstats.mesh import Mesh


class MainPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    bl_idname = "VIEW3D_PT_meshstats"
    bl_label = "Meshstats"

    _draw_handler = None
    _mesh = Mesh()

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
        self.layout.template_ID(
            context.view_layer.objects,
            "active",
            filter='AVAILABLE'
        )
        obj = context.active_object
        self._calculate_stats(obj)
        self._draw_summary_table(self.layout.box())
        self._draw_overlay_options(context, self.layout.box())

    @classmethod
    def _calculate_stats(cls, obj):
        start_time = time.time()
        cls._mesh(obj)
        duration = time.time() - start_time
        # d['_update_duration'] = duration
        print("calculated stats for '{}' in {:.4f} seconds".format(
            obj.name,
            duration
        ))

    @classmethod
    def _draw_summary_table(cls, layout):
        layout.label(text="Face Count")
        j = layout.grid_flow(columns=3)
        j.label(text="")
        j.label(text="Tris")
        j.label(text="Quads")
        j.label(text="Ngons")
        j.label(text="Total")

        j.label(text="count")
        j.label(text="{}".format(cls._mesh.tris_count))
        j.label(text="{}".format(cls._mesh.quads_count))
        j.label(text="{}".format(cls._mesh.ngons_count))
        j.label(text="{}".format(cls._mesh.face_count))

        j.label(text="percentage")
        j.label(text="{}%".format(cls._mesh.tris_percentage))
        j.label(text="{}%".format(cls._mesh.quads_percentage))
        j.label(text="{}%".format(cls._mesh.ngons_percentage))
        j.label(text="{}%".format(
            cls._mesh.tris_percentage
            + cls._mesh.quads_percentage
            + cls._mesh.ngons_percentage
        ))

    @classmethod
    def _draw_overlay_options(cls, context, layout):
        layout.label(text="Overlay Options")
        col = layout.column(align=True)
        col.prop(
            context.scene.meshstats,
            "overlay_tris",
            icon='OVERLAY',
            text="Show tris overlay"
        )
        col.prop(
            context.scene.meshstats,
            "overlay_ngons",
            icon='OVERLAY',
            text="Show ngons overlay"
        )


class BudgetPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_parent_id = "VIEW3D_PT_meshstats"

    bl_label = "Budget"
    bl_id_name = "VIEW3D_PT_meshstats_budget"

    def draw(self, context):
        self.layout.label(text="TODO")


def draw_callback(panel, color_tri, color_ngon):
    shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    shader.bind()
    bgl.glLineWidth(3)

    props = bpy.context.scene.meshstats

    if props.overlay_tris:
        shader.uniform_float("color", (color_tri.r, color_tri.g, color_tri.b, 1.0))
        for tri in panel._mesh.tris:
            batch = gpu_extras.batch.batch_for_shader(
                shader,
                'LINE_LOOP',
                {"pos": tri.to_list()}
            )
            batch.draw(shader)

    if props.overlay_ngons:
        shader.uniform_float(
            "color",
            (color_ngon.r, color_ngon.g, color_ngon.b, 1.0)
        )
        for ngon in panel._mesh.ngons:
            batch = gpu_extras.batch.batch_for_shader(
                shader,
                'LINE_LOOP',
                {"pos": ngon.to_list()}
            )
            batch.draw(shader)

    # Reset defaults
    bgl.glLineWidth(1)
