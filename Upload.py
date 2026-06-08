import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_youtube_service():
    # Force the script to read directly from your GitHub Secrets
    creds = Credentials(
        token=os.environ.get("YOUTUBE_ACCESS_TOKEN"),
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET")
    )
    return build('youtube', 'v3', credentials=creds)
    
