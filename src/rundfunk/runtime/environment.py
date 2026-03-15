import os
import sys
from typing import Dict


_ENV_REEXEC_MARKER = "RUNDFUNK_ENV_SANITIZED"
_UNSET_IF_SNAP_ENV_VARS = (
    "LD_LIBRARY_PATH",
    "LD_PRELOAD",
    "PYTHONHOME",
    "PYTHONPATH",
    "GI_TYPELIB_PATH",
    "GIO_MODULE_DIR",
    "GSETTINGS_SCHEMA_DIR",
    "GST_PLUGIN_PATH",
    "GST_PLUGIN_PATH_1_0",
    "GST_PLUGIN_SYSTEM_PATH",
    "GST_PLUGIN_SYSTEM_PATH_1_0",
    "GST_PLUGIN_SCANNER",
    "GDK_PIXBUF_MODULEDIR",
    "GDK_PIXBUF_MODULE_FILE",
    "GTK_EXE_PREFIX",
    "GTK_IM_MODULE_FILE",
    "GTK_PATH",
    "LOCPATH",
    "XDG_DATA_HOME",
)
_PATHLIKE_IF_SNAP_ENV_VARS = (
    "XDG_DATA_DIRS",
    "XDG_CONFIG_DIRS",
)


def ensure_host_runtime_environment() -> None:
    if _is_running_inside_snap():
        return

    if os.environ.get(_ENV_REEXEC_MARKER) == "1":
        return

    if not _has_snap_pollution():
        return

    env = os.environ.copy()
    env[_ENV_REEXEC_MARKER] = "1"

    for name in _UNSET_IF_SNAP_ENV_VARS:
        if _uses_snap_path(env.get(name, "")):
            env.pop(name, None)

    for name in _PATHLIKE_IF_SNAP_ENV_VARS:
        _restore_or_filter_pathlike_env(env, name)

    os.execve(sys.executable, [sys.executable, *sys.argv], env)


def _has_snap_pollution() -> bool:
    if any(_uses_snap_path(os.environ.get(name, "")) for name in _UNSET_IF_SNAP_ENV_VARS):
        return True

    return any(
        _uses_snap_path(os.environ.get(name, "")) or f"{name}_VSCODE_SNAP_ORIG" in os.environ
        for name in _PATHLIKE_IF_SNAP_ENV_VARS
    )


def _restore_or_filter_pathlike_env(env: Dict[str, str], name: str) -> None:
    original_name = f"{name}_VSCODE_SNAP_ORIG"
    if original_name in env:
        env[name] = env[original_name]
        return

    value = env.get(name)
    if not value or not _uses_snap_path(value):
        return

    filtered_paths = [path for path in value.split(":") if not _uses_snap_path(path)]
    if filtered_paths:
        env[name] = ":".join(filtered_paths)
    else:
        env.pop(name, None)


def _uses_snap_path(value: str) -> bool:
    return "/snap/" in value


def _is_running_inside_snap() -> bool:
    return bool(os.environ.get("SNAP"))
