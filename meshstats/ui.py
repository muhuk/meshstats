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

if "bpy" in locals():
    import importlib
    for mod in [meshstats_context, icon, mesh]:  # noqa: F821
        importlib.reload(mod)
else:
    import bpy
    from meshstats import context as meshstats_context
    from meshstats import (icon, mesh)


class MeshstatsPanel(bpy.types.Panel):
    @staticmethod
    def _draw_overlay_options(context, layout):
        col = layout.column(align=True)
        row1 = col.row(align=True)
        row1.prop(
            context.scene.meshstats,
            "overlay_tris",
            icon_value=icon.get_icon("overlay_tris").icon_id,
            text="Tris"
        )
        row1.prop(
            context.scene.meshstats,
            "overlay_ngons",
            icon_value=icon.get_icon("overlay_ngons").icon_id,
            text="Ngons"
        )
        row2 = col.row(align=True)
        row2.prop(
            context.scene.meshstats,
            "overlay_n_poles",
            icon_value=icon.get_icon("overlay_n_poles").icon_id,
            text="N-poles"
        )
        row2.prop(
            context.scene.meshstats,
            "overlay_e_poles",
            icon_value=icon.get_icon("overlay_e_poles").icon_id,
            text="E-poles"
        )
        row2.prop(
            context.scene.meshstats,
            "overlay_star_poles",
            icon_value=icon.get_icon("overlay_star_poles").icon_id,
            text=" *-poles"
        )


class VIEW3D_PT_meshstats(MeshstatsPanel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ".objectmode"
    bl_category = "Item"

    bl_idname = "VIEW3D_PT_meshstats"
    bl_label = "Meshstats"

    def draw(self, context):
        obj = meshstats_context.get_object(context)
        if obj is None:
            self.layout.alert = True
            self.layout.label(
                text="Not a mesh."
            )
        else:
            self.layout.label(text="Active object: {}".format(obj.name))
            eligibility: mesh.Eligibility = mesh.check_eligibility(obj)
            if eligibility == mesh.Eligibility.OK:
                mesh_data = mesh.cache.get(obj)
                if mesh_data is not None:
                    self._draw_summary_table(self.layout, mesh_data)
                    self.layout.separator(factor=0.75)
                    self._draw_budget(self.layout, context, mesh_data)
                    self.layout.separator(factor=0.75)
                    self.layout.label(text="Overlays:")
                    self._draw_overlay_options(context, self.layout)
                else:
                    self.layout.alert = True
                    self.layout.label(text="Calculating...")
                    self.layout.alert = False
                self.layout.separator(factor=1.5)
                self.layout.operator("object.meshstats_disable_object", icon='QUIT')
            elif eligibility == mesh.Eligibility.TOO_MANY_FACES:
                self.layout.alert = True
                self.layout.label(text="Too many faces")
                self.layout.alert = False
                self.layout.operator("object.meshstats_disable_object", icon='QUIT')
            elif eligibility == mesh.Eligibility.DISABLED:
                self.layout.label(text="Disabled on this object.")
                self.layout.operator("object.meshstats_enable_object", icon='QUIT')

    @staticmethod
    def _draw_budget(layout, context, mesh_data):
        obj = meshstats_context.get_object(context)
        props = obj.meshstats

        layout.label(text="Budget:")
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
                mesh_data.face_budget_utilization(obj.meshstats)
            ))

    @staticmethod
    def _draw_summary_table(layout, mesh_data):
        layout.label(text="Faces:")
        box = layout.box()
        j = box.grid_flow(columns=3)
        j.label(text="")
        j.label(text="Tris")
        j.label(text="Quads")
        j.label(text="Ngons")
        j.label(text="Total")

        j.label(text="count")
        j.label(text="{}".format(mesh_data.tris_count))
        j.label(text="{}".format(mesh_data.quads_count))
        j.label(text="{}".format(mesh_data.ngons_count))
        j.label(text="{}".format(mesh_data.face_count))

        j.label(text="percentage")
        j.label(text="{}%".format(mesh_data.tris_percentage))
        j.label(text="{}%".format(mesh_data.quads_percentage))
        j.label(text="{}%".format(mesh_data.ngons_percentage))
        j.label(text="{}%".format(
            mesh_data.tris_percentage
            + mesh_data.quads_percentage
            + mesh_data.ngons_percentage
        ))

        layout.label(text="Poles:")
        box = layout.box()
        j = box.grid_flow(columns=2)
        j.label(text="N-poles")
        j.label(text="E-poles")
        j.label(text="*-poles")
        j.label(text="Total")

        j.label(text="{}".format(len(mesh_data.n_poles)))
        j.label(text="{}".format(len(mesh_data.e_poles)))
        j.label(text="{}".format(len(mesh_data.star_poles)))
        j.label(text="{}".format(mesh_data.total_poles_count))


class VIEW3D_PT_overlay_meshstats(MeshstatsPanel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_parent_id = 'VIEW3D_PT_overlay'
    bl_label = "Meshstats"

    def draw(self, context):
        self._draw_overlay_options(context, self.layout)
