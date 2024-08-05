from enum import StrEnum

import tomllib
from pydantic import BaseModel, Field

from src.aws.secrets import get_secret
from src.config.constants import APPLICATION_ENV, CWD, ConfigKey


class SecretKeys(StrEnum):
    DALLE_3_API_KEY = "DALLE_3_API_KEY"
    TELEGRAM_TOKEN = "TELEGRAM_TOKEN"


class Secrets(BaseModel):
    dalle_3_api_key: str = Field(..., alias=SecretKeys.DALLE_3_API_KEY)
    telegram_token: str = Field(..., alias=SecretKeys.TELEGRAM_TOKEN)


def load_secrets(config: dict[ConfigKey, str]) -> Secrets:
    secrets = None
    if APPLICATION_ENV == "local":
        with open(f"{CWD}/local/sam/secrets.toml", "rb") as fp:
            secrets_map = tomllib.load(fp)
            secrets = Secrets.model_validate(secrets_map)
    else:
        secret_store: str = config.get(ConfigKey.API_KEY_STORE_NAME)
        secrets_json = get_secret(key_store_name=secret_store)
        secrets = Secrets.model_validate_json(secrets_json)
    return secrets
