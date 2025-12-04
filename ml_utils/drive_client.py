# ml_utils/drive_client.py
from __future__ import annotations

from pathlib import Path
from typing import Optional, IO

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from .drive_config import DEFAULT_SA_KEY_PATH, DEFAULT_DRIVE_FOLDER_ID


class ServiceAccountDriveClient:
    """
    Thin wrapper around the Google Drive API using a service account.

    You can:
    - construct directly from a key file via from_keyfile()
    - or use create_default_client() which uses DEFAULT_SA_KEY_PATH.
    """

    def __init__(self, service, default_folder_id: str | None = None):
        self._service = service
        self._default_folder_id = default_folder_id or None

    # ---------- Construction ----------

    @classmethod
    def from_keyfile(
        cls,
        keyfile_path: str | Path,
        scopes: Optional[list[str]] = None,
        default_folder_id: Optional[str] = None,
    ) -> "ServiceAccountDriveClient":
        scopes = scopes or ["https://www.googleapis.com/auth/drive"]
        keyfile_path = Path(keyfile_path)

        creds = service_account.Credentials.from_service_account_file(
            str(keyfile_path),
            scopes=scopes,
        )
        service = build("drive", "v3", credentials=creds)
        return cls(service, default_folder_id=default_folder_id)

    # ---------- Helpers ----------

    def download_file(
        self,
        file_id: str,
        destination: str | Path | IO[bytes],
        chunk_size: int = 1024 * 1024,
    ) -> None:
        """
        Stream a file from Drive to a local path or a binary file-like object.
        """
        request = self._service.files().get_media(fileId=file_id)

        if isinstance(destination, (str, Path)):
            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            fh: IO[bytes] = dest_path.open("wb")
            close_fh = True
        else:
            fh = destination
            close_fh = False

        try:
            downloader = MediaIoBaseDownload(fh, request, chunksize=chunk_size)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        finally:
            if close_fh:
                fh.close()

    def upload_file(
        self,
        local_path: str | Path,
        folder_id: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> str:
        """
        Upload a local file to Drive.

        Returns:
            The file ID of the uploaded file.
        """
        local_path = Path(local_path)
        folder_id = folder_id or self._default_folder_id

        file_metadata: dict = {"name": local_path.name}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)

        file = (
            self._service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file["id"]

    # Add more helpers here as you need:
    # - list_files_in_folder(...)
    # - get_file_metadata(...)
    # etc.


def create_default_client(
    sa_key_path: str | Path | None = None,
    default_folder_id: str | None = None,
) -> ServiceAccountDriveClient:
    """
    Factory used by notebooks. Uses DEFAULT_SA_KEY_PATH and DEFAULT_DRIVE_FOLDER_ID
    if arguments are not provided.
    """
    sa_key_path = Path(sa_key_path or DEFAULT_SA_KEY_PATH)

    if not sa_key_path.exists():
        raise FileNotFoundError(
            f"Service account key not found at {sa_key_path}. "
            "Upload it once per runtime before calling create_default_client()."
        )

    return ServiceAccountDriveClient.from_keyfile(
        sa_key_path,
        default_folder_id=default_folder_id or DEFAULT_DRIVE_FOLDER_ID or None,
    )
