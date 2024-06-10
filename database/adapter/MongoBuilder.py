import logging
import os

import dotenv
import pymongo
from pymongo import errors

dotenv.load_dotenv()


class MongoBuilder:
    def __init__(self):
        self.client = None
        self.db = None
        try:
            self.client = pymongo.MongoClient(os.getenv('MONGODB_CONNECTION_URL'))
            logging.basicConfig(level=logging.INFO, format='[MONGODB_INFO] %(message)s')
            logging.info("MongoDB connection established.")
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logging.error(f"MongoDB connection timeout: {err}")
        except TimeoutError as err:
            logging.error(f"Connection timeout: {err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def is_database_existed(self, database_name: str) -> bool:
        try:
            return database_name in self.client.list_database_names()
        except Exception as e:
            logging.error(f"An unexpected error occurred while checking database existence: {e}")
            return False

    def is_collection_existed(self, collection_name: str) -> bool:
        try:
            return collection_name in self.db.list_collection_names()
        except Exception as e:
            logging.error(f"An unexpected error occurred while checking collection existence: {e}")
            return False

    def create_database(self, database_name: str) -> None:
        self.db = self.client[database_name]
        if self.is_database_existed(database_name):
            logging.info(f"Database '{database_name}' already exists.")
        else:
            logging.info(f"Database '{database_name}' created.")

    def create_collection(self, collection_name: str) -> None:
        if self.db is None:
            raise Exception("Database not created. Please create the database first.")

        if not self.is_collection_existed(collection_name):
            collection = self.db[collection_name]
            # Creating index based on collection name
            if collection_name == "Profile":
                collection.create_index([("patient_id", pymongo.ASCENDING)], unique=True)
            elif collection_name == "CareGivers":
                collection.create_index([("giver_id", pymongo.ASCENDING)], unique=True)
            elif collection_name == "Status":
                collection.create_index([("patient_id", pymongo.ASCENDING)], unique=True)
            elif collection_name == "ObserveList":
                collection.create_index([("observe_id", pymongo.ASCENDING)], unique=True)
            elif collection_name == "Exercise":
                collection.create_index([("observe_id", pymongo.ASCENDING)], unique=True)
            elif collection_name == "BodyHealth":
                collection.create_index([("observe_id", pymongo.ASCENDING)], unique=True)

            logging.info(f"Collection '{collection_name}' created with indexes.")
        else:
            logging.info(f"Collection '{collection_name}' already exists.")

    def close_connection(self) -> None:
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed.")

    def setup_database(self, database_name: str, collection_names: list) -> bool:
        if self.is_database_existed(database_name):
            logging.info(f"Database '{database_name}' already exists, skipping creation.")
            return False  # Indicates that the database already exists
        else:
            self.create_database(database_name)
            for collection_name in collection_names:
                self.create_collection(collection_name)
            logging.info(f"Setup complete for database '{database_name}' and collections {collection_names}")
            return True  # Indicates that the database is newly created


if __name__ == "__main__":
    file_name = __file__.split("\\")[-1].split(".")[0]
    logging.info(f"{file_name} has been loaded")

    # Example usage
    builder = MongoBuilder()
    database_name = "EmoCareCenter"
    collections = ["Profile", "BodyHealth", "CareGivers", "Exercise", "ObserveList", "Status"]
    builder.setup_database(database_name, collections)
    builder.close_connection()
