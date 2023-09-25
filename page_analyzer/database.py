from dotenv import load_dotenv
import os
from psycopg2 import pool


class DatabaseConnection:
    GET_BACK_VALUES = ('all', 'one', 'none')

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

    def execute(self, *query_content, get_back='all'):
        if get_back not in self.GET_BACK_VALUES:
            raise ValueError('Incorrect value of the \'get_back\' argument')
        result = None
        self.getconn()
        cursor = self.cursor()
        cursor.execute(*query_content)
        match get_back:
            case 'all':
                result = cursor.fetchall()
            case 'one':
                result = cursor.fetchone()
        if get_back == 'none':
            self.conn.commit()
        cursor.close()
        self.putconn()
        return result
