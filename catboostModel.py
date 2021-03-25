import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import sys
from io import StringIO
from catboost import CatBoostRegressor, Pool

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

params = {}
params['iterations'] = 1000
x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)

model = CatBoostRegressor(**params)
model.fit(x_train, y_train, verbose=False)

y_predict = model.predict(x_test)
print(model.score(x_test, y_test))

