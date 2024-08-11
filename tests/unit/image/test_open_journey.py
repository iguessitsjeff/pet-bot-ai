from pytest_mock import MockerFixture
from src.image.generator.protocols.open_journey_image_generator import (
    OpenJourneyImageGenerator,
)
from src.image.store.protocols.s3_image_store import S3ImageStore


def test_temp(mocker: MockerFixture):
    s3_mocker = mocker.patch.object(S3ImageStore, "save")
    oj = OpenJourneyImageGenerator("REPLACEME")
    prompt = "vibrant butterfly"
    oj.generate_image(prompt=prompt, image_store=s3_mocker)
