import os
from dotenv import load_dotenv
from pymongo import MongoClient
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
        """ Select all users from MongoDB """
        rows = self.collection.find()
        return [
            User(
                row.get("id"),
                row.get("name"),
                row.get("email")
            )
            for row in rows
        ]

    def insert(self, user):
        """ Insert given user into MongoDB """
        self.collection.insert_one({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
        

    def update(self, user):
        """ Update given user in MongoDB """
        self.collection.updateOne(
            {"id": user.id},
            {
                "$set": { "name": user.name, "email": user.email }
            }
        )

    def delete(self, user_id):
        """ Delete user from MongoDB with given user ID """
        self.collection.deleteOne(
            {"id": user_id}
        )