from aws_lambda_powertools.logging import Logger
from replicate.client import Client as ReplicateClient
from src.image.store.protocols.s3_image_store import S3ImageStore
from src.utils.image import download_image

logger = Logger()


class OpenJourneyImageGenerator:
    NAME: str = "OpenJourney"
    PROMPT_PREFIX = "A graphically stunning with extensive details image of"

    def __init__(self, api_token: str):
        self.client = ReplicateClient(api_token=api_token)
        self.guidance_scale = 7

    def generate_image(self, prompt: str, image_store: S3ImageStore = None) -> bytes:
        complete_prompt: str = f"{self.PROMPT_PREFIX} {prompt}"

        request_input = {
            "prompt": complete_prompt,
            "guidance_scale": self.guidance_scale,
        }

        logger.info(f"Sending prompt to open journey: {complete_prompt}")

        open_journey_response = self.client.run(
            ref="prompthero/openjourney:ad59ca21177f9e217b9075e7300cf6e14f7e5b4505b87b9689dbd866e9768969",
            input=request_input,
        )

        image_url = "".join(open_journey_response)

        logger.info(f"Open Journey Generated image: {image_url}")

        return download_image(image_url)
