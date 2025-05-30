import os, base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_resume_emails():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', q="has:attachment filename:pdf OR filename:docx").execute()
    messages = results.get('messages', [])
    if not os.path.exists("attachments"):
        os.makedirs("attachments")
    attachments = []
    for msg in messages:
        msg_id = msg['id']
        message = service.users().messages().get(userId='me', id=msg_id).execute()
        for part in message['payload'].get('parts', []):
            if 'filename' in part and part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                elif 'attachmentId' in part['body']:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=att_id).execute()
                    data = att['data']
                else:
                    continue
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                filename = part['filename']
                path = os.path.join("attachments", filename)
                with open(path, "wb") as f:
                    f.write(file_data)
                attachments.append(path)
    return attachments
