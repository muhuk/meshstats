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
    for mod in [constants, meshstats_context, face, pole, props]:  # noqa: F821
        importlib.reload(mod)
else:
    # stdlib
    import copy
    import dataclasses
    import enum
    import time
    import typing
    import itertools
    import logging
    import math
    import statistics
    # blender
    import bmesh
    import bpy
    import mathutils
    # addon
    from meshstats import constants
    from meshstats import context as meshstats_context
    from meshstats import (face, pole, props)


log = logging.getLogger(__name__)


class Eligibility(enum.Enum):
    OK = 1
    TOO_MANY_FACES = 2
    MODIFIER = 3
    DISABLED = 10


@dataclasses.dataclass(eq=False)
class Mesh:
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

    # last_updated is in milliseconds.
    last_updated: int = dataclasses.field(init=False, default=-1)

    def __post_init__(self):
        self._reset()

    def face_budget_utilization(
            self,
            obj_props: props.MeshstatsObjectProperties
    ) -> typing.Optional[float]:
        if obj_props.face_budget_on:
            if obj_props.face_budget_type == 'TRIS':
                return float(self.tesellated_tris_count) \
                    / obj_props.face_budget
            elif obj_props.face_budget_type == 'QUADS_ONLY':
                return float(self.quads_count) / obj_props.face_budget
            elif obj_props.face_budget_type == 'FACES':
                return float(self.face_count) / obj_props.face_budget
            else:
                raise RuntimeError(
                    "Unknown face_budget_type {}".format(
                        obj_props.face_budget_type
                    )
                )
        else:
            return None

    def update(
            self,
            context: bpy.types.Context,
            obj: bpy.types.Object
    ) -> None:
        bm = bmesh.new()
        # Using `from_object` instead of `from_mesh` allows overlays to be
        # displayed correctly on deformed meshes.
        bm.from_object(obj, context.evaluated_depsgraph_get())
        for m in obj.modifiers:
            print("active in viewport: {}".format(m.show_viewport))

        self._reset()

        addon_prefs = context.preferences.addons[constants.ADDON_NAME] \
                                         .preferences

        self._calculate_faces(bm)
        self._calculate_poles(bm, addon_prefs.flat_threshold_angle)

        self._calculate_counts(bm)
        self._calculate_percentages()

        bm.free()

        self.last_updated = int(time.time_ns() / 1000000)

    def _calculate_counts(self, bm: bmesh.types.BMesh) -> None:
        self.face_count = len(bm.faces)
        self.tris_count = len(self.tris)
        self.ngons_count = len(self.ngons)
        self.quads_count = self.face_count - self.tris_count - self.ngons_count
        self.tesellated_tris_count = len(bm.calc_loop_triangles())
        self.total_poles_count = len(self.n_poles) \
            + len(self.e_poles) \
            + len(self.star_poles)

    def _calculate_faces(self,
                         bm: bmesh.types.BMesh) -> None:
        for face_ in bm.faces:
            if len(face_.loops) == 3:
                vertices = [copy.deepcopy(x.vert.co) for x in face_.loops]
                center = face_.calc_center_median()
                self.tris.append(
                    face.FaceTri(
                        center=center,
                        vertices=typing.cast(typing.Tuple[mathutils.Vector,
                                                          mathutils.Vector,
                                                          mathutils.Vector],
                                             tuple(vertices)),
                        normal=copy.deepcopy(face_.normal)
                    )
                )
                del vertices, center
            elif len(face_.loops) > 4:
                vertices = [copy.deepcopy(x.vert.co) for x in face_.loops]
                center = face_.calc_center_median()
                self.ngons.append(
                    face.FaceNgon(
                        center=center,
                        vertices=vertices,
                        normal=copy.deepcopy(face_.normal),
                    )
                )
                del vertices, center

    def _calculate_percentages(self) -> None:
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
        while (self.tris_percentage
               + self.quads_percentage
               + self.ngons_percentage) > 100:
            if self.quads_percentage > self.tris_percentage \
               and self.quads_percentage > self.ngons_percentage:
                self.quads_percentage -= 1
            elif self.tris_percentage > self.ngons_percentage:
                self.tris_percentage -= 1
            else:
                self.ngons_percentage -= 1
        while (self.tris_percentage
               + self.quads_percentage
               + self.ngons_percentage) < 100:
            if self.ngons_percentage < self.quads_percentage \
               and self.ngons_percentage < self.tris_percentage \
               and self.ngons_percentage > 0:
                self.ngons_percentage += 1
            elif self.tris_percentage < self.quads_percentage \
                    and self.tris_percentage > 0:
                self.tris_percentage += 1
            else:
                self.quads_percentage += 1

    def _calculate_poles(
            self,
            bm: bmesh.types.BMesh,
            flat_threshold_angle: float
    ) -> None:
        flat_threshold: float = math.cos(math.radians(flat_threshold_angle))
        for vertex in bm.verts:
            edge_count = len(
                [edge for edge in vertex.link_edges if not edge.is_boundary]
            )
            if edge_count == 3 or edge_count >= 5:
                mean_dot_product: float = statistics.mean(map(
                    lambda normals: abs(normals[0].dot(normals[1])),
                    itertools.combinations(
                        [f.normal for f in vertex.link_faces],
                        2
                    )
                ))
                is_flat: bool = mean_dot_product > flat_threshold
                spokes = copy.deepcopy(
                    [e.other_vert(vertex).co for e in vertex.link_edges]
                )
                if edge_count == 3:
                    self.n_poles.append(pole.NPole(
                        center=copy.deepcopy(vertex.co),
                        is_flat=is_flat,
                        spokes=typing.cast(typing.Tuple[mathutils.Vector,
                                                        mathutils.Vector,
                                                        mathutils.Vector],
                                           tuple(spokes))
                    ))
                elif edge_count == 5:
                    self.e_poles.append(pole.EPole(
                        center=copy.deepcopy(vertex.co),
                        is_flat=is_flat,
                        spokes=typing.cast(typing.Tuple[mathutils.Vector,
                                                        mathutils.Vector,
                                                        mathutils.Vector,
                                                        mathutils.Vector,
                                                        mathutils.Vector],
                                           tuple(spokes))
                    ))
                elif edge_count > 5:
                    self.star_poles.append(pole.StarPole(
                        center=copy.deepcopy(vertex.co),
                        is_flat=is_flat,
                        spokes=list(spokes)
                    ))

    def _reset(self) -> None:
        self.tris = []
        self.ngons = []
        self.n_poles = []
        self.e_poles = []
        self.star_poles = []
        self.face_count = 0
        self.tris_count = 0
        self.quads_count = 0
        self.ngons_count = 0
        self.tris_percentage = 0
        self.quads_percentage = 0
        self.ngons_percentage = 0


class Cache:
    def __init__(self):
        self.d = {}

    def get(
            self,
            context: bpy.types.Context,
            obj: bpy.types.Object
    ) -> typing.Optional[Mesh]:
        self._evict_expired()
        assert obj.type == 'MESH'
        cache_key = hash(obj.data)
        if self.d.get(cache_key) is None:
            self.update(context, obj)
        return self.d.get(cache_key)

    def update(
            self,
            context: bpy.types.Context,
            obj: bpy.types.Object
    ) -> None:
        self._evict_expired()
        start = time.time_ns()
        assert obj.type == 'MESH'
        cache_key = hash(obj.data)
        cached = self.d.get(cache_key)
        if cached is None:
            cached = Mesh()
            self.d[cache_key] = cached
        cached.update(context, obj)
        time_taken = int((time.time_ns() - start) / 1_000_000)
        log.info(
            "Updated meshstats data for '{0}' in {1}ms.".format(
                obj.data.name,
                time_taken
            )
        )

    def _evict_expired(self):
        now = int(time.time_ns() / 1_000_000)
        expired_set = set()
        for (cache_key, m) in self.d.items():
            if m.last_updated + constants.MESHDATA_TTL < now:
                expired_set.add(cache_key)
        for k in expired_set:
            log.debug("Evicting {} from cache".format(cache_key))
            del self.d[k]
        del expired_set
        log.debug("{} items in cache.".format(len(self.d)))


cache = Cache()


def check_eligibility(obj: bpy.types.Object) -> Eligibility:
    assert obj.type == 'MESH'
    obj_props = obj.meshstats
    addon_prefs = \
        bpy.context.preferences.addons[constants.ADDON_NAME].preferences
    if obj_props.status == 'DISABLED':
        return Eligibility.DISABLED
    elif len(obj.data.polygons) > addon_prefs.object_face_limit:
        log.debug("Mesh '{}' has too many faces.".format(obj.data.name))
        return Eligibility.TOO_MANY_FACES
    elif any([m for m in obj.modifiers if m.show_viewport]):
        return Eligibility.MODIFIER
    else:
        return Eligibility.OK


@bpy.app.handlers.persistent
def app__load_pre_handler(*args_):
    global cache
    cache = Cache()


@bpy.app.handlers.persistent
def app__depsgraph_update_post(
        scene: bpy.types.Scene,
        depsgraph: bpy.types.Depsgraph
) -> None:
    global cache
    context: bpy.types.Context = bpy.context
    obj = meshstats_context.get_object(context)
    if obj is not None:
        for u in depsgraph.updates:
            if u.id.original == obj \
               and u.is_updated_geometry \
               and check_eligibility(obj) == Eligibility.OK:
                cache.update(context, obj)
                break
