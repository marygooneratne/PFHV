from configparser import ConfigParser
import psycopg2
from typing import Dict
import pandas as pd
import datetime

homes_query = """
    CREATE TABLE homes (
        id SERIAL PRIMARY KEY,
        address VARCHAR(100),
        bedrooms INT,
        bathrooms INT,
        sq_ft INT,
        year_built INT,
        for_sale BOOL,
        price INT,
        zillow_url VARCHAR(100),
        last_modified TIMESTAMP
    )
"""
history_query = """
    CREATE TABLE history (
        id SERIAL PRIMARY KEY,
        home_id SERIAL REFERENCES homes(id),
        date DATE,
        value INT,
        last_modified TIMESTAMP
    )
"""
macro_national_query = """
    CREATE TABLE macro_national(
        year INT,
        construction_spending INT,
        housing_starts INT,
        home_sales INT,
        housing_price_idx FLOAT,
        last_modified TIMESTAMP
    )
"""
def load_conn_info(filename):
    parser = ConfigParser()
    parser.read(filename)
    conn_info = {param[0]:param[1] for param in parser.items("local")}
    return conn_info

def create_db(conn_info):
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']}"
    conn = psycopg2.connect(psql_conn_str)
    cur = conn.cursor()
    
    conn.autocommit = True
    query = f"CREATE DATABASE {conn_info['database']}"

    try:
        cur.execute(query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"query:{cur.query}")
        cur.close()
    else:
        conn.autocommit = False

def create_table(query, conn_info):
    conn = None
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"query: {cur.query}")
        conn.rollback()
        cur.close()

def delete_table(conn_info, table_name):
    sql = f"DELETE FROM {table_name}"
    conn = None
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def load_table(conn_info, table_name):
    sql = f"SELECT * FROM {table_name}"
    conn = None
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        string = cur.fetchmany(5)
        print(string)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def homes_df_to_db(df, conn_info):
    sql = f"ALTER SEQUENCE homes_id_seq RESTART WITH 1"
    conn = None
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    idx = 0
    homes_list = df.values.tolist()
    
    for i in homes_list:
        idx = idx+1
        insert_home(i, conn_info)

def macro_national_df_to_db(df, conn_info):
    idx = 0
    macro_national_list = df.values.tolist()
    
    for i in macro_national_list:
        idx = idx+1
        insert_macro_national(i, conn_info)

def history_df_to_db(df, conn_info):
    sql = f"ALTER SEQUENCE history_id_seq RESTART WITH 1"
    conn = None
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    try:
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    idx = 0
    history_list = df.values.tolist()

    for i in history_list:
        idx = idx+1
        insert_history(i, conn_info)

def insert_home(home_data, conn_info):
    sql = """INSERT INTO homes(address, bedrooms, bathrooms,
    sq_ft, year_built, for_sale, price, zillow_url, last_modified)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    conn = None
    home_data_2 = [str(i) for i in home_data[1:-1]]
    try:
        home_data_2[0] = str(home_data_2[0])
    except:
        home_data_2[0] = ""
    try:
        home_data_2[1] = int(float(home_data_2[1]))
    except:
        home_data_2[1] = 0
    try:
        home_data_2[2] =int(float(home_data_2[2]))
    except:
        home_data_2[2] = 0
    try:
        home_data_2[3] = int(float(home_data_2[3]))
    except:
        home_data_2[3] = 0
    try:
        home_data_2[4] = int(float(home_data_2[4]))
    except:
        home_data_2[4] = 0
    try:
        home_data_2[5] = bool(home_data_2[5])
    except:
        home_data_2[5] = True
    try:
        home_data_2[6] = int(home_data_2[6])
    except:
        home_data_2[6] = 0
    home_data_2.append(datetime.datetime.now())
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

def insert_history(history_data, conn_info):
    sql = """INSERT INTO history(home_id,date,value, last_modified)
             VALUES(%s, %s, %s, %s)"""
    conn = None
    history_data = [i for i in history_data[1:]]
    try:
        history_data[0] = int(history_data[0])
    except: 
        history_data[0] = 0
    
    try:
        history_data[1] = datetime.datetime.fromtimestamp(history_data[1]/1e3)
    except:
        history_data[1] = datetime.datetime.now()
    try:
        history_data[2] = int(history_data[2])
    except:
        history_data[2] = 0
        
    history_data.append(datetime.datetime.now())
    history_data = tuple(history_data)
    if len(history_data) > 0:
        psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
        try:
            conn = psycopg2.connect(psql_conn_str)
            cur = conn.cursor()
            cur.execute(sql, history_data)
            conn.commit()
            print("successfully inserted ")
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

def insert_macro_national(macro_national_data, conn_info):
    sql = """INSERT INTO macro_national(year,construction_spending,housing_starts, home_sales, housing_price_idx, last_modified)
             VALUES(%s, %s, %s, %s, %s, %s)"""
    conn = None
    macro_national_data = [i for i in macro_national_data]
    try:
        macro_national_data[0] = int(macro_national_data[0])
    except: 
        macro_national_data[0] = 0
    try:
        macro_national_data[1] = int(macro_national_data[1])
    except:
        macro_national_data[1] = 0
    try:
        macro_national_data[2] = int(macro_national_data[2])
    except:
        macro_national_data[2] = 0
    try:
        macro_national_data[3] = int(macro_national_data[3])
    except:
        macro_national_data[3] = 0
    try:
        macro_national_data[4] = float(macro_national_data[3])
    except:
        macro_national_data[4] = 0
        
    macro_national_data.append(datetime.datetime.now())
    macro_national_data = tuple(macro_national_data)
    print(macro_national_data)
    if len(macro_national_data) > 0:
        psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
        try:
            conn = psycopg2.connect(psql_conn_str)
            cur = conn.cursor()
            cur.execute(sql, macro_national_data)
            conn.commit()
            print("successfully inserted ")
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

def load_cols(conn_info, table_name):
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    conn = psycopg2.connect(psql_conn_str)
    cur = conn.cursor()
    conn.autocommit = True
    query = f"SELECT * FROM {table_name} LIMIT 0"
    resp = []
    try:
        cur.execute(query)
        resp = [desc[0] for desc in cur.description]
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"query:{cur.query}")
        cur.close()
    return resp

def alter_cols(conn_info, table_name, prev, new):
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    conn = psycopg2.connect(psql_conn_str)
    cur = conn.cursor()
    conn.autocommit = True
    query = f"ALTER TABLE {table_name} RENAME COLUMN {prev} TO {new}"
    resp = []
    try:
        cur.execute(query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"query:{cur.query}")
        cur.close()

def drop_col(conn_info, table_name, col_name):
    psql_conn_str = f"user={conn_info['user']} password={conn_info['password']} dbname={conn_info['database']}"
    conn = psycopg2.connect(psql_conn_str)
    cur = conn.cursor()
    conn.autocommit = True
    query = f"ALTER TABLE {table_name} DROP COLUMN {col_name} CASCADE"
    try:
        cur.execute(query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"query:{cur.query}")
        cur.close()

if __name__ == "__main__":
    conn_info = load_conn_info("/Users/Goon/Desktop/Duke/ECE496/PFHV/db/db.ini")
    file_name = "../data/macro_national.csv"
    table_name = 'macro_national'
    df = pd.read_csv(file_name)

    # delete_table(conn_info, table)
    # homes_df_to_db(df, conn_info)
    # history_df_to_db(df, conn_info)
    # create_table(macro_national_query, conn_info)
    macro_national_df_to_db(df, conn_info)
    # # print(load_cols(conn_info, table_name))
    load_table(conn_info, table_name)

    


