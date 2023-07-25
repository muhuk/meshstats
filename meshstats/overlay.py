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
    for mod in [constants, face, mesh, meshstats_context, pole]:  # noqa: F821
        importlib.reload(mod)
else:
    # stdlib
    from itertools import (chain, repeat)
    import typing
    # blender
    import bpy
    import bpy.types
    from bpy_extras.view3d_utils import location_3d_to_region_2d
    from bpy_extras.view3d_utils import region_2d_to_origin_3d
    import gpu
    import gpu_extras.batch
    import mathutils
    # addon
    from meshstats import context as meshstats_context
    from meshstats import (constants, face, mesh, pole)


uniform_shader: typing.Optional[gpu.types.GPUShader] = None
smooth_shader: typing.Optional[gpu.types.GPUShader] = None


def draw_callback():
    global uniform_shader, smooth_shader
    if uniform_shader is None:
        uniform_shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    if smooth_shader is None:
        smooth_shader = gpu.shader.from_builtin('SMOOTH_COLOR')

    obj = meshstats_context.get_object()
    if obj is None or mesh.check_eligibility(obj) != mesh.Eligibility.OK:
        return
    transform_matrix = mathutils.Matrix(obj.matrix_world)
    context = bpy.context
    if context.space_data.overlay.show_overlays is False:
        return
    mesh_data = mesh.cache.get(context, obj)
    if mesh_data is None:
        return
    addon_prefs = context.preferences.addons[constants.ADDON_NAME].preferences
    color_tris = addon_prefs.overlay_tris_color
    color_ngons = addon_prefs.overlay_ngons_color
    color_n_poles = addon_prefs.overlay_n_poles_color
    color_e_poles = addon_prefs.overlay_e_poles_color
    color_star_poles = addon_prefs.overlay_star_poles_color

    saved_blend = gpu.state.blend_get()
    gpu.state.blend_set('ALPHA')
    gpu.state.point_size_set(8)
    saved_line_width = gpu.state.line_width_get()
    gpu.state.line_width_set(3)

    props = context.scene.meshstats
    if props.overlay_tris:
        _draw_overlay_faces(
            context,
            uniform_shader,
            color_tris,
            mesh_data.tris,
            transform_matrix,
        )
    if props.overlay_ngons:
        _draw_overlay_faces(
            context,
            uniform_shader,
            color_ngons,
            mesh_data.ngons,
            transform_matrix,
        )
    if props.overlay_n_poles:
        _draw_overlay_poles(
            context,
            uniform_shader,
            smooth_shader,
            color_n_poles,
            mesh_data.n_poles,
            transform_matrix,
        )
    if props.overlay_e_poles:
        _draw_overlay_poles(
            context,
            uniform_shader,
            smooth_shader,
            color_e_poles,
            mesh_data.e_poles,
            transform_matrix,
        )
    if props.overlay_star_poles:
        _draw_overlay_poles(
            context,
            uniform_shader,
            smooth_shader,
            color_star_poles,
            mesh_data.star_poles,
            transform_matrix,
        )

    # Reset defaults
    gpu.state.blend_set(saved_blend)
    gpu.state.point_size_set(1)
    gpu.state.line_width_set(saved_line_width)


def _draw_overlay_faces(
        context: bpy.types.Context,
        shader: gpu.types.GPUShader,
        color: typing.Tuple[float, float, float, float],
        faces: typing.List[face.Face],
        transform_matrix: mathutils.Matrix
):
    faded_alpha = 0.05  # min(color[3] * 0.15 + 0.1, color[3])
    faded_color = (color[0], color[1], color[2], faded_alpha)

    shader.bind()
    for face_ in faces:
        if _is_visible(
            context,
            transform_matrix @ face_.center,
            transform_matrix @ face_.normal
        ):
            shader.uniform_float("color", color)
        else:
            shader.uniform_float("color", faded_color)
        vertices = list(face_.vertices)
        vertices = vertices + vertices[0:1]
        batch = gpu_extras.batch.batch_for_shader(
            shader,
            'LINE_STRIP',
            {"pos": [transform_matrix @ v for v in vertices]}
        )
        batch.draw(shader)


def _draw_overlay_poles(
        context: bpy.types.Context,
        uniform_shader: gpu.types.GPUShader,
        smooth_shader: gpu.types.GPUShader,
        color: typing.Tuple[float, float, float, float],
        poles: typing.List[pole.Pole],
        transform_matrix: mathutils.Matrix
):
    faded_alpha = min(color[3] * 0.15 + 0.1, color[3])
    faded_color = (color[0], color[1], color[2], faded_alpha)
    zeroed_color = (color[0], color[1], color[2], faded_alpha / 10.0)

    use_color = None

    for pole_ in poles:
        if _is_visible(context, transform_matrix @ pole_.center):
            use_color = color
        else:
            use_color = faded_color

        # Apply world transform
        pole_center: mathutils.Vector = transform_matrix @ pole_.center
        midpoints = [(pole_.center + v) / 2 for v in pole_.spokes]
        midpoints = [transform_matrix @ v for v in midpoints]

        # Draw the center
        uniform_shader.bind()
        uniform_shader.uniform_float("color", use_color)
        batch = gpu_extras.batch.batch_for_shader(
            uniform_shader,
            'POINTS',
            {"pos": [pole_center]}
        )
        batch.draw(uniform_shader)

        # Draw spokes
        print(pole_.is_flat)
        if pole_.is_flat:
            smooth_shader.bind()
            batch = gpu_extras.batch.batch_for_shader(
                smooth_shader,
                'LINES',
                {
                    "pos": list(chain(*zip(repeat(pole_center), midpoints))),
                    "color": list(
                        chain(*repeat(
                            [use_color, zeroed_color],
                            len(pole_.spokes)
                        ))
                    )
                }
            )
            batch.draw(smooth_shader)
        else:
            batch = gpu_extras.batch.batch_for_shader(
                smooth_shader,
                'LINES',
                {
                    "pos": list(chain(*zip(repeat(pole_center), midpoints))),
                    "color": list(
                        chain(*repeat(
                            [use_color, use_color],
                            len(pole_.spokes)
                        ))
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
    (result, loc, _, _, obj, _) = context.scene.ray_cast(
        context.view_layer.depsgraph,
        ray_origin,
        ray
    )
    return result \
        and obj == context.active_object \
        and (point - loc).length < epsilon
