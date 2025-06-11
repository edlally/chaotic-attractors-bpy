"""
Frame handlers, live preview functionality, and global simulation data
"""
import bpy
import bpy.app.handlers
import mathutils
import numpy as np
from . import simulation, materials, attractors


# Global dictionary to store optimized simulation data:
# In on‑demand mode, each entry stores the initial state, current state,
# last computed frame, simulation parameters and transformation parameters.
# For precomputed simulation (non‑on‑demand), the dictionary stores the full positions array and a speed factor.
_optimized_particles_data = {}


@bpy.app.handlers.persistent
def update_live_preview(dummy):
    """Update live preview when parameters change"""
    scn = bpy.context.scene
    preview_name = "CHAOS_PREVIEW"
    if not scn.chaos_live_preview:
        preview_obj = bpy.data.objects.get(preview_name)
        if preview_obj:
            bpy.data.objects.remove(preview_obj, do_unlink=True)
        return

    if scn.chaos_mode == 'PARAMETER_ANIMATION':
        if scn.chaos_attractor_type == 'CUSTOM':
            return

        current_frame = scn.frame_current
        anim_frames = scn.chaos_animation_frames
        if current_frame < 1:
            current_frame = 1
        if current_frame > anim_frames:
            current_frame = anim_frames
        t = (current_frame - 1) / (anim_frames - 1) if anim_frames > 1 else 0
        attractor_type = scn.chaos_attractor_type
        sigma = scn.chaos_sigma
        rho   = scn.chaos_rho
        beta  = scn.chaos_beta
        a_val = scn.chaos_a
        b_val = scn.chaos_b
        c_val = scn.chaos_c
        d_val = scn.chaos_d
        e_val = scn.chaos_e
        f_val = scn.chaos_f
        eqn_x = scn.chaos_eqn_x
        eqn_y = scn.chaos_eqn_y
        eqn_z = scn.chaos_eqn_z
        thomas_b = scn.chaos_thomas_b
        lang_a = scn.chaos_lang_a
        lang_b = scn.chaos_lang_b
        lang_c = scn.chaos_lang_c
        lang_d = scn.chaos_lang_d
        lang_e = scn.chaos_lang_e
        lang_f = scn.chaos_lang_f
        dad_a = scn.chaos_dad_a
        dad_b = scn.chaos_dad_b
        dad_c = scn.chaos_dad_c
        dad_d = scn.chaos_dad_d
        dad_e = scn.chaos_dad_e
        fw_a = scn.chaos_fw_a
        fw_b = scn.chaos_fw_b
        fw_c = scn.chaos_fw_c
        sp_a = scn.chaos_sp_a
        sp_b = scn.chaos_sp_b
        halv_a = scn.chaos_halv_a
        l83_a = scn.chaos_l83_a
        l83_b = scn.chaos_l83_b
        l83_f = scn.chaos_l83_f
        l83_g = scn.chaos_l83_g

        if attractor_type == 'LORENZ':
            sigma = scn.chaos_sigma_start + t * (scn.chaos_sigma_end - scn.chaos_sigma_start)
            rho   = scn.chaos_rho_start   + t * (scn.chaos_rho_end   - scn.chaos_rho_start)
            beta  = scn.chaos_beta_start  + t * (scn.chaos_beta_end  - scn.chaos_beta_start)
        elif attractor_type == 'ROSSLER':
            a_val = scn.chaos_a_start + t * (scn.chaos_a_end - scn.chaos_a_start)
            b_val = scn.chaos_b_start + t * (scn.chaos_b_end - scn.chaos_b_start)
            c_val = scn.chaos_c_start + t * (scn.chaos_c_end - scn.chaos_c_start)
        elif attractor_type == 'THOMAS':
            thomas_b = scn.chaos_thomas_b_start + t * (scn.chaos_thomas_b_end - scn.chaos_thomas_b_start)
        elif attractor_type == 'LANGFORD':
            lang_a = scn.chaos_lang_a_start + t * (scn.chaos_lang_a_end - scn.chaos_lang_a_start)
            lang_b = scn.chaos_lang_b_start + t * (scn.chaos_lang_b_end - scn.chaos_lang_b_start)
            lang_c = scn.chaos_lang_c_start + t * (scn.chaos_lang_c_end - scn.chaos_lang_c_start)
            lang_d = scn.chaos_lang_d_start + t * (scn.chaos_lang_d_end - scn.chaos_lang_d_start)
            lang_e = scn.chaos_lang_e_start + t * (scn.chaos_lang_e_end - scn.chaos_lang_e_start)
            lang_f = scn.chaos_lang_f_start + t * (scn.chaos_lang_f_end - scn.chaos_lang_f_start)
        elif attractor_type == 'DADRAS':
            dad_a = scn.chaos_dad_a_start + t * (scn.chaos_dad_a_end - scn.chaos_dad_a_start)
            dad_b = scn.chaos_dad_b_start + t * (scn.chaos_dad_b_end - scn.chaos_dad_b_start)
            dad_c = scn.chaos_dad_c_start + t * (scn.chaos_dad_c_end - scn.chaos_dad_c_start)
            dad_d = scn.chaos_dad_d_start + t * (scn.chaos_dad_d_end - scn.chaos_dad_d_start)
            dad_e = scn.chaos_dad_e_start + t * (scn.chaos_dad_e_end - scn.chaos_dad_e_start)
        elif attractor_type == 'FOURWING':
            fw_a = scn.chaos_fw_a_start + t * (scn.chaos_fw_a_end - scn.chaos_fw_a_start)
            fw_b = scn.chaos_fw_b_start + t * (scn.chaos_fw_b_end - scn.chaos_fw_b_start)
            fw_c = scn.chaos_fw_c_start + t * (scn.chaos_fw_c_end - scn.chaos_fw_c_start)
        elif attractor_type == 'SPROTT':
            sp_a = scn.chaos_sp_a_start + t * (scn.chaos_sp_a_end - scn.chaos_sp_a_start)
            sp_b = scn.chaos_sp_b_start + t * (scn.chaos_sp_b_end - scn.chaos_sp_b_start)
        elif attractor_type == 'HALVORSEN':
            halv_a = scn.chaos_halv_a_start + t * (scn.chaos_halv_a_end - scn.chaos_halv_a_start)
        elif attractor_type == 'LORENZ83':
            l83_a = scn.chaos_l83_a_start + t * (scn.chaos_l83_a_end - scn.chaos_l83_a_start)
            l83_b = scn.chaos_l83_b_start + t * (scn.chaos_l83_b_end - scn.chaos_l83_b_start)
            l83_f = scn.chaos_l83_f_start + t * (scn.chaos_l83_f_end - scn.chaos_l83_f_start)
            l83_g = scn.chaos_l83_g_start + t * (scn.chaos_l83_g_end - scn.chaos_l83_g_start)
        # For new attractors 'ARNEODO' and 'RUCKLIDGE' (and CUSTOM) we do not animate parameters
        points = simulation.generate_points(
            attractor_type, scn.chaos_num_frames, scn.chaos_dt,
            sigma, rho, beta,
            a_val, b_val, c_val,
            scn.chaos_eqn_x, scn.chaos_eqn_y, scn.chaos_eqn_z,
            d_val, e_val, f_val,
            thomas_b,
            lang_a, lang_b, lang_c, lang_d, lang_e, lang_f,
            dad_a, dad_b, dad_c, dad_d, dad_e,
            fw_a, fw_b, fw_c,
            sp_a, sp_b,
            halv_a,
            l83_a, l83_b, l83_f, l83_g,
            x0=0.1, y0=0.11, z0=0.12
        )
    else:
        points = simulation.generate_points(
            scn.chaos_attractor_type, scn.chaos_num_frames, scn.chaos_dt,
            scn.chaos_sigma, scn.chaos_rho, scn.chaos_beta,
            scn.chaos_a, scn.chaos_b, scn.chaos_c,
            scn.chaos_eqn_x, scn.chaos_eqn_y, scn.chaos_eqn_z,
            scn.chaos_d, scn.chaos_e, scn.chaos_f,
            scn.chaos_thomas_b,
            scn.chaos_lang_a, scn.chaos_lang_b, scn.chaos_lang_c,
            scn.chaos_lang_d, scn.chaos_lang_e, scn.chaos_lang_f,
            scn.chaos_dad_a, scn.chaos_dad_b, scn.chaos_dad_c,
            scn.chaos_dad_d, scn.chaos_dad_e,
            scn.chaos_fw_a, scn.chaos_fw_b, scn.chaos_fw_c,
            scn.chaos_sp_a, scn.chaos_sp_b,
            scn.chaos_halv_a,
            scn.chaos_l83_a, scn.chaos_l83_b, scn.chaos_l83_f, scn.chaos_l83_g,
            x0=0.1, y0=0.11, z0=0.12
        )

    points = simulation.rotate_points(points, scn.chaos_rot_x, scn.chaos_rot_y, scn.chaos_rot_z)
    if scn.chaos_scale != 1.0:
        points = [(xx*scn.chaos_scale, yy*scn.chaos_scale, zz*scn.chaos_scale) for (xx, yy, zz) in points]
    origin = bpy.context.scene.cursor.location.copy()
    points = [(xx + origin[0], yy + origin[1], zz + origin[2]) for (xx, yy, zz) in points]

    preview_obj = bpy.data.objects.get(preview_name)
    if preview_obj:
        if not preview_obj.users_collection:
            bpy.context.scene.collection.objects.link(preview_obj)
        curve_data = preview_obj.data
        while curve_data.splines:
            curve_data.splines.remove(curve_data.splines[0])
    else:
        curve_data = bpy.data.curves.new(preview_name, type='CURVE')
        curve_data.dimensions = '3D'
        preview_obj = bpy.data.objects.new(preview_name, curve_data)
        bpy.context.scene.collection.objects.link(preview_obj)

    spline = curve_data.splines.new('POLY')
    spline.points.add(len(points) - 1)
    for i, (xx, yy, zz) in enumerate(points):
        spline.points[i].co = (xx, yy, zz, 1.0)

    curve_data.bevel_depth = 0.005
    curve_data.resolution_u = 2

    if scn.chaos_use_custom_material and scn.chaos_custom_material is not None:
        mat = scn.chaos_custom_material
    elif scn.chaos_use_color_range:
        color = scn.chaos_color_min
        mat = materials.create_uniform_material(color, scn.chaos_use_emission, scn.chaos_emission_strength)
    else:
        color = scn.chaos_color
        mat = materials.create_uniform_material(color, scn.chaos_use_emission, scn.chaos_emission_strength)
    if len(preview_obj.data.materials) == 0:
        preview_obj.data.materials.append(mat)
    else:
        preview_obj.data.materials[0] = mat


@bpy.app.handlers.persistent
def optimized_particles_frame_handler(scene):
    """Handle frame changes for optimized particle simulations"""
    current_frame = scene.frame_current
    for obj_name, data in _optimized_particles_data.items():
        obj = bpy.data.objects.get(obj_name)
        if obj is None or obj.type != 'MESH':
            continue

        # Check whether this simulation is on‑demand:
        if "current_state" in data:
            # On‑Demand Simulation Mode
            speed_factor = data["speed_factor"]
            # Compute target iteration based on timeline and speed factor.
            target_iter = int((current_frame - 1) * speed_factor)
            # If timeline has rewound, reset the simulation.
            if target_iter < data["last_frame"]:
                data["current_state"] = (data["initial_state"][0].copy(),
                                         data["initial_state"][1].copy(),
                                         data["initial_state"][2].copy())
                data["last_frame"] = 0
            x, y, z = data["current_state"]
            dt = data["dt"]
            # Unpack simulation parameters
            attractor_type = data["attractor_type"]
            sigma = data["sigma"]
            rho = data["rho"]
            beta = data["beta"]
            a_val = data["a_val"]
            b_val = data["b_val"]
            c_val = data["c_val"]
            thomas_b = data["thomas_b"]
            lang_a = data["lang_a"]
            lang_b = data["lang_b"]
            lang_c = data["lang_c"]
            lang_d = data["lang_d"]
            lang_e = data["lang_e"]
            lang_f = data["lang_f"]
            dad_a = data["dad_a"]
            dad_b = data["dad_b"]
            dad_c = data["dad_c"]
            dad_d = data["dad_d"]
            dad_e = data["dad_e"]
            fw_a = data["fw_a"]
            fw_b = data["fw_b"]
            fw_c = data["fw_c"]
            sp_a = data["sp_a"]
            sp_b = data["sp_b"]
            halv_a = data["halv_a"]
            l83_a = data["l83_a"]
            l83_b = data["l83_b"]
            l83_f = data["l83_f"]
            l83_g = data["l83_g"]
            eqn_x = data["eqn_x"]
            eqn_y = data["eqn_y"]
            eqn_z = data["eqn_z"]

            # Advance simulation until we reach target iteration
            while data["last_frame"] < target_iter:
                x, y, z = attractors.simulate_step_on_demand(
                    attractor_type, x, y, z, dt,
                    sigma, rho, beta,
                    a_val, b_val, c_val,
                    thomas_b,
                    lang_a, lang_b, lang_c, lang_d, lang_e, lang_f,
                    dad_a, dad_b, dad_c, dad_d, dad_e,
                    fw_a, fw_b, fw_c,
                    sp_a, sp_b,
                    halv_a,
                    l83_a, l83_b, l83_f, l83_g,
                    eqn_x, eqn_y, eqn_z,
                    data.get("d_val", 0.0), data.get("e_val", 0.0), data.get("f_val", 0.0)
                )
                data["last_frame"] += 1
            data["current_state"] = (x, y, z)
            # Form a (num_particles, 3) array of positions.
            positions = np.column_stack((x, y, z))
            # Apply stored transformation: rotation, scale, and add origin.
            rot = data["rot"]
            euler = mathutils.Euler(rot, 'XYZ')
            rot_mat = np.array(euler.to_matrix())
            positions = positions @ rot_mat.T
            positions = positions * data["scale"] + np.array(data["origin"])
        else:
            # Fallback: precomputed simulation (if any)
            positions = data["positions"][min(data["last_frame"], data["positions"].shape[0]-1)]
        mesh = obj.data
        for i, v in enumerate(mesh.vertices):
            v.co = positions[i]
        mesh.update()


def register_handlers():
    """Register frame handlers"""
    if update_live_preview not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(update_live_preview)
    if optimized_particles_frame_handler not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(optimized_particles_frame_handler)


def unregister_handlers():
    """Unregister frame handlers"""
    if update_live_preview in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(update_live_preview)
    if optimized_particles_frame_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(optimized_particles_frame_handler)


def clear_optimized_data():
    """Clear all optimized simulation data"""
    global _optimized_particles_data
    _optimized_particles_data.clear()


def store_optimized_data(obj_name, data):
    """Store optimized simulation data for an object"""
    global _optimized_particles_data
    _optimized_particles_data[obj_name] = data 