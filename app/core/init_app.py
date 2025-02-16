from datetime import datetime
from io import BytesIO

import numpy as np
import pandas as pd
from fastapi import FastAPI
from mypy_boto3_s3.client import S3Client

from app.adapters.s3_client import create_bucket, upload_to_s3
from app.api.v1.service_routes import service_routers
from app.core.storage import init_s3_storage
from app.models import AppConfig


def generate_dummy_data(s3_client: S3Client, bucket_name: str):
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


def init_app(app_config: AppConfig) -> FastAPI:
    app = FastAPI()
    app.state.start_time = datetime.now()

    # routes
    app.include_router(service_routers)
    app.state.start_time = datetime.now()

    # s3 client initialisation
    s3_client = init_s3_storage(app_config.s3)

    create_bucket(s3_client=s3_client, bucket_name=app_config.s3.bucket_name)
    app.state.s3_client = s3_client
    app.state.app_config = app_config

    # TODO: add environment variable to determine if dummy data is needed
    generate_dummy_data(s3_client, bucket_name=app_config.s3.bucket_name)

    return app
