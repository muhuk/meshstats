# <pep8-80 compliant>

import time

import bpy

from meshstats.mesh import cache as mesh_cache


class MainPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    bl_idname = "VIEW3D_PT_meshstats"
    bl_label = "Meshstats"

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' \
            and context.selected_objects \
            and context.active_object.type == 'MESH'

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
        mesh_cache(obj)
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
        j.label(text="{}".format(mesh_cache.tris_count))
        j.label(text="{}".format(mesh_cache.quads_count))
        j.label(text="{}".format(mesh_cache.ngons_count))
        j.label(text="{}".format(mesh_cache.face_count))

        j.label(text="percentage")
        j.label(text="{}%".format(mesh_cache.tris_percentage))
        j.label(text="{}%".format(mesh_cache.quads_percentage))
        j.label(text="{}%".format(mesh_cache.ngons_percentage))
        j.label(text="{}%".format(
            mesh_cache.tris_percentage
            + mesh_cache.quads_percentage
            + mesh_cache.ngons_percentage
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

    bl_id_name = "VIEW3D_PT_meshstats_budget"
    bl_label = "Budget"

    def draw(self, context):
        self.layout.label(text="TODO")
