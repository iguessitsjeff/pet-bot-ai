from io import BytesIO

from src.bots.lex_bot import LexBot
from src.config.constants import ConfigKey
from src.image.generator.factory import get_all_generators
from src.image.generator.protocol import ImageGenerator
from src.image.store.protocols.s3_image_store import S3ImageStore
from src.model.execution_context import ExecutionContext
from src.model.lex_response import LexResponse, LexStates
from telebot import TeleBot
from telebot.types import InputFile


class MessageImpl:
    def __init__(self, execution_context: ExecutionContext):
        self.lex_bot: LexBot = LexBot(
            bot_id=execution_context.config.get(ConfigKey.LEX_BOT_ID),
            bot_alias_id=execution_context.config.get(ConfigKey.LEX_BOT_ALIAS_ID),
        )
        self.tele_bot: TeleBot = TeleBot(token=execution_context.secrets.telegram_token)

    def message(self, chat_id: int, message: str, execution_context: ExecutionContext):
        lex_response: LexResponse = self.lex_bot.send(
            session_id=str(chat_id), message=message
        )
        text_back: str = lex_response.get_text_back()

        self.tele_bot.send_message(chat_id=chat_id, text=text_back)
        if (
            lex_response.unpacked_session_state.intent.state
            is LexStates.READY_FOR_FULLFILLMENT
            and lex_response.unpacked_session_state.intent.name != "FallbackIntent"
        ):
            prompt: str = lex_response.get_prompt()

            image_generators: list[ImageGenerator] = get_all_generators(
                execution_context.secrets
            )
            image_store: S3ImageStore = S3ImageStore(execution_context.config)

            for generator in image_generators:
                image_content: bytes = generator.generate_image(
                    prompt=prompt, image_store=image_store
                )
                execution_context.tele_bot.send_photo(
                    caption=generator.NAME,
                    chat_id=chat_id,
                    photo=InputFile(BytesIO(image_content)),
                )
