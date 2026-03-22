import sys
from pathlib import Path

_SYSTEM_DIST_PACKAGES = (
    Path("/usr/lib/python3/dist-packages"),
    Path("/usr/local/lib/python3/dist-packages"),
)


class MissingSystemDependencyError(ModuleNotFoundError):
    pass


def load_gi():
    try:
        import gi
    except ModuleNotFoundError:
        for path in _SYSTEM_DIST_PACKAGES:
            if path.exists() and str(path) not in sys.path:
                sys.path.append(str(path))

        try:
            import gi
        except ModuleNotFoundError as exc:
            raise MissingSystemDependencyError(
                "PyGObject not available. Install the system package `python3-gi`."
            ) from exc

    return gi


def require_namespace(namespace: str, version: str, package_name: str):
    gi = load_gi()

    try:
        gi.require_version(namespace, version)
    except ValueError as exc:
        raise MissingSystemDependencyError(
            f"Namespace {namespace} not available. Install the system package `{package_name}`."
        ) from exc

    return gi
