import bpy
from drawing_a_topology.drawing.drawing_api import *
from skimage import filters, io, exposure
from os import path, makedirs

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

        #setup nodes for necessary views
        render_layers_node = tree.nodes.new('CompositorNodeRLayers')
        render_layers_node.location = 0,0

        comp_node = tree.nodes.new('CompositorNodeComposite')
        comp_node.location = 400,0

        viewer_node = tree.nodes.new('CompositorNodeViewer')
        viewer_node.location = 400, -200

        links = tree.links
        comp_link = links.new(render_layers_node.outputs[0], comp_node.inputs[0])

        write_path = bpy.data.scenes['Scene'].render.filepath
        #get the views from the nodes
        views = dict()
        views['original'] = self.get_view('Image', viewer_node, render_layers_node, scene, reso_percentage, write_path, True)
        views['normal'] = self.get_view('Normal', viewer_node, render_layers_node, scene, reso_percentage, write_path, write_to_disk)
        views['uv'] = self.get_view('UV', viewer_node, render_layers_node, scene, reso_percentage, write_path, write_to_disk)
        views['ao'] = self.get_view('AO', viewer_node, render_layers_node, scene, reso_percentage, write_path, write_to_disk)
        views['edge'] = filters.sobel(views['ao'][:,:,0]) + filters.sobel(views['normal'][:,:,0])

        #start drawing
        canvas = draw_features(write_path+"sketch.svg", views)
        #draw the shading style chosen
        if shading_style == 'DIAG':
            canvas = draw_shade_diagonal(canvas, views, bands=no_shade_bands, interval=width_of_bands)
        elif shading_style == 'HORIZ':
            canvas = draw_shade_horizontal(canvas, views, bands=no_shade_bands, interval=width_of_bands)
        elif shading_style == 'VERT':
            canvas = draw_shade_vertical(canvas, views, bands=no_shade_bands, interval=width_of_bands)
        elif shading_style == 'DOT':
            canvas = draw_shade_dotted(canvas, views, bands=no_shade_bands, interval=width_of_bands)
        elif shading_style == 'CONT':
            canvas = draw_shade_stream(canvas, views, views['uv'][:,:,0], bands=no_shade_bands, interval=width_of_bands)
            canvas = draw_shade_stream(canvas, views, views['uv'][:,:,1], bands=no_shade_bands, interval=width_of_bands)

        canvas.save()

        return {'FINISHED'}

    def update_display(self, scene, viewer_node):
        scene.node_tree.nodes.active = viewer_node
        scene.node_tree.update_tag()
        scene.update()
        bpy.ops.render.render()

    #gets a view from the node tree, given its name
    def get_view(self, view_name, viewer_node, render_layers_node, scene, reso_percentage, write_path, write_to_disk):
        links = scene.node_tree.links
        viewer_link = links.new(render_layers_node.outputs[view_name], viewer_node.inputs[0])
        self.update_display(scene, viewer_node)
        if write_to_disk:
            bpy.data.images['Viewer Node'].save_render(write_path + view_name +".png")
            return io.imread(write_path + view_name +".png")
        else:
            view_scene = np.asarray(bpy.data.images['Viewer Node'].pixels)
            return np.flip(np.reshape(view_scene, (int(scene.render.resolution_y*(reso_percentage/100)), int(scene.render.resolution_x*(reso_percentage/100)), 4)), axis=0)
