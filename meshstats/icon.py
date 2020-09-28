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

import os
import os.path

import bpy.types
from bpy.utils import previews


ICONS_DIR = os.path.join(os.path.dirname(__file__), "icons")


icons = None


def get_icon(name: str) -> bpy.types.ImagePreview:
    if icons is not None and name in icons:
        return icons[name]
    else:
        return None


def load_icons(path: str = ICONS_DIR):
    global icons
    pcoll = previews.new()
    filenames = [f for f in os.listdir(path) if f.endswith(".png")]
    for filename in filenames:
        icon_name = filename[:-4]
        pcoll.load(icon_name, os.path.join(path, filename), 'IMAGE')
    icons = pcoll


def unload_icons():
    global icons
    previews.remove(icons)
    icons = None
