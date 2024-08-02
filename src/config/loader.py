import os

import tomllib

config: dict | None = None


def load_secrets():
    cwd = os.getcwd()
    global config

    if config is not None:
        return

    with open(f"{cwd}/local/sam/secrets.toml", "rb") as fp:
        config = tomllib.load(fp)


def get_config_key(key: str, default: str | None = None) -> str:
    return config.get(key, default)
