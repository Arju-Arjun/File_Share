import streamlit as st
import random
import os
import json
import tempfile
import zipfile  # Make sure to import zipfile module

# Existing constants and data loading functions...
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ACCESS_CODES_FILE = "access_codes.json"
TEXT_SHARES_FILE = "text_shares.json"
FOLDER_SHARES_FILE = "folder_shares.json"
CHAT_ROOMS_FILE = "chat_rooms.json"

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

# Load existing data
file_codes = load_access_codes()
text_shares = load_text_shares()
folder_shares = load_folder_shares()
chat_rooms = load_chat_rooms()

st.title("Secure File & Text Sharing with Live Chat")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select an option", ("File Share", "File Access", "Text Share", "Text Access", "Folder Share", "Folder Access", "Live Chat"))

if option == "Folder Share":
    st.header("Upload a Folder (Will be automatically zipped)")

    # Multiple file uploader simulating folder upload
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True)

    if uploaded_files:
        # Create a temporary directory to store files
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Save each uploaded file in the temporary directory
            for uploaded_file in uploaded_files:
                with open(os.path.join(tmpdirname, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # Generate a zip file from the uploaded folder
            zip_filename = f"folder_{random.randint(1000, 9999)}.zip"
            zip_path = os.path.join(UPLOAD_DIR, zip_filename)

            # Ensure the zip file is being created and the files are added properly
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(tmpdirname):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tmpdirname))

            # Save the access code for the zip file
            access_code = str(random.randint(1000, 9999))
            folder_shares[access_code] = zip_path
            save_folder_shares(folder_shares)

            st.success(f"Folder uploaded and zipped successfully! Your access code is: {access_code}")
            st.write("Save this code to download your folder later.")
