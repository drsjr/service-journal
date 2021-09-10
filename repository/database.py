import psycopg2
import os

POSTGRES_PORT = 5432
POSTGRES_USERNAME = "folha"
POSTGRES_PASSWORD = "folha"
POSTGRES_DBNAME = "journal_jj"
POSTGRES_HOSTNAME = "172.17.0.2"


class Database():

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.connection = psycopg2.connect(
            #host=os.getenv('DT_HOST'),
            #user=os.getenv('DT_USER'),
            #password=os.getenv('DT_PASS'),
            #dbname=os.getenv('DT_NAME'),
            #port=os.getenv('DT_PORT'))

            host=POSTGRES_HOSTNAME, 
            user=POSTGRES_USERNAME, 
            password=POSTGRES_PASSWORD, 
            dbname=POSTGRES_DBNAME,
            port=POSTGRES_PORT)
