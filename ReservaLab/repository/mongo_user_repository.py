from pymongo import MongoClient
from entity.user import User
from repository.user_repository import UserRepository

class MongoUserRepository(UserRepository):
    def __init__(self, db_name="user_management", collection_name="users"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_user(self, user: User):
        try:
            self.collection.insert_one({
                "user_id": user.user_id,
                "name": user.name,
                "role": user.role,
                "password": user.password
            })
        except Exception as e:
            print(f"Error saving user to MongoDB: {e}")

    def get_all_users(self):
        try:
            users = self.collection.find()
            return [User(user_id=user["user_id"], name=user["name"], role=user["role"], password=user["password"]) for user in users]
        except Exception as e:
            print(f"Error retrieving users from MongoDB: {e}")
            return []

    def __del__(self):
        self.client.close()