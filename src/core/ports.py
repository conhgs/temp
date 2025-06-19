from abc import ABC, abstractmethod
from .models import EmailRef, ExtractionResult

class EmailRepository(ABC):
    @abstractmethod
    async def fetch_html(self, ref: EmailRef) -> str:
        """Retrieve raw HTML for the email identified by ref."""

class LLMExtractor(ABC):
    @abstractmethod
    async def extract_json(self, html: str) -> ExtractionResult:
        """Return structured data extracted from html."""
