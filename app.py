import streamlit as st
import random
import os
import json

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# JSON file to store access codes persistently
ACCESS_CODES_FILE = "access_codes.json"

def load_access_codes():
    if os.path.exists(ACCESS_CODES_FILE):
        with open(ACCESS_CODES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_access_codes(data):
    with open(ACCESS_CODES_FILE, "w") as f:
        json.dump(data, f)

# Load existing access codes
file_codes = load_access_codes()

st.title("Secure File Upload & Access")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select an option", ("Upload File", "Access File"))

if option == "Upload File":
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

elif option == "Access File":
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
