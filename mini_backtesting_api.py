import os

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.init_app import init_app
from app.models import AppConfig, S3Config

s3_config = S3Config(
    url=os.getenv("S3_ENDPOINT", "http://s3:9000"),
    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    bucket_name=os.getenv("S3_BUCKET_NAME", "test"),
)
app_config = AppConfig(
    port=int(os.getenv("APP_PORT", 8080)),
    s3=s3_config,
)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": ", ".join([i.get("msg") for i in exc.errors()]), "Error": "Request body error"}
        ),
    )

app = init_app(app, app_config)


def start(app: FastAPI, app_config: AppConfig):
    """Launched with `poetry run start` at root level"""
    uvicorn.run("mini_backtesting_api:app", host="0.0.0.0", port=app_config.port, reload=True)


if __name__ == "__main__":
    start(app, app_config)
