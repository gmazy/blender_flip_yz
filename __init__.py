# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under Creative Commons CC0
# https://creativecommons.org/publicdomain/zero/1.0/
#
# Note: All Blender API calls are licensed under GNU GPL according to www.blender.org
#
# ##### END LICENSE BLOCK #####

bl_info = {  
    "name": "Flip Y and Z",  
    "author": "Mazay",  
    "version": (0, 2),  
    "blender": (2, 80, 0),  
    "location": "View3D > Object > Flip Y and Z",  
    "description": "Adds Flip Y and Z option to object menu.",  
    "warning": "",  
    "wiki_url": "",  
    "tracker_url": "",  
    "category": "Object"}  

import bpy
import bmesh
import mathutils

class FlipYZ(bpy.types.Operator):
    """Flip Y and Z of object"""
    bl_idname = "object.flip_yz"
    bl_label = "Flip Y and Z"
    bl_options = {'REGISTER', 'UNDO'} # Add to F3 search, Add Undo step

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) > 0

    def execute(self, context):
        for ob in bpy.context.selected_objects:

            # Flip Y and Z in 4x4 transform matrix:
            m = ob.matrix_world
            x, y, z, w = m[0], m[1], m[2], m[3]
            # swapping third and second row, and third and second column                  
            ob.matrix_world = mathutils.Matrix([
                (x.x, x.z, x.y, x.w),
                (z.x, z.z, z.y, z.w),
                (y.x, y.z, y.y, y.w),
                (w.x, w.z, w.y, w.w),
            ])

            # Flip Y and Z of vertices:
            if ob.type == 'MESH':
                mesh = ob.data
                bm = bmesh.new() # Empty BMesh
                bm.from_mesh(mesh) # Fill with data

                for v in bm.verts:
                    y = v.co.y
                    z = v.co.z
                    v.co.y = z
                    v.co.z = y
                    
                bm.to_mesh(mesh) # Overwrite original mesh
                mesh.update() # Update viewport after mesh change
                bm.free() # Free temporary mesh from memory    

        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu.
def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(FlipYZ.bl_idname, text="Flip Y and Z")


def register():
    bpy.utils.register_class(FlipYZ)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(FlipYZ)

if __name__ == "__main__":
    register()
