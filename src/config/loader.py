import tomllib
from src.config.constants import APPLICATION_ENV, CONFIG_PATH, CWD, ConfigKey


def load_config() -> dict:
    config = {}
    initial_config = {}
    env_config = {}

    with open(f"{CWD}/{CONFIG_PATH}/config.toml", "rb") as fp:
        initial_config = tomllib.load(fp)

    with open(f"{CWD}/{CONFIG_PATH}/{APPLICATION_ENV}.toml", "rb") as fp:
        env_config = tomllib.load(fp)

    overall_config = initial_config | env_config
    for key in ConfigKey:
        config[key] = overall_config.get(key, None)

    return config
