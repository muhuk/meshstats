# <pep8-80 compliant>

from dataclasses import dataclass

import mathutils


@dataclass
class FaceTri:
    a: mathutils.Vector
    b: mathutils.Vector
    c: mathutils.Vector

    def to_list(self):
        return [self.a, self.b, self.c]


class FaceNgon:
    pass
