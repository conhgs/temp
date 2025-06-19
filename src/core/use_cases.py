from .ports import EmailRepository, LLMExtractor
from .models import EmailRef, ExtractionResult

class ProcessEmailUseCase:
    """Orchestrates retrieval + LLM extraction."""

    def __init__(self, repo: EmailRepository, llm: LLMExtractor):
        self._repo, self._llm = repo, llm

    async def execute(self, ref: EmailRef) -> ExtractionResult:
        html = await self._repo.fetch_html(ref)
        return await self._llm.extract_json(html)
