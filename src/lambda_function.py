from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.data_classes import SNSEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.config.loader import load
from src.image.generator.factory import get_image_generator
from src.image.generator.protocol import ImageGenerator
from src.image.store.protocols.s3_image_store import S3ImageStore
from src.model.message import Message

logger = Logger()


@event_source(data_class=SNSEvent)
def lambda_handler(event: SNSEvent, context: LambdaContext):
    # Multiple records can be delivered in a single event
    for record in event.records:
        load()
        message: Message = Message.model_validate_json(record.sns.message)

        image_generator: ImageGenerator = get_image_generator()
        image_store: S3ImageStore = S3ImageStore()

        image_generator.generate_image(prompt=message.prompt, image_store=image_store)
