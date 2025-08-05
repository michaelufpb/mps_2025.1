import re
from entity.user import User
from repository.user_repository import UserRepository

class UserController:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def add_user(self, user_id: str, name: str, role: str, password: str):
        self.validate_user_id(user_id)
        self.validate_password(password)
        user = User(user_id, name, role, password)
        self.repository.add_user(user)

    def validate_user_id(self, user_id: str):
        if len(user_id) > 12:
            raise ValueError("Login deve ter no máximo 12 caracteres")
        if not user_id:
            raise ValueError("Login não pode ser vazio")
        if any(char.isdigit() for char in user_id):
            raise ValueError("Login não pode conter números")

    def validate_password(self, password: str):
        if len(password) < 8 or len(password) > 128:
            raise ValueError("Password must be between 8 and 128 characters long")
        if not re.search("[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search("[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search("[0-9]", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search("[@#$%^&+=]", password):
            raise ValueError("Password must contain at least one special character")

    def list_users(self):
        return self.repository.get_all_users()