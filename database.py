from typing import Tuple

import pymongo
from datetime import datetime


class Database:
    """ Класс работы с базой данных """

    def __init__(self, name):
        self.name = name
        self.client = pymongo.MongoClient("194.87.186.63", username='Admin', password='PasswordForMongo63',
                                          authSource='admin', authMechanism='SCRAM-SHA-256')
        self.db = self.client.OTP
        self.users = self.db.users
        self.results = self.db.results

    def record_user_info(self, user_id: int, full_name: str, city: str) -> None:
        self.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "full_name": full_name,
                    "city": city
                }
            },
            upsert=True
        )

    def record_completion(self, user_id: int, score: int) -> None:
        completion_time = datetime.utcnow()  # Используем UTC для согласованного времени
        self.results.update_one(
            {"user_id": user_id},
            {"$set": {'completion_time': completion_time, 'score': score}},
            upsert=True
        )

    def get_best_user(self) -> Tuple[int, int, datetime]:
        # Извлечение данных о пользователях и сортировка сначала по баллам, а затем по времени
        cursor = self.results.find().sort(
            [("score", pymongo.DESCENDING), ("completion_time", pymongo.ASCENDING)]).limit(1)
        best_user = cursor.next()
        return best_user.get("user_id"), best_user.get("score"), best_user.get("completion_time")


database = Database("Street")
