import os, json, asyncio
from vertexai.preview.language_models import ChatModel
from src.core.ports import LLMExtractor
from src.core.models import ExtractionResult

_SYSTEM_PROMPT = (
    "You are an AI assistant that extracts structured data from HTML emails. "
    "Respond ONLY with JSON using this schema:\n"
    "{\n"
    "  \"subject\": string,\n"
    "  \"sender\": string,\n"
    "  \"recipients\": [string],\n"
    "  \"sent_at\": ISO8601 string or null,\n"
    "  \"key_value_pairs\": { string: string | number | null }\n"
    "}"
)

class GeminiExtractor(LLMExtractor):
    """Vertex AI Gemini adapter implementing LLMExtractor."""

    def __init__(self) -> None:
        project = os.environ["VERTEX_PROJECT"]
        location = os.getenv("VERTEX_LOCATION", "us-central1")
        self._chat = (
            ChatModel.from_pretrained(
                "gemini-1.5-pro-preview",
                project=project,
                location=location,
            ).start_chat()
        )

    async def extract_json(self, html: str) -> ExtractionResult:
        prompt = f"{_SYSTEM_PROMPT}\n\nHTML:\n{html}"
        # ChatModel API is sync → offload to thread
        response_text = await asyncio.to_thread(
            lambda: self._chat.send_message(prompt).text
        )
        data = json.loads(response_text)
        return ExtractionResult(**data)
