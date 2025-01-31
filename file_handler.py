import os
import json
import uuid

UPLOAD_DIR = "uploads"
CODE_FILE = "file_codes.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize JSON file if it doesn't exist
if not os.path.exists(CODE_FILE):
    with open(CODE_FILE, "w") as f:
        json.dump({}, f)

def save_file(uploaded_file):
    """Saves the uploaded file and generates a unique access code."""
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.get
