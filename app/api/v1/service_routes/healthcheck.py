from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.models.healthcheck import HealthCheck
from app.utils.healthcheck import check_health

router = APIRouter()


@router.get(
    "/health",
    tags=["Health check"],
    summary="Returns server status.",
    response_class=JSONResponse,
    include_in_schema=False,
)
async def health(request: Request) -> HealthCheck:
    """Handler to get server status"""
    return await check_health(request=request)
