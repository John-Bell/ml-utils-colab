# ml-utils-colab

Helper utilities for working with Google Drive from Colab using a service account. The package keeps the notebook-side setup light: upload a service account key once per runtime, create a Drive client, and download/upload files from a pre-shared folder.

## Features
- Minimal wrapper around the Google Drive API using a service account
- Notebook helper widget to upload your JSON key securely at runtime
- Convenience helpers to download by file name and upload local files
- Sensible defaults for Colab paths and optional per-notebook overrides

## Prerequisites
- A Google Cloud **service account** with Drive access (Editor role on the target folder is usually sufficient)
- The service account JSON key file (keep this out of source control)
- A Google Drive **folder shared with the service account** (copy the folder ID from the share link)

## Installation
Install directly from GitHub (includes the Colab extras for the upload widget):

```bash
%pip install -q "ml-utils-colab[colab] @ git+https://github.com/John-Bell/ml-utils-colab.git"
```

## Usage
Because of a notebook race condition with the upload widget, keep the setup in two cells:

**Cell 1 – upload the key if needed**
```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from ml_utils import DEFAULT_SA_KEY_PATH
from ml_utils.colab_key_upload import upload_service_account_key

if not Path(DEFAULT_SA_KEY_PATH).exists():
    print("Service account key not found – showing upload widget.")
    upload_service_account_key()
    print("Upload the key, then run the next cell to create the Drive client.")
else:
    print(f"Service account key already present at {DEFAULT_SA_KEY_PATH}")
```

**Cell 2 – create the client and use it**
```python
from ml_utils import create_default_client

FOLDER_ID = "FOLDER_ID_FROM_SHARE_LINK"
drive = create_default_client(default_folder_id=FOLDER_ID)

local_csv = drive.download_by_name("FILENAME_TO_DOWNLOAD_TO_KERNEL", show_progress=True)

dataset = pd.read_csv(local_csv)
```

## Notes
- Run the upload cell only once per runtime; the key is stored locally at `DEFAULT_SA_KEY_PATH` (or your override).
- Avoid checking the key into source control or sharing it with collaborators.
- You can call `ServiceAccountDriveClient.upload_file` to push local outputs back to the shared folder.
