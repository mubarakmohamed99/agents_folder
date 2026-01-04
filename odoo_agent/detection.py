"""Odoo executable detection utilities."""

import os
from typing import Iterable, List, Optional, Tuple


def _default_paths() -> List[str]:
    """Return a list of common locations where odoo-bin might live."""

    return [
        "/usr/local/bin/odoo-bin",
        "/opt/odoo/odoo-bin",
        "/usr/bin/odoo-bin",
        "/home/odoo/odoo-bin",
        os.path.expanduser("~/.local/bin/odoo-bin"),
        os.path.join(os.getcwd(), "odoo-bin"),
    ]


def detect_odoo_executable(
    extra_paths: Optional[Iterable[str]] = None,
) -> Tuple[bool, str]:
    """Detect if an Odoo executable is present on the system.

    Args:
        extra_paths: Optional iterable of additional paths to check.

    Returns:
        Tuple[bool, str]: (found_flag, path_to_executable or "").
    """

    print("Detecting Odoo executable...")

    paths = _default_paths()
    if extra_paths is not None:
        paths.extend(list(extra_paths))

    for path in paths:
        if os.path.exists(path) and os.path.isfile(path) and os.access(path, os.X_OK):
            print(f"Odoo executable found at: {path}")
            return True, path

    print("No Odoo executable found in common paths.")
    return False, ""
