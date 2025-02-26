import os
from datetime import datetime
from io import BytesIO

import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from mypy_boto3_s3.client import S3Client

from app.adapters.s3_client import create_bucket, upload_to_s3
from app.api.v1.routes.backtest import router as backtest_router
from app.api.v1.service_routes import service_routers
from app.core.logging import logger
from app.core.storage import init_s3_storage
from app.models import AppConfig


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": ", ".join([i.get("msg") for i in exc.errors()]), "Error": "Request body error"}
        ),
    )


def generate_dummy_data(s3_client: S3Client, bucket_name: str):
    logger.info("Generating dummy data...")
    data_field_identifiers = [
        "market_capitalization",
        "prices",
        "volume",
        "adtv_3_month",
    ]

    securities = [str(i) for i in range(1000)]
    dates = pd.date_range("2020-01-01", "2025-01-22")
    for data_field_indentifier in data_field_identifiers:
        data = np.random.uniform(low=1, high=100, size=(len(dates), len(securities)))
        data_frame = pd.DataFrame(
            data,
            index=dates,
            columns=securities,
        )

        out_buffer = BytesIO(data_frame.to_parquet())

        upload_to_s3(
            s3_client=s3_client,
            bucket_name=bucket_name,
            file_name=f"{data_field_indentifier}.parquet",
            file_content=out_buffer.read(),
        )
    logger.info("Dummy data uploaded to storage.")


def init_app(app: FastAPI, app_config: AppConfig) -> FastAPI:
    logger.info("Initializing application...")
    app.state.start_time = datetime.now()

    # routes
    app.include_router(service_routers)
    app.include_router(backtest_router)

    app.state.start_time = datetime.now()

    # s3 client initialisation
    s3_client = init_s3_storage(app_config.s3)

    create_bucket(s3_client=s3_client, bucket_name=app_config.s3.bucket_name)
    app.state.s3_client = s3_client
    app.state.app_config = app_config

    dummy_data = os.getenv("DUMMY_DATA", "yes")
    if dummy_data == "yes":
        generate_dummy_data(s3_client, bucket_name=app_config.s3.bucket_name)

    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    logger.info("Application initialized.")
    return app
