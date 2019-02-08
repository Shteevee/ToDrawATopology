import bpy
from .DrawingAPI import *
from skimage import filters, io, exposure

class ExportSvgSceneOperator(bpy.types.Operator):
    """"Export an SVG drawing of the scene"""
    bl_idname = "to_draw_a_topology.export_svg"
    bl_label = "Export Drawing of the Scene"
    bl_options = {'REGISTER'}

    def execute(self, context):

        scene = bpy.context.scene
        scene.use_nodes = True
        tree = scene.node_tree

        #set export files to PNG
        scene.render.image_settings.file_format='PNG'
        reso_percentage = scene.render.resolution_percentage

        #set the views we need to be available
        scene.render.layers["RenderLayer"].use_pass_uv = True
        scene.render.layers["RenderLayer"].use_pass_normal = True
        scene.render.layers["RenderLayer"].use_pass_ambient_occlusion = True

        #get the attributes set in the panel
        write_to_disk = scene.panel_features.memory_bool
        no_shade_bands = scene.panel_features.bands_slider+1
        width_of_bands = int(scene.panel_features.shade_dropdown)
        shading_style = scene.panel_features.shading_type_dropdown

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
        # original_scene = np.asarray(bpy.data.images['Viewer Node'].pixels)
        # original_scene = np.flip(np.reshape(original_scene, (int(scene.render.resolution_y*(scene.render.resolution_percentage/100)), int(scene.render.resolution_x*(scene.render.resolution_percentage/100)), 4)), axis=0)

        viewer_link = links.new(render_layers_node.outputs['Normal'], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        if write_to_disk:
            bpy.data.images['Viewer Node'].save_render("object_out\\Normal.png")
            normal_scene = io.imread("object_out\\Normal.png")
        else:
            normal_scene = np.asarray(bpy.data.images['Viewer Node'].pixels)
            normal_scene = np.flip(np.reshape(normal_scene, (int(scene.render.resolution_y*(reso_percentage/100)), int(scene.render.resolution_x*(reso_percentage/100)), 4)), axis=0)

        viewer_link = links.new(render_layers_node.outputs['UV'], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        if write_to_disk:
            bpy.data.images['Viewer Node'].save_render("object_out\\UV.png")
            uv_scene = io.imread("object_out\\UV.png")
        else:
            uv_scene = np.asarray(bpy.data.images['Viewer Node'].pixels)
            uv_scene = np.flip(np.reshape(uv_scene, (int(scene.render.resolution_y*(reso_percentage/100)), int(scene.render.resolution_x*(reso_percentage/100)), 4)), axis=0)

        viewer_link = links.new(render_layers_node.outputs['AO'], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        if write_to_disk:
            bpy.data.images['Viewer Node'].save_render("object_out\\AO.png")
            ao_scene = io.imread("object_out\\AO.png")
        else:
            ao_scene = np.asarray(bpy.data.images['Viewer Node'].pixels)
            ao_scene = np.flip(np.reshape(ao_scene, (int(scene.render.resolution_y*(reso_percentage/100)), int(scene.render.resolution_x*(reso_percentage/100)), 4)), axis=0)

        original_scene = io.imread("object_out\\Original.png")
        edge_scene = filters.sobel(ao_scene[:,:,0] + normal_scene[:,:,0])

        canvas = drawFeatures("object_out\\sketch.svg", edge_scene, ao_scene)
        if shading_style == 'DIAG':
            canvas = drawShadeDiagonal(canvas, original_scene, ao_scene, edge_scene, bands=no_shade_bands, interval=width_of_bands)
        elif shading_style == 'HORIZ':
            canvas = drawShadeHorizontal(canvas, original_scene, ao_scene, edge_scene, bands=no_shade_bands, interval=width_of_bands)
        elif shading_style == 'VERT':
            canvas = drawShadeVertical(canvas, original_scene, ao_scene, edge_scene, bands=no_shade_bands, interval=width_of_bands)
        elif shading_style == 'DOT':
            canvas = drawShadeDotted(canvas, original_scene, ao_scene, edge_scene, bands=no_shade_bands, interval=width_of_bands)
        # elif shading_style == 'CONT':
        #     canvas = drawShadeStream(canvas, original_scene, ao_scene, uv_scene[:,:,0], edge_scene, bands=no_shade_bands, interval=width_of_bands)
        #     canvas = drawShadeStream(canvas, original_scene, ao_scene, uv_scene[:,:,1], edge_scene, bands=no_shade_bands, interval=width_of_bands)
        canvas.save()

        return {'FINISHED'}

    def update_display(self, scene, viewer_node):
        scene.node_tree.nodes.active = viewer_node
        scene.node_tree.update_tag()
        scene.update()
        bpy.ops.render.render()
