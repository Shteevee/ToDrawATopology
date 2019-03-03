bl_info = {
    "name": "To Draw A Topology",
    "author": "Ewan Corbett",
    "version": (0, 0, 2),
    "blender": (2, 79, 0),
    "location": "View3D",
    "description": "NPR pen-and-ink rendering project",
    "category": "Render",
}

import sys
sys.path.append("../")
import bpy

from drawing_a_topology.ui_components.export_components_operator import ExportComponentImagesOperator
from drawing_a_topology.ui_components.export_svg_scene_operator import ExportSvgSceneOperator
from drawing_a_topology.ui_components.export_svg_panel import ToDrawATopologyPanel, PanelFeatures

def register():
    bpy.utils.register_class(PanelFeatures)
    bpy.types.Scene.panel_features = bpy.props.PointerProperty(type=PanelFeatures)
    bpy.utils.register_class(ExportComponentImagesOperator)
    bpy.utils.register_class(ExportSvgSceneOperator)
    bpy.utils.register_class(ToDrawATopologyPanel)

def unregister():
    bpy.utils.unregister_class(PanelFeatures)
    bpy.utils.unregister_class(ExportComponentImagesOperator)
    bpy.utils.unregister_class(ExportSvgSceneOperator)
    bpy.utils.unregister_class(ToDrawATopologyPanel)
    del bpy.types.Scene.panel_features

if __name__ == "__main__":
    register()
