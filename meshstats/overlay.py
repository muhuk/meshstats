# <pep8-80 compliant>

import bgl
import bpy
import gpu
import gpu_extras.batch

from meshstats.mesh import cache as mesh_cache


def draw_callback(color_tri, color_ngon):
    shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
    shader.bind()
    bgl.glLineWidth(3)

    props = bpy.context.scene.meshstats

    if props.overlay_tris:
        shader.uniform_float("color", (color_tri.r, color_tri.g, color_tri.b, 1.0))
        for tri in mesh_cache.tris:
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
        for ngon in mesh_cache.ngons:
            batch = gpu_extras.batch.batch_for_shader(
                shader,
                'LINE_LOOP',
                {"pos": ngon.to_list()}
            )
            batch.draw(shader)

    # Reset defaults
    bgl.glLineWidth(1)
