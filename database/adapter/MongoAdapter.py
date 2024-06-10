import logging

from bson.son import SON
from werkzeug.security import check_password_hash

from modules import get_caregivers
from .MongoChecker import MongoChecker


class MongoAdapter(MongoChecker):
    def get_top_exercises(self):
        try:
            # 聚合 Exercise 表中的运动时间
            pipeline = [
                {"$group": {"_id": "$patient_id", "total_duration": {"$sum": "$duration_minutes"}}},
                {"$sort": SON([("total_duration", -1)])},  # 按 total_duration 倒序排序
                {"$limit": 3}  # 只取前三名
            ]

            exercise_result = list(self.db.Exercise.aggregate(pipeline))

            # 获取前三名患者的 patient_id
            top_patients = [doc["_id"] for doc in exercise_result]

            # 在 Profile 表中找到这些患者的名字
            profile_result = self.db.Profile.find({"patient_id": {"$in": top_patients}})

            # 创建 patient_id 到名字的映射
            patient_name_map = {doc["patient_id"]: doc["name"] for doc in profile_result}

            # 将结果合并，包含 patient_id, name 和 total_duration
            top_exercises = []
            for doc in exercise_result:
                patient_id = doc["_id"]
                total_duration = doc["total_duration"]
                name = patient_name_map.get(patient_id, "Unknown")
                top_exercises.append({
                    "patient_id": patient_id,
                    "name": name,
                    "total_duration": total_duration
                })

            return top_exercises

        except Exception as e:
            logging.error(f"An error occurred during aggregation: {e}")
            return []

    def get_care_givers_data(self):
        collection_name = "CareGivers"
        care_givers_data = []

        result = self.db[collection_name].find({})

        for doc in result:
            care_givers_data.append({
                "giver_id": doc["giver_id"],
                "name": doc["name"],
                "tag": doc["tag"],
                "description": doc["description"],
                "message_action": doc["message_action"]
            })

        return care_givers_data

    def get_care_givers_bubbles(self, domain):
        care_givers_data = self.get_care_givers_data()
        care_givers_bubbles = get_caregivers(domain, care_givers_data)

        return care_givers_bubbles

    def is_user_correct(self, patient_id, password):
        try:
            # 在 Profile 表中查找匹配的文档
            user = self.db.Profile.find_one({"patient_id": patient_id})

            if user is None:
                # 未找到匹配的用户
                return False

            # 如果密码是明文存储的（不推荐），可以直接比较
            # return user["password"] == password

            # 如果密码是加密存储的，使用 werkzeug.security 的 check_password_hash
            return check_password_hash(user["password"], password)

        except Exception as e:
            logging.error(f"An error occurred during user validation: {e}")
            return False

    def get_profile_by_patient_id(self, patient_id):
        profile = self.db.Profile.find_one({"patient_id": patient_id})
        if profile:
            profile['_id'] = str(profile['_id'])  # 转换 _id 为字符串以便于 JSON 序列化
        return profile

    def get_status_by_patient_id(self, patient_id):
        status = self.db.Status.find_one({"patient_id": patient_id})
        if status:
            status['_id'] = str(status['_id'])  # 转换 _id 为字符串以便于 JSON 序列化
        return status

    def get_exercise_by_patient_id(self, patient_id):
        exercise_list = self.db.Exercise.find({"patient_id": patient_id})
        exercise_data = [exercise for exercise in exercise_list]
        return exercise_data

    def get_observe_list_by_patient_id(self, patient_id):
        observe_list = self.db.ObserveList.find({"patient_id": patient_id})
        observe_list_data = [observe for observe in observe_list]
        return observe_list_data

    def get_body_health_by_patient_id(self, patient_id):
        body_health = self.db.BodyHealth.find_one({"patient_id": patient_id})
        if body_health:
            body_health['_id'] = str(body_health['_id'])
        return body_health
