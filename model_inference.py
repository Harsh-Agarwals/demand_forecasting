import pandas as pd

from loading_and_preprocessing import get_holiday_freq, get_employees_holiday_dates, load_data, preprocess_df
from train_model import train_model_2, train_model_ma, train_seasonal_model

import warnings
warnings.filterwarnings('ignore')


def get_future_dates(df):
    """
    getting date list for next 7 days
    """
    future_dates = pd.date_range(df['date'].max() + pd.Timedelta(days=1), periods=7)
    return future_dates


def freq_holiday_7_day(df, staffs):
    """
    getting holiday date of every employee
    and
    list of date of holiday for every employee

    in the dictionary format
    """
    holiday_freq = get_holiday_freq(staffs)
    future_dates = get_future_dates(df)
    holidays_future = holiday_freq.loc[holiday_freq.date.isin([i.strftime("%Y-%m-%d") for i in future_dates])]

    availability = {}

    for dt in future_dates:
        date = dt.strftime("%Y-%m-%d")
        availability[date] = 7
        if date in holidays_future.date.unique():
            availability[date] = 7 - holidays_future.loc[holidays_future.date == date, 'freq'].values[0]

    return holidays_future, availability

def get_peoples_availability(df, staffs):
    """
    get on which days each employee is having holiday

    input:
    - df: historical df
    - staffs: staff df

    output:
    people_avl: {employee_name: [date_of_holiday_list]}
    """
    peoples_avl = {}

    future_dates = get_future_dates(df)
    employees = get_employees_holiday_dates(staffs)

    for dt in future_dates:
        date = dt.strftime("%Y-%m-%d")
        peoples_avl[date] = []
        for k, v in employees.items():
            if date not in v:
                peoples_avl[date].append(k)

    return peoples_avl

def get_result_df(df, staffs, model_output):
    """
    get final dataframe after forecasting and filling up columns like people_required, people_available and overtime

    input: 
    - df
    - staffs
    - model output

    output:
    future_forecast: forecast for the next 7 days
    """
    future_dates = get_future_dates(df)
    df_future = pd.DataFrame(future_dates, columns=['date'])

    df = pd.read_csv("Historical_Load_Data.csv")
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df_new = pd.concat([df, df_future], axis=0, ignore_index=True, join='outer')

    _, availability = freq_holiday_7_day(df, staffs)

    df_new.loc[len(df_new)-7:, 'load_units'] = model_output
    df_new.loc[len(df_new)-7:, 'people_required'] = df_new.iloc[-7:]['load_units']
    df_new.loc[len(df_new)-7:, 'people_available'] = list(availability.values())

    df_new.loc[df_new.people_required > df_new.people_available, 'overtime'] = True
    df_new.loc[df_new.people_required <= df_new.people_available, 'overtime'] = False

    future_forecast = df_new.iloc[-7:].reset_index(drop=True)

    return future_forecast