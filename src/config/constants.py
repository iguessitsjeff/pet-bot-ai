import os
from enum import StrEnum

CWD = os.getcwd()
CONFIG_PATH = "src/resources/config"

APPLICATION_ENV = os.environ.get("APPLICATION_ENV", "local")


class ConfigKey(StrEnum):
    LEX_BOT_ID = "LEX_BOT_ID"
    LEX_BOT_ALIAS_ID = "LEX_BOT_ALIAS_ID"
    API_KEY_STORE_NAME = "API_KEY_STORE_NAME"
    DALLE_3_KEY_NAME = "DALLE_3_KEY_NAME"
    TELEGRAM_TOKEN_NAME = "TELEGRAM_TOKEN_NAME"
