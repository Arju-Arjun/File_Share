import streamlit as st
import os
from datetime import datetime

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Page title
st.title("File Sharing and Access App")

# Section 1: Upload Files
st.header("Upload Files")
uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True, type=None)
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Generate access code based on upload time
        upload_time = datetime.now().strftime('%Y%m%d%H%M%S')  # Format: YYYYMMDDHHMMSS
        access_code = upload_time  # Use upload time as the access code
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.info(f"Access Code for this file: **{access_code}**")  # Display the access code

# Section 2: Access Files
st.header("Access Files")
access_code_input = st.text_input("Enter Access Code to access files", type="password")

if access_code_input:
    # Check if any file matches the access code
    files = os.listdir(UPLOAD_DIR)
    matching_files = []
    for file_name in files:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        upload_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y%m%d%H%M%S')
        if upload_time == access_code_input:
            matching_files.append(file_name)

    if matching_files:
        st.success("Access granted! You can now download the file.")
        for file_name in matching_files:
            file_path = os.path.join(UPLOAD_DIR, file_name)
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            st.download_button(
                label=f"Download {file_name}",
                data=file_bytes,
                file_name=file_name,
                mime="application/octet-stream"
            )
    else:
        st.error("No file found with the provided access code. Please check the code and try again.")
