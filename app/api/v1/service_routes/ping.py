from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get(
    "/ping",
    tags=["Health check"],
    summary="Returns pong.",
    response_class=PlainTextResponse,
    include_in_schema=False,
)
async def ping(request: Request):
    """Handler that returns pong on ping"""
    # request.app.state.logger.info("Ping - Pong!")

    return "pong"
