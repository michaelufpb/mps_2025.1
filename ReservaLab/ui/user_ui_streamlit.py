import streamlit as st
from controller.user_controller import UserController

class UserUIStreamlit:
    def __init__(self, controller: UserController):
        self.controller = controller

    def start(self):
        st.set_page_config(
            page_title="User Management System",
            page_icon="👥",
            layout="wide"
        )
        
        st.title("👥 User Management System")
        st.markdown("---")
        
        # Sidebar for navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Choose an option:",
            ["Add User", "List Users"]
        )
        
        if page == "Add User":
            self.add_user_page()
        elif page == "List Users":
            self.list_users_page()

    def add_user_page(self):
        st.header("➕ Add New User")
        st.markdown("---")
        
        with st.form("add_user_form"):
            user_id = st.text_input("User ID", max_chars=12, help="Maximum 12 characters, no numbers allowed")
            name = st.text_input("Full Name")
            role = st.selectbox("Role", ["User", "Admin"])
            password = st.text_input("Password", type="password", help="8-128 characters, must contain lowercase, uppercase, digit, and special character")
            
            submitted = st.form_submit_button("Add User")
            
            if submitted:
                if not user_id or not name or not password:
                    st.error("Please fill in all fields!")
                else:
                    try:
                        self.controller.add_user(user_id, name, role, password)
                        st.success("The user was added successfully")
                    except ValueError as e:
                        st.error(f"Error: {e}")

    def list_users_page(self):
        st.header("📋 List of Users")
        st.markdown("---")
        
        users = self.controller.list_users()
        
        if not users:
            st.info("There aren't any users")
        else:
            st.write("List of users:")
            for user in users:
                st.write(user)

def main():
    # This would be called from your main application
    # You'll need to initialize the controller and repository here
    pass

if __name__ == "__main__":
    main() 