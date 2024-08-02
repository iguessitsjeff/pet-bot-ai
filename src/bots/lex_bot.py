from aws_lambda_powertools.logging import Logger
from mypy_boto3_lexv2_runtime.type_defs import RecognizeUtteranceResponseTypeDef
from src.aws.session import get_session
from src.model.lex_response import LexResponse

logger: Logger = Logger()


class LexBot:
    def __init__(self, bot_id: str, bot_alias_id: str, locale_id: str = "en_US"):
        self.bot_id = bot_id
        self.bot_alias_id = bot_alias_id
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
