from datetime import datetime
from typing import Any, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyraksRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        payload = {
            "user_id": ObjectId(user_id),
            "type": data["type"],
            "price": data["price"],
            "address": data["address"],
            "area": data["area"],
            "rooms_count": data["rooms_count"],
            "description": data["description"],
        }

        insert_result = self.database["shanyraks"].insert_one(payload)
        print(insert_result)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str) -> List[dict]:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(shanyrak_id)
            }
        )
        return shanyrak

    def update_shanyrak(self, user_id: str, shanyrak_id: str, data: dict[str, Any]) -> UpdateResult:
        updated_shanyrak = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

        return updated_shanyrak
    
    def delete_shanyrak(self, user_id: str, shanyrak_id: str) -> DeleteResult:
        deleted_shanyrak = self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        return deleted_shanyrak
