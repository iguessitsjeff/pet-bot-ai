from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.data_classes import SNSEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@event_source(data_class=SNSEvent)
def lambda_handler(event: SNSEvent, context: LambdaContext):
    # Multiple records can be delivered in a single event
    print(event)
