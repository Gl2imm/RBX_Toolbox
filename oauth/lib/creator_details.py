# Copyright © 2023 Roblox Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# SPDX-License-Identifier: MIT

"""Functions handling the loading and saving of session creator configuration to Add-on preferences"""

if "bpy" in locals():
    # Imports have run before. Need to reload the imported modules
    import importlib

    if "get_add_on_preferences" in locals():
        importlib.reload(get_add_on_preferences)
    if "RbxOAuth2Client" in locals():
        importlib.reload(RbxOAuth2Client)

import bpy
from bpy.types import PropertyGroup
from bpy.props import StringProperty, EnumProperty
import json
import traceback


class RbxCreatorData(PropertyGroup):
    """Stores info about a creator that the user can upload to"""

    id: StringProperty(name="ID")
    type: EnumProperty(
        name="Type",
        items=[
            ("USER", "User", "Upload to your account", "USER", 0),
            ("GROUP", "Group", "Upload to a group", "COMMUNITY", 1),
        ],
        default="USER",
    )
    name: StringProperty(name="Name")


def get_selected_creator_data(window_manager):
    """Returns the RbxCreatorData object in the CollectionProperty corresponding with the current creator ID selected
    in the EnumProperty dropdown."""
    rbx = window_manager.rbx
    creator_data = next(
        (creator_data for creator_data in rbx.creators if creator_data.id == rbx.creator),
        None,
    )
    return creator_data


def save_creator_details(window_manager, preferences):
    """
    Saves the entire login session state to the add-on preferences.
    Simple values are stored directly, complex ones (dicts, collections) are serialized to JSON.
    """
    from .get_add_on_preferences import get_add_on_preferences
    from .oauth2_client import RbxOAuth2Client

    print("Saving Roblox session details to preferences.")
    try:
        add_on_preferences = get_add_on_preferences(preferences)
        rbx = window_manager.rbx
        oauth2_client = RbxOAuth2Client(rbx)

        print(f"Saving the following creator ID: {rbx.get('creator')}")

        # --- Save Simple Properties ---
        add_on_preferences.creator = rbx.get("creator") or ""
        add_on_preferences.is_logged_in = rbx.is_logged_in

        print(f"Saving is_logged_in: {add_on_preferences.is_logged_in}")

        # --- Save Complex Properties as JSON ---

        # Save the token data (access token, refresh token, expiry, etc.)
        print("Saving token data.")
        if RbxOAuth2Client.token_data:
            print("Token data is not empty.")
            add_on_preferences.saved_token_data_json = json.dumps(
                RbxOAuth2Client.token_data)
        else:
            print("Token data is empty.")
            add_on_preferences.saved_token_data_json = ""

        # Save the list of creators (user and groups)
        if rbx.creators:
            print("Saving the list of creators.")
            creators_list = []
            for creator in rbx.creators:
                creators_list.append({
                    "id": creator.id,
                    "type": creator.type,
                    "name": creator.name,
                })
            add_on_preferences.saved_creators_json = json.dumps(creators_list)
        else:
            print("No creators to save.")
            add_on_preferences.saved_creators_json = ""

        # Force user preferences to save.
        preferences.use_preferences_save = True
        bpy.ops.wm.save_userpref()
        print("Successfully updated RBX property and saved creator details.")

    except Exception as e:
        print(f"Error saving Roblox session details: {e}")
        traceback.print_exc()


def load_creator_details(window_manager, preferences):
    """
    Loads the entire login session state from add-on preferences.
    Reads JSON strings and deserializes them back into the session's data structures.
    """
    from .get_add_on_preferences import get_add_on_preferences
    from .oauth2_client import RbxOAuth2Client

    rbx = window_manager.rbx
    rbx.has_called_load_creator = True
    oauth2_client = RbxOAuth2Client(rbx)

    print("Loading Roblox session details from preferences.")
    try:
        add_on_preferences = get_add_on_preferences(preferences)

        # --- Load All Properties without triggering update callbacks ---
        print("Loading simple properties.")
        rbx["creator"] = add_on_preferences.get("creator", "")
        rbx["is_logged_in"] = add_on_preferences.get("is_logged_in", False)

        print(
            f"Loaded simple properties: rbx.creator='{rbx['creator']}', rbx.is_logged_in={rbx['is_logged_in']}")


        print("Loading creators list from preferences.")
        creators_json = add_on_preferences.get("saved_creators_json")
        rbx.creators.clear()

        user_id_from_list = None
        creator_ids_from_list = set()

        if creators_json:
            creators_list = json.loads(creators_json)
            user_name = None
            for creator_data in creators_list:
                creator = rbx.creators.add()
                creator_id = creator_data.get("id")
                creator.id = creator_id
                creator.type = creator_data.get("type")
                creator.name = creator_data.get("name")

                creator_ids_from_list.add(creator_id)

                if creator.type == "USER":
                    user_name = creator.name
                    window_manager.rbx.name = creator.name
                    user_id_from_list = creator_id

            if user_name:
                oauth2_client.name = user_name

        # --- FIX: VALIDATE AND INITIALIZE THE CREATOR PROPERTY ---
        # This is the crucial new block you correctly identified was needed.
        # After rebuilding the creator list, we check if the loaded rbx.creator value is valid.
        if rbx.is_logged_in:
            current_creator_id = rbx.get("creator")
            if current_creator_id not in creator_ids_from_list:
                print(
                    f"Loaded creator ID '{current_creator_id}' is invalid or not found. Resetting to default.")
                # If the stored creator is no longer valid or is empty, default to the user's ID.
                if user_id_from_list:
                    rbx.creator = user_id_from_list
                    print(f"Default creator set to User ID: {rbx.creator}")
                else:
                    print("Warning: Could not find a User ID to set as default.")
            else:
                print(
                    f"Successfully validated loaded creator ID: {current_creator_id}")

        if rbx.is_logged_in:
            print("Roblox login session loaded and validated.")
            print("Loading token data from preferences.")
            token_data_json = add_on_preferences.saved_token_data_json
            RbxOAuth2Client.token_data = json.loads(token_data_json)
            print("Token data loaded.")
        else:
            print("No active Roblox login session found in preferences.")

        # --- FORCE UI REFRESH ---
        print("Forcing UI refresh.")
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

    except Exception as e:
        print(f"Error loading Roblox session details: {e}")
        rbx.is_logged_in = False
        rbx.creators.clear()
        RbxOAuth2Client.token_data = {}
        traceback.print_exc()
