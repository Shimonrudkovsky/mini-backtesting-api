from fastapi import APIRouter

from . import healthcheck, ping

service_routers = APIRouter()


service_routers.include_router(healthcheck.router)
service_routers.include_router(ping.router)
