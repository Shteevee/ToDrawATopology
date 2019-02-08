import bpy

class ToDrawATopologyPanel(bpy.types.Panel):

    bl_idname = "OBJECT_PT_To_Draw_A_Topology"
    bl_label = "To Draw A Topology"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"



    def draw(self, context):
        self.layout.prop(context.scene.panel_features, "memory_bool")
        self.layout.prop(context.scene.panel_features, "bands_slider")
        self.layout.prop(context.scene.panel_features, "shade_dropdown")
        self.layout.prop(context.scene.panel_features, "shading_type_dropdown")
        self.layout.operator("to_draw_a_topology.export_svg")

class PanelFeatures(bpy.types.PropertyGroup):

    bands_slider = bpy.props.IntProperty(
        name = "No. of Shade Bands",
        description = "The number of shade bands to generate",
        default = 3,
        min = 1,
        max = 4
        )

    shade_dropdown = bpy.props.EnumProperty(
        name = "Width of Shade Bands",
        description = "How much shading is encapsulated in one band",
        items = [('30', "Low", ""),
                 ('40', "Medium", ""),
                 ('50', "High", "")]
        )

    shading_type_dropdown = bpy.props.EnumProperty(
        name = "Type of Shading to Use",
        description = "Style of shading",
        items = [('DIAG', "Diagonal", ""),
                 ('HORIZ', "Horizontal", ""),
                 ('VERT', "Vertical", ""),
                 ('DOT', "Dotted", ""),
#                 ('CONT', "Contoured", ""),
                 ('NONE', "None", "")]
        )

    memory_bool = bpy.props.BoolProperty(
        name = "Held on disk",
        description = "Whether the images are written to disk may effect output slightly",
        default = False
        )
