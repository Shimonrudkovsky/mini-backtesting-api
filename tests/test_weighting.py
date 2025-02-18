from app.models import WeightingMethod, WeightingMethodTypeEnum
from app.services.data_processsor import equal_weighting, optimization, weighting


def test_optimization(filtered_df):
    result = optimization(df=filtered_df, lower_bound=0.1, upper_bound=0.42)

    expected = {
        "2021-01-17": {"1": 0.1, "3": 0.1, "5": 0.1, "6": 0.28, "7": 0.42},
        "2022-02-27": {"1": 0.42, "3": 0.38, "4": 0.1, "6": 0.1},
        "2023-03-29": {"3": 0.28, "4": 0.42, "5": 0.1, "6": 0.1, "7": 0.1},
    }

    assert result == expected


def test_equal_weighting(filtered_df):
    result = equal_weighting(filtered_df)

    expected = {
        "2021-01-17": {"1": 0.2, "3": 0.2, "5": 0.2, "6": 0.2, "7": 0.2},
        "2022-02-27": {"1": 0.25, "3": 0.25, "4": 0.25, "6": 0.25},
        "2023-03-29": {"3": 0.2, "4": 0.2, "5": 0.2, "6": 0.2, "7": 0.2}
    }

    assert result == expected


def test_weighting(filtered_df):
    weighting_method = WeightingMethod(
        type=WeightingMethodTypeEnum.optimized,
        lower_bound=0.15,
        upper_bound=0.7,
    )

    result = weighting(filtered_df, weighting_method=weighting_method)

    expected = {
        "2021-01-17": {"1": 0.15, "3": 0.15, "5": 0.15, "6": 0.15, "7": 0.4},
        "2022-02-27": {"1": 0.55, "3": 0.15, "4": 0.15, "6": 0.15},
        "2023-03-29": {"3": 0.15, "4": 0.4, "5": 0.15, "6": 0.15, "7": 0.15}
    }

    assert result == expected
