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

if "bpy" in locals():
    # Imports have run before. Need to reload the imported modules
    import importlib

    if "event_loop" in locals():
        importlib.reload(event_loop)


import bpy
from bpy.types import Operator

import sys
import subprocess
import os
import ensurepip
import shutil
import hashlib
from pathlib import Path
import traceback
import asyncio
import time
import math
import threading

# Get the project root directory path
project_root_dir = Path(__file__).parent.parent

# Set the path to the dependencies_public directory
dependencies_public_directory = project_root_dir / "dependencies_public"

_requirements_file = project_root_dir / "requirements.txt"

# Files written inside the deps folder to detect staleness
_VERSION_STAMP = dependencies_public_directory / "_installed_version"
_REQUIREMENTS_STAMP = dependencies_public_directory / "_installed_requirements_hash"
_PYTHON_STAMP = dependencies_public_directory / "_installed_python_version"

# Marker written next to (not inside) the deps folder.
# On Windows, loaded .pyd/.pyc files are locked and can't be deleted mid-session.
# This marker tells the next startup to wipe the folder before anything is imported.
_PENDING_WIPE = project_root_dir / "_pending_dep_wipe"


def _mark_pending_wipe():
    """Write the pending-wipe marker so the next startup cleans the deps folder."""
    try:
        _PENDING_WIPE.touch()
    except OSError:
        pass


def _get_addon_version():
    """Returns the current addon version string, e.g. '7.2.0'."""
    pkg_name = project_root_dir.parent.name  # e.g. 'RBX_Toolbox'
    pkg = sys.modules.get(pkg_name)
    if pkg and hasattr(pkg, "bl_info"):
        return ".".join(str(x) for x in pkg.bl_info["version"])
    return None


def _get_requirements_hash():
    """Returns the SHA256 hash of requirements.txt, or None if not found."""
    try:
        return hashlib.sha256(_requirements_file.read_bytes()).hexdigest()
    except OSError:
        return None


def _get_python_version():
    """Returns the current Python version string, e.g. '3.11' or '3.13'."""
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def needs_restart_before_install():
    """Returns True if a restart is required to wipe the stale deps folder before installing."""
    return _PENDING_WIPE.exists()


def deps_are_current():
    """
    Returns True only if dependencies are installed, match the current addon version,
    were installed from the current requirements.txt, AND were built for the current
    Python version. If stale, writes a pending-wipe marker so the next startup can
    safely delete the folder before anything is imported (avoiding Windows file locks).
    """
    if not dependencies_public_directory.exists():
        return False

    version = _get_addon_version()
    req_hash = _get_requirements_hash()
    py_version = _get_python_version()

    # No version info available — fall back to existence check
    if version is None:
        return True

    stamps_exist = (
        _VERSION_STAMP.exists()
        and _REQUIREMENTS_STAMP.exists()
        and _PYTHON_STAMP.exists()
    )
    if not stamps_exist:
        # Check if the folder has real package content or is just leftover empty dirs.
        # If empty (post-wipe), show the Install button directly — no restart needed.
        has_packages = any(
            p for p in dependencies_public_directory.iterdir()
            if p.is_dir() and not p.name.startswith("_") and not p.name.endswith(".dist-info")
        )
        if has_packages:
            print("[RBX Toolbox] Stale dependencies detected — restart required for clean reinstall.")
            _mark_pending_wipe()
        else:
            print("[RBX Toolbox] Dependency folder is empty — ready to install.")
        return False

    installed_version = _VERSION_STAMP.read_text(encoding="utf-8").strip()
    installed_req_hash = _REQUIREMENTS_STAMP.read_text(encoding="utf-8").strip()
    installed_py = _PYTHON_STAMP.read_text(encoding="utf-8").strip()

    stale = (
        installed_version != version
        or (req_hash and installed_req_hash != req_hash)
        or installed_py != py_version
    )
    if stale:
        print(
            f"[RBX Toolbox] Dependencies outdated "
            f"(addon: {installed_version}->{version}, "
            f"python: {installed_py}->{py_version}) — restart required for clean reinstall."
        )
        _mark_pending_wipe()
        return False

    return True


# Install state shared between the worker thread (writes) and the modal operator
# (reads, on the main thread).
_install_start = 0.0
_install_done = False
_install_error = None


def _run_pip_install():
    """Runs pip in a background thread so the main thread stays free to animate the
    progress bar and repaint the panel (mirrors the update-download operator). The
    previous asyncio event-loop approach was stepped on the main thread, which
    saturated it during pip's heavy phase and froze the bar / blocked redraws."""
    global _install_done, _install_error
    # suppress the brief console window pip would otherwise flash on Windows
    no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        if dependencies_public_directory.exists():
            shutil.rmtree(str(dependencies_public_directory), ignore_errors=True)
        dependencies_public_directory.mkdir(exist_ok=True)

        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], check=True,
                           creationflags=no_window)
        except subprocess.CalledProcessError:
            ensurepip.bootstrap()
            os.environ.pop("PIP_REQ_TRACKER", None)

        proc = subprocess.run(
            [
                sys.executable, "-m", "pip", "install",
                "-r", str(project_root_dir / "requirements.txt"),
                "--target", str(dependencies_public_directory),
            ],
            capture_output=True,
            creationflags=no_window,
        )
        if proc.stdout:
            print(f"INSTALLATION OUTPUT:\n{proc.stdout.decode(errors='replace')}")
        if proc.returncode != 0:
            raise RuntimeError(
                f"pip install failed (exit code {proc.returncode}).\n"
                f"{proc.stderr.decode(errors='replace').strip()}"
            )
    except Exception as exception:
        _install_error = exception
    finally:
        _install_done = True


class RBX_OT_install_dependencies(Operator):
    """Operator for installing public dependencies for the add-on"""

    bl_idname = "rbx.install_dependencies"
    bl_label = "Install Dependencies"
    bl_description = "Installs add-on dependencies in the background"

    _timer = None

    def execute(self, context):
        global _install_start, _install_done, _install_error
        rbx = context.window_manager.rbx

        rbx.is_installing_dependencies = True
        rbx.dep_install_progress = 0.0
        _install_start = time.monotonic()
        _install_done = False
        _install_error = None

        # pip runs in a background thread; a modal timer animates the bar + redraws
        self._thread = threading.Thread(target=_run_pip_install, daemon=True)
        self._thread.start()
        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type != "TIMER":
            return {"PASS_THROUGH"}

        rbx = context.window_manager.rbx
        # ease the bar toward ~95% (time-based, ~94% near 15s) and repaint the panel
        elapsed = max(0.0, time.monotonic() - _install_start)
        target = 95.0 * (1.0 - math.exp(-elapsed / 3.5))
        rbx.dep_install_progress = min(95.0, max(rbx.dep_install_progress, target))
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

        if _install_done:
            return self._finish(context)
        return {"PASS_THROUGH"}

    def _finish(self, context):
        rbx = context.window_manager.rbx
        if self._timer is not None:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
        rbx.is_installing_dependencies = False
        rbx.dep_install_progress = 0.0

        if _install_error is None:
            # Stamp version, requirements hash and Python version for staleness checks
            version = _get_addon_version()
            if version:
                _VERSION_STAMP.write_text(version, encoding="utf-8")
            req_hash = _get_requirements_hash()
            if req_hash:
                _REQUIREMENTS_STAMP.write_text(req_hash, encoding="utf-8")
            _PYTHON_STAMP.write_text(_get_python_version(), encoding="utf-8")
            _PENDING_WIPE.unlink(missing_ok=True)
            rbx.is_finished_installing_dependencies = True
            rbx.needs_restart = True
        else:
            shutil.rmtree(str(dependencies_public_directory), ignore_errors=True)
            traceback.print_exception(_install_error)
            self.report({'ERROR'}, f"Dependency install failed: {_install_error}")

        # repaint the finished state immediately (no mouse move required)
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        rbx = context.window_manager.rbx
        return not (rbx.is_finished_installing_dependencies or rbx.is_installing_dependencies)
