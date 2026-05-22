import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from models.user import User

class UserDAOMongo:
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        mongo_host = os.getenv("MONGODB_HOST")
        mongo_port = os.getenv("MONGODB_PORT")
        mongo_user = os.getenv("MONGODB_USERNAME")
        mongo_pass = os.getenv("MONGODB_PASSWORD")
        db_name = os.getenv("MONGODB_DB_NAME")

        self.client = MongoClient(
            f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/"
        )

        self.db = self.client[db_name]
        self.collection = self.db["users"]

    def select_all(self):
        rows = self.collection.find()
        return [
            User(
                str(row.get("_id")),
                row.get("name"),
                row.get("email")
            )
            for row in rows
        ]

    def insert(self, user):
        result = self.collection.insert_one({
            "name": user.name,
            "email": user.email
        })
        return str(result.inserted_id)

    def update(self, user):
        self.collection.update_one(
            {"_id": ObjectId(user.id)},
            {"$set": {
                "name": user.name,
                "email": user.email
            }}
        )

    def delete(self, user_id):
        self.collection.delete_one({
            "_id": ObjectId(user_id)
        })

    def delete_all(self):
        """ Empty users collection in MongoDB """
        self.collection.delete_many({})

    def close(self):
        """ Close MongoDB connection """
        self.client.close()