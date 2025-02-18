from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class PortfolioFilterTypeEnum(str, Enum):
    top_n = "top_n"
    filter_by_value = "filter_by_value"


class PortfolioFilter(BaseModel):
    type: PortfolioFilterTypeEnum
    top: Optional[int] = Field(None, gt=0, description="Required for 'top_n' filter")
    u_bound: Optional[float] = Field(None, description="Upper bound for values. Required for 'filter_by_value' filter")

    @model_validator(mode="before")
    def check_exclusive_filter_fields(cls, values):
        type_ = values.get("type")
        top_ = values.get("top")
        u_bound_ = values.get("u_bound")

        if type_ == "top_n" and top_ is None:
            raise ValueError("For 'top_n' filter, 'top' must be provided.")
        if type_ == "filter_by_value" and u_bound_ is None:
            raise ValueError("For 'filter_by_value' filter, 'u_bound' must be provided.")
        if top_ is not None and u_bound_ is not None:
            raise ValueError("'top' and 'u_bound' are mutually exclusive.")

        return values
