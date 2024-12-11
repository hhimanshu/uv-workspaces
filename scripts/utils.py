import os
import sys
from pathlib import Path


def get_workspace_root():
    """
    Gets the root directory of the workspace.
    Used by other scripts to ensure consistent path handling.
    """
    return Path(__file__).parent.parent


def ensure_virtualenv():
    """
    Ensures we're running in a virtual environment.
    Prevents accidental system-wide package installations.
    """
    if not os.environ.get("VIRTUAL_ENV"):
        print("Please activate a virtual environment first")
        sys.exit(1)
