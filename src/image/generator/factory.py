from src.config.secrets import Secrets
from src.image.generator.protocol import ImageGenerator
from src.image.generator.protocols.dalle_image_generator import DalleImageGenerator

image_generator: ImageGenerator | None = None


def get_image_generator(secrets: Secrets) -> ImageGenerator:
    global image_generator
    if image_generator is None:
        image_generator = DalleImageGenerator(api_key=secrets.dalle_3_api_key)

    return image_generator
