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

import abc
from dataclasses import dataclass
from typing import List

import mathutils


class Face(abc.ABC):
    @abc.abstractmethod
    def center(self) -> mathutils.Vector:
        pass

    @abc.abstractmethod
    def to_list(self) -> List[mathutils.Vector]:
        pass


@dataclass(frozen=True)
class FaceTri(Face):
    a: mathutils.Vector
    b: mathutils.Vector
    c: mathutils.Vector
    normal: mathutils.Vector

    def center(self):
        return (self.a + self.b + self.c) / 3

    def to_list(self):
        return [self.a, self.b, self.c]


@dataclass(frozen=True)
class FaceNgon(Face):
    vertices: List[mathutils.Vector]
    normal: mathutils.Vector
    _center: mathutils.Vector

    def center(self):
        return self._center

    def to_list(self):
        return self.vertices
