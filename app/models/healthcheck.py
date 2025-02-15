from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Checks(BaseModel):
    s3: bool = Field(default=False)


class HealthCheck(BaseModel):
    is_sick: bool
    checks: Optional[Checks] = None
    version: str
    start_time: datetime
    up_time: timedelta

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "is_sick": False,
                    "checks": {"s3": True},
                    "version": "0.1.0",
                    "start_time": datetime.now().isoformat(),
                    "up_time": 1,
                }
            ]
        }
    )
