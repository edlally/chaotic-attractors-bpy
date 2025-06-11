"""
Material creation and management utilities
"""
import bpy


def create_uniform_material(color, use_emission, emission_strength):
    """Create or update a uniform material with specified color and emission settings"""
    mat_name = "ChaoticMat_Uniform"
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
        if mat.use_nodes and mat.node_tree:
            nodes = mat.node_tree.nodes
            if "Principled BSDF" in nodes:
                nodes["Principled BSDF"].inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
            if use_emission:
                if "Emission" in nodes:
                    nodes["Emission"].inputs["Color"].default_value = (color[0], color[1], color[2], 1.0)
                    nodes["Emission"].inputs["Strength"].default_value = emission_strength
        return mat
    else:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        nt = mat.node_tree
        nodes = nt.nodes
        links = nt.links
        nodes.clear()
        out_node = nodes.new(type='ShaderNodeOutputMaterial')
        out_node.location = (400, 0)
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.name = "Principled BSDF"
        bsdf.location = (0, 0)
        bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
        if not use_emission:
            links.new(bsdf.outputs["BSDF"], out_node.inputs["Surface"])
        else:
            emission_node = nodes.new(type='ShaderNodeEmission')
            emission_node.name = "Emission"
            emission_node.location = (0, -150)
            emission_node.inputs["Color"].default_value = (color[0], color[1], color[2], 1.0)
            emission_node.inputs["Strength"].default_value = emission_strength
            add_node = nodes.new(type='ShaderNodeAddShader')
            add_node.location = (200, 0)
            links.new(bsdf.outputs["BSDF"], add_node.inputs[0])
            links.new(emission_node.outputs["Emission"], add_node.inputs[1])
            links.new(add_node.outputs["Shader"], out_node.inputs["Surface"])
        return mat 