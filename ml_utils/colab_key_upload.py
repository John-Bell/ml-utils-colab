# ml_utils/colab_key_upload.py
from pathlib import Path

from .drive_config import DEFAULT_SA_KEY_PATH


def upload_service_account_key(target_path: str | Path | None = None):
    """
    Colab/Jupyter helper to upload the SA key via a FileUpload widget.

    This writes the uploaded JSON to DEFAULT_SA_KEY_PATH (or target_path).
    """
    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError as ex:
        raise RuntimeError(
            "ipywidgets/IPython are required for upload_service_account_key(). "
            "Install them or don't call this function outside a notebook."
        ) from ex

    target_path = Path(target_path or DEFAULT_SA_KEY_PATH)

    uploader = widgets.FileUpload(
        accept=".json",
        multiple=False,
        description="Upload service-account JSON",
    )
    display(uploader)

    def _on_upload_change(change):
        if not uploader.value:
            return

        # First (and only) uploaded file
        _, file_info = next(iter(uploader.value.items()))
        target_path.write_bytes(file_info["content"])
        print(f"Saved service-account key to: {target_path.resolve()}")
        uploader._counter = 0  # reset widget to avoid confusion

    uploader.observe(_on_upload_change, names="value")
    return uploader
