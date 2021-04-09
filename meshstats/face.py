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
from typing import Iterable, List, Tuple

import mathutils


class Face(abc.ABC):
    center: mathutils.Vector
    vertices: Iterable[mathutils.Vector]
    normal: mathutils.Vector


@dataclass(frozen=True)
class FaceTri(Face):
    center: mathutils.Vector
    vertices: Tuple[
        mathutils.Vector,
        mathutils.Vector,
        mathutils.Vector
    ]
    normal: mathutils.Vector


@dataclass(frozen=True)
class FaceNgon(Face):
    center: mathutils.Vector
    vertices: List[mathutils.Vector]
    normal: mathutils.Vector
