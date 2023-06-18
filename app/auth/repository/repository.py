from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

    def create_fav(self, user_id: str, shanyrak_id: str):
        favorites = self.get_favorites(user_id)
        if shanyrak_id not in favorites:
            favorites.append(shanyrak_id)

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "favorite": favorites,
                }
            },
        )

    def get_favorites(self, user_id: str):
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id)
            }
        )
        return user["favorite"] if "favorite" in user else []
    
    def get_shanyrak_fav(self, user_id: str):
        shanyrak_ids = self.get_favorites(user_id)
        list_shanyrak_id = [ObjectId(shanyrak_id) for shanyrak_id in shanyrak_ids] 
        shanyraks = self.database["shanyraks"].find(
            {
                "_id": {"$in": list_shanyrak_id}
            }
        )
        return list(shanyraks)
    
    def delete_favorite(self, user_id: str, shanyrak_id: str):
        favorites = self.get_favorites(user_id)
        if shanyrak_id in favorites:
            favorites.remove(shanyrak_id)
        
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "favorite": favorites,
                }
            },
        )

    def add_avatar(self, user_id: str, data: str):
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$push": {"avatar_url": data}},
        )
        
