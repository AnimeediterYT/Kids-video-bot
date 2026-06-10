import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

MARKER_FILE = "first_run_done.txt"


# ----------------------------
# ENV LOADER (SAFE DEBUG)
# ----------------------------
def get_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"⚠️ Missing env: {name}")
    return value


# ----------------------------
# YOUTUBE SERVICE BUILDER (SAFE + ZARCHIVER SUPPORT)
# ----------------------------
def get_youtube_service():
    client_secrets_env = get_env("YOUTUBE_CLIENT_SECRETS")
    refresh_token = get_env("YOUTUBE_REFRESH_TOKEN")

    if not client_secrets_env or not refresh_token:
        print("❌ Upload BLOCKED: YouTube secrets missing")
        return None

    try:
        secrets_data = json.loads(client_secrets_env)

        # support ZArchiver raw JSON format
        if "web" in secrets_data:
            oauth = secrets_data["web"]
        elif "installed" in secrets_data:
            oauth = secrets_data["installed"]
        else:
            print("❌ Invalid OAuth format (missing web/installed)")
            return None

        # strict checks
        if "client_id" not in oauth:
            print("❌ Missing client_id in OAuth file")
            return None

        if "client_secret" not in oauth:
            print("❌ Missing client_secret in OAuth file")
            return None

        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=oauth["client_id"],
            client_secret=oauth["client_secret"],
        )

        return build("youtube", "v3", credentials=creds)

    except Exception as e:
        print("❌ Auth error:", e)
        return None


# ----------------------------
# SAFE PURGE
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
            _ = item["snippet"]["resourceId"]["videoId"]
            # SAFE MODE ONLY

        open(MARKER_FILE, "w").write("done")

    except Exception as e:
        print("⚠️ Purge error:", e)


# ----------------------------
# UPLOAD FUNCTION
# ----------------------------
def upload_shorts(youtube, video_path, matchup_title):

    if youtube is None:
        print("❌ Upload skipped (no YouTube connection)")
        return None

    if not os.path.exists(video_path):
        print("❌ Video file not found:", video_path)
        return None

    video_title = f"{matchup_title} - WHO WINS? #shorts"
    video_description = f"{matchup_title} anime battle #shorts"

    body = {
        "snippet": {
            "title": video_title[:100],
            "description": video_description[:100],
            "tags": ["anime", "shorts", "vs"],
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

        print(f"✅ Uploaded: {response['id']}")
        return response["id"]

    except Exception as e:
        print("❌ Upload failed:", e)
        return None


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    youtube = get_youtube_service()

    video_file = "output/output_video.mp4"

    purge_channel_videos_once(youtube)

    if os.path.exists("current_matchup.json"):
        with open("current_matchup.json", "r") as f:
            title = json.load(f).get("title", "Anime Battle")
    else:
        title = "Anime Battle"

    if youtube and os.path.exists(video_file):
        upload_shorts(youtube, video_file, title)
    else:
        if not youtube:
            print("⚠️ Upload skipped: missing YouTube authentication")
        if not os.path.exists(video_file):
            print("❌ Upload skipped: video file missing")

    print("🎬 Upload step finished (safe mode active)")
