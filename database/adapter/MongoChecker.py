import logging
import os
from datetime import datetime
from typing import Dict, Any, Tuple

import dotenv
import pymongo
from pymongo import errors

# 載入環境變量
dotenv.load_dotenv()


class MongoChecker:
    def __init__(self, db_name="EmoCareCenter"):
        try:
            self.client = pymongo.MongoClient(os.getenv('MONGODB_CONNECTION_URL'), serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            self.collection = None  # 在進行具體操作前設置集合
            logging.basicConfig(level=logging.INFO, format='[MONGODB_INFO] %(message)s')
            logging.info("MongoDB connection established.")
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logging.error(f"MongoDB connection timeout: {err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def set_collection(self, collection_name: str):
        """設置當前的集合"""
        self.collection = self.db[collection_name]

    @staticmethod
    def validate_body_health_data(data):
        required_fields = ["blood_lipids", "blood_oxygen", "blood_sugar", "consume_calories", "heart_rate",
                           "diastolic_pressure", "systolic_pressure", "patient_id", "observe_id"]

        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field in BodyHealth: {field}")
                return False

        # 檢查數據類型
        numeric_fields = ["blood_lipids", "blood_oxygen", "blood_sugar", "consume_calories", "heart_rate",
                          "diastolic_pressure", "systolic_pressure"]
        string_fields = ["patient_id", "observe_id"]

        for field in numeric_fields:
            if not isinstance(data[field], (int, float)):
                logging.error(f"Field '{field}' in BodyHealth must be a number")
                return False

        for field in string_fields:
            if not isinstance(data[field], str):
                logging.error(f"Field '{field}' in BodyHealth must be a string")
                return False

        return True

    @staticmethod
    def validate_exercise_data(data):
        required_fields = ["type", "duration_minutes", "observe_id", "patient_id"]

        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field in Exercise: {field}")
                return False

        if not isinstance(data['type'], str):
            logging.error("Field 'type' in Exercise must be a string")
            return False
        if not isinstance(data['duration_minutes'], (int, float)):
            logging.error("Field 'duration_minutes' in Exercise must be a number")
            return False
        if not isinstance(data['observe_id'], str):
            logging.error("Field 'observe_id' in Exercise must be a string")
            return False
        if not isinstance(data['patient_id'], str):
            logging.error("Field 'patient_id' in Exercise must be a string")
            return False

        return True

    @staticmethod
    def validate_observe_list_data(data):
        required_fields = ["observe_id", "location", "observed_time", "patient_id"]

        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field in ObserveList: {field}")
                return False

        if not isinstance(data['observe_id'], str):
            logging.error("Field 'observe_id' in ObserveList must be a string")
            return False
        if not isinstance(data['location'], str):
            logging.error("Field 'location' in ObserveList must be a string")
            return False
        if not isinstance(data['observed_time'], datetime):
            logging.error("Field 'observed_time' in ObserveList must be a datetime object")
            return False
        if not isinstance(data['patient_id'], str):
            logging.error("Field 'patient_id' in ObserveList must be a string")
            return False

        return True

    @staticmethod
    def validate_status_data(data: Dict[str, Any]) -> bool:
        """
        Validate the status data dictionary for required fields and their types.

        Parameters:
        - data (Dict[str, Any]): The data dictionary containing patient status information.

        Returns:
        - bool: Return True if the status data is valid, otherwise False.
        """
        required_fields_with_types = {
            "patient_id": str,
            "height": (int, float),
            "weight": (int, float),
            "blood_oxygen": (int, float),
            "blood_sugar": (int, float),
            "diastolic_pressure": (int, float),
            "systolic_pressure": (int, float),
            "blood_lipids": (int, float),
            "heart_rate": (int, float)
        }

        for field, expected_type in required_fields_with_types.items():
            if field not in data:
                error_message = f"Missing field in Status: {field}"
                logging.error(error_message)
                return False

            if not isinstance(data[field], expected_type):
                error_message = f"Field '{field}' in Status must be of type {expected_type}, but got {type(data[field])}"
                logging.error(error_message)
                return False

        return True

    @staticmethod
    def validate_profile_data(data):
        required_fields = ["name", "password", "age", "address", "phone_number", "patient_id"]

        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field in Profile: {field}")
                return False

        if not isinstance(data['name'], str):
            logging.error("Field 'name' in Profile must be a string")
            return False
        if not isinstance(data['password'], str):
            logging.error("Field 'password' in Profile must be a string")
            return False
        if not isinstance(data['age'], int):
            logging.error("Field 'name' in Profile must be a string")
            return False
        if not isinstance(data['address'], str):
            logging.error("Field 'name' in Profile must be a string")
            return False
        if not isinstance(data['phone_number'], str):
            logging.error("Field 'password' in Profile must be a string")
            return False
        if not isinstance(data['patient_id'], str):
            logging.error("Field 'patient_id' in Profile must be a string")
            return False

        return True

    @staticmethod
    def validate_care_givers_data(data):
        required_fields = ["giver_id", "name", "tag", "description", "message_action"]

        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field in CareGivers: {field}")
                return False

        if not isinstance(data['giver_id'], str):
            logging.error("Field 'giver_id' in CareGivers must be a string")
            return False
        if not isinstance(data['name'], str):
            logging.error("Field 'name' in CareGivers must be a string")
            return False
        if not isinstance(data['tag'], str):
            logging.error("Field 'tag' in CareGivers must be a string")
            return False
        if not isinstance(data['description'], str):
            logging.error("Field 'description' in CareGivers must be a string")
            return False
        if not isinstance(data['message_action'], str):
            logging.error("Field 'message_action' in CareGivers must be a string")
            return False

        return True

    def validate_data(self, collection_name, data):
        """根據集合名稱調用相應的數據驗證方法"""
        if collection_name == "BodyHealth":
            return self.validate_body_health_data(data)
        elif collection_name == "Exercise":
            return self.validate_exercise_data(data)
        elif collection_name == "ObserveList":
            return self.validate_observe_list_data(data)
        elif collection_name == "Status":
            return self.validate_status_data(data)
        elif collection_name == "Profile":
            return self.validate_profile_data(data)
        elif collection_name == "CareGivers":
            return self.validate_care_givers_data(data)
        else:
            logging.error(f"Unknown collection: {collection_name}")
            return False

    def insert_many(self, collection_name, data_list):
        """批量插入文档"""
        try:
            self.set_collection(collection_name)
            for data in data_list:
                if not self.validate_data(collection_name, data):
                    logging.error("Invalid data format in batch insert")
                    return
            self.collection.insert_many(data_list)
            logging.info(f"Documents inserted successfully into {collection_name}")
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logging.error(f"MongoDB operation timeout: {err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def read_all(self, collection_name, query):
        """查詢集合中的所有文檔"""
        try:
            self.set_collection(collection_name)
            return list(self.collection.find(query))
        except pymongo.errors.ServerSelectionTimeoutError as err:
            logging.error(f"MongoDB operation timeout: {err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None


if __name__ == '__main__':
    adapter = MongoChecker()
    # 示例：插入 Status 数据
    adapter.read_all("CareGivers", "")
