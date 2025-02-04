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

# File Sharing
if option == "File Share":
    st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "pdf", "txt", "csv", "docx"])

    if uploaded_file:
        access_code = str(random.randint(1000, 9999))
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_codes[access_code] = file_path
        save_json(ACCESS_CODES_FILE, file_codes)

        st.success(f"File uploaded! Access code: {access_code}")
        st.write("Save this code to download your file later.")

# File Access
elif option == "File Access":
    st.header("Access Your File")
    access_code_input = st.text_input("Enter 4-digit access code")

    if st.button("Access File"):
        file_codes = load_json(ACCESS_CODES_FILE)
        if access_code_input in file_codes:
            file_path = file_codes[access_code_input]
            with open(file_path, "rb") as f:
                st.download_button("Download File", f, file_name=os.path.basename(file_path))
        else:
            st.error("Invalid access code!")

# Text Sharing
elif option == "Text Share":
    st.header("Share a Text Message")
    text_input = st.text_area("Enter text")

    if st.button("Generate Access Code"):
        if text_input:
            access_code = str(random.randint(1000, 9999))
            text_shares[access_code] = text_input
            save_json(TEXT_SHARES_FILE, text_shares)
            st.success(f"Text shared! Access code: {access_code}")
        else:
            st.error("Please enter some text before sharing.")

# Text Access
elif option == "Text Access":
    st.header("Access Shared Text")
    access_code_input = st.text_input("Enter 4-digit access code")

    if st.button("Access Text"):
        text_shares = load_json(TEXT_SHARES_FILE)
        if access_code_input in text_shares:
            st.text_area("Shared Text", text_shares[access_code_input], height=200, disabled=True)
        else:
            st.error("Invalid access code!")

# Folder Sharing
elif option == "Folder Share":
    st.header("Upload a Folder (Converted to ZIP)")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

    if uploaded_files:
        with tempfile.TemporaryDirectory() as tmpdirname:
            for uploaded_file in uploaded_files:
                with open(os.path.join(tmpdirname, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            zip_filename = f"folder_{random.randint(1000, 9999)}.zip"
            zip_path = os.path.join(UPLOAD_DIR, zip_filename)

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(tmpdirname):
                    for file in files:
                        zipf.write(os.path.join(root, file), file)

            access_code = str(random.randint(1000, 9999))
            folder_shares[access_code] = zip_path
            save_json(FOLDER_SHARES_FILE, folder_shares)

            st.success(f"Folder uploaded & zipped! Access code: {access_code}")

# Folder Access
elif option == "Folder Access":
    st.header("Access Your Folder")
    access_code_input = st.text_input("Enter 4-digit access code")

    if st.button("Access Folder"):
        folder_shares = load_json(FOLDER_SHARES_FILE)
        if access_code_input in folder_shares:
            zip_path = folder_shares[access_code_input]
            with open(zip_path, "rb") as f:
                st.download_button("Download Folder", f, file_name=os.path.basename(zip_path))
        else:
            st.error("Invalid access code!")

# Live Chat
# Live Chat
elif option == "Live Chat":
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
                        # Append the new message to session state and chat_rooms
                        st.session_state[chat_code].append(new_message)
                        chat_rooms[chat_code]["messages"].append(new_message)
                        save_json(CHAT_ROOMS_FILE, chat_rooms)

                        # Directly update the UI with new message
                        st.session_state[f"new_message_{chat_code}"] = new_message  # Store the new message in session state
            else:
                st.error("Invalid chat room code.")
        else:
            st.error("Enter a user name before joining.")

