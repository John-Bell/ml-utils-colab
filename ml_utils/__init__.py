# ml_utils/__init__.py
"""
Shared utilities for using a service account with Google Drive in Colab.

Core exports are UI-agnostic so you can use them from scripts/tests as well.
"""

from .drive_client import ServiceAccountDriveClient, create_default_client
from .drive_config import DEFAULT_SA_KEY_PATH, DEFAULT_DRIVE_FOLDER_ID

__all__ = [
    "ServiceAccountDriveClient",
    "create_default_client",
    "DEFAULT_SA_KEY_PATH",
    "DEFAULT_DRIVE_FOLDER_ID",
]
