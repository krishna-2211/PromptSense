from pathlib import Path

from app.mcp.filesystem_client import FilesystemMCPClient


class FileContextAdapter:
    def __init__(self, upload_dir: str = "uploads") -> None:
        self.upload_dir = Path(upload_dir)
        self.client = FilesystemMCPClient(allowed_dir=str(self.upload_dir.resolve()))

    def get_context(self, file_id: str) -> str:
        file_path = (self.upload_dir / file_id).resolve()
        return self.client.read_file_text(str(file_path))