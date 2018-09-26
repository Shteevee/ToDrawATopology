bl_info = {
    "name": "To Draw A Topology",
    "author": "Ewan Corbett",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D",
    "description": "Dev Sandbox",
    "category": "Development",
}

import sys
sys.path.append("../")

import bpy
from render_freestyle_svg import *
from .export_vector_operator import ExportVectorOperator

def register():
    bpy.utils.register_class(ExportVectorOperator)

def unregister():
    bpy.utils.unregister_class(ExportVectorOperator)

if __name__ == "__main__":
    register()
