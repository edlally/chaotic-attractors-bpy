"""
Chaotic attractor equation definitions
"""
import math
import numpy as np


def step_lorenz(x, y, z, dt, sigma, rho, beta):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_rossler(x, y, z, dt, a, b, c):
    dx = -y - z
    dy = x + a*y
    dz = b + z*(x - c)
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_thomas(x, y, z, dt, bval):
    dx = math.sin(y) - bval*x
    dy = math.sin(z) - bval*y
    dz = math.sin(x) - bval*z
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_langford(x, y, z, dt, a, b, c, d, ee, f):
    dx = (z - b)*x - d*y
    dy = d*x + (z - b)*y
    dz = c + a*z - (z**3)/3 - (x**2 + y**2)*(1 + ee*z) + f*z*(x**3)
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_dadras(x, y, z, dt, a, b, c, d, e):
    dx = y - a*x + b*y*z
    dy = c*y - x*z + z
    dz = d*x*y - e*z
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_custom(x, y, z, dt, eqn_x, eqn_y, eqn_z, a, b, c, d, e, f):
    local_vars = {'x': x, 'y': y, 'z': z,
                  'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f,
                  'math': math}
    dx = eval(eqn_x, {"__builtins__": {}}, local_vars)
    dy = eval(eqn_y, {"__builtins__": {}}, local_vars)
    dz = eval(eqn_z, {"__builtins__": {}}, local_vars)
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_fourwing(x, y, z, dt, a, b, c):
    dx = a*x + y*z
    dy = b*x + c*y - x*z
    dz = -z - x*y
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_sprott(x, y, z, dt, a, b):
    dx = y + a*x*y + x*z
    dy = 1 - b*(x**2) + y*z
    dz = x - (x**2) - (y**2)
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_halvorsen(x, y, z, dt, a):
    dx = -a*x - 4*y - 4*z - (y**2)
    dy = -a*y - 4*z - 4*x - (z**2)
    dz = -a*z - 4*x - 4*y - (x**2)
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_lorenz83(x, y, z, dt, a, b, ff, g):
    dx = -a*x - (y**2) - (z**2) + a*ff
    dy = -y + x*y - b*x*z + g
    dz = -z + b*x*y + x*z
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_arneodo(x, y, z, dt, a, b, c):
    dx = y
    dy = z
    dz = a * x - b * y - z - c * x**3
    return (x + dx*dt, y + dy*dt, z + dz*dt)

def step_rucklidge(x, y, z, dt, A, B):
    dx = -B * x + A * y - y * z
    dy = x
    dz = y**2 - z
    return (x + dx*dt, y + dy*dt, z + dz*dt)


# Optimized simulation step function for on-demand computation
def simulate_step_on_demand(attractor_type, x, y, z, dt,
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
                           d_val=0.0, e_val=0.0, f_val=0.0):
    if attractor_type == 'LORENZ':
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
    elif attractor_type == 'ROSSLER':
        dx = -y - z
        dy = x + a_val * y
        dz = b_val + z * (x - c_val)
    elif attractor_type == 'THOMAS':
        dx = np.sin(y) - thomas_b * x
        dy = np.sin(z) - thomas_b * y
        dz = np.sin(x) - thomas_b * z
    elif attractor_type == 'LANGFORD':
        dx = (z - lang_b) * x - lang_d * y
        dy = lang_d * x + (z - lang_b) * y
        dz = lang_c + lang_a * z - (z**3)/3 - (x**2 + y**2)*(1 + lang_e*z) + lang_f*z*(x**3)
    elif attractor_type == 'DADRAS':
        dx = y - dad_a * x + dad_b * y * z
        dy = dad_c * y - x * z + z
        dz = dad_d * x * y - dad_e * z
    elif attractor_type == 'FOURWING':
        dx = fw_a * x + y * z
        dy = fw_b * x + fw_c * y - x * z
        dz = -z - x * y
    elif attractor_type == 'SPROTT':
        dx = y + sp_a * x * y + x * z
        dy = 1 - sp_b * (x**2) + y * z
        dz = x - (x**2) - (y**2)
    elif attractor_type == 'HALVORSEN':
        dx = -halv_a * x - 4 * y - 4 * z - (y**2)
        dy = -halv_a * y - 4 * z - 4 * x - (z**2)
        dz = -halv_a * z - 4 * x - 4 * y - (x**2)
    elif attractor_type == 'LORENZ83':
        dx = -l83_a * x - (y**2) - (z**2) + l83_a * l83_f
        dy = -y + x * y - l83_b * x * z + l83_g
        dz = -z + l83_b * x * y + x * z
    elif attractor_type == 'ARNEODO':
        dx = y
        dy = z
        dz = a_val * x - b_val * y - z - c_val * (x**3)
    elif attractor_type == 'RUCKLIDGE':
        dx = -b_val * x + a_val * y - y * z
        dy = x
        dz = y**2 - z
    elif attractor_type == 'CUSTOM':
        # Properly use the custom equations for optimized mode
        import math
        local_vars = {'x': x, 'y': y, 'z': z,
                       'a': a_val, 'b': b_val, 'c': c_val, 
                       'd': d_val, 'e': e_val, 'f': f_val,
                       'math': math, 'np': np}
        try:
            dx = eval(eqn_x, {"__builtins__": {}}, local_vars)
            dy = eval(eqn_y, {"__builtins__": {}}, local_vars)
            dz = eval(eqn_z, {"__builtins__": {}}, local_vars)
        except Exception:
            # If there's an error in the custom equation, fall back to Lorenz
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
    else:
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z

    x_new = x + dx * dt
    y_new = y + dy * dt
    z_new = z + dz * dt
    return x_new, y_new, z_new


def initialize_on_demand_simulation(attractor_type, num_particles, dt,
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
                           d_val, e_val, f_val,
                           offset_scale, origin, scale, rot_x, rot_y, rot_z,
                           speed_factor):
    """Initialize on-demand simulation state"""
    # Set up initial conditions with random offset
    x0 = np.random.uniform(0.1 - offset_scale, 0.1 + offset_scale, size=num_particles).astype(np.float32)
    y0 = np.random.uniform(0.11 - offset_scale, 0.11 + offset_scale, size=num_particles).astype(np.float32)
    z0 = np.random.uniform(0.12 - offset_scale, 0.12 + offset_scale, size=num_particles).astype(np.float32)
    
    # Pack simulation and transformation parameters in a dictionary
    state_dict = {
         "initial_state": (x0, y0, z0),
         "current_state": (x0.copy(), y0.copy(), z0.copy()),
         "last_frame": 0,
         "dt": dt,
         "attractor_type": attractor_type,
         "sigma": sigma, "rho": rho, "beta": beta,
         "a_val": a_val, "b_val": b_val, "c_val": c_val,
         "d_val": d_val, "e_val": e_val, "f_val": f_val,
         "thomas_b": thomas_b,
         "lang_a": lang_a, "lang_b": lang_b, "lang_c": lang_c, "lang_d": lang_d, "lang_e": lang_e, "lang_f": lang_f,
         "dad_a": dad_a, "dad_b": dad_b, "dad_c": dad_c, "dad_d": dad_d, "dad_e": dad_e,
         "fw_a": fw_a, "fw_b": fw_b, "fw_c": fw_c,
         "sp_a": sp_a, "sp_b": sp_b,
         "halv_a": halv_a,
         "l83_a": l83_a, "l83_b": l83_b, "l83_f": l83_f, "l83_g": l83_g,
         "eqn_x": eqn_x, "eqn_y": eqn_y, "eqn_z": eqn_z,
         "origin": origin,
         "scale": scale,
         "rot": (rot_x, rot_y, rot_z),
         "speed_factor": speed_factor,
    }
    return state_dict 