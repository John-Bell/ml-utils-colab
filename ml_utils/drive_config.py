# ml_utils/drive_config.py
from pathlib import Path
import os

# On Colab VMs, /content is the usual scratch area.
# Allow override via env var if you ever want something different.
DEFAULT_SA_KEY_PATH = Path(
    os.environ.get("SA_KEY_PATH", "/content/service_account.json")
)

# Default Drive folder ID; override with env var if needed.
DEFAULT_DRIVE_FOLDER_ID = os.environ.get("DEFAULT_DRIVE_FOLDER_ID", "")
