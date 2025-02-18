import pandas as pd

from app.models import PortfolioFilter, PortfolioFilterTypeEnum
from app.services.data_processsor import portfolio_filter


def test_portfolio_filter_top_n(mini_df):
    p_filter_model = PortfolioFilter(
        type=PortfolioFilterTypeEnum.top_n,
        top=5,
    )

    result = portfolio_filter(mini_df, p_filter_model)

    expected = pd.DataFrame(
        data=[
            [0.4, 0.7, None, 0.9, 0.22, 0.99],
            [0.7, 0.5, 0.4, 0.3, 0.2, None],
            [None, 0.33, 0.44, 0.55, 0.66, 0.77],
        ],
        index=["2021-01-17", "2022-02-27", "2023-03-29"],
        columns=["1", "3", "4", "5", "6", "7"],
    )

    assert result.equals(expected)


def test_portfolio_filter_filter_by_value(mini_df):
    p_filter_model = PortfolioFilter(
        type=PortfolioFilterTypeEnum.filter_by_value,
        u_bound=0.3,
    )

    result = portfolio_filter(mini_df, p_filter_model)

    expected = pd.DataFrame(
        data=[
            [None, 0.1, 0.2, None, 0.22, None],
            [None, 0.1, None, 0.3, 0.2, 0.1],
            [0.11, 0.22, None, None, None, None],
        ],
        index=["2021-01-17", "2022-02-27", "2023-03-29"],
        columns=["1", "2", "4", "5", "6", "7"],
    )

    assert result.equals(expected)
