import os
import pickle
import glob
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_PATH = "token.pickle"
STORIES_FOLDER = "stories"

# 1. Connect to YouTube using your token
if not os.path.exists(TOKEN_PATH):
    print("❌ Error: token.pickle missing in GitHub repository!")
    exit(1)

with open(TOKEN_PATH, 'rb') as token_file:
    creds = pickle.load(token_file)
youtube = build('youtube', 'v3', credentials=creds)

# 2. Find the newly generated video
video_files = glob.glob(os.path.join(STORIES_FOLDER, "*.mp4"))

if not video_files:
    print("💤 No new generated videos found in the stories folder.")
else:
    VIDEO_FILE = video_files[0]
    file_name = os.path.basename(VIDEO_FILE)
    
    # Auto-generate viral title from file name
    VIDEO_TITLE = os.path.splitext(file_name)[0].replace('_', ' ').title()
    DESCRIPTION = f"{VIDEO_TITLE}\n\nDaily moral lessons and educational shorts to elevate your mind. Subscribe for more! 💡✨\n\n#shorts #education #moralstories #wisdom"
    TAGS = ["shorts", "education", "moralstories", "wisdom", "lifelessons"]

    print(f"🎬 Uploading Generated Video: {VIDEO_TITLE}")

    body = {
        'snippet': {
            'title': VIDEO_TITLE,
            'description': DESCRIPTION,
            'tags': TAGS,
            'categoryId': '27' # Education Category
        },
        'status': {
            'privacyStatus': 'public' # Straight to the public feed
        }
    }

    media = MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True, mimetype='video/*')

    try:
        request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
        
        VIDEO_ID = response['id']
        print(f"🎉 SUCCESS! Video is live. Video ID: {VIDEO_ID}")

        # 3. Automatically pin a comment for engagement
        print("📌 Leaving and pinning default channel comment...")
        comment_body = {
            "snippet": {
                "videoId": VIDEO_ID,
                "topLevelComment": {
                    "snippet": {
                        "textDisplay": "Welcome! What is the most important moral lesson you learned today? Comment below! 👇✨"
                    }
                }
            }
        }
        youtube.comments().insert(part="snippet", body=comment_body).execute()
        print("✅ Comment pinned successfully!")

        # 4. Clean up the stories folder for the next day's run
        os.remove(VIDEO_FILE)
        print("🗑️ Cleaned up workspace folder.")

    except Exception as e:
        print(f"❌ Upload failed: {e}")
      

