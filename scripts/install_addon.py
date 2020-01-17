import os

import bpy

MODULE = "meshstats"
ZIP_FILE = os.environ['ZIP_FILE']

if MODULE in bpy.context.preferences.addons:
    bpy.ops.preferences.addon_disable(module=MODULE)
    bpy.ops.preferences.addon_remove(module=MODULE)

bpy.ops.preferences.addon_install(filepath=ZIP_FILE)
bpy.ops.preferences.addon_enable(module=MODULE)
