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
import psycopg2

HOMES_DB_COLUMNS = ["id", "address", "bedrooms", "bathrooms", "sq_ft", "year_built", "for_sale", "price", "zillow_url", "last_modified"]
HISTORY_DB_COLUMNS = ["id", "home_id", "date", "event", "price"]
CITY_NAME = "miami"
STATE_NAME = "fl"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def fetch_all_homes(homes_df, city=CITY_NAME, state=STATE_NAME):
   # PATH = '/Users/hannahtaubenfeld/Downloads/chromedriver 2'
   # browser=webdriver.Chrome(PATH)
    for i in range(1,5):
        with requests.Session() as s:
            location = CITY_NAME + '-' + STATE_NAME
            url = 'https://www.zillow.com/' + location + '/'+ str(i) + '_p/'
            print(url)
            #r = browser.page_source
            r = s.get(url, headers=HEADERS)
            print(r)
            page_data = BeautifulSoup(r.content, 'html.parser')
            homes_df = add_homes(homes_df, page_data)
    return homes_df

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

def add_homes(df, soup, num_homes=False):
    '''
    Uses BeautifulSoup object (Zillow page of homes) to scrape list of homes and basic data and adds to df
    '''
    curr_id = len(df.index)
    for i in soup:
        addresses = soup.find_all (class_= 'list-card-addr')
        links = soup.find_all (class_= 'list-card-link')
        prices = soup.find_all (class_= 'list-card-price')
        link_idx = 0
        for i in range(0, min([len(addresses), len(links), len(prices)])):
            a = parse_class(addresses[i])[1:-1]
            l = str(links[link_idx]["href"])
            p = parse_class(prices[i])
            df = df.append({"id": curr_id, "address":a, "zillow_url": l, "price": p, "for_sale": True}, ignore_index=True)
            curr_id += 1
            link_idx +=2
    return df

def find_number(string):
    num = ""
    for c in string:
        if c.isdigit():
            num = num + c
        if not c.isdigit() and len(num) > 0:
            break
    return num


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
    
    sqft = ""
    yr = ""
    bedrooms = ""
    bathrooms = ""
    price = ""

    try:
        sqft = find_number(soup[soup.index('sqft\\":')+9:])
    except:
        print("Unable to find sqft")
    
    try:
        yr = find_number(soup[soup.index('\\"yearBuilt\\":')+14:])
    except:
        print("Unable to find yearBuilt")
    
    try:
        bedrooms = find_number(soup[soup.index("bedrooms")+11:])
    except:
        print("Unable to find bedrooms")
    
    try:
        bathrooms = find_number(soup[soup.index("bathrooms")+12])
    except:
        print("Unable to find bathrooms")
    
    try:
        price = soup[soup.index("bathrooms")+12:]
        price = find_number(price[price.index('\\"price\\":')+10:])
    except:
        print("Unable to find price")
    
    lastmod = datetime.datetime.now()
    details = {"bedrooms": bedrooms, "bathrooms": bathrooms, "sq_ft":sqft, "year_built":yr, "price": price, "last_modified": lastmod}
    return history_cleaned, details

def add_home_details(homes_df, history_df, num_homes=False):
    curr_id = len(history_df.index)
    for i, row in homes_df.iterrows():
        if num_homes and i > num_homes:
            break
        history, details = fetch_home_details(row["zillow_url"])
        home_id = row['id']
        homes_df.loc[i, ["bedrooms", "bathrooms", "sq_ft", "year_built", "price", "last_modified"]] = details
        for h in history:
            if len(h.keys()) > 0:
                r = {"id": curr_id, "home_id": home_id}
                r.update(h)
                curr_id += 1
                history_df = history_df.append(r, ignore_index=True)
                if curr_id > 10: break
    return homes_df, history_df

def homes_df_to_db(homes_df):
    conn_info = load_conn_info("db.ini")
    idx = 0
    homes_list = homes_df.values.tolist()
    for i in homes_list:
        if idx > 2:
            break
        idx = idx+1
        insert_home(i, conn_info)
    
def load_conn_info(filename):
    parser = ConfigParser()
    parser.read(filename)
    conn_info = {param[0]:param[1] for param in parser.items("postgresql")}
    return conn_info

    
def insert_home(home_data, conn_info):
    sql = """INSERT INTO homes(address, bedrooms, bathrooms,
    sq_ft, year_built, for_sale, price, zillow_url, last_modified)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    conn = None
    home_id = None
    home_data_2 = [str(i) for i in home_data[1:-1]]
    home_data_2.append(home_data[len(home_data)-1])
    home_data = tuple(home_data_2)
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:

        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(sql, home_data)
        conn.commit()
        print("successfully inserted ")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def delete_table(conn_info):
    sql = """DELETE * FROM homes"""
    conn = None
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        string = cur.fetchall()
        print(string)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def check(conn_info):
    sql = """SELECT * FROM homes"""
    conn = None
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        string = cur.fetchall()
        print(string)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
<<<<<<< HEAD
    homes_df = pd.DataFrame(columns=HOMES_DB_COLUMNS)
    homes_df = fetch_all_homes(homes_df)
    #history_df = pd.DataFrame(columns=HISTORY_DB_COLUMNS)
    #homes_df, history_df = add_home_details(homes_df, history_df)
   # history_df.to_csv('history.csv', index=False)
    homes_df.to_csv('homes.csv', index=False)
=======
    # fetch_home_details("https://www.zillow.com/homes/8408-Kansas-River-Dr-Austin,-TX,-78745_rb/58316348_zpid/")
    # homes_df = pd.DataFrame(columns=HOMES_DB_COLUMNS)
    # homes = fetch_homes()
    # homes_df = add_homes(homes_df, homes, num_homes=2)
    # history_df = pd.DataFrame(columns=HISTORY_DB_COLUMNS)
    # homes_df, history_df = add_home_details(homes_df, history_df, num_homes=2)
    # homes_df_to_db(homes_df)
    conn_info = load_conn_info("db.ini")
    delete_table(conn_info)
    # history_df.to_csv('history.csv', index=False)
    # homes_df.to_csv('homes.csv', index=False)
>>>>>>> e883c0889759ab57d4c2f32cd3adee14f28dee81










 