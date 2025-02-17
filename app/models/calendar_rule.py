from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from datetime import date
from enum import Enum


class CalendarRuleTypeEnum(str, Enum):
    custom_dates = "custom_dates"
    quarterly = "quarterly"


class CalendarRule(BaseModel):
    type: CalendarRuleTypeEnum
    initial_date: Optional[date] = Field(None, description="Only used for 'quarterly' rule")
    custom_dates: Optional[List[date]] = Field(None, description="Only used for 'custom_dates' rule")

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