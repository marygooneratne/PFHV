import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpl_toolkits
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import math
from sklearn import ensemble
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import calibration_curve

def readData():
    data = pd.read_csv("homes.csv")
    print(data.head())
    print(data.describe())
    return data

def longLat(data):
    locator = Nominatim(user_agent="myGeocoder")
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    data['location'] = data['address'].apply(geocode)
    data['point'] = data['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    data[['latitude', 'longitude', 'altitude']] = pd.DataFrame(data['point'].tolist(), index=data.index)
    newLat = [0 if math.isnan(values) else values for values in data.latitude ]
    data['latitude'] = newLat
    newLong = [0 if math.isnan(values) else values for values in data.longitude]
    data['longitude'] = newLong
    newBath = [0 if math.isnan(values) else values for values in data.bathrooms ]
    data['bathrooms'] = newBath
    newBed = [0 if math.isnan(values) else values for values in data.bedrooms ]
    data['bedrooms'] = newBed
    newFt = [0 if math.isnan(values) else values for values in data.sq_ft ]
    data['sq_ft'] = newFt
    newYear = [0 if math.isnan(values) else values for values in data.year_built ]
    data['year_built'] = newYear
    newData = data.drop(['address', 'altitude','for_sale','zillow_url', 'point', 'location', 'last_modified'], axis=1)
    print(newData)
    return newData

def linearReg(data):
    print(data)
    reg = LinearRegression()
    labels = data['current_price']
    train1 = data.drop(['id', 'current_price'],axis=1)
    x_train, x_test, y_train, y_test = train_test_split(train1, labels, test_size = 0.10, random_state =2)
    print(reg.fit(x_train,y_train))
    print(reg.score(x_test, y_test))

def gradientBoosting(data):
    clf = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2, learning_rate = 0.1, loss = 'ls')
    labels = data['current_price']
    train1 = data.drop(['id', 'current_price'],axis=1)
    x_train, x_test, y_train, y_test = train_test_split(train1, labels, test_size = 0.10, random_state =2)
    clf.fit(x_train, y_train)
    print(clf.score(x_test,y_test))

def logisticReg(data):
    logi=LogisticRegression()
    labels = data['current_price']
    train1 = data.drop(['id', 'current_price'],axis=1)
    x_train, x_test, y_train, y_test = train_test_split(train1, labels, test_size = 0.10, random_state =2)
    print(logi.fit(x_train,y_train))
    print(logi.score(x_test, y_test))


def importantPlots(data):
    plt.figure(figsize=(10,10))
    sns.jointplot(x=data.latitude.values, y=data.longitude.values, size=10)
    plt.ylabel('Longitude', fontsize=12)
    plt.xlabel('Latitude', fontsize=12)
    plt.show()
    plt.scatter(data.price,data.sq_ft)
    plt.title("Price vs Square Feet")
    plt.show()
    plt.scatter(data.price,data.longitude)
    plt.title("Price vs Location of the area")
    plt.show()
    plt.scatter(data.price,data.latitude)
    plt.xlabel("Price")
    plt.ylabel('Latitude')
    plt.title("Latitude vs Price")
    plt.show()
    sns.despine
    plt.scatter(data.bedrooms,data.price)
    plt.title("Bedroom and Price ")
    plt.xlabel("Bedrooms")
    plt.ylabel("Price")
    plt.show()
    sns.despine
    plt.scatter(data['sq_ft'],data['price'])
    plt.show()

def analyzeBedroom(data):
    data['bedrooms'].value_counts().plot(kind='bar')
    plt.title('number of Bedroom')
    plt.xlabel('Bedrooms')
    plt.ylabel('Count')
    sns.despine
    plt.show()

if __name__ == "__main__":
    homeData = readData()
    updatedHomeData = longLat(homeData)
    linearReg(updatedHomeData)
    gradientBoosting(updatedHomeData)
    #importantPlots(updatedHomeData)
    #analyzeBedroom(homeData)