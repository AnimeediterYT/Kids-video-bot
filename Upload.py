import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

MARKER_FILE = "first_run_done.txt"

# 1. Log in securely using updated repository credentials architecture
def get_youtube_service():
    client_secrets_env = os.environ.get("YOUTUBE_CLIENT_SECRETS")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    
    if not client_secrets_env or not refresh_token:
        raise ValueError("❌ ERROR: Essential GitHub Repository secrets configurations are missing!")
        
    secrets_data = json.loads(client_secrets_env)
    
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=secrets_data["web"]["client_id"],
        client_secret=secrets_data["web"]["client_secret"]
    )
    return build('youtube', 'v3', credentials=creds)

# 2. One-Time Global historical channel purge layout
def purge_channel_videos_once(youtube):
    """Checks for marker status file. Purges legacy layout content ONLY during absolute first engine script run."""
    if os.path.exists(MARKER_FILE):
        print("📁 System Status: Safety marker file found. One-time clean loop bypassed.")
        return

    print("⚠️ WARNING: No marker file found. Executing ONE-TIME structural historical channel wipe...")
    try:
        channels_response = youtube.channels().list(mine=True, part="contentDetails").execute()
        uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        playlist_request = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part="snippet",
            maxResults=50
        )
        playlist_response = playlist_request.execute()
        
        items = playlist_response.get("items", [])
        if not items:
            print("✨ Channel is completely blank. No legacy video assets found to purge.")
        else:
            print(f"🚨 Found {len(items)} historical items live on feed. Starting batch platform deletion...")
            for item in items:
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_title = item["snippet"]["title"]
                try:
                    youtube.videos().delete(id=video_id).execute()
                    print(f"🗑️ Deleted legacy asset: {video_title} ({video_id})")
                except Exception as delete_error:
                    print(f"❌ Failed to drop asset {video_id}: {delete_error}")
        
        # Output the local completion milestone state marker
        with open(MARKER_FILE, "w") as f:
            f.write("Initial legacy channel wipe successfully completed.")
        print(f"✅ Protection system active. Marker file '{MARKER_FILE}' initialized.")
                
    except Exception as e:
        print(f"❌ Structural database cleanup operation failed: {e}")

# 3. Enhanced dynamic upload pipeline
def upload_shorts(youtube, video_path, matchup_title):
    # Dynamic Growth Title Integration with US Hype Hashtags
    video_title = f"{matchup_title} - WHO WINS? #anime #shorts"
    
    # Growth Hacker Constraint: Strict 100 character system description limiter
    description_raw = f"Epic battle: {matchup_title}! Drop real scaling facts below. #animebattle #shorts #otaku"
    video_description = description_raw[:100]
    
    body = {
        'snippet': {
            'title': video_title[:100],  # YouTube API absolute hard limit ceiling safe slice
            'description': video_description,
            'tags': ['shorts', 'anime', 'animebattle', 'otaku', 'vsbattle'],
            'categoryId': '1'  # Changed from 22 (People) to 1 (Film & Animation) for high anime target indexing
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False  # Set to False so video has fully active comment sections!
        }
    }

    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)

    print(f"🚀 Launching upload loop for asset: {video_title}")
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"📦 Transfer progress status: {int(status.progress() * 100)}%")
            
    print(f"✅ Upload successful! Managed Video ID: {response['id']}")
    return response['id']

# 4. Scans the channel engine structure for comments to push activity loops
def reply_to_comments(youtube):
    try:
        print("🔍 Checking channel feed for unanswered community comment targets...")
        
        threads = youtube.commentThreads().list(
            part="snippet",
            allThreadsRelatedToChannelId=None,
            mine=True,
            maxResults=10,
            order="time" 
        ).execute()

        for thread in threads.get("items", []):
            top_comment = thread["snippet"]["topLevelComment"]
            comment_id = top_comment["id"]
            author = top_comment["snippet"]["authorDisplayName"]
            total_replies = thread["snippet"]["totalReplyCount"]
            
            if total_replies == 0:
                print(f"💬 Replying to user comment from: {author}!")

                youtube.comments().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "parentId": comment_id,
                            "textOriginal": f"Facts! Who do you think wins the next matchup? Drop your feats below! 🔥"
                        }
                    }
                ).execute()
                print(f"↩️ Reply delivered successfully to {author}")
            else:
                print(f"⏭️ comment already processed for {author}, skipping.")

    except Exception as e:
        print(f"⚠️ Comment polling engine check bypassed: {e}")

# System Master Main execution frame
if __name__ == '__main__':
    youtube_instance = get_youtube_service()
    video_file = "output_video.mp4" 
    
    # 1. Safely run conditional legacy database channel purge sequence first
    purge_channel_videos_once(youtube_instance)
    
    # 2. Extract active running dynamic match details from tracking database
    if os.path.exists("current_matchup.json"):
        with open("current_matchup.json", "r") as f:
            matchup_data = json.load(f)
        match_title = matchup_data.get("title", "Anime Battle")
    else:
        match_title = "Anime Showdown"
    
    # 3. Post out new generation asset directly to global Shorts feed
    if os.path.exists(video_file):
        uploaded_id = upload_shorts(
            youtube=youtube_instance,
            video_path=video_file,
            matchup_title=match_title
        )
    else:
        print(f"❌ Error: Compiled video frame file '{video_file}' not found.")
        
    # 4. Scan and interact with active comment sections to spark algorithm weights
    reply_to_comments(youtube_instance)
    
