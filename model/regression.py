import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sys
from io import StringIO
import datetime
import numpy as np
from db.Database import Database

_HOMES = './data/homes_complete.csv'
_HISTORY = './data/history_complete.csv'
_NATIONAL = "./data/macro_national.csv"
_REGIONAL = "./data/macro_regional.csv"
_ZIPCODE = "./data/macro_zipcode.csv"
_REGIONS = "./data/regions.csv"
_ZIPCODE_TO_REGION ="./zipcode_to_region.csv"


class RegressionModel:
    def __init__(self, use_db=False):
        self.homes_df = None
        self.history_df = None
        self.national_df = None
        self.regional_df = None
        self.zipcode_df = None
        self.regions_df = None
        self.zipcode_to_region_df = None
        self.predict_df = None

        if not use_db:
            self.homes_df = pd.read_csv(_HOMES)
            self.history_df = pd.read_csv(_HISTORY)
            self.national_df = pd.read_csv(_NATIONAL)
            self.regional_df = pd.read_csv(_REGIONAL)
            self.zipcode_df = pd.read_csv(_ZIPCODE)
            self.regions_df = pd.read_csv(_REGIONS)
            self.zipcode_to_region_df = pd.read_csv(_ZIPCODE_TO_REGION)
        else:
            return
            #TODO
    
    def clean_data(self):
        '''
        Clean history DataFrame and introduce additional home data from self.homes_df to rows in self.history_df
        Args:
            None
        Returns:
            None
        '''
        # Adds columns for home data to each history entry in self.history_df
        homes_cols = list(self.homes_df.columns)[1:]
        for col in homes_cols:
            self.history_df[col] = ""
        
        # Adds zip_code column to self.history_df
        self.history_df["zip_code"] = 0

        # Adds home data and zip_code to each history entry by matching history['home_id'] to home['id']
        for i, row in self.history_df.iterrows():
            home_data = self.homes_df.loc[self.homes_df['id'] == row['home_id']].values.tolist()[0][1:]
            self.history_df.loc[i, homes_cols] = home_data
            self.history_df.loc[i, "zip_code"] = home_data[0].split(" ")[-1]
        
        # Transform datetime object to just year
        self.history_df['date'] = self.history_df['date'].apply(lambda x: x.year)
        self.history_df.rename(columns={"date":"year"}, inplace=True)

        # Drop rows irrelevant to model
        self.history_df.drop('id', axis=1, inplace=True)
        self.history_df.drop('for_sale', axis=1, inplace=True)
        self.history_df.drop('current_price', axis=1, inplace=True)
        self.history_df.drop('zillow_url', axis=1, inplace=True)
        self.history_df.drop('last_modified', axis=1, inplace=True)
        self.history_df.drop('address', axis=1, inplace=True)
    
    def build(self, years=3):
        '''
        Restructures DataFrame for *future* home value prediction by including home_data, 
        pred_year (year to predict), pred_value (value of home in year to predict),
        prev_value (value of home in pred_year-years), and home_data.
        Args:
            None
        Returns:
            pred_df: New DataFrame described above
        '''
        pred_df = pd.DataFrame(columns=["pred_year", "pred_value", "prev_value", "bedrooms", "bathrooms", "sq_ft", "year_built", "zip_code"])
        for _, row in df.iterrows():
            # Find row that matches current row and home minus years
            year_prior = row['year']-years
            home_match = self.history_df.loc[self.history_df['home_id'] == row['home_id']]
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

    def predict(self):
        X = df[['pred_year', 'prev_value', 'zip_code', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built']]
        Y = df['pred_value']
        x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)
        mlr = LinearRegression()
        mlr.fit(x_train, y_train)
        score = mlr.score(x_test, y_test)
        return score

# if __name__ == "__main__":
#     data = get_data()
#     history_df = clean_data(data["homes"], data["history"])
#     predict_df = build_predict_df(history_df)
#     print(predict(predict_df))
