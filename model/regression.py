import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sys
from io import StringIO
import datetime
import numpy as np
from db.Database import Database

HOMES_FILENAME = 'data/homes.csv'
HISTORY_FILENAME = 'data/history.csv'

def get_data(homes_filename=HOMES_FILENAME, history_filename=HISTORY_FILENAME):
    db = Database()
    homes_df = db.homes_df
    history_df = pd.read_csv(history_filename)
    return {"homes":homes_df, "history":history_df}

def clean_data(homes_df, history_df):
    '''
    Clean history DataFrame and introduce additional home data to row
    Args:
        homes_df
        history_df
    Returns:
        history_df: cleaned history df with added home data
    '''
    # Adds columns for home data to each history entry in history_df
    homes_cols = list(homes_df.columns)[1:]
    for col in homes_cols:
        history_df[col] = ""
    
    # Adds zip_code column to history_df
    history_df["zip_code"] = 0

    # Adds home data and zip_code to each history entry by matching history['home_id'] to home['id']
    for i, row in history_df.iterrows():
        home_data = homes_df.loc[homes_df['id'] == row['home_id']].values.tolist()[0][1:]
        history_df.loc[i, homes_cols] = home_data
        history_df.loc[i, "zip_code"] = home_data[0].split(" ")[-1]
    
    # Transform datetime object to just year
    history_df['date'] = history_df['date'].apply(lambda x: x.year)
    history_df.rename(columns={"date":"year"}, inplace=True)

    # Drop rows irrelevant to model
    history_df.drop('id', axis=1, inplace=True)
    history_df.drop('for_sale', axis=1, inplace=True)
    history_df.drop('current_price', axis=1, inplace=True)
    history_df.drop('zillow_url', axis=1, inplace=True)
    history_df.drop('last_modified', axis=1, inplace=True)
    history_df.drop('address', axis=1, inplace=True)

    return history_df

def build_predict_df(df, years=3):
    '''
    Restructures DataFrame for *future* home value prediction by including home_data, 
    pred_year (year to predict), pred_value (value of home in year to predict),
    prev_value (value of home in pred_year-years), and home_data.
    Args:
        df: cleaned history DataFrame
        years: number of years in future to predict, default is 1
    Returns:
        pred_df: New DataFrame described above
    '''
    pred_df = pd.DataFrame(columns=["pred_year", "pred_value", "prev_value", "bedrooms", "bathrooms", "sq_ft", "year_built", "zip_code"])
    for _, row in df.iterrows():
        # Find row that matches current row and home minus years
        year_prior = row['year']-years
        home_match = df.loc[df['home_id'] == row['home_id']]
        row_prior = home_match.loc[home_match['year'] == year_prior]

        # Break if not found
        if len(home_match)<2 or len(row_prior) < 1:
            break

        # Create new row with home data, prev_year, prev_value, prev_value
        row_prior = row_prior.drop("home_id", axis=1)
        row_prior = row_prior.drop("year", axis=1)
        row_prior = row_prior.values.tolist()[0]
        row_prior = [row['year'], row['value']] + row_prior

        # Add row to DataFrame
        row_series =  pd.Series(row_prior, index=pred_df.columns)
        pred_df = pred_df.append(row_series, ignore_index=True)
    
    return pred_df

def predict(df):
    X = df[['pred_year', 'prev_value', 'zip_code', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built']]
    Y = df['pred_value']
    x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)
    mlr = LinearRegression()
    mlr.fit(x_train, y_train)
    score = mlr.score(x_test, y_test)
    return score

if __name__ == "__main__":
    data = get_data()
    history_df = clean_data(data["homes"], data["history"])
    predict_df = build_predict_df(history_df)
    print(predict(predict_df))
