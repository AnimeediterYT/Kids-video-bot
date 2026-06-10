import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

MARKER_FILE = "first_run_done.txt"


# ----------------------------
# SAFE KEY LOADER (CLEAR DEBUG)
# ----------------------------
def get_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"⚠️ Missing env: {name}")
    return value


# ----------------------------
# YOUTUBE SERVICE BUILDER
# ----------------------------
def get_youtube_service():
    client_secrets_env = get_env("YOUTUBE_CLIENT_SECRETS")
    refresh_token = get_env("YOUTUBE_REFRESH_TOKEN")

    if not client_secrets_env or not refresh_token:
        print("❌ Upload BLOCKED: YouTube secrets missing")
        return None

    try:
        secrets_data = json.loads(client_secrets_env)

        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=secrets_data["web"]["client_id"],
            client_secret=secrets_data["web"]["client_secret"],
        )

        return build("youtube", "v3", credentials=creds)

    except Exception as e:
        print("❌ Auth error:", e)
        return None


# ----------------------------
# SAFE PURGE (DISABLED SAFELY)
# ----------------------------
def purge_channel_videos_once(youtube):
    if youtube is None:
        print("⚠️ Purge skipped (no service)")
        return

    if os.path.exists(MARKER_FILE):
        return

    print("⚠️ One-time purge (SAFE MODE)")

    try:
        channels = youtube.channels().list(
            mine=True,
            part="contentDetails"
        ).execute()

        uploads = channels["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        playlist = youtube.playlistItems().list(
            playlistId=uploads,
            part="snippet",
            maxResults=50
        ).execute()

        for item in playlist.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]
            # SAFE MODE ONLY (no delete)

        open(MARKER_FILE, "w").write("done")

    except Exception as e:
        print("⚠️ Purge error:", e)


# ----------------------------
# UPLOAD FUNCTION (ROBUST)
# ----------------------------
def upload_shorts(youtube, video_path, title):

    if youtube is None:
        print("❌ Upload blocked (no YouTube connection)")
        return None

    if not os.path.exists(video_path):
        print("❌ Video missing:", video_path)
        return None

    print("📤 Uploading video...")

    body = {
        "snippet": {
            "title": (title + " - WHO WINS? #shorts")[:100],
            "description": (title + " anime battle #shorts")[:200],
            "tags": ["anime", "shorts", "battle"],
            "categoryId": "1",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    try:
        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()

        print(f"✅ UPLOADED SUCCESSFULLY: {response['id']}")
        return response["id"]

    except Exception as e:
        print("❌ Upload failed:", e)
        return None


# ----------------------------
# MAIN PIPELINE
# ----------------------------
if __name__ == "__main__":

    print("🚀 UPLOAD MODULE STARTED")

    youtube = get_youtube_service()

    video_file = "output/output_video.mp4"

    purge_channel_videos_once(youtube)

    # LOAD TITLE SAFE
    try:
        if os.path.exists("current_matchup.json"):
            with open("current_matchup.json", "r") as f:
                title = json.load(f).get("title", "Anime Battle")
        else:
            title = "Anime Battle"
    except:
        title = "Anime Battle"

    # DECISION LOGIC (CLEAR OUTPUT)
    if youtube and os.path.exists(video_file):
        upload_shorts(youtube, video_file, title)
    elif not youtube:
        print("⚠️ Upload skipped: missing YouTube authentication")
    elif not os.path.exists(video_file):
        print("❌ Upload skipped: video file missing")

    print("🎬 UPLOAD MODULE FINISHED")
