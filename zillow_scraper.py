import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import pandas as pd
import regex as re
import requests
import lxml
from lxml.html.soupparser import fromstring
import prettify
import numbers
import htmltext

HOMES_DB_COLUMNS = ["id", "address", "bedrooms", "bathrooms", "sq_ft", "year_built", "for_sale", "price", "zillow_url", "last_modified"]
HISTORY_DB_COLUMNS = ["id", "home_id", "date", "event", "price"]
CITY_NAME = "austin"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def fetch_homes(city=CITY_NAME):
    with requests.Session() as s:
        city = CITY_NAME + '/'
        url = 'https://www.zillow.com/homes/for_sale/'+city    
        r = s.get(url, headers=HEADERS)
    return BeautifulSoup(r.content, 'html.parser')

def fetch_home(url):
    with requests.Session() as s:
        r = s.get(url, headers=HEADERS)
    return BeautifulSoup(r.content, 'html.parser')

def parse_class(s):
    s = str(s)
    s = s[s.index(">")+1:]
    s = s[:s.index("<")]
    return s

def add_homes(df, soup):
    '''
    Uses BeautifulSoup object (Zillow page of homes) to scrape list of homes and basic data and adds to df
    '''
    for i in soup:
        addresses = soup.find_all (class_= 'list-card-addr')
        links = soup.find_all (class_= 'list-card-link')
        prices = soup.find_all (class_= 'list-card-price')
        curr_id = len(df.index)
        for i in range(0, min([len(addresses), len(links), len(prices)])):           
            a = parse_class(addresses[i])
            l = str(links[i]["href"])
            p = parse_class(prices[i])
            df = df.append({"id": curr_id, "address":a, "zillow_url": l, "price": p, "for_sale": True}, ignore_index=True)
            curr_id += 1
    return df


def fetch_home_details(url):
    soup = fetch_home(url)
    soup = str(soup)
    soup = soup[soup.index("priceHistory")+16:]
    history = soup[:soup.index("]")].replace("\\", "").replace("\"", "").split("},")
    
    history_cleaned = []
    for row in history:
        event = {}
        row = row[1:].replace("}", "").replace("{", "").split(",")
        for d in row:
            d = d.split(":")
            if(d[0] == "event"): event["event"] = d[1]
            if(d[0] == "date"): event["date"] = d[1]
            if(d[0] == "price"): event["price"] = d[1]
        history_cleaned.append(event)
    
    bedrooms = soup[soup.index("bedrooms")+11]
    bathrooms = soup[soup.index("bathrooms")+12]
    price = soup[soup.index("price\\")+8:]
    price = price[:price.index(",")]
    details = {"bedrooms": bedrooms, "bathrooms": bathrooms, "price": price }


    return history_cleaned, details

def add_home_details(homes_df, history_df):
    curr_id = len(history_df.index)
    for i, row in homes_df.iterrows():
        history, details = fetch_home_details(row["zillow_url"])
        home_id = row['id']
        homes_df.loc[i, ["bedrooms", "bathrooms", "price"]] = details
        for h in history:
            if len(h.keys()) > 0:
                r = {"id": curr_id, "home_id": home_id}
                r.update(h)
                curr_id += 1
                history_df = history_df.append(r, ignore_index=True)
                print(history_df.head())
                if curr_id > 10: break
            
    return homes_df, history_df

if __name__ == "__main__":
    homes_df = pd.DataFrame(columns=HOMES_DB_COLUMNS)
    homes = fetch_homes()
    homes_df = add_homes(homes_df, homes)
    history_df = pd.DataFrame(columns=HISTORY_DB_COLUMNS)
    homes_df, history_df = add_home_details(homes_df, history_df)
    history_df.to_csv('history.csv', index=False)
    homes_df.to_csv('homes.csv', index=False)










 