from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class WeightingMethodTypeEnum(str, Enum):
    equal = "equal"
    optimized = "optimized"


class WeightingMethod(BaseModel):
    type: WeightingMethodTypeEnum
    lower_bound: Optional[float] = Field(None, gt=0, description="Lower bound for optimized weighting")
    upper_bound: Optional[float] = Field(None, gt=0, description="Upper bound for optimized weighting")

    @model_validator(mode="before")
    def check_optimized_weighting(cls, values):
        type_ = values.get("type")
        lower_bound_ = values.get("lower_bound")
        upper_bound_ = values.get("upper_bound")

        if type_ == "optimized" and (lower_bound_ is None or upper_bound_ is None):
            raise ValueError("For 'optimized' weighting, both 'lower_bound' and 'upper_bound' must be provided.")

        return values
