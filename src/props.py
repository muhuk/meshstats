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

from meshstats.constants import (
    ADDON_NAME,
    DEFAULT_TRIS_OUTLINE_COLOR,
    DEFAULT_NGONS_OUTLINE_COLOR,
    DEFAULT_N_POLES_COLOR,
    DEFAULT_E_POLES_COLOR,
    DEFAULT_STAR_POLES_COLOR,
)


class MeshstatsAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_NAME

    overlay_tris_color: bpy.props.FloatVectorProperty(
        name="overlay_tris_color",
        description="Color to be used to draw overlay of tris in 3D view.",
        default=DEFAULT_TRIS_OUTLINE_COLOR,
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0
    )
    overlay_ngons_color: bpy.props.FloatVectorProperty(
        name="overlay_ngons_color",
        description="Color to be used to draw overlay of ngons in 3D view.",
        default=DEFAULT_NGONS_OUTLINE_COLOR,
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0
    )
    overlay_n_poles_color: bpy.props.FloatVectorProperty(
        name="overlay_n_poles_color",
        description="Color to be used to draw overlay of N-poles in 3D view.",
        default=DEFAULT_N_POLES_COLOR,
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0
    )

    overlay_e_poles_color: bpy.props.FloatVectorProperty(
        name="overlay_e_poles_color",
        description="Color to be used to draw overlay of E-poles in 3D view.",
        default=DEFAULT_E_POLES_COLOR,
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0
    )

    overlay_star_poles_color: bpy.props.FloatVectorProperty(
        name="overlay_star_poles_color",
        description="Color to be used to draw overlay of *-poles in 3D view.",
        default=DEFAULT_STAR_POLES_COLOR,
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Overlay Preferences")
        col = layout.column(align=True)
        col.prop(self, "overlay_tris_color")
        col.prop(self, "overlay_ngons_color")
        col = layout.column(align=True)
        col.prop(self, "overlay_e_poles_color")
        col.prop(self, "overlay_n_poles_color")
        col.prop(self, "overlay_star_poles_color")
        layout.operator(MeshstatsResetSettings.bl_idname)


class MeshstatsObjectProperties(bpy.types.PropertyGroup):
    face_budget_on: bpy.props.BoolProperty(
        name="face_budget_on",
        description="Toggle face budget"
    )

    face_budget: bpy.props.IntProperty(
        name="face_budget",
        description="Budget for number of faces in this mesh.",
        default=1000,
        min=1,
        max=10_000_000,
        soft_max=10_000,
        step=1000,
        subtype='UNSIGNED'
    )

    face_budget_type: bpy.props.EnumProperty(
        name="face_budget_type",
        description="Whether to cound tris or quads",
        default='TRIS',
        items=[
            ('TRIS', "Tris", "Count triangulated faces", 1),
            ('QUADS_ONLY', "Quads Only", "Count only quads", 2),
            (
                'FACES',
                "Faces",
                "Count of any kind of faces, including ngons",
                3
            ),
        ]
    )


class MeshstatsResetSettings(bpy.types.Operator):
    """Reset Meshstats settings"""
    bl_idname = "preferences.meshstats_reset_settings"
    bl_label = "Reset Meshstats settings"

    def execute(self, context):
        addon_prefs = context.preferences.addons[ADDON_NAME].preferences
        addon_prefs.overlay_tris_color = DEFAULT_TRIS_OUTLINE_COLOR
        addon_prefs.overlay_ngons_color = DEFAULT_NGONS_OUTLINE_COLOR
        addon_prefs.overlay_e_poles_color = DEFAULT_E_POLES_COLOR
        addon_prefs.overlay_n_poles_color = DEFAULT_N_POLES_COLOR
        addon_prefs.overlay_star_poles_color = DEFAULT_STAR_POLES_COLOR
        return {'FINISHED'}


class MeshstatsSceneProperties(bpy.types.PropertyGroup):
    overlay_tris: bpy.props.BoolProperty(
        name="overlay_tris",
        description="Toggle overlay of tris.",
        default=False
    )
    overlay_ngons: bpy.props.BoolProperty(
        name="overlay_ngons",
        description="Toggle overlay of ngons.",
        default=False
    )
    overlay_n_poles: bpy.props.BoolProperty(
        name="overlay_n_poles",
        description="Toggle overlay of N-poles.",
        default=False
    )
    overlay_e_poles: bpy.props.BoolProperty(
        name="overlay_e_poles",
        description="Toggle overlay of E-poles.",
        default=False
    )
    overlay_star_poles: bpy.props.BoolProperty(
        name="overlay_star_poles",
        description="Toggle overlay of *-poles.",
        default=False
    )
