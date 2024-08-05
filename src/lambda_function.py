import telebot
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.config.constants import ConfigKey
from src.config.loader import load_config
from src.config.secrets import Secrets, load_secrets
from src.model.execution_context import ExecutionContext
from src.routes import message

logger = Logger()
config: dict[ConfigKey, str] = load_config()
secrets: Secrets = load_secrets(config=config)

app = APIGatewayRestResolver()
app.include_router(message.router, prefix="/message")
tele_bot = telebot.TeleBot(token=secrets.telegram_token)


@app.get("/health")
def health():
    return {}


def lambda_handler(event: dict, context: LambdaContext):
    try:
        logger.info(event)
        execution_context = ExecutionContext(
            config=config, secrets=secrets, tele_bot=tele_bot
        )
        app.append_context(execution_context=execution_context)
        app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
    return {}
