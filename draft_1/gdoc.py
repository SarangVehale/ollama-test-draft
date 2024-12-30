
m googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth import default

# Initialize the Google Docs API client
def authenticate_google_api():
    creds, project = default()
    if not creds.valid:
        creds.refresh(Request())
    service = build('docs', 'v1', credentials=creds)
    return service

def process_google_doc(doc_id):
    service = authenticate_google_api()
    doc = service.documents().get(documentId=doc_id).execute()
    content = doc.get('body').get('content')
    
    # Extract and process the text from Google Docs
    text = ''
    for element in content:
        if 'paragraph' in element:
            for para in element['paragraph']['elements']:
                text += para['textRun']['content']
    return text

