import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def load_data(path_df, path_staffs_df):
    """
    function to load the historical and staffs data

    input: path to historical data and path to staffs data
    output: historical and staffs dataframes
    """
    df = pd.read_csv(path_df)
    staffs = pd.read_csv(path_staffs_df)

    return df, staffs

def preprocess_df(df):
    """
    function that converts date column in historical df to datetime datatype and drop load_units column since it is same as people_required column

    input: historical df
    output: updated historical df
    """
    df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y")
    df.drop(columns=['load_units'], inplace=True)

    return df

def get_employees_holiday_dates(staffs):
    """
    function that converts holiday data in staffs dataframe as separate entity which were earlier joined by ","

    input: staffs dataframe
    output: {employee: [dates list]} format dictionary
    """
    employees = staffs.set_index('name').drop(columns=['employee_id']).to_dict()['holidays']

    for k, v in employees.items():
        employees[k] = v.split(",")

    return employees

def get_holiday_freq(staffs):
    """
    get the holiday data and makes a dataframe having total people being absent that date.

    input: staffs data
    output: dataframe with holiday dates and total count of people in leave that day
    """
    employees = get_employees_holiday_dates(staffs)
    holidays = [v for v in employees.values()]
    holidays = [i.strip() for j in holidays for i in j]
    holidays = sorted(holidays)

    holiday_freq = {}
    for dt in set(holidays):
        holiday_freq[dt] = holidays.count(dt)

    holiday_freq = pd.DataFrame({'freq': holiday_freq})
    holiday_freq.reset_index(inplace=True)
    holiday_freq.rename(columns={'index': 'date'}, inplace=True)
    holiday_freq.sort_values(by=['date'], ascending=True, inplace=True)
    holiday_freq.reset_index(drop=True, inplace=True)

    return holiday_freq