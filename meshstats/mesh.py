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

import copy
import dataclasses
import typing

import bmesh
import bpy
import mathutils

from meshstats.context import get_object
from meshstats.face import FaceTri, FaceNgon


@dataclasses.dataclass(eq=False)
class Mesh:
    obj: bpy.types.Object

    tris: typing.List[FaceTri] = dataclasses.field(
        init=False,
        default_factory=list
    )
    ngons: typing.List[FaceNgon] = dataclasses.field(
        init=False,
        default_factory=list
    )

    face_count: int = dataclasses.field(init=False, default=0)
    tris_count: int = dataclasses.field(init=False, default=0)
    quads_count: int = dataclasses.field(init=False, default=0)
    ngons_count: int = dataclasses.field(init=False, default=0)

    tris_percentage: int = dataclasses.field(init=False, default=0)
    quads_percentage: int = dataclasses.field(init=False, default=0)
    ngons_percentage: int = dataclasses.field(init=False, default=0)

    def __post_init__(self):
        self._reset()

        bm = bmesh.new()
        bm.from_mesh(self.obj.data)
        m = mathutils.Matrix(self.obj.matrix_world)
        bm.transform(m)

        for face in bm.faces:
            if len(face.loops) == 3:
                [a, b, c] = [copy.deepcopy(l.vert.co) for l in face.loops]
                self.tris.append(
                    FaceTri(a, b, c, copy.deepcopy(face.normal))
                )
                del a, b, c
            elif len(face.loops) > 4:
                self.ngons.append(
                    FaceNgon(
                        [copy.deepcopy(l.vert.co) for l in face.loops],
                        copy.deepcopy(face.normal)
                    )
                )

        self.face_count = len(bm.faces)
        self._update_counts()
        self._update_percentages()

        bm.free()

    def _update_counts(self):
        self.tris_count = len(self.tris)
        self.ngons_count = len(self.ngons)
        self.quads_count = self.face_count - self.tris_count - self.ngons_count

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
        while self.tris_percentage + self.quads_percentage + self.ngons_percentage > 100:
            if self.quads_percentage > self.tris_percentage \
                   and self.quads_percentage > self.ngons_percentage:
                self.quads_percentage -= 1
            elif self.tris_percentage > self.ngons_percentage:
                self.tris_percentage -= 1
            else:
                self.ngons_percentage -= 1
        while self.tris_percentage + self.quads_percentage + self.ngons_percentage < 100:
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
def app__load_pre_handler():
    global cache
    cache = None


@bpy.app.handlers.persistent
def app__depsgraph_update_post(scene, depsgraph):
    global cache
    if get_object():
        cache = Mesh(bpy.context.active_object)
        print("updated mesh cache to {}".format(bpy.context.active_object))
    else:
        cache = None
