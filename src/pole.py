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


class Pole(abc.ABC):
    pass


@dataclass(frozen=True)
class EPole(Pole):
    center: mathutils.Vector
    spokes: (
        mathutils.Vector,
        mathutils.Vector,
        mathutils.Vector,
        mathutils.Vector,
        mathutils.Vector
    )


@dataclass(frozen=True)
class NPole(Pole):
    center: mathutils.Vector
    spokes: (
        mathutils.Vector,
        mathutils.Vector,
        mathutils.Vector
    )


@dataclass(frozen=True)
class StarPole(Pole):
    center: mathutils.Vector
    spokes: List[mathutils.Vector]
