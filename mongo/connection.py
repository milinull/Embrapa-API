from pymongo import MongoClient
from decouple import config

class DBconnectionHandler:
    def __init__(self):
        self.__connection_String = f'mongodb://{config("MDB_USER")}:{config("MDB_PASS")}@{config("MDB_HOST")}:{config("MDB_PORT")}/?authSource=admin'
        self.__database_name = config('MDB_NAME')
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_String)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client
    
    