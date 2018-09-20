import bpy

class ExportVectorOperator(bpy.types.Operator):
    """"Export As SVG"""
    bl_idname = "export_scene.export_svg"
    bl_label = "Vector Image Rendering"
    bl_options = {'REGISTER'}

    def execute(self, context):

        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        return {'FINISHED'}
