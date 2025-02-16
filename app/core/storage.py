import boto3
from mypy_boto3_s3.client import S3Client

from app.models import S3Config


def init_s3_storage(s3_conf: S3Config) -> S3Client:
    return boto3.client(
        "s3",
        endpoint_url=s3_conf.url,
        aws_access_key_id=s3_conf.aws_access_key_id,
        aws_secret_access_key=s3_conf.aws_secret_access_key,
    )
