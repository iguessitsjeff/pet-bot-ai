from io import BytesIO

import telebot
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from telebot.types import InputFile

from src.bots.lex_bot import LexBot
from src.config.constants import ConfigKey
from src.config.loader import load_config
from src.config.secrets import Secrets, load_secrets
from src.image.generator.factory import get_image_generator
from src.image.generator.protocol import ImageGenerator
from src.image.store.protocols.s3_image_store import S3ImageStore
from src.model.lex_response import LexResponse, LexStates
from src.model.telegram_message import TelegramEvent

logger = Logger()

config: dict[ConfigKey, str] = load_config()
secrets: Secrets = load_secrets(config=config)

app = APIGatewayRestResolver()
tele_bot = telebot.TeleBot(token=secrets.telegram_token)


@app.get("/health")
def health():
    return {}


@app.post("/telegram")
def telegram():
    event_body: str | None = app.current_event.body
    if event_body is None:
        return {}
    tel_event: TelegramEvent = TelegramEvent.model_validate_json(event_body)
    logger.info(tel_event)

    lex_bot: LexBot = LexBot(
        bot_id=config.get(ConfigKey.LEX_BOT_ID),
        bot_alias_id=config.get(ConfigKey.LEX_BOT_ALIAS_ID),
    )
    lex_response: LexResponse = lex_bot.send(
        session_id=str(tel_event.message.chat.id), message=tel_event.message.text
    )

    text_back: str = lex_response.get_text_back()

    tele_bot.send_message(chat_id=tel_event.message.chat.id, text=text_back)

    if (
        lex_response.unpacked_session_state.intent.state
        is LexStates.READY_FOR_FULLFILLMENT
    ):
        prompt: str = lex_response.get_prompt()

        image_generator: ImageGenerator = get_image_generator(secrets)
        image_store: S3ImageStore = S3ImageStore()
        image_content: bytes = image_generator.generate_image(
            prompt=prompt, image_store=image_store
        )
        tele_bot.send_photo(
            chat_id=tel_event.message.chat.id, photo=InputFile(BytesIO(image_content))
        )


def lambda_handler(event: dict, context: LambdaContext):
    app.resolve(event, context)
    return {}
