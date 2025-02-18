from typing import Optional

from pydantic import BaseModel


class BacktestReply(BaseModel):
    data: dict[str, Optional[dict[str, float]]]
