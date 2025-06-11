bl_info = {
    "name": "Chaotic Attractors",
    "author": "Edward Lally",
    "version": (1, 2, 3),
    "blender": (4, 3, 0),
    "location": "3D View > Sidebar > Chaotic tab",
    "description": "Generates particle/line chaotic attractors (particle_trail_animation, particle_animation, line_static, parameter_animation) with trailing option, bevel, rotation, live preview, parameter animation and now an optimized mode for high particle counts.",
    "category": "Add Mesh",
}

import bpy
from bpy.utils import register_class, unregister_class

from . import properties, operators, ui, handlers

# Store list of classes for easy registration
_classes = [
    operators.CHAOS_OT_generate_animation,
    operators.CHAOS_OT_clear_scene,
    operators.CHAOS_OT_save_last,
    operators.CHAOS_OT_reset_defaults,
    ui.CHAOS_PT_panel,
]

def register():
    # Register scene properties first
    properties.register_properties()
    
    # Register classes
    for cls in _classes:
        try:
            register_class(cls)
        except Exception:
            pass
    
    # Register handlers
    handlers.register_handlers()

def unregister():
    # Unregister handlers first
    handlers.unregister_handlers()
    
    # Unregister classes
    for cls in reversed(_classes):
        try:
            unregister_class(cls)
        except Exception:
            pass
    
    # Unregister scene properties last
    properties.unregister_properties()

if __name__ == "__main__":
    register() 