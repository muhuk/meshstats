# <pep8-80 compliant>

import bpy


class MeshstatsProperties(bpy.types.PropertyGroup):
    overlay_tris: bpy.props.BoolProperty(
        name="overlay_tris",
        description="Display an overlay of tris.",
        default=False
    )
    overlay_ngons: bpy.props.BoolProperty(
        name="overlay_ngons",
        description="Display an overlay of ngons.",
        default=False
    )
