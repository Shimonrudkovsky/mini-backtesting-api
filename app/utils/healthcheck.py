from datetime import datetime

from botocore.exceptions import BotoCoreError
from fastapi import Request

from app.adapters.s3_client import is_bucket_exists
from app.models.healthcheck import Checks, HealthCheck


async def check_health(request: Request) -> HealthCheck:
    try:
        s3_check = is_bucket_exists(request.app.state.s3_client, request.app.state.app_config.s3.bucket_name)
    except BotoCoreError:
        s3_check = False
    checks = Checks(s3=s3_check)
    return HealthCheck(
        is_sick=False if s3_check else True,
        checks=checks,
        version=request.app.version,
        start_time=request.app.state.start_time,
        up_time=datetime.now() - request.app.state.start_time,
    )
