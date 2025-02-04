import streamlit as st
import random
import os
import json

# Existing constants and data loading functions...
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ACCESS_CODES_FILE = "access_codes.json"
TEXT_SHARES_FILE = "text_shares.json"
FOLDER_SHARES_FILE = "folder_shares.json"
CHAT_ROOMS_FILE = "chat_rooms.json"

def load_chat_rooms():
    if os.path.exists(CHAT_ROOMS_FILE):
        with open(CHAT_ROOMS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chat_rooms(data):
    with open(CHAT_ROOMS_FILE, "w") as f:
        json.dump(data, f)

# Load existing chat rooms
chat_rooms = load_chat_rooms()

st.title("Secure File & Text Sharing with Live Chat")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select an option", ("File Share", "File Access", "Text Share", "Text Access", "Folder Share", "Folder Access", "Live Chat"))

if option == "Live Chat":
    st.sidebar.title("Live Chat Options")
    chat_action = st.sidebar.radio("Choose an action", ("Create a New Chat", "Join an Existing Chat"))
    
    if chat_action == "Create a New Chat":
        # Create a new chat room
        chat_code = str(random.randint(1000, 9999))
        
        # Initialize chat room with an empty message list
        chat_rooms[chat_code] = {"messages": []}
        save_chat_rooms(chat_rooms)
        
        st.header("Create a New Chat Room")
        st.success(f"Your chat room is created! Share this code with others to join: {chat_code}")
        
    elif chat_action == "Join an Existing Chat":
        # Join an existing chat room
        chat_code = st.text_input("Enter Chat Room Code")
        
        if chat_code:
            if chat_code in chat_rooms:
                st.header(f"Chat Room {chat_code}")
                if "messages" not in st.session_state:
                    st.session_state.messages = []

                # Display existing messages in the chat room
                for msg in chat_rooms[chat_code]["messages"]:
                    st.markdown(f"**{msg['user']}**: {msg['message']}")

                # Input to send message
                chat_input = st.text_input("Type your message")
                
                if st.button("Send Message"):
                    if chat_input:
                        # Add the message to the chat room's messages
                        user_name = f"User {random.randint(1, 100)}"  # You can replace this with actual user names
                        chat_rooms[chat_code]["messages"].append({"user": user_name, "message": chat_input})
                        save_chat_rooms(chat_rooms)
                        
                        # Show the new message in the chat
                        st.session_state.messages.append({"user": user_name, "message": chat_input})
                        st.text_input("Type your message", value="", key="chat_input")  # Clear input box
            else:
                st.error("Invalid chat room code. Please try again.")
