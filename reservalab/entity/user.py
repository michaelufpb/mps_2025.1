class User:
    def __init__(self, user_id: str, name: str, role: str, password: str):
        self.user_id = user_id
        self.name = name
        self.role = role  # "admin" ou "usuario"
        self.password = password

    def __str__(self):
        return f"User {self.user_id}: Name = {self.name} | Role = {self.role}"
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "role": self.role,
            "password": self.password
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            role=data["role"],
            password=data["password"]
        )