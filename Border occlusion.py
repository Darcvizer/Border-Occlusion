import bpy
import bgl
from mathutils import Vector
from bpy.props import IntProperty, BoolProperty


################################################
#This script Chebhou, I only made small changes#
################################################


bl_info = {
"name": "Border back face",
"location": "View3D > Add > Mesh > Destructive Extrude,",
"description": "Drag mause for seletion back and front faces by dorder",
"author": "Chebhou, Vladislav Kindushov",
"version": (0,1),
"blender": (2, 7, 8),
"category": "Mesh",
}


def draw_callback_px(self, context):

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(1.0, 1.0, 1.0, 0.5)
    bgl.glLineWidth(2)

    if self.selecting :
        # when selecting draw dashed line box
        bgl.glEnable(bgl.GL_LINE_STIPPLE)
        bgl.glLineStipple(2, 0x3333)
        bgl.glBegin(bgl.GL_LINE_LOOP)

        bgl.glVertex2i(self.min_x, self.min_y)
        bgl.glVertex2i(self.min_x, self.max_y)
        bgl.glVertex2i(self.max_x, self.max_y)
        bgl.glVertex2i(self.max_x, self.min_y)

        bgl.glEnd()

        bgl.glDisable(bgl.GL_LINE_STIPPLE)
    '''else :
        # before selection starts draw infinite cross
        bgl.glBegin(bgl.GL_LINES)

        bgl.glVertex2i(0, self.max_y)
        bgl.glVertex2i(context.area.width, self.max_y)        

        bgl.glVertex2i(self.max_x, 0)
        bgl.glVertex2i(self.max_x, context.area.height)

        bgl.glEnd()'''

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class SelectOperator(bpy.types.Operator):
    """simple box selection """
    bl_idname = "view3d.box_select"
    bl_label = "Simple Box Select Operator"
    bl_options = {'REGISTER', 'UNDO'}

    min_x = IntProperty(default = 0)
    min_y = IntProperty(default = 0)
    max_x = IntProperty()
    max_y = IntProperty()

    selecting = BoolProperty(default = False) # just for drawing in bgl

    def modal(self, context, event):
        context.area.tag_redraw()
        context.space_data.use_occlude_geometry = False
        if event.type == 'MOUSEMOVE': # just for drawing the box
            self.selecting = True
            self.max_x = event.mouse_region_x
            self.max_y = event.mouse_region_y

        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS': # start selection
                self.selecting = True
                self.min_x = event.mouse_region_x
                self.min_y = event.mouse_region_y
                
            if event.value == 'RELEASE': # end of selection
                #we have to sort the coordinates before passing them to select_border()
                self.max_x = max(event.mouse_region_x, self.min_x)
                self.max_y = max(event.mouse_region_y, self.min_y)
                self.min_x = min(event.mouse_region_x, self.min_x)
                self.min_y = min(event.mouse_region_y, self.min_y)
                if event.shift:
                    bpy.ops.view3d.select_border(gesture_mode=3, xmin=self.min_x, xmax=self.max_x, ymin=self.min_y, ymax=self.max_y, extend=True)
                    bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                    context.space_data.use_occlude_geometry = True
                    return {'FINISHED'}
                else:
                    bpy.ops.view3d.select_border(gesture_mode=3, xmin=self.min_x, xmax=self.max_x, ymin=self.min_y, ymax=self.max_y, extend=False)
                    bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                    context.space_data.use_occlude_geometry = True
                    return {'FINISHED'}
        elif event.type in {'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        if context.space_data.type == 'VIEW_3D':
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            self.min_x = event.mouse_region_x
            self.min_y = event.mouse_region_y
            
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(SelectOperator)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('view3d.box_select', 'RIGHTMOUSE', 'PRESS',)
        kmi.active = True

def unregister():
    bpy.utils.unregister_class(SelectOperator)
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["3D View"]
        for kmi in km.keymap_items:
            if kmi.idname == 'view3d.box_select':
                km.keymap_items.remove(kmi)
                break

if __name__ == "__main__":
    register()