import json
import azure.functions as func
from src.core.models import EmailRef

def parse_message(msg: func.ServiceBusMessage) -> EmailRef:
    """Convert the ServiceBus message body JSON -> EmailRef."""
    body = json.loads(msg.get_body().decode())
    return EmailRef(body["ConversationId"], body["MessageId"])
