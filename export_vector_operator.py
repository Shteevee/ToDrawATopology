import bpy
import numpy as np

class ExportVectorOperator(bpy.types.Operator):
    """"Export As SVG"""
    bl_idname = "export_scene.export_svg"
    bl_label = "Vector Image Rendering"
    bl_options = {'REGISTER'}

    def execute(self, context):

        scene = bpy.context.scene

        width  = int( scene.render.resolution_x * scene.render.resolution_percentage / 100 )
        height = int( scene.render.resolution_y * scene.render.resolution_percentage / 100 )
        depth  = 4 # RGBA

        img = list( bpy.data.images['Viewer Node'].pixels )      # Read viewer node

        img = np.array( img ).reshape( [height, width, depth] )[:,:,0]

        edgePixelCoordinates = np.array( img.nonzero() ).T

        np.savetxt("2.79\\scripts\\addons\\drawing_a_topology\\coords.out", edgePixelCoordinates, newline="\n")

        print(edgePixelCoordinates)

        return {'FINISHED'}
