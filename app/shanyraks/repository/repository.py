from datetime import datetime
from typing import Any, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyraksRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any], location: dict[str, Any]):
        payload = {
            "user_id": ObjectId(user_id),
            "type": data["type"],
            "price": data["price"],
            "address": data["address"],
            "area": data["area"],
            "rooms_count": data["rooms_count"],
            "description": data["description"],
            "location": location,
        }

        insert_result = self.database["shanyraks"].insert_one(payload)
        print(insert_result)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str) -> List[dict]:
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        return shanyrak

    def update_shanyrak(
        self, user_id: str, shanyrak_id: str, data: dict[str, Any]
    ) -> UpdateResult:
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

    def add_media_to_shanyrak(self, user_id: str, shanyrak_id: str, data: str):
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={"$push": {"media": data}},
        )

    def delete_media_from_shanyrak(self, user_id: str, shanyrak_id: str, data: str):
        shanyrak = self.database["shanyraks"].find_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        if shanyrak:
            media = shanyrak.get("media", [])
            media.remove(data)
            self.database["shanyraks"].update_one(
                {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
                {"$set": {"media": media}},
            )

    def add_comment_to_shanyrak(self, user_id: str, shanyrak_id: str, comment: str):
        insert_comment = {
            "_id": str(ObjectId()),
            "content": comment,
            "created_at": datetime.utcnow(),
            "user_id": user_id,
        }

        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={"$push": {"comments": insert_comment}},
        )

    def get_comments(self, shanyrak_id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        return shanyrak["comments"]

    def update_comment(
        self, comment_id: str, shanyrak_id: str, user_id: str, content: str
    ):
        filter = {
            "_id": ObjectId(shanyrak_id),
            "comments": {"$elemMatch": {"_id": comment_id, "user_id": user_id}},
        }
        update = {"$set": {"comments.$.content": content}}

        updated_shanyrak = self.database["shanyraks"].update_one(filter, update)
        return updated_shanyrak

    def delete_comment(self, shanyrak_id: str, comment_id: str):
        self.database["shanyraks"].update_one(
            {"_id": ObjectId(shanyrak_id)},
            {"$pull": {"comments": {"_id": comment_id}}}
        )
