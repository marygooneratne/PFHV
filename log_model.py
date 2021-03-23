import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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
plt.style.use('ggplot')

# colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#000000']

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

# print(df.head())
# print(df.shape)
# print(df.dtypes)
# print(df.info())
# zip_codes = df.zip_code.unique()

# for i in range(0,3):
#     zip_code = zip_codes[i]
#     print(df[df['zip_code'] == zip_code].value)
#     df[df['zip_code'] == zip_code].value.plot(kind='hist', color=colors[i], edgecolor='black', alpha=0.5, figsize=(10, 7))

df.drop('id', axis=1, inplace=True)
df.drop('home_id', axis=1, inplace=True)
df.drop('for_sale', axis=1, inplace=True)
df.drop('current_price', axis=1, inplace=True)
df.drop('zillow_url', axis=1, inplace=True)
df.drop('last_modified', axis=1, inplace=True)
df.drop('address', axis=1, inplace=True)


print(df.head())
print(df.columns)
df.fillna(0, inplace=True)
df = df.astype(int)


# X = df[['date', 'zip_code', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built']]
X = df[['date', 'zip_code', 'bedrooms', 'bathrooms', 'sq_ft', 'year_built']]
Y = df['value']

x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size =0.2)
logi=LogisticRegression()
data = pd.read_csv("homes.csv")
labels = data['current_price']
train1 = data.drop(['id', 'current_price'],axis=1)
x_train, x_test, y_train, y_test = train_test_split(train1, labels, test_size = 0.10, random_state =2)
#print(logi.fit(x_train,y_train))
print(logi.score(x_test, y_test))

mlr = LinearRegression()
mlr.fit(x_train, y_train)

home_ids = range(0,152)
x_plt =x_test.values.tolist()
sqfts = [row[4] for row in x_plt]

print(sqfts)
y_predict = mlr.predict(x_test)
print(mlr.score(x_test, y_test))
print(x_test.shape)
print(y_test.shape)
plt.scatter(sqfts, y_test)
plt.plot(sqfts,y_predict)
plt.show()