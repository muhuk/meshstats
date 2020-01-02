# <pep8-80 compliant>

import dataclasses
import typing

import bmesh
import mathutils

from meshstats.face import FaceTri, FaceNgon


@dataclasses.dataclass(eq=False)
class Mesh:
    tris: typing.List[FaceTri] = dataclasses.field(
        init=False,
        default_factory=list
    )
    ngons: typing.List[FaceNgon] = dataclasses.field(
        init=False,
        default_factory=list
    )

    tris_count: int = dataclasses.field(init=False, default=0)
    quads_count: int = dataclasses.field(init=False, default=0)
    ngons_count: int = dataclasses.field(init=False, default=0)

    def __call__(self, obj):
        self._reset()

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        m = mathutils.Matrix(obj.matrix_world)

        for face in bm.faces:
            if len(face.loops) == 3:
                self.tris.append(
                    FaceTri(*[(m @ l.vert.co) for l in face.loops])
                )
            elif len(face.loops) > 4:
                self.ngons.append(
                    FaceNgon([(m @ l.vert.co) for l in face.loops])
                )
        self.tris_count = len(self.tris)
        self.ngons_count = len(self.ngons)
        self.quads_count = len(bm.faces) - self.tris_count - self.ngons_count

        bm.free()

    def _reset(self):
        self.tris = []
        self.ngons = []
        self.tris_count = 0
        self.quads_count = 0
        self.ngons_count = 0
