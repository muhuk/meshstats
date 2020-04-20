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

from itertools import (chain, repeat)
from math import degrees
from typing import List

import bgl
import bpy
import bpy.types
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy_extras.view3d_utils import region_2d_to_origin_3d
import gpu
import gpu_extras.batch
import mathutils

from meshstats import mesh
from meshstats.constants import ADDON_NAME
from meshstats.face import Face
from meshstats.pole import Pole


def draw_callback():
    mesh_cache = mesh.get_cache()
    if bpy.context.space_data.overlay.show_overlays is False \
       or mesh_cache is None:
        return
    context = bpy.context
    addon_prefs = context.preferences.addons[ADDON_NAME].preferences
    color_tris = addon_prefs.overlay_tris_color
    color_ngons = addon_prefs.overlay_ngons_color
    color_poles = addon_prefs.overlay_poles_color

    uniform_shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    smooth_shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')
    uniform_shader.bind()
    smooth_shader.bind()

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(3)
    bgl.glPointSize(8)

    props = context.scene.meshstats
    if props.overlay_tris:
        _draw_overlay_faces(
            context,
            uniform_shader,
            color_tris,
            mesh_cache.tris
        )
    if props.overlay_ngons:
        _draw_overlay_faces(
            context,
            uniform_shader,
            color_ngons,
            mesh_cache.ngons
        )
    if props.overlay_poles:
        _draw_overlay_poles(
            context,
            uniform_shader,
            smooth_shader,
            color_poles,
            mesh_cache.n_poles
        )
        _draw_overlay_poles(
            context,
            uniform_shader,
            smooth_shader,
            color_poles,
            mesh_cache.e_poles
        )
        _draw_overlay_poles(
            context,
            uniform_shader,
            smooth_shader,
            color_poles,
            mesh_cache.star_poles
        )

    # Reset defaults
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glLineWidth(1)
    bgl.glPointSize(1)


def _draw_overlay_faces(
        context: bpy.types.Context,
        shader: gpu.types.GPUShader,
        color: (float, float, float, float),
        faces: List[Face]
):
    faded_alpha = min(color[3] * 0.15 + 0.1, color[3])
    faded_color = (color[0], color[1], color[2], faded_alpha)

    for face in faces:
        if _is_visible(context, face.center, face.normal):
            shader.uniform_float("color", color)
        else:
            shader.uniform_float("color", faded_color)
        batch = gpu_extras.batch.batch_for_shader(
            shader,
            'LINE_LOOP',
            {"pos": face.vertices}
        )
        batch.draw(shader)


def _draw_overlay_poles(
        context: bpy.types.Context,
        uniform_shader: gpu.types.GPUShader,
        smooth_shader: gpu.types.GPUShader,
        color: (float, float, float, float),
        poles: List[Pole]
):
    faded_alpha = min(color[3] * 0.15 + 0.1, color[3])
    faded_color = (color[0], color[1], color[2], faded_alpha)
    zeroed_color = (color[0], color[1], color[2], faded_alpha / 10.0)

    use_color = None

    for pole in poles:
        if _is_visible(context, pole.center):
            use_color = color
        else:
            use_color = faded_color

        # Draw the center
        uniform_shader.uniform_float("color", use_color)
        batch = gpu_extras.batch.batch_for_shader(
            uniform_shader,
            'POINTS',
            {"pos": [pole.center]}
        )
        batch.draw(uniform_shader)

        # Draw spokes
        midpoints = [(pole.center + v) / 2 for v in pole.spokes]
        batch = gpu_extras.batch.batch_for_shader(
            smooth_shader,
            'LINES',
            {
                "pos": list(chain(*zip(repeat(pole.center), midpoints))),
                "color": list(
                    chain(*repeat([use_color, zeroed_color], len(pole.spokes)))
                )
            }
        )
        batch.draw(smooth_shader)


def _is_visible(
        context: bpy.types.Context,
        point: mathutils.Vector,
        normal: mathutils.Vector = None,
        epsilon: float = 0.00001
) -> bool:
    projected_vertex = location_3d_to_region_2d(
        context.region,
        context.space_data.region_3d,
        point
    )
    ray_origin = region_2d_to_origin_3d(
        context.region,
        context.space_data.region_3d,
        projected_vertex
    )
    ray = (point - ray_origin).normalized()
    if normal and degrees(ray.angle(normal)) < 90:
        return False
    (result, loc, _, _, obj, _) = context.scene.ray_cast(
        context.view_layer,
        ray_origin,
        ray
    )
    return result \
        and obj == context.active_object \
        and (point - loc).length < epsilon
