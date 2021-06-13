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
    for mod in [constants, mesh, meshstats_context]:  # noqa: F821
        importlib.reload(mod)
else:
    import bpy
    from meshstats import context as meshstats_context
    from meshstats import (constants, mesh)


class OBJECT_OT_MeshstatsDisableObject(bpy.types.Operator):
    """Enable Meshstats for object"""
    bl_idname = "object.meshstats_disable_object"
    bl_label = "Disable"

    def execute(self, context):
        obj = meshstats_context.get_object(context)
        if obj is not None:
            obj.meshstats.status = 'DISABLED'
            context.area.tag_redraw()
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class OBJECT_OT_MeshstatsEnableObject(bpy.types.Operator):
    """Enable Meshstats for object"""
    bl_idname = "object.meshstats_enable_object"
    bl_label = "Enable"

    def execute(self, context):
        obj = meshstats_context.get_object(context)
        if obj is not None:
            obj.meshstats.status = 'ENABLED'
            if mesh.check_eligibility(obj) == mesh.Eligibility.OK:
                mesh.cache.update(obj)
                context.area.tag_redraw()
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class PREFERENCES_OT_MeshstatsResetSettings(bpy.types.Operator):
    """Reset Meshstats settings"""
    bl_idname = "preferences.meshstats_reset_settings"
    bl_label = "Reset Meshstats settings"

    def execute(self, context):
        addon_prefs = \
            context.preferences.addons[constants.ADDON_NAME].preferences
        addon_prefs.disabled_by_default = constants.DISABLED_BY_DEFAULT_DEFAULT
        addon_prefs.object_face_limit = constants.OBJECT_FACE_LIMIT_DEFAULT
        addon_prefs.overlay_tris_color = constants.OVERLAY_TRIS_COLOR_DEFAULT
        addon_prefs.overlay_ngons_color = constants.OVERLAY_NGONS_COLOR_DEFAULT
        addon_prefs.overlay_n_poles_color = \
            constants.OVERLAY_N_POLES_COLOR_DEFAULT
        addon_prefs.overlay_e_poles_color = \
            constants.OVERLAY_E_POLES_COLOR_DEFAULT
        addon_prefs.overlay_star_poles_color = \
            constants.OVERLAY_STAR_POLES_COLOR_DEFAULT
        return {'FINISHED'}
