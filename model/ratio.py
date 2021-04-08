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
_MARKET_VALUE ="../data/market_value_data_complete.csv"

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
        self.market_value_df = None
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
            self.market_value_df = pd.read_csv(_MARKET_VALUE)
        else:
            self.use_db = True
            return
            #TODO Add database
        self.clean_data()

    def clean_data(self):
        '''
        Clean marketvalue DataFrame and introduce additional home data from self.homes_df to rows in self.market_value_df
        Args:
            None
        Returns:
            None
        '''
        self.market_value_df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
        self.market_value_df.dropna()
        if self.verbose:
            print('function: clean_data')
        # Adds columns for home data to each market_value entry in self.market_value_df
        homes_cols = list(self.homes_df.columns)[1:]
        for col in homes_cols:
            self.market_value_df[col] = ""

        # Adds zip_code column to self.market_value_df
        self.market_value_df["zip_code"] = 0

        # Adds home data and zip_code to each market_value entry by matching market_value['home_id'] to home['id']
        for i, row in self.market_value_df.iterrows():
            home_data = self.homes_df.loc[self.homes_df['id'] == row['home_id']].values.tolist()[0][1:]
            self.market_value_df.loc[i, homes_cols] = home_data
            self.market_value_df.loc[i, "zip_code"] = home_data[0].split(" ")[-1]
        
        # Adds ratio column to self.history_df
        self.market_value_df["ratio"] = 0
        self.market_value_df["ratio"] = self.market_value_df["market_val"]/self.market_value_df["assessed_val"]

         # Drop rows irrelevant to model
        self.market_value_df.drop('id', axis=1, inplace=True)
        self.market_value_df.drop('for_sale', axis=1, inplace=True)
        self.market_value_df.drop('current_price', axis=1, inplace=True)
        self.market_value_df.drop('zillow_url', axis=1, inplace=True)
        self.market_value_df.drop('last_modified', axis=1, inplace=True)
        self.market_value_df.drop('address', axis=1, inplace=True)

        #ensure model cleaned of string types
        self.market_value_df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
        self.market_value_df.dropna()
        if self.verbose:
            print('cleaned market_value_df:', self.market_value_df.head())        
    
    def predict(self, use_macro=None):
        #TODO better NaN fill
        self.market_value_df = self.market_value_df.fillna(value=0)
        
        X=self.market_value_df[['year', 'market_val', 'assessed_val', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built', 'zip_code']]
        Y = self.market_value_df['ratio']
        x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)
        mlr = LinearRegression()
        mlr.fit(x_train, y_train)
        score = mlr.score(x_test, y_test)
        return score
        print(score)
