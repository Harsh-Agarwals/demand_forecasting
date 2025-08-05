from train_model import train_all_models
from loading_and_preprocessing import load_data, preprocess_df
from model_inference import get_result_df
from staff_roster import get_final_roster
import pandas as pd
from datetime import timedelta

def load_data_preprocess_and_train_model(path_df="Historical_Load_Data.csv", path_staffs_df="Staff_List_with_Holidays.csv", model_name="model2"):
    """
    final function that will do everything from
    - loading data
    - preprocessing data
    - modelling
    - getting roster and duty count for each employee

    input:
    - path_df: path of historical data
    - path_staffs_df: path of staff data
    - model_name: name of model we will use ('ma', 'model2', 'seasonal')

    output:
    - forecast: final forecast
    - roster: final roster for each day
    - duty_counts: duty count for every employee
    """
    df, staffs = load_data(path_df=path_df, path_staffs_df=path_staffs_df)
    df = preprocess_df(df)
    date = (pd.to_datetime(df.date.max()) + timedelta(7)).strftime("%Y-%m-%d")
    print(date)

    model1_output, model2_output, model3_output = train_all_models(df)

    if model_name=="ma":
        people_required = model1_output
    elif model_name=="model2":
        people_required = model2_output
    elif model_name=="seasonal":
        people_required = model3_output

    forecast = get_result_df(df, staffs, people_required)
    roster, duty_counts = get_final_roster(df, staffs, date, forecast)

    print("\n\nHere is the roster")
    print(roster)
    print("=================")
    
    print("\n\nHere is the duties count")
    print(duty_counts)
    print("=================")

    print("\n\nHere is the forecast")
    print(forecast)
    print("=================")

    return forecast, roster, duty_counts

if __name__=="__main__":
    forecast, roster, duty_counts = load_data_preprocess_and_train_model()