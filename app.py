import streamlit as st
import random
import os
import json
import tempfile
import zipfile

# Constants for file storage
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ACCESS_CODES_FILE = "access_codes.json"
TEXT_SHARES_FILE = "text_shares.json"
FOLDER_SHARES_FILE = "folder_shares.json"
CHAT_ROOMS_FILE = "chat_rooms.json"

# Load and save functions
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Load data
file_codes = load_json(ACCESS_CODES_FILE)
text_shares = load_json(TEXT_SHARES_FILE)
folder_shares = load_json(FOLDER_SHARES_FILE)
chat_rooms = load_json(CHAT_ROOMS_FILE)

st.title("Secure File & Text Sharing with Live Chat")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select an option", 
                          ("File Share", "File Access", "Text Share", "Text Access", 
                           "Folder Share", "Folder Access", "Live Chat"))

# Live Chat
if option == "Live Chat":
    st.sidebar.title("Live Chat Options")
    chat_action = st.sidebar.radio("Choose an action", ("Create a New Chat", "Join an Existing Chat"))

    if chat_action == "Create a New Chat":
        user_name = st.text_input("Enter your user name")

        if user_name:
            chat_code = str(random.randint(1000, 9999))
            chat_rooms[chat_code] = {"messages": []}
            save_json(CHAT_ROOMS_FILE, chat_rooms)

            st.header("New Chat Room Created")
            st.success(f"Chat Room Code: {chat_code}")
        else:
            st.error("Enter a user name.")

    elif chat_action == "Join an Existing Chat":
        user_name = st.text_input("Enter your user name")

        if user_name:
            chat_code = st.text_input("Enter Chat Room Code")

            if chat_code and chat_code in chat_rooms:
                st.header(f"Chat Room {chat_code}")

                if chat_code not in st.session_state:
                    st.session_state[chat_code] = chat_rooms[chat_code]["messages"]

                # Display chat messages
                for msg in st.session_state[chat_code]:
                    st.markdown(f"**{msg['user']}**: {msg['message']}")

                # Chat input box
                chat_input = st.text_input("Type your message", key=f"chat_input_{chat_code}")

                if st.button("Send Message"):
                    if chat_input:
                        new_message = {"user": user_name, "message": chat_input}
                        st.session_state[chat_code].append(new_message)
                        chat_rooms[chat_code]["messages"].append(new_message)
                        save_json(CHAT_ROOMS_FILE, chat_rooms)

                        # Clear the input box after sending the message
                        st.experimental_rerun()
            else:
                st.error("Invalid chat room code.")
        else:
            st.error("Enter a user name before joining.")
