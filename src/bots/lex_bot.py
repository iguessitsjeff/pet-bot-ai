from aws_lambda_powertools.logging import Logger
from mypy_boto3_lexv2_runtime.type_defs import RecognizeUtteranceResponseTypeDef
from src.aws.session import get_session
from src.config.loader import get_config_key
from src.model.lex_response import LexResponse

logger: Logger = Logger()


class LexBot:
    def __init__(
        self, bot_id: str = None, bot_alias_id: str = None, locale_id: str = "en_US"
    ):
        self.bot_id = bot_id if bot_id else get_config_key("LEX_BOT_ID")
        self.bot_alias_id = (
            bot_alias_id if bot_alias_id else get_config_key("LEX_BOT_ALIAS_ID")
        )
        self.locale_id = locale_id

        self.client = get_session().client("lexv2-runtime")

    def send(self, session_id: str, message: str) -> LexResponse:
        response: RecognizeUtteranceResponseTypeDef = self.client.recognize_utterance(
            botId=self.bot_id,
            botAliasId=self.bot_alias_id,
            sessionId=session_id,
            localeId=self.locale_id,
            requestContentType="text/plain;charset=utf-8",
            inputStream=message.encode(encoding="utf-8"),
        )

        logger.info(response)

        lex_response: LexResponse = LexResponse.model_validate(response)

        lex_response.decode_fields()

        return lex_response
