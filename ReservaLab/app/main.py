from repository.user_repository import UserRepository
from repository.mongo_user_repository import MongoUserRepository
from controller.user_controller import UserController
from ui.user_ui import UserUI

def main():
    persistence_type = input("Choose persistence method (RAM/MONGO): ").strip().upper()

    if persistence_type == "MONGO":
        repository = MongoUserRepository()
    else:
        repository = UserRepository()

    controller = UserController(repository)
    ui = UserUI(controller)
    ui.start()

if __name__ == "__main__":
    main()