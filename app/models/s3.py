from pydantic import BaseModel


class S3Config(BaseModel):
    url: str
    aws_access_key_id: str
    aws_secret_access_key: str
