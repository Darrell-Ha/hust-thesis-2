import os
from dotenv import load_dotenv

from typing import TypedDict
from pymongo import MongoClient, collection

load_dotenv()

__all__ = [
    "create_connection_mdb"
]


def create_connection_mdb(collection_name: str, database_name: str="login_services") -> collection.Collection:
    colltn = None
    new_client = MongoConnection().get_client()
    if database_name in new_client.list_database_names():
        db = new_client.get_database(database_name)
        if collection_name in db.list_collection_names():
            colltn = db.get_collection(collection_name)
            return colltn
        else:
            raise ValueError(f"Collection: {collection_name} not found!")
    raise ValueError(f"Database: {database_name} not found!!")

class ConfigMongo(TypedDict):
    """
    A configuration for MongoDB to get client
    """
    type_mongo_cloud: bool 
    username: str
    password: str
    hostname: str
    port: str

config_mongo_schema=ConfigMongo(
    type_mongo_cloud=bool(os.getenv("MDB_TYPE_CLOUD", False)),
    hostname=os.getenv("MDB_HOSTNAME"),
    port=os.getenv("MDB_PORT"),
    username=os.getenv("MDB_USERNAME"),
    password=os.getenv("MDB_PASSWORD")
)

class MongoConnection:
    """
    Connection class to work with mongodb

    Attributes:
        config: set up configuration to connect subwallet_db in mongo
    
    Methods:
        create_connection(self):

    """
    config: ConfigMongo
    client: MongoClient

    def __init__(self, config: ConfigMongo=config_mongo_schema) -> None:
        self.config = config
        try:
            self.client = self.create_connection()
        except ValueError as val_err:
            print(val_err)
        
    def create_connection(self) -> MongoClient:
        """
        Create connection to mongodb
        """
        client: MongoClient
        link = ''
        config = self.get_config()
        if any(s not in config.values() for s in {'', 0}):
            user = config.get("username")
            password = config.get("password")
            hostname = config.get("hostname")
            if config.get("type_mongo_cloud", False):
                link = f"mongodb+srv://{user}:{password}@{hostname}"
            else:
                port = config.get("port")
                link = f'mongodb://{user}:{password}@{hostname}:{port}'
        
        if link:
            client = MongoClient(link)
        else:
            raise ValueError("CLIENT IS NULL: CAN'T CONNECT MONGODB")
        return client

    def set_config(self, config: ConfigMongo) -> None:
        self.config = config
    
    def get_config(self) -> ConfigMongo:
        return self.config
    
    def get_client(self) -> MongoClient:
        return self.client

