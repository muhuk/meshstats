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
    for mod in [meshstats_context, face, pole]:  # noqa: F821
        importlib.reload(mod)
else:
    # stdlib
    import copy
    import dataclasses
    from functools import reduce
    import typing
    # blender
    import bmesh
    import bpy
    import mathutils
    # addon
    from meshstats import context as meshstats_context
    from meshstats import (face, pole)


@dataclasses.dataclass(eq=False)
class Mesh:
    obj: bpy.types.Object

    tris: typing.List[face.FaceTri] = dataclasses.field(
        init=False,
        default_factory=list
    )
    ngons: typing.List[face.FaceNgon] = dataclasses.field(
        init=False,
        default_factory=list
    )
    n_poles: typing.List[pole.NPole] = dataclasses.field(
        init=False,
        default_factory=list
    )
    e_poles: typing.List[pole.EPole] = dataclasses.field(
        init=False,
        default_factory=list
    )
    star_poles: typing.List[pole.StarPole] = dataclasses.field(
        init=False,
        default_factory=list
    )

    face_count: int = dataclasses.field(init=False, default=0)
    tris_count: int = dataclasses.field(init=False, default=0)
    quads_count: int = dataclasses.field(init=False, default=0)
    ngons_count: int = dataclasses.field(init=False, default=0)
    tesellated_tris_count: int = dataclasses.field(init=False, default=0)

    tris_percentage: int = dataclasses.field(init=False, default=0)
    quads_percentage: int = dataclasses.field(init=False, default=0)
    ngons_percentage: int = dataclasses.field(init=False, default=0)

    total_poles_count: int = dataclasses.field(init=False, default=0)

    def __post_init__(self):
        self._reset()

        bm = bmesh.new()
        bm.from_mesh(self.obj.data)
        m = mathutils.Matrix(self.obj.matrix_world)
        bm.transform(m)
        m_inverted = m.inverted()

        for face_ in bm.faces:
            if len(face_.loops) == 3:
                vertices = [copy.deepcopy(l.vert.co) for l in face_.loops]
                center = (vertices[0] + vertices[1] + vertices[2]) / 3
                self.tris.append(
                    face.FaceTri(
                        center=center,
                        vertices=tuple(vertices),
                        normal=copy.deepcopy(face_.normal)
                    )
                )
                del vertices, center
            elif len(face_.loops) > 4:
                vertices = [copy.deepcopy(l.vert.co) for l in face_.loops]
                # vertices are in world coords so we need to transform center
                # to object coords first to be able to call
                # closest_point_on_mesh then convert back to world coords.
                center = reduce(lambda a, b: a + b, vertices) / len(vertices)
                center = m_inverted @ center
                center = mathutils.Vector(
                    self.obj.closest_point_on_mesh(center)[1]
                )
                center = m @ center
                self.ngons.append(
                    face.FaceNgon(
                        center=center,
                        vertices=vertices,
                        normal=copy.deepcopy(face_.normal),
                    )
                )
                del vertices, center

        for vertex in bm.verts:
            edge_count = len(
                [edge for edge in vertex.link_edges if not edge.is_boundary]
            )
            if edge_count == 3 or edge_count >= 5:
                spokes = copy.deepcopy(
                    [e.other_vert(vertex).co for e in vertex.link_edges]
                )
                if edge_count == 3:
                    self.n_poles.append(pole.NPole(
                        center=copy.deepcopy(vertex.co),
                        spokes=tuple(spokes)
                    ))
                elif edge_count == 5:
                    self.e_poles.append(pole.EPole(
                        center=copy.deepcopy(vertex.co),
                        spokes=tuple(spokes)
                    ))
                elif edge_count > 5:
                    self.star_poles.append(pole.StarPole(
                        center=copy.deepcopy(vertex.co),
                        spokes=list(spokes)
                    ))

        self._update_counts(bm)
        self._update_percentages()

        bm.free()

    @property
    def face_budget_utilization(self):
        if self.obj.meshstats.face_budget_on:
            props = self.obj.meshstats
            if props.face_budget_type == 'TRIS':
                return float(self.tesellated_tris_count) / props.face_budget
            elif props.face_budget_type == 'QUADS_ONLY':
                return float(self.quads_count) / props.face_budget
            elif props.face_budget_type == 'FACES':
                return float(self.face_count) / props.face_budget
            else:
                raise RuntimeError(
                    "Unknown face_budget_type {}".format(
                        props.face_budget_type
                    )
                )
        else:
            return None

    def _update_counts(self, bm):
        self.face_count = len(bm.faces)
        self.tris_count = len(self.tris)
        self.ngons_count = len(self.ngons)
        self.quads_count = self.face_count - self.tris_count - self.ngons_count
        self.tesellated_tris_count = len(bm.calc_loop_triangles())
        self.total_poles_count = len(self.n_poles) \
            + len(self.e_poles) \
            + len(self.star_poles)

    def _update_percentages(self):
        self.tris_percentage = int(self.tris_count * 100.0 / self.face_count)
        self.quads_percentage = int(self.quads_count * 100.0 / self.face_count)
        self.ngons_percentage = int(self.ngons_count * 100.0 / self.face_count)

        # Percentage is not zero if there is at least one face
        if self.tris_count > 0:
            self.tris_percentage = max(1, self.tris_percentage)
        if self.quads_count > 0:
            self.quads_percentage = max(1, self.quads_percentage)
        if self.ngons_count > 0:
            self.ngons_percentage = max(1, self.ngons_percentage)

        # Adjust if the sum is not 100
        while (self.tris_percentage +
               self.quads_percentage +
               self.ngons_percentage) > 100:
            if self.quads_percentage > self.tris_percentage \
                   and self.quads_percentage > self.ngons_percentage:
                self.quads_percentage -= 1
            elif self.tris_percentage > self.ngons_percentage:
                self.tris_percentage -= 1
            else:
                self.ngons_percentage -= 1
        while (self.tris_percentage +
               self.quads_percentage +
               self.ngons_percentage) < 100:
            if self.ngons_percentage < self.quads_percentage \
                   and self.ngons_percentage < self.tris_percentage \
                   and self.ngons_percentage > 0:
                self.ngons_percentage += 1
            elif self.tris_percentage < self.quads_percentage \
                    and self.tris_percentage > 0:
                self.tris_percentage += 1
            else:
                self.quads_percentage += 1

    def _reset(self):
        self.tris = []
        self.ngons = []
        self.face_count = 0
        self.tris_count = 0
        self.quads_count = 0
        self.ngons_count = 0
        self.tris_percentage = 0
        self.quads_percentage = 0
        self.ngons_percentage = 0


cache: typing.Optional[Mesh] = None


def get_cache():
    return cache


@bpy.app.handlers.persistent
def app__load_pre_handler(*args_):
    global cache
    cache = None


@bpy.app.handlers.persistent
def app__depsgraph_update_post(scene, depsgraph):
    global cache
    obj = meshstats_context.get_object()
    if obj:
        cache = Mesh(obj)
    else:
        cache = None
