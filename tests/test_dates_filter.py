from app.models import CalendarRule, CalendarRuleTypeEnum
from app.services.data_processsor import dates_filter


def test_dates_filter_quarterly(df):
    calendar_rule = CalendarRule(
        type=CalendarRuleTypeEnum.quarterly,
        initial_date="2023-06-01",
    )

    filtered_df = dates_filter(df=df, calendar_rule=calendar_rule)
    result_dates = [str(ts.date()) for ts in filtered_df.index.to_list()]

    expected_dates = ["2023-06-30", "2023-09-30", "2023-12-31", "2024-03-31", "2024-06-30", "2024-09-30", "2024-12-31"]
    assert result_dates == expected_dates


def test_dates_filter_custom_dates(df):
    custom_dates = ["2023-05-17", "2023-10-30", "2023-11-12", "2024-03-31"]
    calendar_rule = CalendarRule(
        type=CalendarRuleTypeEnum.custom_dates,
        custom_dates=custom_dates,
    )

    filtered_df = dates_filter(df=df, calendar_rule=calendar_rule)
    result_dates = [str(ts.date()) for ts in filtered_df.index.to_list()]

    assert result_dates == custom_dates
