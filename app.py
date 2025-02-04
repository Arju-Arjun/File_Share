import streamlit as st
import os
from datetime import datetime

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Page title
st.title("File Sharing and Access App")

# File upload section
st.header("Upload Files")
uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True, type=None)
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Generate a unique access code based on upload time
        upload_time = datetime.now().strftime('%Y%m%d%H%M%S')  # Format: YYYYMMDDHHMMSS
        access_code = upload_time  # Use upload time as the access code
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.info(f"Access Code for this file: **{access_code}**")  # Display the access code

# File list section
st.header("Uploaded Files")
files = os.listdir(UPLOAD_DIR)
if files:
    # Display a table of uploaded files
    file_data = []
    for file_name in files:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        file_size = os.path.getsize(file_path)
        upload_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        file_data.append([file_name, file_size, upload_time])

    # Display the table
    st.table({
        "File Name": [item[0] for item in file_data],
        "File Size (Bytes)": [item[1] for item in file_data],
        "Upload Time": [item[2] for item in file_data]
    })

    # File download section
    st.header("Download Files")
    selected_file = st.selectbox("Select a file to download", files)
    if selected_file:
        # Get the upload time of the selected file
        file_path = os.path.join(UPLOAD_DIR, selected_file)
        upload_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y%m%d%H%M%S')
        
        # Ask the user to enter the access code
        access_code_input = st.text_input(f"Enter Access Code for '{selected_file}'", type="password")
        
        # Verify the access code
        if access_code_input == upload_time:  # Compare with the upload time
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            st.download_button(
                label=f"Download {selected_file}",
                data=file_bytes,
                file_name=selected_file,
                mime="application/octet-stream"
            )
        elif access_code_input:  # Show error only if the user has entered something
            st.error("Incorrect access code. Please try again.")
else:
    st.info("No files uploaded yet.")
