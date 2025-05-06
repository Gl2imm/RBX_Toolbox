import bpy
import os
import sys
import requests
import zipfile
from threading import Thread
import shutil
import glob_vars



if glob_vars.aepbr_lts_ver == None:
    aepbr_url = ""
    aepbr_file = ""
else:
    aepbr_url = "https://github.com/paribeshere/AEPBR/releases/download/" + "v." + glob_vars.aepbr_lts_ver + "/"
    aepbr_file = glob_vars.aepbr_lts_title + ".zip"
AEPBR_UPDATE_URL = aepbr_url + aepbr_file


# Global variables to track the state of the operator
aepbr_download_progress = 0
aepbr_operator_state = "IDLE"  # States: IDLE, DOWNLOADING, INSTALLING, FINISHED, ERROR
aepbr_error_message = ""
aepbr_current_operator = None




class RBX_UPDATE_AEPBR(bpy.types.Operator):
    bl_idname = "wm.update_aepbr"
    bl_label = "Install AEPBR Update"
    _timer = None

    # Add a property for the progress bar
    progress: bpy.props.FloatProperty(
        name="Progress",
        subtype="PERCENTAGE",
        soft_min=0,
        soft_max=100,
        precision=1,
    ) # type: ignore


    def execute(self, context):
        global aepbr_operator_state, aepbr_download_progress, aepbr_error_message, aepbr_current_operator

        # Start the download in a separate thread
        if aepbr_operator_state == "IDLE":
            aepbr_current_operator = self  # Store the operator instance
            aepbr_operator_state = "DOWNLOADING"
            aepbr_download_progress = 0
            aepbr_error_message = ""
            self.download_thread = Thread(target=self.download_file)
            self.download_thread.start()
            context.window_manager.modal_handler_add(self)
            self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
            return {'RUNNING_MODAL'}
        else:
            self.report({'ERROR'}, "Operator is already running.")
            return {'CANCELLED'}



    def download_file(self):
        """Download and install update from GitHub"""
        global aepbr_operator_state, aepbr_download_progress, aepbr_error_message

        try:
            # Get the addon's directory
            addon_path = os.path.dirname(os.path.abspath(__file__))
            aepbr_path = os.path.join(addon_path, glob_vars.rbx_aepbr_fldr)
            # Create the folder if it does not exist
            os.makedirs(aepbr_path, exist_ok=True)
            download_path = os.path.join(aepbr_path, "update.zip")

            # Simulate a file download
            print("Downloading update...")
            print("AEPBR Update URL: ", AEPBR_UPDATE_URL)
            response = requests.get(AEPBR_UPDATE_URL, stream=True)
            response.raise_for_status()  # Raise an error for bad status codes
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        aepbr_download_progress = (downloaded_size / total_size) * 100

                        # Update the progress property
                        self.progress = aepbr_download_progress


            # Simulate installation after download
            aepbr_operator_state = "INSTALLING"
            self.install_addon(download_path, aepbr_path)

        except Exception as e:
            aepbr_operator_state = "ERROR"
            aepbr_error_message = str(e)
            print("Download ERROR: ", aepbr_error_message)


    def move_updated_file(self, aepbr_path):
        global aepbr_operator_state, aepbr_error_message
        # List all entries in aepbr_path and filter for directories
        subfolders = [f for f in os.listdir(aepbr_path) if os.path.isdir(os.path.join(aepbr_path, f))]

        if subfolders:
            # Assume there's only one subfolder; if multiple, pick the first one
            subfolder = subfolders[0]
            subfolder_path = os.path.join(aepbr_path, subfolder)
            
            # List files in the subfolder (ignore directories)
            files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
            
            if files:
                # Get the first file
                file_to_move = files[0]
                src_file = os.path.join(subfolder_path, file_to_move)
                dst_file = os.path.join(aepbr_path, file_to_move)
                
                # Move the file to the parent folder
                shutil.move(src_file, dst_file)
            else:
                aepbr_operator_state = "ERROR"
                aepbr_error_message = "Update Error (moving files)"
                print("Update Error (moving files)")

            # Delete the subfolder (and its contents)
            shutil.rmtree(subfolder_path)
        else:
            aepbr_operator_state = "ERROR"
            aepbr_error_message = "Update Error (moving files)"
            print("Update Error (moving files)")




    def install_addon(self, download_path, aepbr_path):
        """Download and install update from GitHub"""
        global aepbr_operator_state, aepbr_error_message

        try:
            print("Simulate installing")
            #Delete old add-on files (except update.zip)
            for filename in os.listdir(aepbr_path):
                file_path = os.path.join(aepbr_path, filename)
                if os.path.isfile(file_path) and filename != "update.zip":
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            # Extract ZIP
            #normpath - Normalizes the path (removes trailing / or \ if present)
            #dirname - Extracts the parent directory
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(aepbr_path)

            # Cleanup update.zip and extracted folder
            self.move_updated_file(aepbr_path)
            os.remove(download_path)

            # Mark installation as complete
            print("Update Installed! Successfully")
            aepbr_operator_state = "FINISHED"

        except Exception as e:
            aepbr_operator_state = "ERROR"
            aepbr_error_message = str(e)
            print("Update ERROR: ", aepbr_error_message)

        aepbr_operator_state = "IDLE"



    def modal(self, context, event):
        global aepbr_operator_state, aepbr_error_message, aepbr_download_progress
        scene = context.scene


        if event.type == 'TIMER':
            # Redraw all regions of the UI type where your panel resides (e.g., 'VIEW_3D')
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':  # Adjust if your panel is in a different area
                    area.tag_redraw()

        
        if aepbr_operator_state == "ERROR":
            self.report({'ERROR'}, f"Error: {aepbr_error_message}")
            return {'FINISHED'}

        if aepbr_operator_state == "FINISHED":
            self.report({'INFO'}, "Installation finished.")
            return {'FINISHED'}

        # Continue running
        return {'PASS_THROUGH'}


