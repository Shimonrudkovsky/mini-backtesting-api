from enum import Enum

from pydantic import BaseModel, Field

from app.models import CalendarRule, PortfolioFilter, WeightingMethod


class DatasetEnum(str, Enum):
    market_capitalization = "market_capitalization"
    prices = "prices"
    volume = "volume"
    adtv_3_month = "adtv_3_month"


class BacktestRequest(BaseModel):
    dataset: DatasetEnum = Field(..., description="Identifier for a dataset, used for filtering and weighting")
    calendar_rule: CalendarRule
    portfolio_filter: PortfolioFilter
    weighting_method: WeightingMethod
