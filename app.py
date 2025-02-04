import streamlit as st
import random
import os

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dictionary to store access codes
if "file_codes" not in st.session_state:
    st.session_state.file_codes = {}

st.title("Secure File Upload & Access")

# File Upload Section
st.header("Upload a File")
uploaded_file = st.file_uploader("Choose a file to upload", type=["png", "jpg", "pdf", "txt", "csv", "docx"])

if uploaded_file is not None:
    # Generate a 4-digit access code
    access_code = str(random.randint(1000, 9999))
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Store the access code and file path
    st.session_state.file_codes[access_code] = file_path
    
    st.success(f"File uploaded successfully! Your access code is: {access_code}")
    st.write("Save this code to download your file later.")

# File Access Section
st.header("Access Your File")
access_code_input = st.text_input("Enter your 4-digit access code")

if st.button("Access File"):
    if access_code_input in st.session_state.file_codes:
        file_path = st.session_state.file_codes[access_code_input]
        with open(file_path, "rb") as f:
            st.download_button("Download File", f, file_name=os.path.basename(file_path))
    else:
        st.error("Invalid access code. Please try again.")
