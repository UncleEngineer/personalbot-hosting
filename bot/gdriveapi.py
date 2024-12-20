from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/home/pythonanywhere_username/personalbot-hosting/bot/service_account.json'
PARENT_FOLDER_ID = 'Google Drive folder id'

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_to_gdrive(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_name = file_path.split('/')[-1]

    file_metadata = {
        'name': file_name,
        'parents': [PARENT_FOLDER_ID],
    }

    media = MediaFileUpload(file_path, resumable=True)

    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        file_id = file.get('id')
        file_link = file.get('webViewLink')

        # Save the file link or ID as a variable
        return file_id, file_link
    except Exception as e:
        return None, None

    return file_link
