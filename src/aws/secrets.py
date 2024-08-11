from aws_lambda_powertools.logging import Logger
from botocore.exceptions import ClientError
from src.aws.session import get_session

logger = Logger()


def get_secret(key_store_name: str, region_name: str = "us-east-1") -> str:
    # Create a Secrets Manager client
    session = get_session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=key_store_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secrets: str = get_secret_value_response["SecretString"]

    return secrets
