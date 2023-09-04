from dotenv import load_dotenv
import os
from psycopg2 import pool


class DatabaseConnection:
    minconn = 0
    maxconn = 10

    def __init__(self):
        load_dotenv()
        DATABASE_URL = os.getenv('DATABASE_URL')
        DatabaseConnection.conn_pool = pool.SimpleConnectionPool(DatabaseConnection.minconn, DatabaseConnection.maxconn, dsn=DATABASE_URL)  #noqa: E501
    
    def getconn(self):
        DatabaseConnection.conn = DatabaseConnection.conn_pool.getconn()

    def putconn(self):
        DatabaseConnection.conn_pool.putconn(DatabaseConnection.conn)

    def cursor(self):
        cursor = DatabaseConnection.conn.cursor()
        return cursor

    def execute(self, *query_content, get_back=True, commit=False):
        self.getconn()
        cursor = self.cursor()
        cursor.execute(*query_content)
        result = None
        if get_back:
            result = cursor.fetchall()
        if commit:
            DatabaseConnection.conn.commit()
        cursor.close()
        self.putconn()
        return result
