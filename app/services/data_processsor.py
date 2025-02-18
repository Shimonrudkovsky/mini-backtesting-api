import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.optimize import minimize

from app.models import (
    CalendarRule,
    CalendarRuleTypeEnum,
    PortfolioFilter,
    PortfolioFilterTypeEnum,
    WeightingMethod,
    WeightingMethodTypeEnum,
)


def dates_filter(df: DataFrame, calendar_rule: CalendarRule) -> DataFrame:
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


def portfolio_filter(df: DataFrame, portfolio_filter: PortfolioFilter) -> DataFrame:
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


def objective(weights, values):
    return -np.sum(weights * values)  # negative because using minimize


def weights_constraint(weights):
    return np.sum(weights) - 1.0


def optimization(df: DataFrame, lower_bound: float, upper_bound: float) -> dict:
    result_dict = {}

    for idx, row in df.iterrows():
        values = row.dropna().values
        length = len(values)

        # Guess
        initial_weights = np.ones(length) / length
        # Bounds for each weight
        bounds = [(lower_bound, upper_bound) for _ in range(length)]
        # Constraint: sum of weights = 1
        constraints = [{'type': 'eq', 'fun': weights_constraint}]
        # Optimize
        result = minimize(
            objective,
            initial_weights,
            args=(values,),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        rounded_weights = {
            str(col): round(weight, 2)
            for col, weight in zip(row.dropna().index, result.x)
            if weight > 1e-6  # to eliminate values that are close to 0
        }

        if rounded_weights:
            result_dict[str(idx)] = {k: float(w) for k, w in rounded_weights.items()}

    return result_dict


def equal_weighting(df: DataFrame) -> dict:
    result_dict = {}
    for idx, row in df.iterrows():
        values = row.dropna().values
        length = len(values)
        weight = 1 / length
        weights = {
            str(col): round(weight, 3)
            for col in row.dropna().index
        }
        result_dict[str(idx)] = {k: float(w) for k, w in weights.items()}

    return result_dict


def weighting(df: DataFrame, weighting_method: WeightingMethod) -> dict:
    result = {}
    if weighting_method.type == WeightingMethodTypeEnum.equal:
        result = equal_weighting(df)
    elif weighting_method.type == WeightingMethodTypeEnum.optimized:
        result = optimization(
            df=df,
            lower_bound=weighting_method.lower_bound,
            upper_bound=weighting_method.upper_bound
        )

    return result
