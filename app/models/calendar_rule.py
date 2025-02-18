from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator, field_validator


class CalendarRuleTypeEnum(str, Enum):
    custom_dates = "custom_dates"
    quarterly = "quarterly"


class CalendarRule(BaseModel):
    type: CalendarRuleTypeEnum
    initial_date: Optional[date] = Field(None, description="Only used for 'quarterly' rule")
    custom_dates: Optional[List[date]] = Field(None, description="Only used for 'custom_dates' rule")

    @field_validator('initial_date')
    def validate_initial_date(cls, v):
        max_date = date(2025, 1, 22)
        if v and v > max_date:
            raise ValueError(f"initial_date cannot be greater than {max_date}")
        return v

    @field_validator('custom_dates')
    def validate_custom_dates(cls, v):
        max_date = date(2025, 1, 22)
        if v:
            for date_item in v:
                if date_item > max_date:
                    raise ValueError(f"custom_dates cannot contain dates greater than {max_date}")
        return v

    @model_validator(mode="before")
    def check_exclusive_calendar_fields(cls, values):
        type_ = values.get("type")
        initial_date = values.get("initial_date")
        custom_dates = values.get("custom_dates")

        if type_ == "quarterly" and initial_date is None:
            raise ValueError("For 'quarterly' rule, 'initial_date' must be provided.")
        if type_ == "custom_dates" and (not custom_dates or len(custom_dates) == 0):
            raise ValueError("For 'custom_dates' rule, 'custom_dates' must be provided.")
        if initial_date and custom_dates:
            raise ValueError("'initial_date' and 'custom_dates' are mutually exclusive.")

        return values
