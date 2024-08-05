import os
from enum import StrEnum

CWD = os.getcwd()
CONFIG_PATH = "src/resources/config"

APPLICATION_ENV = os.environ.get("APPLICATION_ENV", "local")


class ConfigKey(StrEnum):
    LEX_BOT_ID = "LEX_BOT_ID"
    LEX_BOT_ALIAS_ID = "LEX_BOT_ALIAS_ID"
    API_KEY_STORE_NAME = "API_KEY_STORE_NAME"
    S3_STORE_BUCKET = "S3_STORE_BUCKET"
    S3_STORE_KEY_PREFIX = "S3_STORE_KEY_PREFIX"
