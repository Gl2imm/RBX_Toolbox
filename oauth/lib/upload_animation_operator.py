if "bpy" in locals():
    import importlib

    if "status_indicators" in locals():
        importlib.reload(status_indicators)  # type: ignore
    if "creator_details" in locals():
        importlib.reload(creator_details)  # type: ignore
    if "constants" in locals():
        importlib.reload(constants)  # type: ignore
    if "str_to_int" in locals():
        importlib.reload(str_to_int)  # type: ignore
    if "extract_exception_message" in locals():
        importlib.reload(extract_exception_message)  # type: ignore
    if "event_loop" in locals():
        importlib.reload(event_loop)  # type: ignore
    if "RbxOAuth2Client" in locals():
        importlib.reload(RbxOAuth2Client)  # type: ignore

import bpy
from bpy.types import Operator
import traceback
from tempfile import TemporaryDirectory
from pathlib import Path

from . import constants

NO_ASSET_ID = 0
LIBRARY_URL_PREFIX = "https://www.roblox.com/library/"


class RBX_OT_upload_animation(Operator):
    """Upload active animation from selected armature to Roblox"""

    bl_idname = "rbx.upload_animation"
    bl_label = "Upload Animation"
    limiter = None

    @classmethod
    def description(cls, context, _):
        rbx = context.window_manager.rbx
        if not rbx.is_logged_in:
            return "Log in before uploading"
        if rbx.is_processing_login_or_logout:
            return "Wait for login or logout to finish"
        if rbx.num_objects_uploading != 0:
            return "Wait for current upload process to finish"
        selected = context.selected_objects
        if len(selected) != 1 or selected[0].type != "ARMATURE":
            return "Select an armature to upload its animation"
        armature = selected[0]
        if armature.animation_data and armature.animation_data.action:
            return f"Upload animation '{armature.animation_data.action.name}' to Roblox"
        return f"Upload animation from '{armature.name}' to Roblox"

    @classmethod
    def poll(cls, context):
        rbx = context.window_manager.rbx
        if not rbx.is_logged_in:
            return False
        if rbx.is_processing_login_or_logout:
            return False
        if rbx.num_objects_uploading != 0:
            return False
        selected = context.selected_objects
        if len(selected) != 1 or selected[0].type != "ARMATURE":
            return False
        return True

    def execute(self, context):
        selected = context.selected_objects
        if len(selected) != 1 or selected[0].type != "ARMATURE":
            self.report({"ERROR"}, "Select an armature to upload its animation")
            return {"CANCELLED"}

        armature = selected[0]
        rbx_prefs = context.scene.rbx_prefs

        # Read name/description and upload options from UI fields
        name_override = rbx_prefs.rbx_upload_anim_name.strip()
        desc_override = rbx_prefs.rbx_upload_anim_desc.strip()
        force_new = rbx_prefs.rbx_upload_anim_as_new

        rbx = context.window_manager.rbx
        rbx.num_objects_uploading = 1

        from . import status_indicators
        from ... import glob_vars as glob_vars

        status_indicators.clear_statuses(context.window_manager)
        glob_vars.rbx_last_anim_upload_url = None  # clear previous link

        self.upload(
            context.window_manager,
            context.area,
            context.scene,
            context.view_layer,
            armature,
            name_override,
            desc_override,
            force_new=force_new,
        )

        return {"FINISHED"}

    @classmethod
    def upload(cls, window_manager, area, scene, view_layer, armature, name_override="", desc_override="", force_new=False):
        from . import status_indicators

        try:
            temporary_directory = TemporaryDirectory()

            # Resolve animation name: prefer user field, then action name, then armature name
            if name_override:
                anim_name = name_override
            elif armature.animation_data and armature.animation_data.action:
                anim_name = armature.animation_data.action.name
            else:
                anim_name = armature.name

            anim_desc = desc_override if desc_override else constants.ASSET_DESCRIPTION

            exported_file_path = Path(temporary_directory.name) / f"{anim_name}.fbx"
            cls._export_animation_fbx(scene, view_layer, armature, exported_file_path)
        except Exception as exception:
            traceback.print_exception(exception)
            status_indicators.set_status(
                window_manager, area, armature, constants.ERROR_MESSAGES["ADD_ON_ERROR"], "ERROR"
            )
            cls.upload_complete(window_manager, temporary_directory)
        else:
            status_indicators.set_status(window_manager, area, armature, "Waiting to upload", "DECORATE")

            from .str_to_int import str_to_int

            anim_id = NO_ASSET_ID if force_new else str_to_int(armature.get(constants.RBX_ANIMATION_ID_PROPERTY_NAME))
            coroutine = cls.upload_task(
                window_manager, area, armature, anim_name, anim_desc, exported_file_path, anim_id
            )

            def task_complete(task):
                cls.upload_task_complete(task, window_manager, area, armature, temporary_directory)

            from . import event_loop

            event_loop.submit(coroutine, task_complete)

    @classmethod
    def _export_animation_fbx(cls, scene, view_layer, armature, exported_file_path):
        collection = bpy.data.collections.new("RobloxAnimExportCollection")
        scene.collection.children.link(collection)
        collection.objects.link(armature)

        layer_collection = cls._find_layer_collection(view_layer.layer_collection, collection)
        previous_active = view_layer.active_layer_collection
        view_layer.active_layer_collection = layer_collection

        try:
            bpy.ops.export_scene.fbx(
                filepath=str(exported_file_path),
                use_active_collection=True,
                object_types={"ARMATURE"},
                add_leaf_bones=False,
                global_scale=0.01,
                axis_forward="-Z",
                axis_up="Y",
                bake_anim=True,
                bake_anim_use_nla_strips=False,
                bake_anim_use_all_actions=False,
                bake_anim_step=1.0,
                bake_anim_simplify_factor=0.0,
            )
        finally:
            view_layer.active_layer_collection = previous_active
            bpy.data.collections.remove(collection)

    @staticmethod
    def _find_layer_collection(layer_collection, target_collection):
        if layer_collection.collection == target_collection:
            return layer_collection
        for child in layer_collection.children:
            result = RBX_OT_upload_animation._find_layer_collection(child, target_collection)
            if result:
                return result

    @classmethod
    async def upload_task(cls, window_manager, area, armature, anim_name, anim_desc, file_path, anim_id):
        from .oauth2_client import RbxOAuth2Client
        from . import creator_details

        creator_data = creator_details.get_selected_creator_data(window_manager)
        rbx = window_manager.rbx
        oauth2_client = RbxOAuth2Client(rbx)
        await oauth2_client.refresh_login_if_needed()
        access_token = oauth2_client.token_data["access_token"]

        from assets_upload_client import AssetsUploadClient
        from openapi_client.models import (
            RobloxOpenCloudAssetsV1Creator as AssetsCreator,
            RobloxOpenCloudAssetsV1AssetType as AssetType,
        )

        match creator_data.type:
            case "USER":
                creator = AssetsCreator(user_id=int(creator_data.id))
            case "GROUP":
                creator = AssetsCreator(group_id=int(creator_data.id))

        if not cls.limiter:
            import aiolimiter

            cls.limiter = aiolimiter.AsyncLimiter(constants.MAX_UPLOADS_PER_MIN)

        async with cls.limiter, AssetsUploadClient(creator=creator, oauth2_token=access_token) as client:
            from . import status_indicators

            status_indicators.set_status(window_manager, area, armature, "Uploading", "DECORATE")
            operation = await client.upload_asset_and_wait_for_done_async(
                asset_type=AssetType.ANIMATION,
                asset_name=anim_name,
                asset_description=anim_desc,
                file_path=file_path,
                asset_id=anim_id or NO_ASSET_ID,
                upload_request_timeout_seconds=25,
            )

        return operation

    @staticmethod
    def upload_complete(window_manager, temporary_directory):
        temporary_directory.cleanup()
        rbx = window_manager.rbx
        rbx.num_objects_uploading = rbx.num_objects_uploading - 1

    @staticmethod
    def upload_task_complete(task, window_manager, area, armature, temporary_directory):
        from . import status_indicators
        import openapi_client
        import asyncio
        from ... import glob_vars as glob_vars

        try:
            operation = task.result()
            print(f"[RBX Anim Upload] Operation path: {operation.path}")
            print(f"[RBX Anim Upload] Full response: {operation}")

            if operation.error:
                status_indicators.set_status(window_manager, area, armature, operation.error.message, "ERROR")
                print(f"[RBX Anim Upload] Failed — {operation.error.code}: {operation.error.message}")
            elif not operation.done:
                status_indicators.set_status(
                    window_manager, area, armature, constants.ERROR_MESSAGES["OPERATION_TIMED_OUT"], "ERROR"
                )
            elif operation.response:
                armature[constants.RBX_ANIMATION_ID_PROPERTY_NAME] = str(operation.response.asset_id)
                status_indicators.set_status(
                    window_manager,
                    area,
                    armature,
                    f"Uploaded version {operation.response.revision_id}",
                    "CHECKMARK",
                )
                print(f"[RBX Anim Upload] Success! Asset ID: {operation.response.asset_id}, Revision: {operation.response.revision_id}")

                asset_id = getattr(operation.response, "asset_id", None)
                if asset_id:
                    glob_vars.rbx_last_anim_upload_url = LIBRARY_URL_PREFIX + str(asset_id)
                    glob_vars.rbx_last_anim_upload_id = str(asset_id)
                    print(f"[RBX Anim Upload] Library URL: {glob_vars.rbx_last_anim_upload_url}")
            else:
                status_indicators.set_status(
                    window_manager, area, armature, constants.ERROR_MESSAGES["INVALID_RESPONSE"], "ERROR"
                )
                print(f"[RBX Anim Upload] Invalid response:\n{operation}")
        except asyncio.exceptions.TimeoutError:
            status_indicators.set_status(
                window_manager, area, armature, constants.ERROR_MESSAGES["UPLOAD_TIMED_OUT"], "ERROR"
            )
        except openapi_client.rest.ApiException as exception:
            traceback.print_exception(exception)
            from .extract_exception_message import extract_exception_message

            status_indicators.set_status(
                window_manager,
                area,
                armature,
                extract_exception_message(exception),
                "ERROR",
            )
        except Exception as exception:
            traceback.print_exception(exception)
            status_indicators.set_status(
                window_manager, area, armature, constants.ERROR_MESSAGES["ADD_ON_ERROR"], "ERROR"
            )
        finally:
            RBX_OT_upload_animation.upload_complete(window_manager, temporary_directory)


class RBX_OT_copy_to_clipboard(bpy.types.Operator):
    """Copy text to the system clipboard"""

    bl_idname = "rbx.copy_to_clipboard"
    bl_label = "Copy to Clipboard"

    text: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        context.window_manager.clipboard = self.text
        self.report({"INFO"}, f"Copied: {self.text}")
        return {"FINISHED"}
