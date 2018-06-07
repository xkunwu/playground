import bpy
import bgl
# import blf


bl_info = {
    "name": "Draw curvature",
    "description": "",
    "author": "xkunwu",
    "version": (0, 0, 1),
    "blender": (2, 70, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

def draw_callback_px(self, context):

    # 50% alpha, 2 pixel width line
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    bgl.glLineWidth(context.scene.BGL_DEMO_PROP_THICKNESS)

    bgl.glBegin(bgl.GL_LINE_STRIP)
    for co in self.mouse_path:
        bgl.glVertex3f(*co)

    bgl.glEnd()

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class ModalDrawOperator(bpy.types.Operator):

    bl_idname = "view3d.bgl_demo_modal_operator"
    bl_label = "Simple Modal View3D Operator"

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'MIDDLEMOUSE'}:
            return {'RUNNING_MODAL'}


        if event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)

            draw_handler_add = bpy.types.SpaceView3D.draw_handler_add
            self._handle = draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_VIEW')

            self.mouse_path = [v.co for v in context.active_object.data.vertices]

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


class OBJECT_PT_draw_curvature(bpy.types.Panel):
    """ Creates a Panel in the Object properties window """
    bl_label = "Draw Curvature Panel"
    bl_idname = "obj_draw_curvature"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # bl_context = "object"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(context.scene, 'BGL_DEMO_PROP_THICKNESS', text='thickness')
        col.operator("view3d.bgl_demo_modal_operator")


def register():
    bpy.types.Scene.BGL_DEMO_PROP_THICKNESS = bpy.props.IntProperty(default=1, max=5)
    bpy.utils.register_class(OBJECT_PT_draw_curvature)
    bpy.utils.register_class(ModalDrawOperator)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_draw_curvature)
    bpy.utils.unregister_class(ModalDrawOperator)
    del bpy.types.Scene.BGL_DEMO_PROP_THICKNESS

if __name__ == "__main__":
    register()
