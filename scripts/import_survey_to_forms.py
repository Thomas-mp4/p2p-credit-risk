"""
Automates creation of a Google Form from a plain-text file of questions.

Each line in QUESTIONS_FILE should be formatted as:
    What is your opinion on X? (Description)

This script turns each into a 1–5 scale question.

Before running, update the CONFIGURATION section below.
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

# === CONFIGURATION (edit these before running) ===
SERVICE_ACCOUNT_FILE = "service-account.json"      # Path to your service account JSON
SCOPES = [
    "https://www.googleapis.com/auth/forms.body",  # to create/modify form content
    "https://www.googleapis.com/auth/drive"        # to share the form
]
QUESTIONS_FILE = "questions.txt"                   # Local file with survey questions
FORM_TITLE = "Imported Survey"                     # Title for the new Google Form
COLLABORATOR_EMAIL = ""                            # Email to share as writer
SEND_NOTIFICATION = True                           # Whether to notify collaborator by email
# ==================================================

def main():
    # Authenticate using the service account
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    # Build the Forms and Drive service clients
    forms_service = build("forms", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # Step 1: Read and clean questions from the local file
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Step 2: Create a new Google Form
    form = forms_service.forms().create(body={
        "info": {"title": FORM_TITLE}
    }).execute()
    form_id = form["formId"]

    # Step 3: (Optional) Share the form with a collaborator
    drive_service.permissions().create(
        fileId=form_id,
        body={
            "type": "user",
            "role": "writer",
            "emailAddress": COLLABORATOR_EMAIL
        },
        sendNotificationEmail=SEND_NOTIFICATION
    ).execute()

    # Step 4: Build scale-type question requests in reverse order
    requests = []
    for line in reversed(lines):
        m = re.match(r"^(.+?)\s*\((.+)\)", line)
        if not m:
            # skip lines that don’t match the expected pattern
            continue
        title, desc = m.groups()
        requests.append({
            "createItem": {
                "item": {
                    "title": f"{title} ({desc})",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "scaleQuestion": {
                                "low": 1,
                                "high": 5,
                                # Uncomment to add labels:
                                # "lowLabel": "Strongly Disagree",
                                # "highLabel": "Strongly Agree"
                            }
                        }
                    }
                },
                "location": {"index": 0}
            }
        })

    # Step 5: Send all questions in a batch update
    if requests:
        forms_service.forms().batchUpdate(
            formId=form_id,
            body={"requests": requests}
        ).execute()

    # Output the Form URL
    print(f"Form URL: https://docs.google.com/forms/d/{form_id}/edit")

if __name__ == "__main__":
    main()