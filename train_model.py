import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from loading_and_preprocessing import load_data, preprocess_df

import warnings
warnings.filterwarnings('ignore')

def train_model_ma(df):
    """
    trains the model based on 7 day moving average

    input: df
    output: model trained on 7 day moving average
    """
    last_7_reqd = df['people_required'][-7:].values

    forecast_dates = pd.date_range(df['date'].max() + pd.Timedelta(days=1), periods=7)

    forecasts = []
    for i in range(7):
        forecast = int(np.mean(last_7_reqd))
        forecasts.append(forecast)
        # For iterative forecasting (rolling window with forecasts), uncomment below:
        last_7_reqd = list(last_7_reqd[1:]) + [forecast]

    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'reqd_forecast': forecasts
    })
    print("MA model training done")

    return forecasts

def train_model_2(df):
    """
    trains the model based on mean people required each day of the week

    input: df
    output: model trained on mean people required each day of the week
    """
    df['day_of_week'] = df['date'].dt.dayofweek
    dow_means = df.groupby('day_of_week')['people_required'].mean()

    future_days = [(df['date'].max() + pd.Timedelta(days=i)).dayofweek for i in range(1, 8)]
    people_required = [round(dow_means[day]) for day in future_days]
    future_dates = pd.date_range(df['date'].max() + pd.Timedelta(days=1), periods=7)

    print(future_days, people_required, future_dates)

    forecast_df = pd.DataFrame({
        'date': future_dates,
        'people_required': people_required
    })
    print("2nd model training done")

    return people_required

def train_seasonal_model(df):
    """
    trains the model based on seasonal decomposition

    input: df
    output: model trained on seasonal decomposition
    """
    # df.set_index('date', inplace=True)

    # Choosing column with demand (adjust column name if needed)
    series = df['people_required']

    # Applying seasonal decomposition
    result = seasonal_decompose(series, model='additive', period=7)  # 7 for weekly seasonality

    # get the seasonal component for the upcoming 7 days
    # We'll use the last available trend + seasonal component for forecasting

    last_trend = result.trend.dropna()[-7:].mean()    # mean of last week trend
    seasonal_vals = result.seasonal[-7:]              # last 7 days of seasonality

    # Forecast for next 7 days = last trend + seasonal pattern
    forecast = last_trend + seasonal_vals.values
    future_dates = pd.date_range(df['date'].max() + pd.Timedelta(days=1), periods=7)

    forecast_df2 = pd.DataFrame({
        'date': future_dates,
        'people_required': forecast.round().astype(int)
    })
    print("Seasonal model training done")

    return forecast.round().astype(int)

def train_all_models(df):
    """
    a go to function for training all the models on the historical data

    input: dataframe df
    output: results of all the model, trained on df
    """
    model1_output = train_model_ma(df)
    model2_output = train_model_2(df)
    model3_output = train_seasonal_model(df)

    print("All models trained")

    return model1_output, model2_output, model3_output

