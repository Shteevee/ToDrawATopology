bl_info = {
    "name": "To Draw A Topology",
    "author": "Ewan Corbett",
    "version": (0, 0, 2),
    "blender": (2, 79, 0),
    "location": "View3D",
    "description": "Dev Sandbox",
    "category": "Development",
}

import sys
sys.path.append("../")

import bpy

from .export_components_operator import ExportComponentImagesOperator
from .export_svg_scene_operator import ExportSvgSceneOperator

def register():
    bpy.utils.register_class(ExportComponentImagesOperator)
    bpy.utils.register_class(ExportSvgSceneOperator)

def unregister():
    bpy.utils.unregister_class(ExportComponentImagesOperator)
    bpy.utils.unregister_class(ExportSvgSceneOperator)

if __name__ == "__main__":
    register()
