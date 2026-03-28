"""Fetches and caches the logged-in user's Roblox avatar thumbnail."""

import bpy
import os
import tempfile
import threading
import traceback

DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

_IMAGE_KEY = "__rbx_user_avatar__"
_loading = False
_loaded_for_user_id = None


def _tag_redraw():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def _fetch_in_thread(user_id):
    global _loading
    dprint("[AVATAR] thread started")
    try:
        import urllib.request
        import json
        import ssl

        try:
            import certifi
            ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            ssl_ctx = ssl.create_default_context()

        url = (
            f"https://thumbnails.roblox.com/v1/users/avatar-headshot"
            f"?userIds={user_id}&size=150x150&format=Png&isCircular=false"
        )
        dprint(f"[AVATAR] GET {url}")

        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=15) as resp:
            body = resp.read().decode()
        dprint(f"[AVATAR] thumbnail response: {body[:300]}")

        data = json.loads(body)
        entries = data.get("data", [])
        if not entries:
            dprint("[AVATAR] No entries in response — aborting.")
            _loading = False
            return

        entry = entries[0]
        image_url = entry.get("imageUrl")
        state = entry.get("state", "?")
        dprint(f"[AVATAR] state={state!r}  imageUrl={image_url!r}")

        if not image_url:
            dprint("[AVATAR] No imageUrl (Pending?) — will retry next draw.")
            _loading = False
            return

        dprint(f"[AVATAR] downloading {image_url[:80]}...")
        img_req = urllib.request.Request(image_url)
        with urllib.request.urlopen(img_req, context=ssl_ctx, timeout=15) as resp:
            img_bytes = resp.read()
        dprint(f"[AVATAR] downloaded {len(img_bytes)} bytes")

        tmp_path = os.path.join(tempfile.gettempdir(), "rbx_user_avatar.png")
        with open(tmp_path, "wb") as f:
            f.write(img_bytes)
        dprint(f"[AVATAR] saved to {tmp_path}")

        def _load_on_main_thread():
            global _loading, _loaded_for_user_id
            try:
                existing = bpy.data.images.get(_IMAGE_KEY)
                if existing:
                    bpy.data.images.remove(existing)
                img = bpy.data.images.load(tmp_path)
                img.name = _IMAGE_KEY
                img.preview_ensure()
                _loaded_for_user_id = user_id
                dprint(f"[AVATAR] image loaded  size={img.size[:]}  icon_id={img.preview.icon_id}")
                _tag_redraw()
            except Exception as e:
                print(f"[AVATAR] error loading image: {e}")
                traceback.print_exc()
            finally:
                _loading = False
            return None

        bpy.app.timers.register(_load_on_main_thread, first_interval=0.05)

    except Exception as e:
        print(f"[AVATAR] error fetching thumbnail: {e}")
        traceback.print_exc()
        _loading = False


def schedule_fetch(user_id):
    global _loading
    if _loading:
        return
    if bpy.data.images.get(_IMAGE_KEY) and _loaded_for_user_id == user_id:
        return
    dprint(f"[AVATAR] schedule_fetch — launching thread for user {user_id!r}")
    _loading = True
    t = threading.Thread(target=_fetch_in_thread, args=(user_id,), daemon=True)
    t.start()


def get_icon_id():
    img = bpy.data.images.get(_IMAGE_KEY)
    if img:
        img.preview_ensure()
        icon_id = img.preview.icon_id
        if icon_id:
            return icon_id
        _tag_redraw()
    return None


def clear():
    global _loading, _loaded_for_user_id
    _loading = False
    _loaded_for_user_id = None
    img = bpy.data.images.get(_IMAGE_KEY)
    if img:
        bpy.data.images.remove(img)
