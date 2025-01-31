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
        f.write(uploaded_file.getbuffer())

    # Generate unique code
    file_code = str(uuid.uuid4())[:8]  # Generate an 8-character code

    # Save file-code mapping
    with open(CODE_FILE, "r") as f:
        file_codes = json.load(f)
    
    file_codes[file_code] = uploaded_file.name  # Map code to filename

    with open(CODE_FILE, "w") as f:
        json.dump(file_codes, f)

    return file_code  # Return the generated access code

def get_file_by_code(file_code):
    """Returns the filename for a given access code."""
    with open(CODE_FILE, "r") as f:
        file_codes = json.load(f)

    return file_codes.get(file_code, None)

# def delete_file_by_code(file_code):
#     """Deletes a file using the access code."""
#     with open(CODE_FILE, "r") as f:
#         file_codes = json.load(f)

#     file_name = file_codes.get(file_code)

#     if file_name:
#         file_path = os.path.join(UPLOAD_DIR, file_name)
#         if os.path.exists(file_path):
#             os.remove(file_path)
#             del file_codes[file_code]  # Remove entry from mapping

#             with open(CODE_FILE, "w") as f:
#                 json.dump(file_codes, f)
                
#             return True
#     return False
