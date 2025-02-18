from datetime import datetime

from fastapi import Request

from app.adapters.s3_client import is_bucket_exists
from app.models.healthcheck import Checks, HealthCheck


async def check_health(request: Request) -> HealthCheck:
    checks = Checks(s3=is_bucket_exists(request.app.state.s3_client, request.app.state.app_config.s3.bucket_name))
    return HealthCheck(
        is_sick=False,
        checks=checks,
        version=request.app.version,
        start_time=request.app.state.start_time,
        up_time=datetime.now() - request.app.state.start_time,
    )
