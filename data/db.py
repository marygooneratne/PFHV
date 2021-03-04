from configparser import ConfigParser
import psycopg2
from typing import Dict

def load_conn_info(filename):
    parser = ConfigParser()
    parser.read(filename)
    conn_info = {param[0]:param[1] for param in parser.items("postgresql")}
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

def create_table(query, conn, cur):
    try:
        cur.execute(query)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        conn.commit()

if __name__ == "__main__":
    conn_info = load_conn_info("db.ini")
    create_db(conn_info)
    conn = psycopg2.connect(**conn_info)
    cur = conn.cursor()
    homes_query = """
        CREATE TABLE homes (
            
        )
    """
    history_query = """
        CREATE TABLE history (

        )
    """

    create_table(homes_query, conn, cur)
    create_table(history_query, conn, cur)