import streamlit as st
import os
from datetime import datetime

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Hardcoded access code (for demonstration purposes)
ACCESS_CODE = "1234"  # Change this to your desired numerical code

# Page title
st.title("File Sharing and Access App")

# Access code input
access_code = st.text_input("Enter Access Code", type="password")

# Check if the access code is correct
if access_code == ACCESS_CODE:
    st.success("Access granted! You can now upload, view, and download files.")

    # File upload section
    st.header("Upload Files")
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True, type=None)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")

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
            file_path = os.path.join(UPLOAD_DIR, selected_file)
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            st.download_button(
                label=f"Download {selected_file}",
                data=file_bytes,
                file_name=selected_file,
                mime="application/octet-stream"
            )
    else:
        st.info("No files uploaded yet.")
else:
    if access_code:  # Only show error if the user has entered something
        st.error("Incorrect access code. Please try again.")
