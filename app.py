import streamlit as st
import random
import os
import json
import zipfile
import shutil

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# JSON file to store access codes persistently
ACCESS_CODES_FILE = "access_codes.json"
TEXT_SHARES_FILE = "text_shares.json"
FOLDER_SHARES_FILE = "folder_shares.json"

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

# Load existing access codes
file_codes = load_access_codes()
text_shares = load_text_shares()
folder_shares = load_folder_shares()

st.title("Secure File & Text Sharing")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select an option", ("File Share", "File Access", "Text Share", "Text Access", "Folder Share", "Folder Access"))

if option == "File Share":
    st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a file to upload", type=["png", "jpg", "pdf", "txt", "csv", "docx"])
    
    if uploaded_file is not None:
        # Generate a 4-digit access code
        access_code = str(random.randint(1000, 9999))
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Store the access code and file path persistently
        file_codes[access_code] = file_path
        save_access_codes(file_codes)
        
        st.success(f"File uploaded successfully! Your access code is: {access_code}")
        st.write("Save this code to download your file later.")

elif option == "File Access":
    st.header("Access Your File")
    access_code_input = st.text_input("Enter your 4-digit access code")
    
    if st.button("Access File"):
        file_codes = load_access_codes()  # Reload the latest codes
        if access_code_input in file_codes:
            file_path = file_codes[access_code_input]
            with open(file_path, "rb") as f:
                st.download_button("Download File", f, file_name=os.path.basename(file_path))
        else:
            st.error("Invalid access code. Please try again.")

elif option == "Text Share":
    st.header("Share a Text Message")
    text_input = st.text_area("Enter text to share")
    
    if st.button("Generate Access Code"):
        if text_input:
            access_code = str(random.randint(1000, 9999))
            text_shares[access_code] = text_input
            save_text_shares(text_shares)
            st.success(f"Text shared successfully! Your access code is: {access_code}")
            st.write("Save this code to access your text later.")
        else:
            st.error("Please enter some text before sharing.")

elif option == "Text Access":
    st.header("Access Shared Text")
    access_code_input = st.text_input("Enter your 4-digit access code")
    
    if st.button("Access Text"):
        text_shares = load_text_shares()  # Reload latest text shares
        if access_code_input in text_shares:
            st.text_area("Shared Text", text_shares[access_code_input], height=200, disabled=True)
        else:
            st.error("Invalid access code. Please try again.")

elif option == "Folder Share":
    st.header("Upload a Folder (Will be converted to Zip)")
    uploaded_folder = st.file_uploader("Choose a folder to upload", type=["zip"])
    
    if uploaded_folder is not None:
        # Generate a 4-digit access code
        access_code = str(random.randint(1000, 9999))
        folder_path = os.path.join(UPLOAD_DIR, f"folder_{access_code}.zip")
        
        # Save the folder as a zip file
        with open(folder_path, "wb") as f:
            f.write(uploaded_folder.getbuffer())
        
        # Store the access code and folder path persistently
        folder_shares[access_code] = folder_path
        save_folder_shares(folder_shares)
        
        st.success(f"Folder uploaded successfully as a zip! Your access code is: {access_code}")
        st.write("Save this code to download your folder later.")

elif option == "Folder Access":
    st.header("Access Your Folder")
    access_code_input = st.text_input("Enter your 4-digit access code")
    
    if st.button("Access Folder"):
        folder_shares = load_folder_shares()  # Reload latest folder shares
        if access_code_input in folder_shares:
            folder_path = folder_shares[access_code_input]
            with open(folder_path, "rb") as f:
                st.download_button("Download Folder", f, file_name=os.path.basename(folder_path))
        else:
            st.error("Invalid access code. Please try again.")
