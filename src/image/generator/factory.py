import random

from aws_lambda_powertools.logging import Logger
from src.config.secrets import Secrets
from src.image.generator.protocol import ImageGenerator
from src.image.generator.protocols.dalle_image_generator import DalleImageGenerator
from src.image.generator.protocols.open_journey_image_generator import (
    OpenJourneyImageGenerator,
)

logger = Logger()


def get_image_generator(secrets: Secrets) -> ImageGenerator:
    coin_flip = random.randint(0, 1)

    if coin_flip == 0:
        logger.info("Using Dalle3")
        return DalleImageGenerator(api_key=secrets.dalle_3_api_key)
    else:
        logger.info("Using OJ")
        return OpenJourneyImageGenerator(api_token=secrets.replicate_api_token)


def get_all_generators(secrets: Secrets) -> list[ImageGenerator]:
    generators: list = []
    generators.append(DalleImageGenerator(api_key=secrets.dalle_3_api_key))
    # generators.append(OpenJourneyImageGenerator(api_token=secrets.replicate_api_token))
    return generators
