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

from math import degrees
from typing import List

import bgl
import bpy
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy_extras.view3d_utils import region_2d_to_origin_3d
import gpu
import gpu_extras.batch
import mathutils

from meshstats import mesh
from meshstats.face import Face
from meshstats.pole import Pole


shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')


def draw_callback():
    mesh_cache = mesh.get_cache()
    if mesh_cache is None:
        return
    addon_prefs = bpy.context.preferences.addons[__package__].preferences
    color_tris = addon_prefs.overlay_tris_color
    color_ngons = addon_prefs.overlay_ngons_color
    color_poles = addon_prefs.overlay_poles_color

    shader.bind()

    bgl.glLineWidth(3)
    bgl.glEnable(bgl.GL_BLEND)

    props = bpy.context.scene.meshstats
    if props.overlay_tris:
        _draw_overlay_faces(
            shader,
            color_tris,
            mesh_cache.tris
        )
    if props.overlay_ngons:
        _draw_overlay_faces(
            shader,
            color_ngons,
            mesh_cache.ngons
        )
    if props.overlay_poles:
        _draw_overlay_poles(
            shader,
            color_poles,
            mesh_cache.poles
        )

    # Reset defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)


def _draw_overlay_faces(
        shader: gpu.types.GPUShader,
        color: (float, float, float, float),
        faces: List[Face]
):
    faded_alpha = min(color[3] * 0.15 + 0.1, color[3])
    faded_color = (color[0], color[1], color[2], faded_alpha)

    for face in faces:
        if _is_visible(face.center(), face.normal):
            shader.uniform_float("color", color)
            batch = gpu_extras.batch.batch_for_shader(
                shader,
                'LINE_LOOP',
                {"pos": face.to_list()}
            )
            batch.draw(shader)
        else:
            shader.uniform_float("color", faded_color)
            batch = gpu_extras.batch.batch_for_shader(
                shader,
                'LINE_LOOP',
                {"pos": face.to_list()}
            )
            batch.draw(shader)


def _draw_overlay_poles(
        shader: gpu.types.GPUShader,
        color: (float, float, float, float),
        poles: List[Pole]
):
    faded_alpha = min(color[3] * 0.15 + 0.1, color[3])
    faded_color = (color[0], color[1], color[2], faded_alpha)

    for pole in poles:
        if _is_visible(pole.center):
            shader.uniform_float("color", color)
            batch = gpu_extras.batch.batch_for_shader(
                shader,
                'POINTS',
                {"pos": [pole.center]}
            )
            batch.draw(shader)
        else:
            shader.uniform_float("color", faded_color)
            batch = gpu_extras.batch.batch_for_shader(
                shader,
                'POINTS',
                {"pos": [pole.center]}
            )
            batch.draw(shader)


def _is_visible(
        point: mathutils.Vector,
        normal: mathutils.Vector = None,
        epsilon: float = 0.00001
) -> bool:
    projected_vertex = location_3d_to_region_2d(
        bpy.context.region,
        bpy.context.space_data.region_3d,
        point
    )
    ray_origin = region_2d_to_origin_3d(
        bpy.context.region,
        bpy.context.space_data.region_3d,
        projected_vertex
    )
    ray = (point - ray_origin).normalized()
    if normal and degrees(ray.angle(normal)) < 90:
        return False
    (result, loc, _, _, obj, _) = bpy.context.scene.ray_cast(
        bpy.context.view_layer,
        ray_origin,
        ray
    )
    return result \
        and obj == bpy.context.active_object \
        and (point - loc).length < epsilon
