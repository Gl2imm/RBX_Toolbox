"""Checks the logged-in user's RBX Toolbox supporter game-pass ownership
and exposes the highest owned tier for display in the UI."""

import bpy
import threading
import traceback

DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

# RBX Toolbox tip game passes, ordered low -> high tier.
# (display name, game pass id)
_TIERS = [
    ("Supporter", 1292957634),
    ("Hero",      132720885),
    ("Legend",    132688311),
    ("Epic",      1292117937),
    ("Mythic",    1893442485),
]

_loading = False
_checked_for_user_id = None
_highest_tier = None  # display name string, or None if no pass owned


def _tag_redraw():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def _owns_gamepass(user_id, gamepass_id, ssl_ctx):
    import urllib.request

    url = (
        f"https://inventory.roblox.com/v1/users/{user_id}"
        f"/items/GamePass/{gamepass_id}/is-owned"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "RBX-Toolbox"})
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=15) as resp:
        body = resp.read().decode().strip().lower()
    dprint(f"[SUPPORTER] gamepass {gamepass_id} -> {body!r}")
    return body == "true"


def _fetch_in_thread(user_id):
    global _loading
    dprint("[SUPPORTER] thread started")
    try:
        import ssl

        try:
            import certifi
            ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            ssl_ctx = ssl.create_default_context()

        # Check from the highest tier down and stop at the first one owned.
        highest = None
        for name, gp_id in reversed(_TIERS):
            try:
                if _owns_gamepass(user_id, gp_id, ssl_ctx):
                    highest = name
                    break
            except Exception as exception:
                dprint(f"[SUPPORTER] check failed for {gp_id}: {exception}")

        def _store_on_main_thread():
            global _loading, _checked_for_user_id, _highest_tier
            _highest_tier = highest
            _checked_for_user_id = user_id
            _loading = False
            dprint(f"[SUPPORTER] highest tier = {highest!r}")
            _tag_redraw()
            return None

        bpy.app.timers.register(_store_on_main_thread, first_interval=0.05)

    except Exception as exception:
        print(f"[SUPPORTER] error checking game passes: {exception}")
        traceback.print_exc()
        _loading = False


def schedule_fetch(user_id):
    global _loading
    if _loading:
        return
    if _checked_for_user_id == user_id:
        return
    dprint(f"[SUPPORTER] schedule_fetch for user {user_id!r}")
    _loading = True
    t = threading.Thread(target=_fetch_in_thread, args=(user_id,), daemon=True)
    t.start()


def get_tier():
    """Returns the display name of the highest owned supporter tier, or None."""
    return _highest_tier


def clear():
    global _loading, _checked_for_user_id, _highest_tier
    _loading = False
    _checked_for_user_id = None
    _highest_tier = None
