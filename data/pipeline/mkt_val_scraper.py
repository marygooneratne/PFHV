import os
import datetime
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
from configparser import ConfigParser


HOMES_DB_COLUMNS = ["id", "address", "bedrooms", "bathrooms", "sq_ft", "year_built", "for_sale", "current_price", "zillow_url", "last_modified"]
HISTORY_DB_COLUMNS = ["id", "home_id", "date", "value"]
MARKET_HISTORY_DB_COLUMNS = ["home_id", "year", "assessed_value", "market_value"]
CITY = "austin"
STATE = "tx"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
NUM_PAGES = 5

def fetch_home(url):
    with requests.Session() as s:
        r = s.get(url, headers=HEADERS)
    return BeautifulSoup(r.content, 'html.parser')

# def parse_class(s):
#     s = str(s)
#     s = s[s.index(">")+1:]
#     s = s[:s.index("<")]
#     return s

def fetch_market_history(url):
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
        
        if "event" in event.keys() and event["event"] == "Listed for sale":
            history_cleaned.append(event)
    return history_cleaned

# def find_number(string):
#     num = ""
#     for c in string:
#         if c.isdigit():
#             num = num + c
#         if not c.isdigit() and len(num) > 0:
#             break
#     return num

if __name__ == "__main__":
    homes_df = None
    hist_df = None
    mkt_hist = []
    for i, r in homes_df.iterrrows():
        row = {}
        url = ""
        assessed_val = ""
        hist = fetch_market_history(url)
        row["home_id"] = ""
        row["year"] = ""
        row["mkt_val"] = ""
        row 

    hist = fetch_market_history("https://www.zillow.com/homes/8408-Kansas-River-Dr-Austin,-TX,-78745_rb/58316348_zpid/")
    print(hist)


    # fetch_home_details("https://www.zillow.com/homes/8408-Kansas-River-Dr-Austin,-TX,-78745_rb/58316348_zpid/")
    # db = df.read_cs
    # homes_df = pd.DataFrame(columns=HOMES_DB_COLUMNS)
    # for i in range(1,NUM_PAGES):
    #     homes = fetch_homes(i)
    #     homes_df = add_homes(homes_df, homes)
    #     print(homes_df.head())
    # history_df = pd.DataFrame(columns=HISTORY_DB_COLUMNS)
    # homes_df, history_df = add_home_details(homes_df, history_df)
    # # homes_df_to_db(homes_df)

    # history_df.to_csv('history.csv', index=False)
    # homes_df.to_csv('homes.csv', index=False)

    # conn_info = load_conn_info("db.ini")
    # delete_table(conn_info)

