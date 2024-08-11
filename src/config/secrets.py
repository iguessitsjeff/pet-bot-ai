import json
from enum import Enum

import tomllib
from aws_lambda_powertools.logging import Logger
from pydantic import BaseModel, Field
from src.aws.secrets import get_secret
from src.config.constants import APPLICATION_ENV, CWD

logger = Logger()


class SecretKeys(Enum):
    DALLE_3_API_KEY = "dalle-3-api-key", "DALLE_3_API_KEY"
    TELEGRAM_TOKEN = "telegram-token", "TELEGRAM_TOKEN"
    REPLICATE_API_KEY = "replicate-api-key", "REPLICATE_API_KEY"

    def __init__(self, store: str, key: str):
        self.store = store
        self.key = key


class Secrets(BaseModel):
    dalle_3_api_key: str = Field(..., alias=SecretKeys.DALLE_3_API_KEY.key)
    replicate_api_token: str = Field(..., alias=SecretKeys.REPLICATE_API_KEY.key)
    telegram_token: str = Field(..., alias=SecretKeys.TELEGRAM_TOKEN.key)


def load_secrets() -> Secrets:
    secrets = None
    if APPLICATION_ENV == "local":
        logger.info("Using local secrets.")
        with open(f"{CWD}/local/sam/secrets.toml", "rb") as fp:
            secrets_map = tomllib.load(fp)
            secrets = Secrets.model_validate(secrets_map)
    else:
        logger.info("Using AWS Secret manager.")
        secrets_map: dict = {}
        for secret in SecretKeys:
            secrets_map = secrets_map | json.loads(
                get_secret(key_store_name=secret.store)
            )
        secrets = Secrets.model_validate(secrets_map)
    return secrets
