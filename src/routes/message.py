from aws_lambda_powertools.event_handler.router import APIGatewayRouter
from aws_lambda_powertools.logging import Logger

from src.impl.message_impl import MessageImpl
from src.model.execution_context import ExecutionContext
from src.model.telegram_message import TelegramEvent

router = APIGatewayRouter()
logger = Logger()


@router.post("/")
def message():
    execution_context: ExecutionContext = router.context.get("execution_context", None)
    event_body: str | None = router.current_event.body
    if event_body is None:
        return {}
    tel_event: TelegramEvent = TelegramEvent.model_validate_json(event_body)
    logger.info(tel_event)
    message_impl: MessageImpl = MessageImpl(execution_context=execution_context)
    message_impl.message(
        chat_id=tel_event.message.chat.id,
        message=tel_event.message.text,
        execution_context=execution_context,
    )
    
    return {}