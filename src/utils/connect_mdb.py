import os
from dotenv import load_dotenv
from src.model.db import *

load_dotenv()

account_db = MongoConnection(
    config=ConfigMongo(
        type_mongo_cloud=os.getenv("MDB_TYPE_CLOUD", False),
        hostname=os.getenv("MDB_HOSTNAME"),
        port=os.getenv("MDB_PORT"),
        username=os.getenv("MDB_USERNAME"),
        password=os.getenv("MDB_PASSWORD")
    )
).get_client()

