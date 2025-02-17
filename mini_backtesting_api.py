import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "Error": "Name field is missing"}),
    )

def start(app: FastAPI, app_config: AppConfig):
    """Launched with `poetry run start` at root level"""
    app = init_app(app, app_config)
    uvicorn.run("mini_backtesting_api:app", host="0.0.0.0", port=app_config.port, reload=True)


if __name__ == "__main__":
    start(app, app_config)
