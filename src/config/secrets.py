import tomllib
from pydantic import BaseModel, Field

from src.aws.secrets import get_secret
from src.config.constants import APPLICATION_ENV, CWD, ConfigKey

DALLE_3_KEY_NAME = "DALLE_3_API_KEY"
TELEGRAM_TOKEN_NAME = "TELEGRAM_TOKEN"


class Secrets(BaseModel):
    dalle_3_api_key: str = Field(..., alias=DALLE_3_KEY_NAME)
    telegram_token: str = Field(..., alias=TELEGRAM_TOKEN_NAME)


def load_secrets(config: dict[ConfigKey, str]) -> Secrets:
    secrets = None
    if APPLICATION_ENV == "local":
        with open(f"{CWD}/local/sam/secrets.toml", "rb") as fp:
            secrets_map = tomllib.load(fp)
            secrets = Secrets.model_validate(secrets_map)
    else:
        secret_store: str = config.get(ConfigKey.API_KEY_STORE_NAME)
        secret_key_name: str = config.get(ConfigKey.DALLE_3_KEY_NAME)
        secrets_json = get_secret(
            key_store_name=secret_store, secret_key=secret_key_name
        )
        secrets = Secrets.model_validate_json(secrets_json)
    return secrets
