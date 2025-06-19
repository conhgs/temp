from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class EmailRef:
    conversation_id: str
    message_id: str

    @property
    def blob_path(self) -> str:
        return f"emails/{self.conversation_id}/{self.message_id}.html"

@dataclass
class Email:
    ref: EmailRef
    html_body: str
    received_utc: datetime

@dataclass
class ExtractionResult:
    subject: str
    sender: str
    recipients: List[str]
    sent_at: Optional[datetime]
    key_value_pairs: Dict[str, Any]
