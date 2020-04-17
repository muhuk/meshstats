# <pep8-80 compliant>

# meshstats is a Blender addon that provides mesh statistics.
# Copyright (C) 2020  Atamert Ölçgen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bpy

from meshstats import mesh
from meshstats.constants import ADDON_NAME
from meshstats.context import get_object


class MainPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ".objectmode"
    bl_category = "Item"

    bl_idname = "VIEW3D_PT_meshstats"
    bl_label = "Meshstats"

    def draw(self, context):
        self.layout.template_ID(
            context.view_layer.objects,
            "active",
            filter='AVAILABLE'
        )
        if get_object(context) is None:
            self.layout.label(
                text="Mesh statistics is only available for meshes."
            )
        else:
            if mesh.get_cache() is not None:
                self._draw_summary_table(self.layout.box())
                self._draw_budget(context, self.layout.box())
                self._draw_overlay_options(context, self.layout.box())
            else:
                self.layout.alert = True
                self.layout.label(text="Calculating...")
                self.layout.alert = False

    @staticmethod
    def _draw_budget(context, layout):
        obj = get_object(context)
        props = obj.meshstats
        mesh_cache = mesh.get_cache()

        layout.label(text="Budget")
        col = layout.column(align=True)
        col.prop(
            props,
            "face_budget_on",
            icon='FACESEL',
            text="Face Budget"
        )
        if props.face_budget_on:
            row = col.row(align=True)
            row.prop(props, "face_budget", text="Budget")
            row.prop(props, "face_budget_type", text="")
            col.label(text="Utilization is {:.2%}.".format(
                mesh_cache.face_budget_utilization
            ))

    @staticmethod
    def _draw_summary_table(layout):
        mesh_cache = mesh.get_cache()
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

    @staticmethod
    def _draw_overlay_options(context, layout):
        addon_prefs = context.preferences.addons[ADDON_NAME].preferences

        layout.label(text="Overlay Options")
        col1 = layout.column(align=True)
        col1.prop(
            context.scene.meshstats,
            "overlay_tris",
            icon='OVERLAY',
            text="Overlay tris"
        )
        if context.scene.meshstats.overlay_tris:
            col1.prop(
                addon_prefs,
                "overlay_tris_color",
                text=""
            )

        col2 = layout.column(align=True)
        col2.prop(
            context.scene.meshstats,
            "overlay_ngons",
            icon='OVERLAY',
            text="Overlay ngons"
        )
        if context.scene.meshstats.overlay_ngons:
            col2.prop(
                addon_prefs,
                "overlay_ngons_color",
                text=""
            )

        col3 = layout.column(align=True)
        col3.prop(
            context.scene.meshstats,
            "overlay_poles",
            icon='OVERLAY',
            text="Overlay poles"
        )
        if context.scene.meshstats.overlay_poles:
            col3.prop(
                addon_prefs,
                "overlay_poles_color",
                text=""
            )
