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

import bpy

from meshstats.icon import (
    load_icons,
    unload_icons
)
from meshstats.mesh import (
    app__depsgraph_update_post,
    app__load_pre_handler
)
from meshstats.overlay import draw_callback
from meshstats.props import (
    MeshstatsAddonPreferences,
    MeshstatsObjectProperties,
    MeshstatsResetSettings,
    MeshstatsSceneProperties
)
from meshstats.ui import (
    VIEW3D_PT_meshstats,
    VIEW3D_PT_overlay_meshstats
)


bl_info = {
    "name": "meshstats",
    "description": "Mesh statistics.",
    "author": "Atamert Ölçgen",
    "version": (0, 4),
    "blender": (2, 82, 0),
    "location": "View3D > Meshstats panel",
    "tracker_url": "https://github.com/muhuk/meshstats",
    "support": "COMMUNITY",
    "category": "Mesh"
}


draw_handler = None


def register():
    global draw_handler

    load_icons()

    # Register Props
    bpy.utils.register_class(MeshstatsAddonPreferences)
    bpy.utils.register_class(MeshstatsSceneProperties)
    bpy.types.Scene.meshstats = bpy.props.PointerProperty(
        type=MeshstatsSceneProperties
    )
    bpy.utils.register_class(MeshstatsObjectProperties)
    bpy.types.Object.meshstats = bpy.props.PointerProperty(
        type=MeshstatsObjectProperties
    )

    # Register Operations
    bpy.utils.register_class(MeshstatsResetSettings)

    # Register UI
    bpy.utils.register_class(VIEW3D_PT_meshstats)
    bpy.utils.register_class(VIEW3D_PT_overlay_meshstats)

    # Register Handlers
    bpy.app.handlers.load_pre.append(app__load_pre_handler)
    bpy.app.handlers.depsgraph_update_post.append(app__depsgraph_update_post)
    draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        draw_callback,
        (),
        'WINDOW',
        'POST_VIEW'
    )


def unregister():
    # Unregister Handlers
    bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
    bpy.app.handlers.load_pre.remove(app__load_pre_handler)
    bpy.app.handlers.depsgraph_update_post.remove(app__depsgraph_update_post)

    # Unregister UI
    bpy.utils.unregister_class(VIEW3D_PT_overlay_meshstats)
    bpy.utils.unregister_class(VIEW3D_PT_meshstats)

    # Unregister Operations
    bpy.utils.unregister_class(MeshstatsResetSettings)

    # Unregister Props
    del bpy.types.Object.meshstats
    bpy.utils.unregister_class(MeshstatsObjectProperties)
    del bpy.types.Scene.meshstats
    bpy.utils.unregister_class(MeshstatsSceneProperties)
    bpy.utils.unregister_class(MeshstatsAddonPreferences)

    unload_icons()


if __name__ == "__main__":
    register()
