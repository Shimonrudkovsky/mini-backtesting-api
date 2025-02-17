import pandas as pd
from pandas import DataFrame
from enum import Enum
from app.models import CalendarRule, CalendarRuleTypeEnum


def dates_filter(df: DataFrame, calendar_rule: CalendarRule):
    dates = None
    if calendar_rule.type == CalendarRuleTypeEnum.quarterly:
        #TODO: remove hardcoded end date
        dates = pd.date_range(
            start=calendar_rule.initial_date,
            end="2025-01-22",
            freq="3ME",
        )
    elif calendar_rule.type == CalendarRuleTypeEnum.custom_dates:
        dates = calendar_rule.custom_dates
    
    return df.loc[dates]
