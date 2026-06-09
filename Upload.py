import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

MARKER_FILE = "first_run_done.txt"

def get_youtube_service():
    client_secrets_env = os.environ.get("YOUTUBE_CLIENT_SECRETS")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    
    if not client_secrets_env or not refresh_token:
        raise ValueError("❌ ERROR: Essential GitHub Secrets configurations are missing!")
        
    secrets_data = json.loads(client_secrets_env)
    
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=secrets_data["web"]["client_id"],
        client_secret=secrets_data["web"]["client_secret"]
    )
    return build('youtube', 'v3', credentials=creds)

def purge_channel_videos_once(youtube):
    if os.path.exists(MARKER_FILE):
        return

    print("⚠️ Executing ONE-TIME historical channel content purge...")
    try:
        channels_response = youtube.channels().list(mine=True, part="contentDetails").execute()
        uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        playlist_response = youtube.playlistItems().list(playlistId=uploads_playlist_id, part="snippet", maxResults=50).execute()
        items = playlist_response.get("items", [])
        
        for item in items:
            video_id = item["snippet"]["resourceId"]["videoId"]
            youtube.videos().delete(id=video_id).execute()
            
        with open(MARKER_FILE, "w") as f:
            f.write("Initial legacy channel wipe successfully completed.")
    except Exception as e:
        print(f"Purge note: {e}")

def upload_shorts(youtube, video_path, matchup_title):
    video_title = f"{matchup_title} - WHO WINS? #anime #shorts"
    description_raw = f"Epic match: {matchup_title}! Drop scaling facts below. #animebattle #shorts"
    video_description = description_raw[:100] # Hard 100 character system restriction limit
    
    body = {
        'snippet': {
            'title': video_title[:100],
            'description': video_description,
            'tags': ['shorts', 'anime', 'vsbattle'],
            'categoryId': '1'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False # Keeps comment sections open and unrestricted
        }
    }

    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
    print(f"✅ Success! Posted Video ID: {response['id']}")
    return response['id']

if __name__ == '__main__':
    youtube_instance = get_youtube_service()
    video_file = "output_video.mp4" 
    
    purge_channel_videos_once(youtube_instance)
    
    if os.path.exists("current_matchup.json"):
        with open("current_matchup.json", "r") as f:
            matchup_data = json.load(f)
        match_title = matchup_data.get("title", "Anime Battle")
    else:
        match_title = "Anime Showdown"
    
    if os.path.exists(video_file):
        upload_shorts(youtube_instance, video_file, match_title)
        
