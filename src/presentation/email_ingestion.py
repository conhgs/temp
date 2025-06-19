import os, json, logging, azure.functions as func
from src.presentation.blueprints import bp
from src.infrastructure.azure.sb_parser import parse_message
from src.infrastructure.azure.blob_utils import BlobStorageEmailRepository
from src.infrastructure.vertex.gemini_llm import GeminiExtractor
from src.core.use_cases import ProcessEmailUseCase

@bp.function_name("ProcessEmailServiceBusTrigger")
@bp.service_bus_queue_trigger(
    arg_name="msg",
    queue_name=os.getenv("QUEUE_NAME"),
    connection="SERVICEBUS_CONNECTION",
)
async def main(msg: func.ServiceBusMessage):
    """Azure Function entry – triggered by Service Bus queue."""
    ref = parse_message(msg)
    repo = BlobStorageEmailRepository()
    llm = GeminiExtractor()
    result = await ProcessEmailUseCase(repo, llm).execute(ref)

    logging.info("LLM extraction result: %s", json.dumps(result.__dict__, default=str))
    return json.dumps(result.__dict__, default=str)
