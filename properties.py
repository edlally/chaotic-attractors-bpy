"""
Scene property definitions and update functions
"""
import bpy
from bpy.types import Scene


def update_attractor_type(self, context):
    """Update default timestep when attractor type changes"""
    if self.chaos_attractor_type == 'LORENZ':
        self.chaos_dt = 0.01
    elif self.chaos_attractor_type == 'ROSSLER':
        self.chaos_dt = 0.07
    elif self.chaos_attractor_type == 'THOMAS':
        self.chaos_dt = 0.21
    elif self.chaos_attractor_type == 'LANGFORD':
        self.chaos_dt = 0.01
    elif self.chaos_attractor_type == 'DADRAS':
        self.chaos_dt = 0.01
    elif self.chaos_attractor_type == 'FOURWING':
        self.chaos_dt = 0.088
    elif self.chaos_attractor_type == 'SPROTT':
        self.chaos_dt = 0.02
    elif self.chaos_attractor_type == 'HALVORSEN':
        self.chaos_dt = 0.01
    elif self.chaos_attractor_type == 'LORENZ83':
        self.chaos_dt = 0.01
    elif self.chaos_attractor_type == 'ARNEODO':
        self.chaos_dt = 0.025
        self.chaos_a = 5.5
        self.chaos_b = 3.5
        self.chaos_c = 0.01
    elif self.chaos_attractor_type == 'RUCKLIDGE':
        self.chaos_dt = 0.07
        self.chaos_a = 6.7
        self.chaos_b = 2.0


def register_properties():
    """Register all scene properties"""
    Scene.chaos_mode = bpy.props.EnumProperty(
        name="Mode",
        items=[
            ('PARTICLE_ANIMATION', "Particle Animation", "Multiple objects, keyframed"),
            ('LINE_STATIC', "Static Line", "Single curve, no animation"),
            ('PARTICLE_TRAIL_ANIMATION', "Particle Trail Animation", "Particles + trailing curves"),
            ('PARAMETER_ANIMATION', "Parameter Animation", "Animate attractor parameters")
        ],
        default='PARTICLE_ANIMATION'
    )

    Scene.chaos_attractor_type = bpy.props.EnumProperty(
        name="Attractor",
        items=[
            ('LORENZ', "Lorenz", ""),
            ('ROSSLER', "Rössler", ""),
            ('THOMAS', "Thomas", ""),
            ('LANGFORD', "Langford (Aizawa)", ""),
            ('DADRAS', "Dadras", ""),
            ('FOURWING', "Four-Wing", ""),
            ('SPROTT', "Sprott", ""),
            ('HALVORSEN', "Halvorsen", ""),
            ('LORENZ83', "Lorenz83", ""),
            ('CUSTOM', "Custom", ""),
            ('ARNEODO', "Arneodo", "Arneodo Attractor"),
            ('RUCKLIDGE', "Rucklidge", "Rucklidge Attractor"),
        ],
        default='LORENZ',
        update=update_attractor_type
    )

    # Simulation parameters
    Scene.chaos_num_frames = bpy.props.IntProperty(name="Frames", default=100, min=1, description="Number of iterations/frames.\nWARNING: High iterations increase simulation time.")
    Scene.chaos_dt = bpy.props.FloatProperty(name="dt", default=0.01, min=1e-6, description="Determines the time interval between sampling points.")
    Scene.chaos_anim_speed = bpy.props.FloatProperty(name="Animation Speed", default=1.0, min=0.01, description="Determines spacing between keyframes")
    Scene.chaos_num_particles = bpy.props.IntProperty(name="Particles", default=5, min=1, description="Determines the number of particles.\nWARNING:")
    Scene.chaos_offset_scale = bpy.props.FloatProperty(name="Offset", default=0.02, min=0.0)
    Scene.chaos_scale = bpy.props.FloatProperty(name="Scale", default=1.0, min=0.0)
    Scene.chaos_particle_size = bpy.props.FloatProperty(name="Particle Size", default=0.05, min=1e-6)
    
    # Attractor parameters
    Scene.chaos_sigma = bpy.props.FloatProperty(name="sigma", default=10.0)
    Scene.chaos_rho = bpy.props.FloatProperty(name="rho", default=28.0)
    Scene.chaos_beta = bpy.props.FloatProperty(name="beta", default=2.6667)
    Scene.chaos_a = bpy.props.FloatProperty(name="a", default=0.2)
    Scene.chaos_b = bpy.props.FloatProperty(name="b", default=0.2)
    Scene.chaos_c = bpy.props.FloatProperty(name="c", default=5.7)
    Scene.chaos_d = bpy.props.FloatProperty(name="d", default=0.0)
    Scene.chaos_e = bpy.props.FloatProperty(name="e", default=0.0)
    Scene.chaos_f = bpy.props.FloatProperty(name="f", default=0.0)
    
    # Custom equations
    Scene.chaos_eqn_x = bpy.props.StringProperty(name="dx/dt", default="a*(y - x)")
    Scene.chaos_eqn_y = bpy.props.StringProperty(name="dy/dt", default="x*(b - z) - y")
    Scene.chaos_eqn_z = bpy.props.StringProperty(name="dz/dt", default="x*y - c*z")
    
    # Thomas parameters
    Scene.chaos_thomas_b = bpy.props.FloatProperty(name="b", default=0.208186)
    
    # Langford parameters
    Scene.chaos_lang_a = bpy.props.FloatProperty(name="a", default=0.95)
    Scene.chaos_lang_b = bpy.props.FloatProperty(name="b", default=0.7)
    Scene.chaos_lang_c = bpy.props.FloatProperty(name="c", default=0.6)
    Scene.chaos_lang_d = bpy.props.FloatProperty(name="d", default=3.5)
    Scene.chaos_lang_e = bpy.props.FloatProperty(name="e", default=0.25)
    Scene.chaos_lang_f = bpy.props.FloatProperty(name="f", default=0.1)
    
    # Dadras parameters
    Scene.chaos_dad_a = bpy.props.FloatProperty(name="a", default=3.0)
    Scene.chaos_dad_b = bpy.props.FloatProperty(name="b", default=2.7)
    Scene.chaos_dad_c = bpy.props.FloatProperty(name="c", default=1.7)
    Scene.chaos_dad_d = bpy.props.FloatProperty(name="d", default=2.0)
    Scene.chaos_dad_e = bpy.props.FloatProperty(name="e", default=9.0)
    
    # Four-Wing parameters
    Scene.chaos_fw_a = bpy.props.FloatProperty(name="a", default=0.2)
    Scene.chaos_fw_b = bpy.props.FloatProperty(name="b", default=0.01)
    Scene.chaos_fw_c = bpy.props.FloatProperty(name="c", default=-0.4)
    
    # Sprott parameters
    Scene.chaos_sp_a = bpy.props.FloatProperty(name="a", default=2.07)
    Scene.chaos_sp_b = bpy.props.FloatProperty(name="b", default=1.79)
    
    # Halvorsen parameters
    Scene.chaos_halv_a = bpy.props.FloatProperty(name="a", default=1.89)
    
    # Lorenz83 parameters
    Scene.chaos_l83_a = bpy.props.FloatProperty(name="a", default=0.95)
    Scene.chaos_l83_b = bpy.props.FloatProperty(name="b", default=7.91)
    Scene.chaos_l83_f = bpy.props.FloatProperty(name="f", default=4.83)
    Scene.chaos_l83_g = bpy.props.FloatProperty(name="g", default=4.66)
    
    # Particle shape settings
    Scene.chaos_particle_shape = bpy.props.EnumProperty(
        name="Particle Shape",
        items=[
            ('SPHERE', "Sphere", "UV sphere per particle"),
            ('CUBE', "Cube", "Cube per particle"),
            ('CUSTOM', "Custom", "Instance a custom object")
        ],
        default='SPHERE'
    )
    Scene.chaos_sphere_segments = bpy.props.IntProperty(name="Segments", default=16, min=3)
    Scene.chaos_sphere_rings = bpy.props.IntProperty(name="Rings", default=8, min=2)
    Scene.chaos_cube_subdiv = bpy.props.IntProperty(name="Subdiv", default=0, min=0, max=4)
    
    # Line settings
    Scene.chaos_line_smooth = bpy.props.BoolProperty(name="Smooth Line", default=False)
    Scene.chaos_line_resolution = bpy.props.IntProperty(name="Line Resolution", default=12, min=1)
    
    # Color and material settings
    Scene.chaos_color = bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', size=3, default=(1, 1, 1), min=0.0, max=1.0)
    Scene.chaos_use_emission = bpy.props.BoolProperty(name="Use Emission", default=False)
    Scene.chaos_emission_strength = bpy.props.FloatProperty(name="Emission Strength", default=1.0, min=0.0)
    Scene.chaos_use_color_range = bpy.props.BoolProperty(name="Use Color Range", default=False)
    Scene.chaos_color_min = bpy.props.FloatVectorProperty(name="Min Color", subtype='COLOR', size=3, default=(0.0, 0.5, 1.0))
    Scene.chaos_color_max = bpy.props.FloatVectorProperty(name="Max Color", subtype='COLOR', size=3, default=(0.0, 1, 1))
    Scene.chaos_use_custom_material = bpy.props.BoolProperty(name="Use Custom Material", default=False)
    Scene.chaos_custom_material = bpy.props.PointerProperty(name="Custom Material", type=bpy.types.Material, description="Material to apply to all attractor objects")
    
    # Other settings
    Scene.chaos_bevel_depth = bpy.props.FloatProperty(name="Bevel Depth", description="Thickness of the generated curves", default=0.05, min=0.0)
    Scene.chaos_last_run_time = bpy.props.FloatProperty(name="Last Run Time", default=0.0, description="How long the last generation took (seconds)")
    Scene.chaos_custom_particle = bpy.props.PointerProperty(name="Custom Particle", type=bpy.types.Object, description="Object to instance as the particle")
    Scene.chaos_rot_x = bpy.props.FloatProperty(name="Rotation X", default=0.0, subtype='ANGLE')
    Scene.chaos_rot_y = bpy.props.FloatProperty(name="Rotation Y", default=0.0, subtype='ANGLE')
    Scene.chaos_rot_z = bpy.props.FloatProperty(name="Rotation Z", default=0.0, subtype='ANGLE')
    Scene.chaos_live_preview = bpy.props.BoolProperty(name="Live Preview", default=False)
    Scene.chaos_taper_trail = bpy.props.BoolProperty(name="Taper Trail", default=False, description="Limit the trail length following the particle")
    Scene.chaos_trail_length = bpy.props.FloatProperty(name="Trail Length", default=0.2, min=0.0, max=1.0, description="Fraction of the attractor points used for the trail")
    Scene.chaos_animation_frames = bpy.props.IntProperty(name="Animation Frames", default=100, min=1)
    
    # Parameter animation start/end values
    Scene.chaos_sigma_start = bpy.props.FloatProperty(name="sigma Start", default=10.0)
    Scene.chaos_sigma_end = bpy.props.FloatProperty(name="sigma End", default=10.0)
    Scene.chaos_rho_start = bpy.props.FloatProperty(name="rho Start", default=28.0)
    Scene.chaos_rho_end = bpy.props.FloatProperty(name="rho End", default=28.0)
    Scene.chaos_beta_start = bpy.props.FloatProperty(name="beta Start", default=2.6667)
    Scene.chaos_beta_end = bpy.props.FloatProperty(name="beta End", default=2.6667)
    Scene.chaos_a_start = bpy.props.FloatProperty(name="a Start", default=0.2)
    Scene.chaos_a_end = bpy.props.FloatProperty(name="a End", default=0.2)
    Scene.chaos_b_start = bpy.props.FloatProperty(name="b Start", default=0.2)
    Scene.chaos_b_end = bpy.props.FloatProperty(name="b End", default=0.2)
    Scene.chaos_c_start = bpy.props.FloatProperty(name="c Start", default=5.7)
    Scene.chaos_c_end = bpy.props.FloatProperty(name="c End", default=5.7)
    Scene.chaos_d_start = bpy.props.FloatProperty(name="d Start", default=0.0)
    Scene.chaos_d_end = bpy.props.FloatProperty(name="d End", default=0.0)
    Scene.chaos_e_start = bpy.props.FloatProperty(name="e Start", default=0.0)
    Scene.chaos_e_end = bpy.props.FloatProperty(name="e End", default=0.0)
    Scene.chaos_f_start = bpy.props.FloatProperty(name="f Start", default=0.0)
    Scene.chaos_f_end = bpy.props.FloatProperty(name="f End", default=0.0)
    Scene.chaos_thomas_b_start = bpy.props.FloatProperty(name="b Start", default=0.208186)
    Scene.chaos_thomas_b_end = bpy.props.FloatProperty(name="b End", default=0.208186)
    Scene.chaos_lang_a_start = bpy.props.FloatProperty(name="a Start", default=0.95)
    Scene.chaos_lang_a_end = bpy.props.FloatProperty(name="a End", default=0.95)
    Scene.chaos_lang_b_start = bpy.props.FloatProperty(name="b Start", default=0.7)
    Scene.chaos_lang_b_end = bpy.props.FloatProperty(name="b End", default=0.7)
    Scene.chaos_lang_c_start = bpy.props.FloatProperty(name="c Start", default=0.6)
    Scene.chaos_lang_c_end = bpy.props.FloatProperty(name="c End", default=0.6)
    Scene.chaos_lang_d_start = bpy.props.FloatProperty(name="d Start", default=3.5)
    Scene.chaos_lang_d_end = bpy.props.FloatProperty(name="d End", default=3.5)
    Scene.chaos_lang_e_start = bpy.props.FloatProperty(name="e Start", default=0.25)
    Scene.chaos_lang_e_end = bpy.props.FloatProperty(name="e End", default=0.25)
    Scene.chaos_lang_f_start = bpy.props.FloatProperty(name="f Start", default=0.1)
    Scene.chaos_lang_f_end = bpy.props.FloatProperty(name="f End", default=0.1)
    Scene.chaos_dad_a_start = bpy.props.FloatProperty(name="a Start", default=3.0)
    Scene.chaos_dad_a_end = bpy.props.FloatProperty(name="a End", default=3.0)
    Scene.chaos_dad_b_start = bpy.props.FloatProperty(name="b Start", default=2.7)
    Scene.chaos_dad_b_end = bpy.props.FloatProperty(name="b End", default=2.7)
    Scene.chaos_dad_c_start = bpy.props.FloatProperty(name="c Start", default=1.7)
    Scene.chaos_dad_c_end = bpy.props.FloatProperty(name="c End", default=1.7)
    Scene.chaos_dad_d_start = bpy.props.FloatProperty(name="d Start", default=2.0)
    Scene.chaos_dad_d_end = bpy.props.FloatProperty(name="d End", default=2.0)
    Scene.chaos_dad_e_start = bpy.props.FloatProperty(name="e Start", default=9.0)
    Scene.chaos_dad_e_end = bpy.props.FloatProperty(name="e End", default=9.0)
    Scene.chaos_fw_a_start = bpy.props.FloatProperty(name="a Start", default=0.2)
    Scene.chaos_fw_a_end = bpy.props.FloatProperty(name="a End", default=0.2)
    Scene.chaos_fw_b_start = bpy.props.FloatProperty(name="b Start", default=0.01)
    Scene.chaos_fw_b_end = bpy.props.FloatProperty(name="b End", default=0.01)
    Scene.chaos_fw_c_start = bpy.props.FloatProperty(name="c Start", default=-0.4)
    Scene.chaos_fw_c_end = bpy.props.FloatProperty(name="c End", default=-0.4)
    Scene.chaos_sp_a_start = bpy.props.FloatProperty(name="a Start", default=2.07)
    Scene.chaos_sp_a_end = bpy.props.FloatProperty(name="a End", default=2.07)
    Scene.chaos_sp_b_start = bpy.props.FloatProperty(name="b Start", default=1.79)
    Scene.chaos_sp_b_end = bpy.props.FloatProperty(name="b End", default=1.79)
    Scene.chaos_halv_a_start = bpy.props.FloatProperty(name="a Start", default=1.89)
    Scene.chaos_halv_a_end = bpy.props.FloatProperty(name="a End", default=1.89)
    Scene.chaos_l83_a_start = bpy.props.FloatProperty(name="a Start", default=0.95)
    Scene.chaos_l83_a_end = bpy.props.FloatProperty(name="a End", default=0.95)
    Scene.chaos_l83_b_start = bpy.props.FloatProperty(name="b Start", default=7.91)
    Scene.chaos_l83_b_end = bpy.props.FloatProperty(name="b End", default=7.91)
    Scene.chaos_l83_f_start = bpy.props.FloatProperty(name="f Start", default=4.83)
    Scene.chaos_l83_f_end = bpy.props.FloatProperty(name="f End", default=4.83)
    Scene.chaos_l83_g_start = bpy.props.FloatProperty(name="g Start", default=4.66)
    Scene.chaos_l83_g_end = bpy.props.FloatProperty(name="g End", default=4.66)
    
    # Animation settings
    Scene.chaos_follow_curve = bpy.props.BoolProperty(name="Follow Curve", default=False, description="Make particles follow the heading of the curve")
    Scene.chaos_stagger_release = bpy.props.BoolProperty(name="Stagger Release", default=False, description="Stagger particle release times")
    Scene.chaos_release_offset = bpy.props.IntProperty(name="Release Offset", default=0, min=0, description="Delay in frames between particle releases")
    Scene.chaos_optimized_mode = bpy.props.BoolProperty(name="Optimized Mode", default=False, description="Use optimized instancing for high particle counts (supported for selected attractors in Particle Animation mode)")


def unregister_properties():
    """Unregister all scene properties"""
    # Core properties
    del Scene.chaos_mode
    del Scene.chaos_attractor_type
    del Scene.chaos_num_frames
    del Scene.chaos_dt
    del Scene.chaos_anim_speed
    del Scene.chaos_num_particles
    del Scene.chaos_offset_scale
    del Scene.chaos_particle_size
    del Scene.chaos_scale
    
    # Attractor parameters
    del Scene.chaos_sigma
    del Scene.chaos_rho
    del Scene.chaos_beta
    del Scene.chaos_a
    del Scene.chaos_b
    del Scene.chaos_c
    del Scene.chaos_d
    del Scene.chaos_e
    del Scene.chaos_f
    
    # Custom equations
    del Scene.chaos_eqn_x
    del Scene.chaos_eqn_y
    del Scene.chaos_eqn_z
    
    # Specific attractor parameters
    del Scene.chaos_thomas_b
    del Scene.chaos_lang_a
    del Scene.chaos_lang_b
    del Scene.chaos_lang_c
    del Scene.chaos_lang_d
    del Scene.chaos_lang_e
    del Scene.chaos_lang_f
    del Scene.chaos_dad_a
    del Scene.chaos_dad_b
    del Scene.chaos_dad_c
    del Scene.chaos_dad_d
    del Scene.chaos_dad_e
    del Scene.chaos_fw_a
    del Scene.chaos_fw_b
    del Scene.chaos_fw_c
    del Scene.chaos_sp_a
    del Scene.chaos_sp_b
    del Scene.chaos_halv_a
    del Scene.chaos_l83_a
    del Scene.chaos_l83_b
    del Scene.chaos_l83_f
    del Scene.chaos_l83_g
    
    # Display properties
    del Scene.chaos_line_smooth
    del Scene.chaos_line_resolution
    del Scene.chaos_particle_shape
    del Scene.chaos_sphere_segments
    del Scene.chaos_sphere_rings
    del Scene.chaos_cube_subdiv
    del Scene.chaos_bevel_depth
    
    # Color and material properties
    del Scene.chaos_color
    del Scene.chaos_use_emission
    del Scene.chaos_emission_strength
    del Scene.chaos_use_color_range
    del Scene.chaos_color_min
    del Scene.chaos_color_max
    del Scene.chaos_use_custom_material
    del Scene.chaos_custom_material
    
    # Other properties
    del Scene.chaos_last_run_time
    del Scene.chaos_custom_particle
    del Scene.chaos_rot_x
    del Scene.chaos_rot_y
    del Scene.chaos_rot_z
    del Scene.chaos_live_preview
    del Scene.chaos_taper_trail
    del Scene.chaos_trail_length
    del Scene.chaos_animation_frames
    
    # Parameter animation properties
    del Scene.chaos_sigma_start
    del Scene.chaos_sigma_end
    del Scene.chaos_rho_start
    del Scene.chaos_rho_end
    del Scene.chaos_beta_start
    del Scene.chaos_beta_end
    del Scene.chaos_a_start
    del Scene.chaos_a_end
    del Scene.chaos_b_start
    del Scene.chaos_b_end
    del Scene.chaos_c_start
    del Scene.chaos_c_end
    del Scene.chaos_d_start
    del Scene.chaos_d_end
    del Scene.chaos_e_start
    del Scene.chaos_e_end
    del Scene.chaos_f_start
    del Scene.chaos_f_end
    del Scene.chaos_thomas_b_start
    del Scene.chaos_thomas_b_end
    del Scene.chaos_lang_a_start
    del Scene.chaos_lang_a_end
    del Scene.chaos_lang_b_start
    del Scene.chaos_lang_b_end
    del Scene.chaos_lang_c_start
    del Scene.chaos_lang_c_end
    del Scene.chaos_lang_d_start
    del Scene.chaos_lang_d_end
    del Scene.chaos_lang_e_start
    del Scene.chaos_lang_e_end
    del Scene.chaos_lang_f_start
    del Scene.chaos_lang_f_end
    del Scene.chaos_dad_a_start
    del Scene.chaos_dad_a_end
    del Scene.chaos_dad_b_start
    del Scene.chaos_dad_b_end
    del Scene.chaos_dad_c_start
    del Scene.chaos_dad_c_end
    del Scene.chaos_dad_d_start
    del Scene.chaos_dad_d_end
    del Scene.chaos_dad_e_start
    del Scene.chaos_dad_e_end
    del Scene.chaos_fw_a_start
    del Scene.chaos_fw_a_end
    del Scene.chaos_fw_b_start
    del Scene.chaos_fw_b_end
    del Scene.chaos_fw_c_start
    del Scene.chaos_fw_c_end
    del Scene.chaos_sp_a_start
    del Scene.chaos_sp_a_end
    del Scene.chaos_sp_b_start
    del Scene.chaos_sp_b_end
    del Scene.chaos_halv_a_start
    del Scene.chaos_halv_a_end
    del Scene.chaos_l83_a_start
    del Scene.chaos_l83_a_end
    del Scene.chaos_l83_b_start
    del Scene.chaos_l83_b_end
    del Scene.chaos_l83_f_start
    del Scene.chaos_l83_f_end
    del Scene.chaos_l83_g_start
    del Scene.chaos_l83_g_end
    
    # Animation properties
    del Scene.chaos_follow_curve
    del Scene.chaos_stagger_release
    del Scene.chaos_release_offset
    del Scene.chaos_optimized_mode 