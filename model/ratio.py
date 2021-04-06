import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sys
from io import StringIO
import datetime
import numpy as np
#from db.Database import Database
DATA_FILENAME = 'cleaned_market_data.csv'

data_df = pd.read_csv(DATA_FILENAME)
X = data_df['assessed_val_cleaned']
Y = data_df['market_val_cleaned']
X_array=np.array(X)
Y_array=np.array(Y)
X_array.reshape(len(X_array),1)
Y_array.reshape(len(Y_array),1)
#print(X_array)
LinReg=LinearRegression().fit(X_array.reshape(len(X_array),1),Y_array.reshape(len(Y_array),1))
print(LinReg.coef_)
