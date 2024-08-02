from aws_lambda_powertools.logging import Logger

logger: Logger = Logger()


class SmsMessenger:
    def __init__(self):
        pass

    def send_messages(
        messages: list[str], destination_number: str, origination_number: str
    ):
        for message in messages:
            logger.info(message)
