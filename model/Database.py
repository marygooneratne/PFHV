from configparser import ConfigParser
import psycopg2
import pandas as pd

class Database:
    def __init__(self):
        self.conn_info = self.load_conn_info("/Users/joshuayen/Documents/Github/PFHV/db/db.ini")
        self.homes_df = self.get_df("homes")
        self.history_df = self.get_df("history")
        self.macro_national_df = self.get_df("macro_national")
        self.macro_regional_df = self.get_df("macro_regional")

        # TODO @Mary
        # self.state_df = self.get_df("macro_state")
        # self.zip_code_df = 
    
    def get_df(self, table_name):
        return pd.DataFrame(self.load_table(self.conn_info, table_name), columns=self.load_cols(self.conn_info, table_name))

    def load_conn_info(self,filename):
        parser = ConfigParser()
        parser.read(filename)
        conn_info = {param[0]:param[1] for param in parser.items("heroku")}
        return conn_info
    
    def load_cols(self, conn_info, table_name):
        psql_conn_str = f"dbname={conn_info['database']} user={conn_info['user']} password={conn_info['password']} host={conn_info['host']} port={conn_info['port']}"
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
    
    def load_table(self, conn_info, table_name):
        psql_conn_str = f"dbname={conn_info['database']} user={conn_info['user']} password={conn_info['password']} host={conn_info['host']} port={conn_info['port']}"
        conn = psycopg2.connect(psql_conn_str)
        cur = conn.cursor()
        conn.autocommit = True
        query = f"SELECT * FROM {table_name}"
        resp = []
        try:
            cur.execute(query)
            resp = list(cur.fetchmany(size=5))
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            print(f"query:{cur.query}")
            cur.close()
        return resp
    