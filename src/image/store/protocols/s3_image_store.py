from uuid import uuid4

import boto3
from aws_lambda_powertools.logging import Logger
from mypy_boto3_s3.client import S3Client

logger = Logger()


class S3ImageStore:
    BUCKET = "jpalmasolutions"
    KEY_PREFIX = "openai/objects"
    SESSION = boto3.Session()

    def save(self, content: bytes) -> bool:
        s3_client: S3Client = self.SESSION.client("s3")

        id: str = uuid4().__str__()

        key: str = f"{self.KEY_PREFIX}/{id}"

        logger.info(f"Uploading new object {key} into {self.BUCKET}.")

        try:
            s3_client.put_object(Bucket=self.BUCKET, Key=key, Body=content)
            return True
        except Exception:
            logger.exception()
            return False
