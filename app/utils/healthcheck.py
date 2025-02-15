from datetime import datetime

from fastapi import Request

from app.models.healthcheck import Checks, HealthCheck


async def check_health(request: Request) -> HealthCheck:
    return HealthCheck(
        is_sick=False,
        checks=None,
        version=request.app.version,
        start_time=request.app.state.start_time,
        up_time=datetime.now() - request.app.state.start_time,
    )
