from pymongo import MongoClient
from decouple import config


class DBconnectionHandler:
    def __init__(self):
        # Use 'mongo' como host quando rodando em Docker
        # Use 'localhost' ou '127.0.0.1' quando rodando localmente
        host = config("MDB_HOST", default="mongo")
        port = config("MDB_PORT", default="27017")
        user = config("MDB_USER")
        password = config("MDB_PASS")

        self.__connection_String = (
            f"mongodb://{user}:{password}@{host}:{port}/?authSource=admin"
        )
        self.__database_name = config("MDB_NAME")
        self.__client = None
        self.__db_connection = None

    def connect_to_db(self):
        self.__client = MongoClient(self.__connection_String)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        return self.__db_connection

    def get_db_client(self):
        return self.__client
