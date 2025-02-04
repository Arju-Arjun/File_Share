import streamlit as st
import random
import os
import json

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

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(tmpdirname):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tmpdirname))

            # Generate an access code
            access_code = str(random.randint(1000, 9999))

            # Store the access code and zip file path persistently
            folder_shares[access_code] = zip_path
            save_folder_shares(folder_shares)

            st.success(f"Folder uploaded successfully and converted to a zip! Your access code is: {access_code}")
            st.write("Save this code to download your folder later.")

elif option == "Folder Access":
    st.header("Access Your Folder")
    access_code_input = st.text_input("Enter your 4-digit access code")
    
    if st.button("Access Folder"):
        folder_shares = load_folder_shares()  # Reload latest folder shares
        if access_code_input in folder_shares:
            zip_path = folder_shares[access_code_input]
            with open(zip_path, "rb") as f:
                st.download_button("Download Folder", f, file_name=os.path.basename(zip_path))
        else:
            st.error("Invalid access code. Please try again.")

elif option == "Live Chat":
    st.sidebar.title("Live Chat Options")
    chat_action = st.sidebar.radio("Choose an action", ("Create a New Chat", "Join an Existing Chat"))
    
    if chat_action == "Create a New Chat":
        # Prompt for user name when creating a chat
        user_name = st.text_input("Enter your user name", value="")
        
        if user_name:
            # Create a new chat room
            chat_code = str(random.randint(1000, 9999))
            
            # Initialize chat room with an empty message list
            chat_rooms[chat_code] = {"messages": []}
            save_chat_rooms(chat_rooms)
            
            st.header("Create a New Chat Room")
            st.success(f"Your chat room is created! Share this code with others to join: {chat_code}")
            st.write(f"Your user name: {user_name}")
            
        else:
            st.error("Please enter your user name.")

    elif chat_action == "Join an Existing Chat":
        # Prompt for user name when joining a chat
        user_name = st.text_input("Enter your user name", value="")
        
        if user_name:
            # Join an existing chat room
            chat_code = st.text_input("Enter Chat Room Code")
            
            if chat_code:
                if chat_code in chat_rooms:
                    st.header(f"Chat Room {chat_code}")
                    if "messages" not in st.session_state:
                        st.session_state.messages = []

                    # Display existing messages in the chat room
                    for msg in chat_rooms[chat_code]["messages"]:
                        st.markdown(f"**{msg['user']}**: {msg['message']}")

                    # Input to send message
                    chat_input = st.text_input("Type your message")
                    
                    if st.button("Send Message"):
                        if chat_input:
                            # Add the message to the chat room's messages
                            chat_rooms[chat_code]["messages"].append({"user": user_name, "message": chat_input})
                            save_chat_rooms(chat_rooms)
                            
                            # Show the new message in the chat
                            st.session_state.messages.append({"user": user_name, "message": chat_input})
                            st.text_input("Type your message", value="", key="chat_input")  # Clear input box
                else:
                    st.error("Invalid chat room code. Please try again.")
        else:
            st.error("Please enter your user name before joining.")
# st.markdown("""[![Instagram](https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png)](https://www.instagram.com/_arjun._x_/)""")
import streamlit as st

# Display clickable icons for Instagram, GitHub, and LinkedIn with space between them
st.markdown(
    '''
    <br><br><br><br>
    <br>
    <div style="display: flex; justify-content: center; gap: 20px; padding-top: 20px;">
        <a href="https://www.instagram.com/_arjun._x_/">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30" height="30">
        </a>
        <a href="https://github.com/Arju-Arjun">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" width="30" height="30">
        </a>
        <a href="https://www.linkedin.com/in/arjun-k-525a45334/">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="30" height="30">
        </a>
    </div>
    ''',
    unsafe_allow_html=True
)

