import streamlit as st
from ui.user_ui_streamlit import UserUIStreamlit
from controller.user_controller import UserController
from repository.mongo_user_repository import MongoUserRepository
from repository.user_repository import UserRepository

def main():
    # Initialize the repository and controller with session state persistence
    # repository = MongoUserRepository()
    if 'user_repository' not in st.session_state:
        st.session_state.user_repository = UserRepository()
    
    controller = UserController(st.session_state.user_repository)
    
    # Initialize and start the Streamlit UI
    ui = UserUIStreamlit(controller)
    ui.start()

if __name__ == "__main__":
    main() 