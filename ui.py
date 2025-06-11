"""
User Interface panel and update functions
"""
import bpy
from bpy.types import Panel


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
        self.chaos_dt = 0.025  # Set a suitable default timestep for Arneodo
        self.chaos_a = 5.5
        self.chaos_b = 3.5
        self.chaos_c = 0.01
    elif self.chaos_attractor_type == 'RUCKLIDGE':
        self.chaos_dt = 0.07  # Set a suitable default timestep for Rucklidge
        self.chaos_a = 6.7
        self.chaos_b = 2.0


class CHAOS_PT_panel(Panel):
    bl_label = "Chaotic Attractors"
    bl_idname = "VIEW3D_PT_chaos_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Chaotic"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        # -- Top: Mode and Attractor Type --
        layout.prop(scn, "chaos_mode", text="Mode")
        layout.prop(scn, "chaos_attractor_type", text="Attractor")
        layout.separator()

        # -- Mode-Specific Options --
        if scn.chaos_mode == 'PARTICLE_ANIMATION':
            box = layout.box()
            box.label(text="Particle Animation Settings")
            box.prop(scn, "chaos_num_particles", text="Particles")
            box.prop(scn, "chaos_offset_scale", text="Offset Scale")
            box.prop(scn, "chaos_scale", text="Attractor Scale")
            # Display Optimized Mode toggle only in Particle Animation mode
            box.prop(scn, "chaos_optimized_mode", text="Optimized Mode")
            # Only show follow curve and stagger release if NOT in optimized mode
            if not scn.chaos_optimized_mode:
                box.prop(scn, "chaos_follow_curve", text="Follow Curve Heading")
                box.prop(scn, "chaos_stagger_release", text="Stagger Release")
                if scn.chaos_stagger_release:
                    box.prop(scn, "chaos_release_offset", text="Release Offset (frames)")
            box.prop(scn, "chaos_particle_shape", text="Shape")
            if scn.chaos_particle_shape == 'CUSTOM':
                box.prop(scn, "chaos_custom_particle", text="Custom Particle")
            box.prop(scn, "chaos_particle_size", text="Particle Size")
            if scn.chaos_particle_shape == 'SPHERE':
                box.prop(scn, "chaos_sphere_segments", text="Segments")
                box.prop(scn, "chaos_sphere_rings", text="Rings")
            elif scn.chaos_particle_shape == 'CUBE':
                box.prop(scn, "chaos_cube_subdiv", text="Cube Subdiv")
        elif scn.chaos_mode == 'PARTICLE_TRAIL_ANIMATION':
            box = layout.box()
            box.label(text="Particle Trail Animation Settings")
            box.prop(scn, "chaos_num_particles", text="Particles")
            box.prop(scn, "chaos_offset_scale", text="Offset Scale")
            box.prop(scn, "chaos_scale", text="Attractor Scale")
            box.label(text="Particle Settings:")
            box.prop(scn, "chaos_particle_shape", text="Particle Head")
            if scn.chaos_particle_shape == 'CUSTOM':
                box.prop(scn, "chaos_custom_particle", text="Custom Particle")
            box.prop(scn, "chaos_particle_size", text="Head Size")
            if scn.chaos_particle_shape == 'SPHERE':
                box.prop(scn, "chaos_sphere_segments", text="Segments")
                box.prop(scn, "chaos_sphere_rings", text="Rings")
            elif scn.chaos_particle_shape == 'CUBE':
                box.prop(scn, "chaos_cube_subdiv", text="Cube Subdiv")
            box.separator()
            box.label(text="Trail Line Settings:")
            box.prop(scn, "chaos_line_smooth", text="Smooth Line")
            if scn.chaos_line_smooth:
                box.prop(scn, "chaos_line_resolution", text="Line Resolution")
            box.prop(scn, "chaos_bevel_depth", text="Bevel Depth")
            box.prop(scn, "chaos_taper_trail", text="Following Trail")
            if scn.chaos_taper_trail:
                box.prop(scn, "chaos_trail_length", text="Trail Length")
        elif scn.chaos_mode == 'PARAMETER_ANIMATION':
            box = layout.box()
            box.label(text="Parameter Animation Settings")
            box.prop(scn, "chaos_animation_frames", text="Animation Frames")
            box.prop(scn, "chaos_scale", text="Attractor Scale")
            box.prop(scn, "chaos_bevel_depth", text="Bevel Depth")
        else:  # LINE_STATIC
            box = layout.box()
            box.label(text="Static Line Settings")
            box.prop(scn, "chaos_scale", text="Attractor Scale")
            box.prop(scn, "chaos_line_smooth", text="Smooth Line")
            if scn.chaos_line_smooth:
                box.prop(scn, "chaos_line_resolution", text="Line Resolution")
            box.prop(scn, "chaos_bevel_depth", text="Bevel Depth")
        layout.separator()

        # -- Global Simulation Settings --
        layout.label(text="Simulation Settings:")
        rot_row = layout.row(align=True)
        rot_row.prop(scn, "chaos_rot_x", text="Rotation X")
        rot_row.prop(scn, "chaos_rot_y", text="Rotation Y")
        rot_row.prop(scn, "chaos_rot_z", text="Rotation Z")
        layout.prop(scn, "chaos_num_frames", text="Iterations")
        layout.prop(scn, "chaos_dt", text="Timestep (dt)")
        if scn.chaos_mode in ('PARTICLE_ANIMATION', 'PARTICLE_TRAIL_ANIMATION'):
            layout.prop(scn, "chaos_anim_speed", text="Animation Speed")
        layout.separator()

        # -- Attractor Parameters --
        at = scn.chaos_attractor_type
        if scn.chaos_mode == 'PARAMETER_ANIMATION':
            if at == 'LORENZ':
                layout.label(text="Animate Lorenz Parameters:")
                layout.prop(scn, "chaos_sigma_start", text="σ Start")
                layout.prop(scn, "chaos_sigma_end", text="σ End")
                layout.prop(scn, "chaos_rho_start", text="ρ Start")
                layout.prop(scn, "chaos_rho_end", text="ρ End")
                layout.prop(scn, "chaos_beta_start", text="β Start")
                layout.prop(scn, "chaos_beta_end", text="β End")
            elif at == 'ROSSLER':
                layout.label(text="Animate Rössler Parameters:")
                layout.prop(scn, "chaos_a_start", text="a Start")
                layout.prop(scn, "chaos_a_end", text="a End")
                layout.prop(scn, "chaos_b_start", text="b Start")
                layout.prop(scn, "chaos_b_end", text="b End")
                layout.prop(scn, "chaos_c_start", text="c Start")
                layout.prop(scn, "chaos_c_end", text="c End")
            elif at == 'THOMAS':
                layout.label(text="Animate Thomas Parameter:")
                layout.prop(scn, "chaos_thomas_b_start", text="b Start")
                layout.prop(scn, "chaos_thomas_b_end", text="b End")
            elif at == 'LANGFORD':
                layout.label(text="Animate Langford Parameters:")
                layout.prop(scn, "chaos_lang_a_start", text="a Start")
                layout.prop(scn, "chaos_lang_a_end", text="a End")
                layout.prop(scn, "chaos_lang_b_start", text="b Start")
                layout.prop(scn, "chaos_lang_b_end", text="b End")
                layout.prop(scn, "chaos_lang_c_start", text="c Start")
                layout.prop(scn, "chaos_lang_c_end", text="c End")
                layout.prop(scn, "chaos_lang_d_start", text="d Start")
                layout.prop(scn, "chaos_lang_d_end", text="d End")
                layout.prop(scn, "chaos_lang_e_start", text="e Start")
                layout.prop(scn, "chaos_lang_e_end", text="e End")
                layout.prop(scn, "chaos_lang_f_start", text="f Start")
                layout.prop(scn, "chaos_lang_f_end", text="f End")
            elif at == 'DADRAS':
                layout.label(text="Animate Dadras Parameters:")
                layout.prop(scn, "chaos_dad_a_start", text="a Start")
                layout.prop(scn, "chaos_dad_a_end", text="a End")
                layout.prop(scn, "chaos_dad_b_start", text="b Start")
                layout.prop(scn, "chaos_dad_b_end", text="b End")
                layout.prop(scn, "chaos_dad_c_start", text="c Start")
                layout.prop(scn, "chaos_dad_c_end", text="c End")
                layout.prop(scn, "chaos_dad_d_start", text="d Start")
                layout.prop(scn, "chaos_dad_d_end", text="d End")
                layout.prop(scn, "chaos_dad_e_start", text="e Start")
                layout.prop(scn, "chaos_dad_e_end", text="e End")
            elif at == 'FOURWING':
                layout.label(text="Animate Four-Wing Parameters:")
                layout.prop(scn, "chaos_fw_a_start", text="a Start")
                layout.prop(scn, "chaos_fw_a_end", text="a End")
                layout.prop(scn, "chaos_fw_b_start", text="b Start")
                layout.prop(scn, "chaos_fw_b_end", text="b End")
                layout.prop(scn, "chaos_fw_c_start", text="c Start")
                layout.prop(scn, "chaos_fw_c_end", text="c End")
            elif at == 'SPROTT':
                layout.label(text="Animate Sprott Parameters:")
                layout.prop(scn, "chaos_sp_a_start", text="a Start")
                layout.prop(scn, "chaos_sp_a_end", text="a End")
                layout.prop(scn, "chaos_sp_b_start", text="b Start")
                layout.prop(scn, "chaos_sp_b_end", text="b End")
            elif at == 'HALVORSEN':
                layout.label(text="Animate Halvorsen Parameter:")
                layout.prop(scn, "chaos_halv_a_start", text="a Start")
                layout.prop(scn, "chaos_halv_a_end", text="a End")
            elif at == 'LORENZ83':
                layout.label(text="Animate Lorenz83 Parameters:")
                layout.prop(scn, "chaos_l83_a_start", text="a Start")
                layout.prop(scn, "chaos_l83_a_end", text="a End")
                layout.prop(scn, "chaos_l83_b_start", text="b Start")
                layout.prop(scn, "chaos_l83_b_end", text="b End")
                layout.prop(scn, "chaos_l83_f_start", text="f Start")
                layout.prop(scn, "chaos_l83_f_end", text="f End")
                layout.prop(scn, "chaos_l83_g_start", text="g Start")
                layout.prop(scn, "chaos_l83_g_end", text="g End")
            # New attractors (ARNEODO and RUCKLIDGE) do not have animated parameter defaults.
        else:
            if at == 'LORENZ':
                layout.prop(scn, "chaos_sigma")
                layout.prop(scn, "chaos_rho")
                layout.prop(scn, "chaos_beta")
            elif at == 'ROSSLER':
                layout.prop(scn, "chaos_a", text="a")
                layout.prop(scn, "chaos_b", text="b")
                layout.prop(scn, "chaos_c", text="c")
            elif at == 'THOMAS':
                layout.prop(scn, "chaos_thomas_b", text="b")
            elif at == 'LANGFORD':
                layout.prop(scn, "chaos_lang_a", text="a")
                layout.prop(scn, "chaos_lang_b", text="b")
                layout.prop(scn, "chaos_lang_c", text="c")
                layout.prop(scn, "chaos_lang_d", text="d")
                layout.prop(scn, "chaos_lang_e", text="e")
                layout.prop(scn, "chaos_lang_f", text="f")
            elif at == 'DADRAS':
                layout.prop(scn, "chaos_dad_a", text="a")
                layout.prop(scn, "chaos_dad_b", text="b")
                layout.prop(scn, "chaos_dad_c", text="c")
                layout.prop(scn, "chaos_dad_d", text="d")
                layout.prop(scn, "chaos_dad_e", text="e")
            elif at == 'CUSTOM':
                layout.label(text="Custom Equations:")
                layout.prop(scn, "chaos_eqn_x", text="dx/dt =")
                layout.prop(scn, "chaos_eqn_y", text="dy/dt =")
                layout.prop(scn, "chaos_eqn_z", text="dz/dt =")
                layout.label(text="Parameters (a..f):")
                row = layout.row()
                row.prop(scn, "chaos_a", text="a")
                row.prop(scn, "chaos_b", text="b")
                row.prop(scn, "chaos_c", text="c")
                row = layout.row()
                row.prop(scn, "chaos_d", text="d")
                row.prop(scn, "chaos_e", text="e")
                row.prop(scn, "chaos_f", text="f")
            elif at == 'FOURWING':
                layout.prop(scn, "chaos_fw_a", text="a")
                layout.prop(scn, "chaos_fw_b", text="b")
                layout.prop(scn, "chaos_fw_c", text="c")
            elif at == 'SPROTT':
                layout.prop(scn, "chaos_sp_a", text="a")
                layout.prop(scn, "chaos_sp_b", text="b")
            elif at == 'HALVORSEN':
                layout.prop(scn, "chaos_halv_a", text="a")
            elif at == 'LORENZ83':
                layout.prop(scn, "chaos_l83_a", text="a")
                layout.prop(scn, "chaos_l83_b", text="b")
                layout.prop(scn, "chaos_l83_f", text="f")
                layout.prop(scn, "chaos_l83_g", text="g")
            # New attractors: ARNEODO and RUCKLIDGE
            elif at in ('ARNEODO', 'RUCKLIDGE'):
                layout.label(text="Parameters:")
                layout.prop(scn, "chaos_a", text="a")
                layout.prop(scn, "chaos_b", text="b")
                if at == 'ARNEODO':
                    layout.prop(scn, "chaos_c", text="c")
        layout.separator()

        # -- Color and Material Settings --
        color_box = layout.box()
        color_box.label(text="Color Settings:")
        color_box.prop(scn, "chaos_use_color_range", text="Color Range")
        if scn.chaos_use_color_range:
            col = color_box.column(align=True)
            col.prop(scn, "chaos_color_min", text="Min Color")
            col.prop(scn, "chaos_color_max", text="Max Color")
        else:
            color_box.prop(scn, "chaos_color", text="Color")
        color_box.prop(scn, "chaos_use_emission", text="Emission")
        if scn.chaos_use_emission:
            color_box.prop(scn, "chaos_emission_strength", text="Emission Strength")
        color_box.prop(scn, "chaos_use_custom_material", text="Custom Material")
        if scn.chaos_use_custom_material:
            color_box.prop(scn, "chaos_custom_material", text="Custom Material")
        layout.separator()

        # -- Live Preview and Operators --
        layout.prop(scn, "chaos_live_preview", text="Live Preview")
        row = layout.row()
        row.operator("chaos.generate_animation", text="Generate Chaos", icon='MOD_PARTICLES')
        row = layout.row()
        row.operator("chaos.save_last", text="Save Last", icon='FILE_TICK')
        row = layout.row()
        row.operator("chaos.clear_scene", text="Clear Scene", icon='TRASH')
        row = layout.row()
        row.operator("chaos.reset_defaults", text="Reset Defaults", icon='FILE_REFRESH')
        row = layout.row()
        row.label(text=f"Last Run: {scn.chaos_last_run_time:.3f} s") 