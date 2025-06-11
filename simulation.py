"""
Simulation and point generation utilities
"""
import random
import mathutils
import numpy as np
from . import attractors


def rotate_points(points, rx, ry, rz):
    """Rotate a list of points around their centroid"""
    if rx == 0 and ry == 0 and rz == 0:
        return points
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    cz = sum(p[2] for p in points) / len(points)
    centroid = mathutils.Vector((cx, cy, cz))
    euler = mathutils.Euler((rx, ry, rz), 'XYZ')
    rotated = []
    for p in points:
        vec = mathutils.Vector(p)
        vec -= centroid
        vec = euler.to_matrix() @ vec
        vec += centroid
        rotated.append((vec.x, vec.y, vec.z))
    return rotated


def generate_points(attractor_type, iterations, dt,
                    sigma, rho, beta, 
                    a_val, b_val, c_val, 
                    eqn_x, eqn_y, eqn_z,
                    d_val, e_val, f_val,
                    thomas_b,
                    lang_a, lang_b, lang_c, lang_d, lang_e, lang_f,
                    dad_a, dad_b, dad_c, dad_d, dad_e,
                    fw_a, fw_b, fw_c,
                    sp_a, sp_b,
                    halv_a,
                    l83_a, l83_b, l83_f, l83_g,
                    x0=0.1, y0=0.1, z0=0.1):
    """Generate points for a chaotic attractor"""
    x, y, z = x0, y0, z0
    points = [None] * iterations
    
    # Select the appropriate step function
    if attractor_type == 'LORENZ':
        step = lambda x, y, z: attractors.step_lorenz(x, y, z, dt, sigma, rho, beta)
    elif attractor_type == 'ROSSLER':
        step = lambda x, y, z: attractors.step_rossler(x, y, z, dt, a_val, b_val, c_val)
    elif attractor_type == 'THOMAS':
        step = lambda x, y, z: attractors.step_thomas(x, y, z, dt, thomas_b)
    elif attractor_type == 'LANGFORD':
        step = lambda x, y, z: attractors.step_langford(x, y, z, dt, lang_a, lang_b, lang_c, lang_d, lang_e, lang_f)
    elif attractor_type == 'DADRAS':
        step = lambda x, y, z: attractors.step_dadras(x, y, z, dt, dad_a, dad_b, dad_c, dad_d, dad_e)
    elif attractor_type == 'CUSTOM':
        step = lambda x, y, z: attractors.step_custom(x, y, z, dt, eqn_x, eqn_y, eqn_z, a_val, b_val, c_val, d_val, e_val, f_val)
    elif attractor_type == 'FOURWING':
        step = lambda x, y, z: attractors.step_fourwing(x, y, z, dt, fw_a, fw_b, fw_c)
    elif attractor_type == 'SPROTT':
        step = lambda x, y, z: attractors.step_sprott(x, y, z, dt, sp_a, sp_b)
    elif attractor_type == 'HALVORSEN':
        step = lambda x, y, z: attractors.step_halvorsen(x, y, z, dt, halv_a)
    elif attractor_type == 'LORENZ83':
        step = lambda x, y, z: attractors.step_lorenz83(x, y, z, dt, l83_a, l83_b, l83_f, l83_g)
    elif attractor_type == 'ARNEODO':
        step = lambda x, y, z: attractors.step_arneodo(x, y, z, dt, a_val, b_val, c_val)
    elif attractor_type == 'RUCKLIDGE':
        step = lambda x, y, z: attractors.step_rucklidge(x, y, z, dt, a_val, b_val)
    else:
        return []
    
    # Generate points
    for i in range(iterations):
        points[i] = (x, y, z)
        try:
            x, y, z = step(x, y, z)
        except OverflowError:
            continue
    return points


