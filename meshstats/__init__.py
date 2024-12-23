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
    for mod in [icon, mesh, ops, overlay, props, ui]:  # noqa: F821
        importlib.reload(mod)
else:
    import bpy
    from . import (
        icon,
        mesh,
        ops,
        overlay,
        props,
        ui
    )


draw_handler = None


def register():
    global draw_handler

    icon.load_icons()

    # Register Props
    bpy.utils.register_class(props.MeshstatsAddonPreferences)
    bpy.utils.register_class(props.MeshstatsSceneProperties)
    bpy.types.Scene.meshstats = bpy.props.PointerProperty(
        type=props.MeshstatsSceneProperties
    )
    bpy.utils.register_class(props.MeshstatsObjectProperties)
    bpy.types.Object.meshstats = bpy.props.PointerProperty(
        type=props.MeshstatsObjectProperties
    )

    # Register Operations
    bpy.utils.register_class(ops.OBJECT_OT_MeshstatsDisableObject)
    bpy.utils.register_class(ops.OBJECT_OT_MeshstatsEnableObject)
    bpy.utils.register_class(ops.PREFERENCES_OT_MeshstatsResetSettings)

    # Register UI
    bpy.utils.register_class(ui.VIEW3D_PT_meshstats)
    bpy.utils.register_class(ui.VIEW3D_PT_overlay_meshstats)

    # Register Handlers
    bpy.app.handlers.load_pre.append(mesh.app__load_pre_handler)
    bpy.app.handlers.depsgraph_update_post.append(
        mesh.app__depsgraph_update_post
    )
    draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        overlay.draw_callback,
        (),
        'WINDOW',
        'POST_VIEW'
    )


def unregister():
    # Unregister Handlers
    bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
    bpy.app.handlers.load_pre.remove(mesh.app__load_pre_handler)
    bpy.app.handlers.depsgraph_update_post.remove(
        mesh.app__depsgraph_update_post
    )

    # Unregister UI
    bpy.utils.unregister_class(ui.VIEW3D_PT_overlay_meshstats)
    bpy.utils.unregister_class(ui.VIEW3D_PT_meshstats)

    # Unregister Operations
    bpy.utils.unregister_class(ops.OBJECT_OT_MeshstatsDisableObject)
    bpy.utils.unregister_class(ops.OBJECT_OT_MeshstatsEnableObject)
    bpy.utils.unregister_class(ops.PREFERENCES_OT_MeshstatsResetSettings)

    # Unregister Props
    del bpy.types.Object.meshstats
    bpy.utils.unregister_class(props.MeshstatsObjectProperties)
    del bpy.types.Scene.meshstats
    bpy.utils.unregister_class(props.MeshstatsSceneProperties)
    bpy.utils.unregister_class(props.MeshstatsAddonPreferences)

    icon.unload_icons()


if __name__ == "__main__":
    register()
