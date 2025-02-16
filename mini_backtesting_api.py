import uvicorn

from app.core.init_app import init_app
from app.models import AppConfig, S3Config

s3_config = S3Config(
    url="http://localhost:9000",
    aws_access_key_id="TF4QBBMadLeEiAm",
    aws_secret_access_key="k9uVR3K1LvUR66z",
    bucket_name="test",
)
app_config = AppConfig(
    port=8080,
    s3=s3_config,
)
app = init_app(app_config)


def start(app_config: AppConfig):
    """Launched with `poetry run start` at root level"""
    uvicorn.run("mini_backtesting_api:app", host="0.0.0.0", port=app_config.port, reload=True)


if __name__ == "__main__":
    start(app_config)
