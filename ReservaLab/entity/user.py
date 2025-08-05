class User:
    def __init__(self, user_id: str, name: str, role: str, password: str):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.password = password

    def __str__(self):
        return f"User {self.user_id}: Name = {self.name} | Role = {self.role}"