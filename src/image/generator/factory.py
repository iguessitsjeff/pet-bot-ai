from src.config.loader import get_config_key
from src.image.generator.protocol import ImageGenerator
from src.image.generator.protocols.dalle_image_generator import DalleImageGenerator

image_generator: ImageGenerator | None = None


def get_image_generator() -> ImageGenerator:
    global image_generator
    if image_generator is None:
        api_key = get_config_key("DALLE_3_API_KEY")
        image_generator = DalleImageGenerator(api_key=api_key)

    return image_generator
