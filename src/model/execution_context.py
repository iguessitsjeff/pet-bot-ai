from src.config.constants import ConfigKey
from src.config.secrets import Secrets
from telebot import TeleBot


class ExecutionContext:
    def __init__(
        self, config: dict[ConfigKey, str], secrets: Secrets, tele_bot: TeleBot
    ):
        self.config = config
        self.secrets = secrets
        self.tele_bot = tele_bot
