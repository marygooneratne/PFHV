import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import sys
from io import StringIO
from sklearn import ensemble
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import calibration_curve
import numpy as np

history_df = pd.read_csv('history.csv')
homes_df = pd.read_csv('homes.csv')
homes_cols = list(homes_df.columns)[1:]
for col in homes_cols:
    history_df[col] = ""
history_df["zip_code"] = 0

for i, row in history_df.iterrows():
    home_data = homes_df.loc[homes_df['id'] == row['home_id']].values.tolist()[0][1:]
    history_df.loc[i, homes_cols] = home_data
    history_df.loc[i, "zip_code"] = home_data[0].split(" ")[-1]

df = history_df

df.drop('id', axis=1, inplace=True)
df.drop('home_id', axis=1, inplace=True)
df.drop('for_sale', axis=1, inplace=True)
df.drop('current_price', axis=1, inplace=True)
df.drop('zillow_url', axis=1, inplace=True)
df.drop('last_modified', axis=1, inplace=True)
df.drop('address', axis=1, inplace=True)

df.fillna(0, inplace=True)
df = df.astype(int)

X = df[['date', 'zip_code', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built']]
Y = df['value']

x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)

logi=LogisticRegression()
logi.fit(x_train,y_train)
y_logi_predict=logi.predict(x_test)
print(logi.score(x_test,y_test))

reg = linear_model.Lasso(alpha=0.1)
reg.fit(x_train, y_train)

y_predict = reg.predict(x_test)
print(reg.score(x_test, y_test))

