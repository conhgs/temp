import os
from azure.storage.blob.aio import BlobServiceClient
from src.core.ports import EmailRepository
from src.core.models import EmailRef

class BlobStorageEmailRepository(EmailRepository):
    """Fetches an email's HTML from Azure Blob Storage."""

    def __init__(self) -> None:
        conn_str = os.environ["BLOB_CONNECTION"]
        self._container = os.environ["BLOB_CONTAINER"]
        self._client = BlobServiceClient.from_connection_string(conn_str)

    async def fetch_html(self, ref: EmailRef) -> str:
        blob = self._client.get_blob_client(self._container, ref.blob_path)
        downloader = await blob.download_blob()
        return (await downloader.readall()).decode()
