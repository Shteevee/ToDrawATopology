import bpy
import numpy as np

class ExportComponentImagesOperator(bpy.types.Operator):
    """"Export As PNG"""
    bl_idname = "to_draw_a_topology.export_component"
    bl_label = "Export component images"
    bl_options = {'REGISTER'}

    def execute(self, context):

        scene = bpy.context.scene
        scene.use_nodes = True
        tree = scene.node_tree

        #set export files to PNG
        scene.render.image_settings.file_format='PNG'
        scene.render.resolution_percentage = 100

        #set the views we need to be available
        scene.render.layers["RenderLayer"].use_pass_uv = True
        scene.render.layers["RenderLayer"].use_pass_normal = True
        scene.render.layers["RenderLayer"].use_pass_ambient_occlusion = True

        #set the background to be transparent
        scene.render.image_settings.color_mode = 'RGBA' 
        scene.render.alpha_mode = 'TRANSPARENT'

        #delete existing nodes
        for node in tree.nodes:
            tree.nodes.remove(node)

        render_layers_node = tree.nodes.new('CompositorNodeRLayers')
        render_layers_node.location = 0,0

        comp_node = tree.nodes.new('CompositorNodeComposite')
        comp_node.location = 400,0

        viewer_node = tree.nodes.new('CompositorNodeViewer')
        viewer_node.location = 400, -200

        links = tree.links
        comp_link = links.new(render_layers_node.outputs[0], comp_node.inputs[0])

        viewer_link = links.new(render_layers_node.outputs['Image'], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        bpy.data.images['Viewer Node'].save_render("object_out\\Original.png")

        viewer_link = links.new(render_layers_node.outputs['Normal'], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        bpy.data.images['Viewer Node'].save_render("object_out\\Normal.png")

        viewer_link = links.new(render_layers_node.outputs['UV'], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        bpy.data.images['Viewer Node'].save_render("object_out\\UV.png")

        viewer_link = links.new(render_layers_node.outputs['AO'], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        bpy.data.images['Viewer Node'].save_render("object_out\\AO.png")

        return {'FINISHED'}

    def update_display(self, scene, viewer_node):
        scene.node_tree.nodes.active = viewer_node
        scene.node_tree.update_tag()
        scene.update()
        bpy.ops.render.render()
