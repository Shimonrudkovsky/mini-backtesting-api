import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.optimize import minimize

from app.models import CalendarRule, CalendarRuleTypeEnum, PortfolioFilter, PortfolioFilterTypeEnum


def dates_filter(df: DataFrame, calendar_rule: CalendarRule):
    if calendar_rule.type == CalendarRuleTypeEnum.quarterly:
        # TODO: remove hardcoded end date
        dates = pd.date_range(
            start=calendar_rule.initial_date,
            end="2025-01-22",
            freq="3ME",
        )
    elif calendar_rule.type == CalendarRuleTypeEnum.custom_dates:
        dates = calendar_rule.custom_dates

    return df.loc[dates]


def portfolio_filter(df: DataFrame, portfolio_filter: PortfolioFilter):
    if portfolio_filter.type == PortfolioFilterTypeEnum.top_n:
        values = df.values
        # Get the indices to sort rows
        partition_idx = np.argpartition(-values, portfolio_filter.top, axis=1)[:, : portfolio_filter.top]
        # Create row indices matrix
        row_indices = np.arange(len(df))[:, None]
        # Create mask of same shape as values
        mask = np.zeros_like(values, dtype=bool)
        # Set True for top positions
        mask[row_indices, partition_idx] = True
    elif portfolio_filter.type == PortfolioFilterTypeEnum.filter_by_value:
        values = df.values
        # Create mask for values less than or equal to upper bound
        mask = values <= portfolio_filter.u_bound

    # Convert back to DataFrame and apply mask
    df = pd.DataFrame(np.where(mask, values, np.nan), index=df.index, columns=df.columns)
    # Drop columns where all rows are equal to NaN
    df = df.dropna(axis=1, how='all')

    return df
