import bpy
import os
from bpy import context
from bpy.props import StringProperty, BoolProperty
import re  # For cleaning up object names

bl_info = {
    "name": "Blender MOF Bridge",
    "description": "Unwrap your objects with MINISTRY OF Fdef register():
    """Addon activation process"""
    bpy.utils.register_class(MyAddonPreferences)
    bpy.utils.register_class(AutoUV)
    bpy.utils.register_class(MOF_BRIDGE_PT_panel)  # Register panel class
    
    try:
        bpy.types.VIEW3D_MT_object.append(menu_func)
        print("✓ MOF Bridge: Menu registration successful (VIEW3D_MT_object)")
    except AttributeError:
        print("⚠ MOF Bridge: Menu registration failed")
    
    print("✓ MOF Bridge: Panel registration successful (sidebar tab)")istry of Flat, your flatness!!!",
    "blender": (2, 80, 0),
    "category": "UV",
    "location": "Object > Unwrap in Ministry of Flat",
    "version": (1, 1),
    "author": "rentanek0",
    "doc_url": "https://www.quelsolaar.com/ministry_of_flat/",
    "tracker_url":"https://github.com/garanovich/mofbridge/",
}

class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    folder_path: StringProperty(
        name="MOF folder",
        description="Enter the path to the folder containing Ministry of Flat",  # Enter the path to the folder containing Ministry of Flat
        subtype="DIR_PATH",
    )

    separate: BoolProperty(
        name="Separate edges. Guarantees that all hard edges are separated. Useful for lightmapping and Normalmapping",
        default=True,
    )

    pack: BoolProperty(
        name="Pack after unwrap. (Packing in blender)",
        default=True,
    )

    showUV: BoolProperty(
        name="Show UV when done. (Goes to edit mode)",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "folder_path")
        layout.prop(self, "separate")
        layout.prop(self, "pack")
        layout.prop(self, "showUV")

class AutoUV(bpy.types.Operator):
    """Uses Ministry of Flat to automatically perform UV unwrapping"""  # Description shown on hover

    bl_idname = "object.autouv"  # Operator ID (must be in lowercase)
    bl_label = "Unwrap in Ministry of Flat"  # Name displayed in the UI
    bl_options = {"REGISTER"}

    def execute(self, context):  # Main operator logic
        # Step 1: Export selected objects
        active_object = context.active_object
        selected_objects = context.selected_objects  # Get all selected objects
        if not selected_objects:
            self.report({"ERROR"}, "No objects selected!")  # Error if no objects are selected
            return {"CANCELLED"}

        # Save original object names
        #original_names = {obj: obj.name for obj in selected_objects}

        # Export all selected objects to a single .obj file
        fn = os.path.join(bpy.app.tempdir, "exported_objects.obj")  # Temporary export file
        bpy.ops.wm.obj_export(
            filepath=fn,
            export_selected_objects=True,  # Export only selected objects
            export_materials=False,  # Do not export materials
            apply_modifiers=False,  # Do not apply modifiers
        )

        # Renaming original objects so imported objects can keep their names
        suffix = "_1ja"
        for obj in selected_objects:
            obj.name = obj.name + suffix        


        # Step 2: Run Ministry of Flat for UV unwrapping
        fn2 = os.path.join(bpy.app.tempdir, "unpacked_objects.obj")  # Temporary output file
        preferences = context.preferences.addons[__name__].preferences
        folder_path = preferences.folder_path  # Path to Ministry of Flat
        path = os.path.join(folder_path, "UnWrapConsole3.exe")

        if not os.path.isfile(path):
            self.report({'ERROR'}, f"MOF executable not found: {path}")
            print(f"✗ MOF Bridge: Executable not found: {path}")
            print(f"  Configured folder: {folder_path}")
            return {"CANCELLED"}

        separate = "TRUE" if preferences.separate else "FALSE"  # separate edges or not
        
        import subprocess
        cmd = [path, fn, fn2, "-CUTDEBUG", "FALSE", "-SEPARATE", separate]
        print(f"✓ MOF Bridge: Execute command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print(f"  MOF exit code: {result.returncode}")
            if result.stdout:
                print(f"  MOF output: {result.stdout}")
            if result.stderr:
                print(f"  MOF error: {result.stderr}")
            
            if result.returncode != 0:
                self.report({'ERROR'}, f"MOF execution failed (exit code: {result.returncode})")
                return {"CANCELLED"}
        except subprocess.TimeoutExpired:
            self.report({'ERROR'}, "MOF execution timed out (over 5 minutes)")
            return {"CANCELLED"}
        except Exception as e:
            self.report({'ERROR'}, f"Error during MOF execution: {e}")
            print(f"✗ MOF Bridge: Execution error: {e}")
            return {"CANCELLED"}

        if not os.path.isfile(fn2):
            self.report({'ERROR'}, f"MOF did not generate output file: {fn2}")
            print(f"✗ MOF Bridge: Output file does not exist: {fn2}")
            return {"CANCELLED"}

        print(f"✓ MOF Bridge: Output file confirmed: {fn2}")

        # Step 3: Import the result of UV unwrapping
        bpy.ops.wm.obj_import(filepath=fn2)

        # Step 4: Restore original names for imported objects
        imported_objects = context.selected_objects  # Get all imported objects

        # Step 5: Copy UV maps from imported objects to the original objects
        for obj in selected_objects:
            for imported_obj in imported_objects:
                if imported_obj.name + suffix == obj.name:  # Match by original name including suffix
                    # Check if both objects have UV layers
                    if obj.data.uv_layers and imported_obj.data.uv_layers:
                        # Remove all existing UV layers from the original object
                        while obj.data.uv_layers:
                            obj.data.uv_layers.remove(obj.data.uv_layers[0])

                        # Copy UV layers from the imported object to the original object
                        for src_uv in imported_obj.data.uv_layers:
                            new_uv = obj.data.uv_layers.new(name=src_uv.name)
                            
                            # Create an array to store UV coordinates
                            uv_coords = [0.0] * (len(src_uv.data) * 2)  # 2 values (u, v) per vertex
                            
                            # Get UV coordinates from the source UV layer
                            src_uv.data.foreach_get("uv", uv_coords)
                            
                            # Set UV coordinates in the new UV layer
                            new_uv.data.foreach_set("uv", uv_coords)

        # Step 6: Delete all imported objects
        for imported_obj in imported_objects:
            bpy.data.objects.remove(imported_obj)

        for obj in selected_objects:
            obj.name = obj.name.removesuffix(suffix)
            obj.select_set(True)  

        bpy.context.view_layer.objects.active = active_object

        # Step 7: Clean up temporary files
        os.remove(fn)
        os.remove(fn2)

        if preferences.pack:
            wm = bpy.context.window_manager
            wm.progress_begin(0, 99)
            wm.progress_update(77)
            
            try:
                # Step 6: Pack UV islands
                bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit Mode
                bpy.ops.mesh.select_all(action='SELECT')
                
                with bpy.context.temp_override():
                    bpy.ops.uv.select_all(action='SELECT')
                    bpy.ops.uv.pack_islands(margin=0.001)
                
                bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object Mode
            except RuntimeError as e:
                print(f"⚠ MOF Bridge: Error in UV packing process: {e}")
            finally:
                wm.progress_end()

        if preferences.showUV: bpy.ops.object.mode_set(mode='EDIT')            

        self.report({'INFO'}, f"Processing complete. ")

        return {"FINISHED"}  # Operation completed


class MOF_BRIDGE_PT_panel(bpy.types.Panel):
    """MOF Bridge Panel - 3D Viewport Sidebar"""
    bl_label = "MOF Bridge"
    bl_idname = "MOF_BRIDGE_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MOF Bridge"

    @classmethod
    def poll(cls, context):
        """Conditions for panel display"""
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.scale_y = 2.0
        row.operator(AutoUV.bl_idname, text="Unwrap in Ministry of Flat", icon="UV")
        
        layout.separator()
        
        layout.label(text="Settings:", icon="PREFERENCES")
        
        row = layout.row()
        row.operator("preferences.addon_show", text="Open Preferences").module = __name__
        
        layout.separator()
        layout.label(text="Status Information:", icon="INFO")
        row = layout.row()
        if context.selected_objects:
            row.label(text=f"Selected: {len(context.selected_objects)} object(s)")
        else:
            row.label(text="No objects selected")


def menu_func(self, context):
    self.layout.operator(AutoUV.bl_idname)  # Add operator to the menu


def register():
    """Addon activation process"""
    bpy.utils.register_class(MyAddonPreferences)
    bpy.utils.register_class(AutoUV)
    bpy.utils.register_class(MOF_BRIDGE_PT_panel)
    
    try:
        bpy.types.VIEW3D_MT_object.append(menu_func)
        print("✓ MOF Bridge: Menu registration successful (VIEW3D_MT_object)")
    except AttributeError:
        print("⚠ MOF Bridge: Menu registration failed")
    
    print("✓ MOF Bridge: Panel registration successful (sidebar tab)")


def unregister():
    """Addon deactivation process"""
    try:
        bpy.types.VIEW3D_MT_object.remove(menu_func)
    except ValueError:
        pass
    
    bpy.utils.unregister_class(MOF_BRIDGE_PT_panel)
    bpy.utils.unregister_class(AutoUV)
    bpy.utils.unregister_class(MyAddonPreferences)


if __name__ == "__main__":
    register()
