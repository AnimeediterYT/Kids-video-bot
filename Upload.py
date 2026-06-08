import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# 1. Log in securely using GitHub Secrets only
def get_youtube_service():
    creds = Credentials(
        token=os.environ.get("YOUTUBE_ACCESS_TOKEN"),
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET")
    )
    return build('youtube', 'v3', credentials=creds)

# 2. Upload the video as a Short
def upload_shorts(youtube, video_path, title, description):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['shorts', 'kids', 'anime'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': True  # Safe for kids content
        }
    }

    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)

    print(f"🎬 Uploading video: {title}")
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
            
    print(f"✅ Success! Video ID: {response['id']}")
    return response['id']

# 3. Scans the ENTIRE channel for comments (even old videos!)
def reply_to_comments(youtube):
    try:
        print("🔍 Scanning the whole channel for recent comments...")
        
        threads = youtube.commentThreads().list(
            part="snippet",
            allThreadsRelatedToChannelId=os.environ.get("YOUTUBE_CHANNEL_ID"), 
            maxResults=10,
            order="time" 
        ).execute()

        for thread in threads.get("items", []):
            top_comment = thread["snippet"]["topLevelComment"]
            comment_id = top_comment["id"]
            author = top_comment["snippet"]["authorDisplayName"]
            total_replies = thread["snippet"]["totalReplyCount"]
            
            # Only reply if the bot hasn't already replied!
            if total_replies == 0:
                print(f"💬 Found a new comment from {author}!")

                youtube.comments().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "parentId": comment_id,
                            "textOriginal": f"Thanks for watching, {author}! Always glad to have you here! ✨"
                        }
                    }
                ).execute()
                print(f"↩️ Replied to {author}")
            else:
                print(f"⏭️ Already replied to {author}, skipping.")

    except Exception as e:
        print(f"⚠️ Could not scan channel comments: {e}")

# Main Runner Loop
if __name__ == '__main__':
    youtube_instance = get_youtube_service()
    video_file = "output_video.mp4" # Make sure this matches your video file name
    
    # 1. First, check and reply to any comments on the channel (old or new)
    reply_to_comments(youtube_instance)
    
    # 2. Second, upload the new video if it exists
    if os.path.exists(video_file):
        uploaded_id = upload_shorts(
            youtube=youtube_instance,
            video_path=video_file,
            title="Cool Anime Short!",
            description="Automated video upload."
        )
    else:
        print(f"❌ Error: {video_file} not found.")
        
