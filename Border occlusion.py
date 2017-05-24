import bpy
from bpy.types import Operator, Macro

bl_info = {
"name": "Border Occlusion",
"location": "View3D > Add > Mesh > Border Occlusion",
"description": "Drag mause for seletion back and front faces by dorder",
"author": "Vladislav Kindushov",
"version": (0,2),
"blender": (2, 7, 8),
"category": "Mesh",
}


class BorderOcclusion(bpy.types.Operator):
	"""Border Occlusion selection """
	bl_idname = "view3d.border_occlusion"
	bl_label = "Border Occlusion"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		#context.space_data.use_occlude_geometry = False
		#bpy.ops.view3d.select_lasso('INVOKE_DEFAULT')
		#context.space_data.use_occlude_geometry = True
		return {'FINISHED'}

class a(bpy.types.Operator):
	"""Border Occlusion selection """
	bl_idname = "view3d.a"
	bl_label = "a"

	# bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		context.space_data.use_occlude_geometry = False
		#bpy.ops.view3d.select_lasso('INVOKE_DEFAULT')
		# context.space_data.use_occlude_geometry = True
		return {'FINISHED'}

class b(bpy.types.Operator):
	"""Border Occlusion selection """
	bl_idname = "view3d.b"
	bl_label = "b"
	#bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		#context.space_data.use_occlude_geometry = False
		#bpy.ops.view3d.select_lasso('INVOKE_DEFAULT')
		context.space_data.use_occlude_geometry = True
		return {'FINISHED'}

class OcclusionMacro(Macro):
	bl_idname = 'view3d.occlusion_macro'
	bl_label = 'Occlusion Macro'
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		OcclusionMacro.define('view3d.a')
		OcclusionMacro.define('VIEW3D_OT_select_lasso')
		OcclusionMacro.define('view3d.b')
		return {'FINISHED'}
#
# class c(bpy.types.Operator):
# 	"""Border Occlusion selection """
# 	bl_idname = "view3d.c"
# 	bl_label = "c"
# 	#bl_options = {'REGISTER', 'UNDO'}
#
# 	def execute(self, context):
# 		OcclusionMacro.define('view3d.a')
# 		OcclusionMacro.define('VIEW3D_OT_select_lasso')
# 		OcclusionMacro.define('view3d.b')
# 		return {'FINISHED'}

def register():
	bpy.utils.register_module(__name__)


	OcclusionMacro.define('VIEW3D_OT_a')
	OcclusionMacro.define('VIEW3D_OT_select_lasso')
	OcclusionMacro.define('VIEW3D_OT_b')
	kc = bpy.context.window_manager.keyconfigs.addon
	if kc:
		km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
		kmi = km.keymap_items.new('view3d.occlusion_macro', 'RIGHTMOUSE', 'PRESS',)
		kmi = km.keymap_items.new('view3d.occlusion_macro', 'RIGHTMOUSE', 'PRESS', )
		kmi = km.keymap_items.new('view3d.occlusion_macro', 'RIGHTMOUSE', 'PRESS',)
		kmi.active = True

def unregister():
	bpy.utils.unregister_module(__name__)
	kc = bpy.context.window_manager.keyconfigs.addon
	if kc:
		km = kc.keymaps["3D View"]
		for kmi in km.keymap_items:
			if kmi.idname == 'view3d.occlusion_macro':
				km.keymap_items.remove(kmi)

if __name__ == "__main__":
	register()