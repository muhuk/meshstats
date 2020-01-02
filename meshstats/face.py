# <pep8-80 compliant>

from dataclasses import dataclass
from typing import List

import mathutils


@dataclass(frozen=True)
class FaceTri:
    a: mathutils.Vector
    b: mathutils.Vector
    c: mathutils.Vector

    def to_list(self):
        return [self.a, self.b, self.c]


@dataclass(frozen=True)
class FaceNgon:
    vertices: List[mathutils.Vector]

    def to_list(self):
        return self.vertices
