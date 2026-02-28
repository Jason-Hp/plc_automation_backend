from __future__ import annotations

from pathlib import Path

from app.config import settings

#TODO: This need to be refactored to use S3 instead of Local

class StorageService:
    def __init__(self) -> None:
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, filename: str, payload: bytes) -> Path:
        destination = self.upload_dir / filename
        destination.write_bytes(payload)
        return destination
