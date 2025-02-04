import streamlit as st
import os
from datetime import datetime
import random

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Page title and navigation bar
st.title("File Share App")
st.markdown("---")  # Horizontal line for separation

# Section 1: File Upload
st.header("Upload Files")
uploaded_file = st.file_uploader("Choose a file to upload", type=None)
if uploaded_file:
    # Save the file
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Generate a 4-digit access code
    access_code = str(random.randint(1000, 9999))
    
    # Save the access code and file mapping (for demo, we use a dictionary)
    if not hasattr(st.session_state, "file_access_codes"):
        st.session_state.file_access_codes = {}
    st.session_state.file_access_codes[access_code] = uploaded_file.name
    
    # Display success message and access code
    st.success("File uploaded successfully!")
    st.info(f"Your access code: **{access_code}**")

# Section 2: Access Files
st.header("Access Files")
access_code_input = st.text_input("Enter Access Code", max_chars=4, placeholder="1234")

if access_code_input:
    if hasattr(st.session_state, "file_access_codes"):
        if access_code_input in st.session_state.file_access_codes:
            file_name = st.session_state.file_access_codes[access_code_input]
            file_path = os.path.join(UPLOAD_DIR, file_name)
            
            # Display file details
            st.success("Access granted!")
            st.write(f"File Name: **{file_name}**")
            st.write(f"File Size: **{os.path.getsize(file_path)} bytes**")
            
            # Download button
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            st.download_button(
                label="Download File",
                data=file_bytes,
                file_name=file_name,
                mime="application/octet-stream"
            )
        else:
            st.error("Invalid access code. Please try again.")
    else:
        st.error("No files uploaded yet.")
