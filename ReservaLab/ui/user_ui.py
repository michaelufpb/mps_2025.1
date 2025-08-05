from controller.user_controller import UserController

class UserUI:
    def __init__(self, controller: UserController):
        self.controller = controller

    def start(self):
        while True:
            print("\nUser Management Menu")
            print("1. Add user")
            print("2. List users")
            print("0. Exit")

            choice = input("\nChoose an option: ")

            if choice == "1":
                self.add_user()
            elif choice == "2":
                self.list_users()
            elif choice == "0":
                print("Exiting program")
                break
            else:
                print("Invalid option")

    def add_user(self):
        user_id = input("\nEnter user ID: ")
        name = input("Enter user name: ")
        role = input("Enter user role (Admin/User): ")
        password = input("Enter password: ")
        try:
            self.controller.add_user(user_id, name, role, password)
            print("\nThe user was added successfully")
        except ValueError as e:
            print(f"Error: {e}")

    def list_users(self):
        users = self.controller.list_users()
        if not users:
            print("There aren't any users")
        else:
            print("\nList of users:")
            for user in users:
                print(user)