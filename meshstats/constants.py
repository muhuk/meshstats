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

ADDON_NAME = __package__

DISABLED_BY_DEFAULT_DEFAULT = True

FLAT_THRESHOLD_ANGLE_DEFAULT = 10.0  # degrees

MESHDATA_TTL = 60_000  # milliseconds

OBJECT_FACE_LIMIT_DEFAULT = 10_000
OBJECT_FACE_LIMIT_MAX = 10_000_000
OBJECT_FACE_LIMIT_MIN = 1
OBJECT_FACE_LIMIT_SOFT_MAX = 100_000
OBJECT_FACE_LIMIT_STEP = 1000

OVERLAY_TRIS_COLOR_DEFAULT = (0.0, 1.0, 0.0, 0.7)
OVERLAY_NGONS_COLOR_DEFAULT = (0.0, 1.0, 1.0, 0.7)
OVERLAY_N_POLES_COLOR_DEFAULT = (1.0, 0.334, 0.0, 0.8)
OVERLAY_E_POLES_COLOR_DEFAULT = (1.0, 0.8, 0.0, 0.8)
OVERLAY_STAR_POLES_COLOR_DEFAULT = (1.0, 0.0, 0.0, 0.8)
