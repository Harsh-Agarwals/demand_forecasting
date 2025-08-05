import pandas as pd

from model_inference import get_peoples_availability, get_result_df
from loading_and_preprocessing import load_data, preprocess_df
from datetime import datetime, timedelta
from collections import Counter

import warnings
warnings.filterwarnings('ignore')

def chose_people(df, staffs, date, model_output):
    """
    This function is responsible for doing caluclations and returning the roster based on the logics:

    (As provided in the question)
    For each day in the forecasted week:
    Identify available staff (not on holiday and didn’t work yesterday, unless overtime)
    - Sort them by how many days they’ve already worked (fewest first)
    - If load > available staff, flag “overtime” and allow reusing who worked yesterday

    Input: 
    - df: historical dataframe
    - staffs: staffs holiday dataframe
    - date: date for which we are finding the roster

    Output:
    - counts: count of every duties of each staff
    - roster: roster day wise
    """

    peoples_avl = get_peoples_availability(df, staffs)
    print('----here---')
    future_forecast = model_output
    print(future_forecast)

    # We will store our duties in dt_full dictionary based on dates
    print(peoples_avl)
    dt_full = {}
    for v, k in peoples_avl.items():
        dt_full[v] = [] # setting up dt_full

    # pdf is rows from starting to last date (it will be used to calculate total counts till this point)
    pdf = future_forecast.loc[future_forecast.date< pd.to_datetime(date, format="%Y-%m-%d")]
    # counts is the dictionary storing counts of appearance of people
    counts = {}
    # initializing counts
    for n in staffs.name.unique():
        counts[n] = 0

    # counting and making dt_full for all rows till last date
    i_value = 0
    for i in range(len(pdf)):
        print(i)
        i_value = i
        x = pdf.iloc[i, :]
        if x['overtime'] == True:
            for ppl in peoples_avl[x.date.strftime("%Y-%m-%d")]:
                counts[ppl] += 1
            dt_full[x.date.strftime("%Y-%m-%d")] = peoples_avl[x.date.strftime("%Y-%m-%d")]
        else:
            if i==0:
                dt_full[x.date.strftime("%Y-%m-%d")] = peoples_avl[x.date.strftime("%Y-%m-%d")][:x.people_required]
            else:
                dminus = pd.to_datetime(x.date, format="%Y-%m-%d") - timedelta(1)
                not_common = set(peoples_avl[x.date.strftime("%Y-%m-%d")]) - set(dt_full[dminus.strftime("%Y-%m-%d")]).intersection(set(peoples_avl[x.date.strftime("%Y-%m-%d")]))
                first_values = list(not_common)
                first_values = sorted(first_values, key=lambda o: counts[o], reverse=False)
                sorted_names = sorted(peoples_avl[x.date.strftime("%Y-%m-%d")], key=lambda o: counts[o], reverse=False)
                sorted_names = [i for i in sorted_names if i not in first_values]

                sorted_names = first_values + sorted_names
                dt_full[x.date.strftime("%Y-%m-%d")] = sorted_names[:int(x.people_required)]
            for name in dt_full[x.date.strftime("%Y-%m-%d")]:
                counts[name] += 1

    # counting and making dt_full for the last row
    x = future_forecast.iloc[i_value+1, :]
    if x['overtime'] == True:
        for ppl in peoples_avl[x.date.strftime("%Y-%m-%d")]:
            counts[ppl] += 1
        dt_full[x.date.strftime("%Y-%m-%d")] = peoples_avl[x.date.strftime("%Y-%m-%d")]
    else:
        dminus = pd.to_datetime(x.date, format="%Y-%m-%d") - timedelta(1)
        not_common = set(peoples_avl[x.date.strftime("%Y-%m-%d")]) - set(dt_full[dminus.strftime("%Y-%m-%d")]).intersection(set(peoples_avl[x.date.strftime("%Y-%m-%d")]))
        first_values = list(not_common)
        first_values = sorted(first_values, key=lambda o: counts[o], reverse=False)
        sorted_names = sorted(peoples_avl[x.date.strftime("%Y-%m-%d")], key=lambda o: counts[o], reverse=False)
        sorted_names = [i for i in sorted_names if i not in first_values]

        sorted_names = first_values + sorted_names
        print(sorted_names)
        print(x)
        dt_full[x.date.strftime("%Y-%m-%d")] = sorted_names[:int(x.people_required)]
    return counts, dt_full

def get_total_count(roster):
    """
    count the number of duties done by each employee in these 7 days after model is built

    input: roster
    output: count frequency of duties of each employee
    """
    duties = []

    for k, v in roster.items():
        duties += v

    return Counter(duties)

def get_final_roster(df, staffs, date, model_output):
    """
    function to get the roster and duty count for each employees

    input:
     - df: historical df
     - staffs: staffs df
     - date: end date till which roster is being made
     - model_output: final output of the model we will chose
    """
    counts, roster = chose_people(df, staffs, date, model_output)
    duties_count = get_total_count(roster)
    return roster, duties_count