# <pep8-80 compliant>

import bpy


def get_object(context=None):
    obj = None
    if context is None:
        context = bpy.context
    if context.mode == 'OBJECT' \
       and context.selected_objects \
       and context.active_object.type == 'MESH':
        obj = context.active_object
    return obj
