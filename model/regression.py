import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sys
from io import StringIO
import datetime
import numpy as np
# from db.Database import Database

_HOMES = '../data/homes_complete.csv'
_HISTORY = '../data/history_complete.csv'
_NATIONAL = "../data/macro_national.csv"
_REGIONAL = "../data/macro_regional.csv"
_ZIPCODE = "../data/macro_zipcode.csv"
_REGIONS = "../data/regions.csv"
_ZIPCODE_TO_REGION ="../data/zipcode_to_region.csv"


class RegressionModel:
    def __init__(self, use_macro=True, limit=20000, use_db=False, verbose=True):
        self.homes_df = None
        self.history_df = None
        self.national_df = None
        self.regional_df = None
        self.zipcode_df = None
        self.regions_df = None
        self.zipcode_to_region_df = None
        self.predict_df = None
        self.verbose = verbose
        self.use_macro = use_macro
        if not use_db:
            self.use_db = False
            if int(limit) > 0:
                self.history_df = pd.read_csv(_HISTORY).head(limit)
            else:
                self.history_df = pd.read_csv(_HISTORY)
            self.homes_df = pd.read_csv(_HOMES)
            self.national_df = pd.read_csv(_NATIONAL)
            self.regional_df = pd.read_csv(_REGIONAL)
            self.zipcode_df = pd.read_csv(_ZIPCODE)
            self.regions_df = pd.read_csv(_REGIONS)
            self.zipcode_to_region_df = pd.read_csv(_ZIPCODE_TO_REGION)
        else:
            self.use_db = True
            return
            #TODO Add database
        self.clean_data()
        self.build()
    
    def clean_data(self):
        '''
        Clean history DataFrame and introduce additional home data from self.homes_df to rows in self.history_df
        Args:
            None
        Returns:
            None
        '''
        if self.verbose:
            print('function: clean_data')
        # Adds columns for home data to each history entry in self.history_df
        homes_cols = list(self.homes_df.columns)[1:]
        for col in homes_cols:
            self.history_df[col] = ""
        
        # Adds zip_code column to self.history_df
        self.history_df["zip_code"] = 0

        #Compute ratio
        # Adds home data and zip_code to each history entry by matching history['home_id'] to home['id']
        for i, row in self.history_df.iterrows():
            home_data = self.homes_df.loc[self.homes_df['id'] == row['home_id']].values.tolist()[0][1:]
            self.history_df.loc[i, homes_cols] = home_data
            self.history_df.loc[i, "zip_code"] = home_data[0].split(" ")[-1]
        
        # Transform datetime object to just year
        if self.use_db:
            self.history_df['date'] = self.history_df['date'].apply(lambda x: x.year)
        else:
             self.history_df['date'] = self.history_df['date'].apply(lambda x: int(datetime.datetime.fromtimestamp(x/1e3).year))

        self.history_df.rename(columns={"date":"year"}, inplace=True)

        # Drop rows irrelevant to model
        self.history_df.drop('id', axis=1, inplace=True)
        self.history_df.drop('for_sale', axis=1, inplace=True)
        self.history_df.drop('current_price', axis=1, inplace=True)
        self.history_df.drop('zillow_url', axis=1, inplace=True)
        self.history_df.drop('last_modified', axis=1, inplace=True)
        self.history_df.drop('address', axis=1, inplace=True)
        
        if self.verbose:
            print('cleaned history_df:', self.history_df.head())
    
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
        if self.verbose:
            print('function: build')
            print('history_df len:', len(self.history_df.index))
        pred_df = pd.DataFrame(columns=["pred_year", 
            "pred_value", "prev_value", "bedrooms",
            "bathrooms", "sq_ft", "year_built",
            "zip_code", "zipcode_rating",
            "rgl_housing_starts", "rgl_new_home_sales",
            "ntl_construction_spending","ntl_housing_starts", "ntl_home_sales",
            "ntl_housing_price_idx"])

        for _, row in self.history_df.iterrows():
            # Find row that matches current row and home minus years
            year_prior = row['year']-years
            home_match = self.history_df.loc[self.history_df['home_id'] == row['home_id']]
            row_prior = home_match.loc[home_match['year'] == year_prior]

            # Break if not found
            if len(home_match)<2 or len(row_prior) < 1:
                continue

            # Create new row with home data, prev_year, prev_value, prev_value
            row_prior = row_prior.drop("home_id", axis=1)
            row_prior = row_prior.drop("year", axis=1)
    
            row_prior = row_prior.values.tolist()[0]
            row_prior = [row['year'], row['value']] + row_prior
            macro_data = self.macro_data(row_prior[:-1][0], year_prior)
            row_prior = row_prior + list(macro_data.values())
            
            if self.verbose:
                print("row prior with macro:", row_prior)

            # Add row to DataFrame
            row_series =  pd.Series(row_prior, index=pred_df.columns)
            pred_df = pred_df.append(row_series, ignore_index=True)
        
        self.predict_df = pred_df
        if self.verbose:
            print('built predict_df:', self.predict_df.head())

        
        return pred_df
    
    def macro_data(self, zipcode, year):
        data = {
            "zipcode_rating": None,
            "rgl_housing_starts": None,
            "rgl_new_home_sales": None,
            "ntl_construction_spending": None,
            "ntl_housing_starts": None,
            "ntl_home_sales": None,
            "ntl_housing_price_idx": None
        }

        zipcode_rating = self.zipcode_df.loc[self.zipcode_df['zipcode']==int(zipcode)].values.tolist()
        region = self.zipcode_to_region_df[self.zipcode_to_region_df['zipcode']==int(zipcode)].values.tolist()
        print(region)
        if len(zipcode_rating) > 0:
            data["zipcode_rating"] = zipcode_rating[0][1]
        if len(region) > 0:
            region = region[0][1]
            rgl_data = self.regional_df[(self.regional_df['region']==int(region)) & (self.regional_df['year'] == int(year))].values.tolist()
            if len(rgl_data) > 0:
                data["rgl_housing_starts"], data["rgl_new_home_sales"]= tuple(rgl_data[0][1:3])
        ntl_data = self.national_df[self.national_df['year'] == int(year)].values.tolist()
        if len(ntl_data) > 0:
                data["ntl_construction_spending"], data["ntl_housing_starts"], data["ntl_home_sales"], data["ntl_housing_price_idx"]= tuple(ntl_data[0][1:])
        return data

    def predict(self, use_macro=None):
        if use_macro is None:
            use_macro = self.use_macro
        #TODO better NaN fill
        self.predict_df = self.predict_df.fillna(value=0)
        if use_macro:
            X = self.predict_df[['pred_year', 'prev_value', 'zip_code', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built', "zipcode_rating",
                "rgl_housing_starts", "rgl_new_home_sales",
                "ntl_construction_spending","ntl_housing_starts", "ntl_home_sales",
                "ntl_housing_price_idx"]]
        else:
            X = self.predict_df[['pred_year', 'prev_value', 'zip_code', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built']]
        Y = self.predict_df['pred_value']
        x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)
        mlr = LinearRegression()
        mlr.fit(x_train, y_train)
        score = mlr.score(x_test, y_test)
        return score