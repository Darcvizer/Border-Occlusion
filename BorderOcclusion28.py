import bpy
from bpy.types import Operator, Macro
from bpy.types import Header
bl_info = {
"name": "Border Occlusion",
"location": "View3D > Add > Mesh > Border Occlusion",
"description": "Drag mause for seletion back and front faces by dorder",
"author": "Vladislav Kindushov",
"version": (0,3),
"blender": (2, 80, 0),
"category": "Mesh",
}

Mode = True
ModS = "wm.tool_set_by_name"

class BorderOn(bpy.types.Operator):
	"""Border Occlusion selection """
	bl_idname = "view3d.border_on"
	bl_label = "BorderOn"

	def execute(self, context):
		context.space_data.shading.show_xray = True
		print("sosok")
		return {'FINISHED'}

class BorderOff(bpy.types.Operator):
	"""Border Occlusion selection """
	bl_idname = "view3d.border_off"
	bl_label = "BorderOff"

	def execute(self, context):
		context.space_data.shading.show_xray = False
		return {'FINISHED'}

class BorderSwap(bpy.types.Operator):
	"""Border Occlusion selection """
	bl_idname = "view3d.border_swap"
	bl_label = "BorderSwap"

	def execute(self, context):
		global Mode
		global ModS
		if Mode:
			Mode = False
			ModS = "VIEW3D_OT_select_lasso"
		else:
			Mode = True
			ModS = "VIEW3D_OT_select_box"
		print(Mode)
		return {'FINISHED'}

class OcclusionMacro(Macro):	
	bl_idname = 'view3d.occlusion_macro'
	bl_label = 'Occlusion Macro'
	bl_options = {'REGISTER', 'UNDO'}

class OcclusionMacro_HT_darcvizer(Header):
	bl_space_type = 'VIEW_3D'
	def draw(self, context):
		layout = self.layout
		col = layout.column()
		row = col.row(align = True)

		if Mode:
			row.operator("view3d.border_swap", text = "", icon="MESH_CAPSULE",)
		else:
			row.operator("view3d.border_swap", text="", icon="MESH_PLANE", )



classes = (BorderOn, BorderOff, OcclusionMacro, OcclusionMacro_HT_darcvizer,BorderSwap,)



def register():
	global Mode
	global ModS
	for c in classes:
		bpy.utils.register_class(c)
	OcclusionMacro.define("view3d.border_on")
	#OcclusionMacro.define("view3d.select_lasso")
	OcclusionMacro.define("view3d.select_box")
	OcclusionMacro.define('view3d.border_off')


	kc = bpy.context.window_manager.keyconfigs.addon
	if kc:
		km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
		kmi = km.keymap_items.new('view3d.occlusion_macro', 'EVT_TWEAK_L', 'PRESS',)
		print(kmi.properties)
		#kmi = km.keymap_items.new('view3d.occlusion_macro', 'BUTTON5MOUSE', 'PRESS', )
		#kmi = km.keymap_items.new('view3d.occlusion_macro', 'BUTTON5MOUSE', 'PRESS',)
		kmi.active = True

def unregister():
	for c in reversed(classes):
		bpy.utils.unregister_class(c)
	kc = bpy.context.window_manager.keyconfigs.addon
	if kc:
		km = kc.keymaps["3D View"]
		for kmi in km.keymap_items:
			if kmi.idname == 'view3d.occlusion_macro':
				km.keymap_items.remove(kmi)

if __name__ == "__main__":
	register()
