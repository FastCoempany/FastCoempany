import re
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Function to retrieve content from Google Docs
def fetch_content_from_google_docs():
    # Load the credentials
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # Call the Docs API
    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId='1IA7oXYl0EvVrEcF0a-8-rr-W9wdV3SCMH9nBb8rLM6c').execute()
    content = document['body']['content']
    
    # Extract the text from the content
    text = ""
    for item in content:
        if 'paragraph' in item:
            elements = item['paragraph']['elements']
            for element in elements:
                if 'textRun' in element:
                    text += element['textRun']['content']
    
    return text

# Function to convert URLs into markdown format
def convert_to_markdown(text):
    # Regular expression to detect URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    # Replace all plain URLs with Markdown links
    text = url_pattern.sub(r'[\1](\1)', text)
    return text

# Fetch content
doc_content = fetch_content_from_google_docs()

# Convert to markdown
markdown_content = convert_to_markdown(doc_content)
print(markdown_content)
