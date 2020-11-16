import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty
import rna_keymap_ui
bl_info = {
"name": "BorderOcclusion",
"location": "View3D > Add > Object > Border Occlusion",
"description": "Drag mause for seletion back and front faces by dorder",
"author": "Vladislav Kindushov",
"version": (0,5),
"blender": (2, 90, 0),
"category": "Object",
}
addon_keymaps = []

class OBJECT_OT_BorderOcclusion(Operator):
    """Border Occlusion selection """
    bl_idname = "object.border_occlusion"
    bl_label = "Border Occlusion"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "VIEW_3D"

    Deselect: BoolProperty(
        name="Deselect",
        description="",
        default = False,
    )
    Extend: BoolProperty(
        name="Extend",
        description="",
        default = False,
    )

    def modal(self, context, event):
        if not self.Select:
            if self.Deselect:
                #print('Sub')
                if self.SelectMode:
                    bpy.ops.view3d.select_lasso('INVOKE_DEFAULT', mode='SUB')
                else: 
                    bpy.ops.view3d.select_box('INVOKE_DEFAULT', wait_for_input=False, mode='SUB')
            elif self.Extend:
                #print('ADD')
                if self.SelectMode:
                    bpy.ops.view3d.select_lasso('INVOKE_DEFAULT', mode='ADD')
                else: 
                    bpy.ops.view3d.select_box('INVOKE_DEFAULT', wait_for_input=False, mode='ADD')
            else:
                #print('New')
                if self.SelectMode:
                    bpy.ops.view3d.select_lasso('INVOKE_DEFAULT', mode='SET')
                else: 
                    bpy.ops.view3d.select_box('INVOKE_DEFAULT', wait_for_input=False, mode='SET')
            self.Select = True
            return {'RUNNING_MODAL'}
        context.space_data.shading.show_xray = self.show_xray
        return {'CANCELLED'}

    def invoke(self, context, event):
        self.show_xray = context.space_data.shading.show_xray
        context.space_data.shading.show_xray = True
        self.Select = False
        self.SelectMode = context.scene.border_occlude_mode
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def add_hotkey(prop=None, prop_value=None, shift=False, ctrl=False, alt=False):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    # km = kc.keymaps.new(name="3D View Generic", space_type='VIEW_3D', region_type='WINDOW') 
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('object.border_occlusion', 'RIGHTMOUSE', 'PRESS', shift=shift, ctrl=ctrl, alt=alt, head=True)
   # kmi.active = True
    #km.update()

    # print('create')

    if not prop is None:
        kmi.properties[prop] = prop_value

    global addon_keymaps
    addon_keymaps.append((km, kmi))


def remove_hotkey():
    kc = bpy.context.window_manager.keyconfigs.user
    km = kc.keymaps.get('3D View')
    for i in km.keymap_items:
        if i.name == 'Border Occlusion' or i.name == 'OBJECT_OT_border_occlusion':
            # print('remove')
            km.keymap_items.remove(i)


def CheckConflict(box):
    for km, kmi in addon_keymaps: 
        for i in bpy.context.window_manager.keyconfigs.user.keymaps['3D View'].keymap_items:
            if kmi.type == i.type and kmi.ctrl == i.ctrl and kmi.alt == i.alt and kmi.shift == i.shift and i.active and kmi.name != i.name:
                box.column().label(text='Conflict hotkey: ' + '3D View -> ' +  '3D View Global -> ' + i.name)
    
    for km, kmi in addon_keymaps: 
        for i in bpy.context.window_manager.keyconfigs.user.keymaps['Mesh'].keymap_items:
            if kmi.type == i.type and kmi.ctrl == i.ctrl and kmi.alt == i.alt and kmi.shift == i.shift and i.active and kmi.name != i.name:
                box.column().label(text='Conflict hotkey: ' + '3D View -> ' +  'Mesh -> ' + i.name)

    for km, kmi in addon_keymaps: 
        for i in bpy.context.window_manager.keyconfigs.user.keymaps['Object Mode'].keymap_items:
            if kmi.type == i.type and kmi.ctrl == i.ctrl and kmi.alt == i.alt and kmi.shift == i.shift and i.active and kmi.name != i.name:
                box.column().label(text='Conflict hotkey: ' + '3D View -> ' +  'Object Mode -> ' + i.name)

def GetKMI():
    kc = bpy.context.window_manager.keyconfigs.user
    km = kc.keymaps.get('3D View')
    kmi=[]
    for i in km.keymap_items:
        if i.name == 'Border Occlusion' or i.name == 'OBJECT_OT_border_occlusion':
            kmi.append(i)
    return kmi

class BorderOccludePref(AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        CheckConflict(box)

        kc = bpy.context.window_manager.keyconfigs.user
        km = kc.keymaps.get('3D View')
        
        for i in GetKMI()[-3:]:
            km.active()
            box = layout.box()
            col = box.column()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, i, col, 0)


def draw(self, context):
    layout = self.layout
    if bpy.context.scene.border_occlude_mode:
        icon = 'MESH_CAPSULE'
    else:
        icon = 'MESH_PLANE'

    layout.prop(bpy.context.scene, 'border_occlude_mode' ,icon=icon)



classes = (OBJECT_OT_BorderOcclusion, BorderOccludePref)

def register():
    for i in classes:
        bpy.utils.register_class(i)
    
    bpy.types.Scene.border_occlude_mode = BoolProperty(
        name="",
        description="",
        default = False,
    )
    bpy.types.VIEW3D_HT_header.append(draw)

    add_hotkey(prop='Deselect', prop_value=True,shift=False, ctrl=True)
    add_hotkey(prop='Extend', prop_value=True , shift=True, ctrl=False)
    add_hotkey()

def unregister():
    remove_hotkey()
    for i in reversed(classes):
        bpy.utils.unregister_class(i)

    bpy.types.VIEW3D_HT_header.remove(draw)

    del bpy.types.Scene.border_occlude_mode

    addon_keymaps.clear()

if __name__ == "__main__":
    register()
