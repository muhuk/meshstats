# <pep8-80 compliant>

import abc
from dataclasses import dataclass
from functools import reduce
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

    def center(self):
        return reduce(lambda a, b: a + b, self.vertices) / len(self.vertices)

    def to_list(self):
        return self.vertices
