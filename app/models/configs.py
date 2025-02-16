from pydantic import BaseModel


class S3Config(BaseModel):
    url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    bucket_name: str


class AppConfig(BaseModel):
    port: int
    s3: S3Config
