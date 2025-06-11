# chaotic-attractors-bpy
A free addon for Blender3D that simulates chaotic attractor motion. Releasing July 2025.

# Overview

### 1. PARTICLE_ANIMATION:
PURPOSE - Keyframed animation of particles following trajectory of the attractor. Watch as particles with slighly different offsets are sent on wildly different paths. 
 
Tech - Pre-calculates `num_frames` points via forward Euler integration, and creates keyframes at intervals determined by `anim_speed`. 

**Optimised Mode** - The best mode! Uses geometry nodes instancing with on-demand NumPy computation via frame handlers. Creates single mesh object that can be manipulated easily after generation (scale, color, move, etc...). Optimised mode can handle significantly more particles (1,000,000+) on mid-range hardware. Optimised mode can not use the `stagger_release` or `follow_curve` options (...yet, at least) and is not ideal for exporting animation data. 

Settings - num_particles, offset_scale (initial condition variance), particle shape/size/geometry (sphere/cube/custom), stagger release timing, material choice/emission, attractor scale, rotation, dt, num_frames, attractor specific parameters (e.g., sigma rho...), 


### 2. PARTICLE_TRAIL_ANIMATION
PURPOSE - Generates keyframed (non-optimised) animations with trails following the particles. These trails can be cut short and follow closely, or extend the full path of the particle.

Settings - Trail line smoothing, bevel depth, curve resolution, follow curve heading.



### 3. PARAMETER_ANIMATION
PURPOSE - Single curve object with vertices keyframed. For each timeline frame, linearly interpolates attractor parameters between start/end values, recalculates entire trajectory, updates curve vertices.

Limitation - No support for CUSTOM attractor equations

Settings - Animation frame count, parameter start/end ranges per attractor type


### 4. LINE_STATIC
PURPOSE - Generates a simple static line representing the trajectory of the attractor.

Limitations - Boring.


# Core stuff
- 12 attractors: Lorenz, Rössler, Thomas, Langford, Dadras, FourWing, Sprott, Halvorsen, Lorenz83, Arneodo, Rucklidge, Custom (eval-based)
- Integration: Forward Euler with configurable timestep dt
- **Live preview: Real-time curve update via depsgraph handlers** (this is cool).
- Materials: Uniform color, color ranges, emission, custom material override
- Transform: Post-generation rotation, scaling, 3D cursor positioning


