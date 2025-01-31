import streamlit as st
import file_handler
import os

st.title("Secure File Upload & Access System")

name = st.text_input("Enter pass key", type="password")

if st.button("Submit"):
    if name == "arjun":
        st.subheader("Upload a File")
        uploaded_file = st.file_uploader("Choose a file", type=None)

        if uploaded_file is not None:
            file_code = file_handler.save_file(uploaded_file)
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            st.write(f"Your access code: `{file_code}`")
            st.write("Use this code to access or delete your file later.")

        st.subheader("Access a File")
        access_code = st.text_input("Enter access code to retrieve file")

        if st.button("Download File"):
            file_name = file_handler.get_file_by_code(access_code)
            if file_name:
                file_path = os.path.join("uploads", file_name)
                st.download_button(label=f"Download {file_name}", data=open(file_path, "rb").read(), file_name=file_name)
            else:
                st.error("Invalid access code!")

        if st.button("Delete File"):
            if file_handler.delete_file_by_code(access_code):
                st.success("File deleted successfully!")
            else:
                st.error("Invalid access code or file already deleted!")

    else:
        st.error("Wrong pass key!")
