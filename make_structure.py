import os

folders = [
    "app/services",
    "attachments"
]

files = [
    "config.py",
    "app.py",
    "requirements.txt",
    "README.md",
    "credentials.json",  # Will create an empty file. You must replace it with real credentials!
    "app/services/db_service.py",
    "app/services/email_service.py",
    "app/services/resume_parser.py"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    if not os.path.exists(file):
        with open(file, "w") as f:
            pass  # Creates an empty file

print("Folder structure created!")
