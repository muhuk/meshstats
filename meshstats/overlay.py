# <pep8-80 compliant>

from math import degrees
from typing import List

import bgl
import bpy
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy_extras.view3d_utils import region_2d_to_origin_3d
import gpu
import gpu_extras.batch
import mathutils

from meshstats.face import Face
from meshstats.mesh import cache as mesh_cache


shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')


def draw_callback():
    color_tri = bpy.context.preferences.themes[0].view_3d.extra_face_area
    color_ngon = bpy.context.preferences.themes[0].view_3d.extra_face_angle

    shader.bind()
    bgl.glLineWidth(3)

    props = bpy.context.scene.meshstats
    if props.overlay_tris:
        _draw_overlay_faces(
            shader,
            color_tri,
            [f for f in mesh_cache.tris if _is_visible(f)]
        )
    if props.overlay_ngons:
        _draw_overlay_faces(
            shader,
            color_ngon,
            [f for f in mesh_cache.ngons if _is_visible(f)]
        )

    # Reset defaults
    bgl.glLineWidth(1)


def _is_visible(face: Face, epsilon: float = 0.00001) -> bool:
    if face.normal.length < 0.0001:
        print("Problem face: {}".format(face))
    point = face.center()
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
    print("{} {}".format(ray.length, face.normal.length))
    if degrees(ray.angle(face.normal)) < 90:
        return False
    (result, loc, _, _, obj, _) = bpy.context.scene.ray_cast(
        bpy.context.view_layer,
        ray_origin,
        ray
    )
    return result \
        and obj == bpy.context.active_object \
        and (point - loc).length < epsilon


def _draw_overlay_faces(
        shader: gpu.types.GPUShader,
        color: mathutils.Color,
        faces: List[Face]
):
    shader.uniform_float("color", (color.r, color.g, color.b, 1.0))
    for face in faces:
        batch = gpu_extras.batch.batch_for_shader(
            shader,
            'LINE_LOOP',
            {"pos": face.to_list()}
        )
        batch.draw(shader)
