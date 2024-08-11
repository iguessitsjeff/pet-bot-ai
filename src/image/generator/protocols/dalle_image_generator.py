from aws_lambda_powertools.logging import Logger
from openai import OpenAI
from openai.types.image import Image
from openai.types.images_response import ImagesResponse
from src.image.store.protocol import ImageStore
from src.utils.image import download_image

logger = Logger()


class DalleImageGenerator:
    NAME: str = "Dalle 3"
    PROMPT_PREFIX = "A graphically stunning with extensive details image of"

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt: str, image_store: ImageStore = None) -> bytes:
        complete_prompt: str = f"{self.PROMPT_PREFIX} {prompt}"

        logger.info(f"Sending prompt to dall-e-3: {complete_prompt}")

        response: ImagesResponse = self.client.images.generate(
            model="dall-e-3",
            prompt=complete_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image: Image = response.data.pop()

        image_url: str | None = image.url

        if image_url is None:
            raise ValueError("Could not retrieve generated image.")

        logger.info(f"Dall e 3 Generated image: {image_url}")

        content = download_image(image_url)

        if image_store:
            self._store_image(content=content, image_store=image_store)

        return content

    def _store_image(self, content: bytes, image_store: ImageStore):
        if not image_store.save(content=content):
            logger.error("Could not store image.")
