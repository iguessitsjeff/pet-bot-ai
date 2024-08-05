from uuid import uuid4

from aws_lambda_powertools.logging import Logger
from mypy_boto3_s3.client import S3Client

from src.aws.session import get_session
from src.config.constants import ConfigKey

logger = Logger()


class S3ImageStore:
    def __init__(self, config: dict[ConfigKey, str]):
        self.BUCKET = config.get(ConfigKey.S3_STORE_BUCKET)
        self.KEY_PREFIX = config.get(ConfigKey.S3_STORE_KEY_PREFIX)

    def save(self, content: bytes) -> bool:
        s3_client: S3Client = get_session().client("s3")

        id: str = uuid4().__str__()

        key: str = f"{self.KEY_PREFIX}/{id}"

        logger.info(f"Uploading new object {key} into {self.BUCKET}.")

        try:
            s3_client.put_object(Bucket=self.BUCKET, Key=key, Body=content)
            return True
        except Exception as e:
            logger.exception(e)
            return False
