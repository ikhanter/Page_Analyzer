from dotenv import load_dotenv
import os
from psycopg2 import pool


class DatabaseConnection:

    def __init__(self):
        self.minconn = 0
        self.maxconn = 10
        load_dotenv()
        db_url = os.getenv('DATABASE_URL')
        self.conn_pool = pool.SimpleConnectionPool(self.minconn, self.maxconn, dsn=db_url)  # noqa: E501

    def getconn(self):
        self.conn = self.conn_pool.getconn()

    def putconn(self):
        self.conn_pool.putconn(self.conn)

    def cursor(self):
        cursor = self.conn.cursor()
        return cursor

    def execute(self, *query_content, get_back=True):
        self.getconn()
        cursor = self.cursor()
        cursor.execute(*query_content)
        result = None
        if get_back:
            result = cursor.fetchall()
        cursor.close()
        self.putconn()
        return result
