import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient, event_loggers
from setup_logging import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("pymongo.command")



load_dotenv()


class AtlasClient:
   def __init__(self, atlas_uri, dbname):
       self.mongodb_client = MongoClient(atlas_uri)
       self.database = self.mongodb_client[dbname]

   def ping(self):
       self.mongodb_client.admin.command('ping')

   def get_collection(self, collection_name):
       collection = self.database[collection_name]
       return collection


if __name__ == "__main__":
    ATLAS_URI = os.getenv("ATLAS_URI")
    client = AtlasClient(ATLAS_URI, "users")
    # client.ping()
    users_collection = client.get_collection("users")
    print(users_collection.find_one())