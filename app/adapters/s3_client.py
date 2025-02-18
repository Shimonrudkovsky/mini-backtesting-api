import boto3
import boto3.exceptions
from botocore.exceptions import BotoCoreError, DataNotFoundError
from mypy_boto3_s3.client import S3Client

from app.core.logging import logger


def is_bucket_exists(s3_client: S3Client, bucket_name: str) -> bool:
    try:
        response = s3_client.list_buckets()
    except boto3.exceptions.Boto3Error:
            raise BotoCoreError(error="can't get buckets list")

    return any(bucket["Name"] == bucket_name for bucket in response["Buckets"])


def create_bucket(s3_client: S3Client, bucket_name: str) -> None:
    s3_client.list_buckets
    if not is_bucket_exists(s3_client=s3_client, bucket_name=bucket_name):
        try:
            s3_client.create_bucket(
                ACL="private",
                Bucket=bucket_name,
            )
        except boto3.exceptions.Boto3Error as err:
            raise BotoCoreError(error=f"can't create bucket {err}")


def upload_to_s3(s3_client: S3Client, bucket_name: str, file_name: str, file_content: bytes) -> None:
    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
    except boto3.exceptions.Boto3Error as err:
        logger.error(f"Storage error: {err}")
        raise BotoCoreError(error="can't upload to bucket")


def get_from_s3(s3_client: S3Client, bucket_name: str, file_name: str) -> bytes:
    try:
        objects_list = s3_client.list_objects_v2(Bucket=bucket_name).get("Contents")
    except boto3.exceptions.Boto3Error as err:
        logger.error(f"Storage error: {err}")
        raise BotoCoreError(error="can't get the file")
    if not objects_list or len(objects_list) == 0:
        logger.error(f"Storage error: can't find the file path: {bucket_name}/{file_name}")
        raise DataNotFoundError(data_path=f"{bucket_name}/{file_name}")

    response = None
    for obj in objects_list:
        if file_name == obj["Key"]:
            try:
                response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
            except boto3.exceptions.Boto3Error as err:
                logger.error(f"Storage error: {err}")
                raise BotoCoreError(error="can't get the file")

    if not response:
        raise DataNotFoundError(data_path=f"{bucket_name}/{file_name}")

    body = response.get("Body")
    if not body:
        raise DataNotFoundError

    return body.read()
