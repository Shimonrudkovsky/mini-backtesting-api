from io import BytesIO

import pandas as pd
from botocore.exceptions import BotoCoreError, DataNotFoundError
from fastapi import APIRouter, Request

from app.adapters import s3_client
from app.schemas.errors import DataNotFoundException, StorageError
from app.schemas.requests import BacktestRequest
from app.schemas.responses import BacktestReply
from app.services import data_processsor

router = APIRouter()


@router.post(
    "/backtest",
    tags=["Backtest"],
    summary="Runs backtest on historical data.",
    response_model=BacktestReply,
)
def backtest(request: Request, request_body: BacktestRequest):
    try:
        data = BytesIO(s3_client.get_from_s3(
            request.app.state.s3_client,
            bucket_name=request.app.state.app_config.s3.bucket_name,
            file_name=f"{request_body.dataset.value}.parquet",
        ))
    except DataNotFoundError:
        raise DataNotFoundException()
    except BotoCoreError:
        raise StorageError()

    df = pd.read_parquet(data)

    # filter dates
    df = data_processsor.dates_filter(df=df, calendar_rule=request_body.calendar_rule)

    # filter values
    df = data_processsor.portfolio_filter(df=df, portfolio_filter=request_body.portfolio_filter)

    # getting weights
    result = data_processsor.weighting(df=df, weighting_method=request_body.weighting_method)

    return {"data": result}
