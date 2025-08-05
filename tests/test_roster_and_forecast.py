import pandas as pd
import pytest
from src.your_module import freq_holiday_7_day, staff_assignment_roster, moving_average_forecast

def test_moving_average_forecast():
    df = pd.DataFrame({
        'date': pd.date_range('2025-04-01', periods=7),
        'load_units': [10, 12, 11, 9, 13, 10, 12]
    })
    forecast = moving_average_forecast(df, target_col='load_units', window=7, forecast_days=7)
    assert all(forecast['load_units'] == pytest.approx(11.0))

def test_staff_assignment_minimum():
    forecast_df = pd.DataFrame({
        'date': pd.date_range('2025-04-21', periods=3),
        'people_required': [2, 2, 2]
    })
    staff_df = pd.DataFrame({
        'name': ['A', 'B', 'C'],
        'holiday_dates': ['', '', '']
    })
    roster_df, assignments = staff_assignment_roster(forecast_df, staff_df)
    assert all(len(assignments[d]) == 2 for d in assignments)
