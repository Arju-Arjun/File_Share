import streamlit as st
import random
import os
import json
from datetime import datetime

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# JSON file to store access codes persistently
ACCESS_CODES_FILE = "access_codes.json"
TEXT_SHARES_FILE = "text_shares.json"
FOLDER_SHARES_FILE = "folder_shares.json"
CHAT_ROOMS_FILE = "chat_rooms.json"

# Dictionary to store text shares
def load_access_codes():
    if os.path.exists(ACCESS_CODES_FILE):
        with open(ACCESS_CODES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_access_codes(data):
    with open(ACCESS_CODES_FILE, "w") as f:
        json.dump(data, f)

def load_text_shares():
    if os.path.exists(TEXT_SHARES_FILE):
        with open(TEXT_SHARES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_text_shares(data):
    with open(TEXT_SHARES_FILE, "w") as f:
        json.dump(data, f)

def load_folder_shares():
    if os.path.exists(FOLDER_SHARES_FILE):
        with open(FOLDER_SHARES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_folder_shares(data):
    with open(FOLDER_SHARES_FILE, "w") as f:
        json.dump(data, f)

def load_chat_rooms():
    if os.path.exists(CHAT_ROOMS_FILE):
        with open(CHAT_ROOMS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chat_rooms(data):
    with open(CHAT_ROOMS_FILE, "w") as f:
        json.dump(data, f)

# Load existing access codes, text shares, folder shares, and chat rooms
file_codes = load_access_codes()
text_shares = load_text_shares()
folder_shares = load_folder_shares()
chat_rooms = load_chat_rooms()

st.title("Secure File & Text Sharing with Live Chat")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select an option", ("File Share", "File Access", "Text Share", "Text Access", "Folder Share", "Folder Access", "Live Chat"))

if option == "Live Chat":
    st.sidebar.title("Live Chat Options")
    chat_option = st.sidebar.radio("Select Option", ["Create a Chat Room", "Join a Chat Room"])

    if chat_option == "Create a Chat Room":
        st.header("Create a New Chat Room")
        chat_name = st.text_input("Enter a name for your chat room")
        
        if st.button("Create Chat Room"):
            if chat_name:
                # Generate a unique chat room code
                chat_code = str(random.randint(1000, 9999))
                
                # Store the new chat room in chat_rooms with members list
                chat_rooms[chat_code] = {"name": chat_name, "members": [], "messages": []}
                save_chat_rooms(chat_rooms)
                
                st.success(f"Chat room '{chat_name}' created successfully! Your chat room code is: {chat_code}")
            else:
                st.error("Please enter a name for the chat room.")

    elif chat_option == "Join a Chat Room":
        st.header("Join a Chat Room")
        room_code = st.text_input("Enter a chat room code to join")
        user_name = st.text_input("Enter your name to join the chat")
        
        if st.button("Join Chat Room"):
            if room_code in chat_rooms and user_name:
                # Add the user to the chat room's members list
                if user_name not in chat_rooms[room_code]["members"]:
                    chat_rooms[room_code]["members"].append(user_name)
                    save_chat_rooms(chat_rooms)
                
                # Display chat room info
                st.subheader(f"Chat Room: {chat_rooms[room_code]['name']}")
                
                # Show the list of members
                st.write("Members:")
                for member in chat_rooms[room_code]["members"]:
                    st.write(member)
                
                # Initialize chat session for the room if not initialized
                if "messages" not in st.session_state:
                    st.session_state.messages = chat_rooms[room_code]["messages"]
                
                # Display chat messages
                chat_display = st.empty()  # Empty element to update chat display dynamically
                with chat_display.container():
                    for message in st.session_state.messages:
                        st.markdown(message)
                
                # Send new message
                chat_input = st.text_input("Type your message", value="")
                
                if st.button("Send Message"):
                    if chat_input:
                        # Create a timestamp for the message
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message = f"{user_name} [{timestamp}]: {chat_input}"
                        
                        # Append the new message
                        st.session_state.messages.append(message)
                        chat_rooms[room_code]["messages"] = st.session_state.messages  # Save the updated messages
                        save_chat_rooms(chat_rooms)
                        
                        # Re-render the chat messages (this part is key for immediate display)
                        with chat_display.container():
                            for message in st.session_state.messages:
                                st.markdown(message)
                        
                        # Clear the input box after sending
                        st.session_state.chat_input = ""  # Reset the chat input box

                # Display the input box with previous message cleared
                chat_input = st.text_input("Type your message", value="")
                
            else:
                st.error("Invalid chat room code or missing name. Please try again.")
