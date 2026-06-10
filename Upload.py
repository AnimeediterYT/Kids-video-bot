import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

MARKER_FILE = "first_run_done.txt"


# ----------------------------
# SAFE ENV LOADER
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

    # HARD STOP if missing
    if not client_secrets_env or not refresh_token:
        print("❌ Upload BLOCKED: Missing YouTube authentication")
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
        print("❌ AUTH ERROR (invalid secret format):", e)
        return None


# ----------------------------
# SAFE PURGE (DISABLED)
# ----------------------------
def purge_channel_videos_once(youtube):
    if youtube is None:
        print("⚠️ Purge skipped (no service)")
        return

    if os.path.exists(MARKER_FILE):
        return

    print("⚠️ One-time purge skipped (safe mode)")

    try:
        open(MARKER_FILE, "w").write("done")
    except:
        pass


# ----------------------------
# UPLOAD FUNCTION
# ----------------------------
def upload_shorts(youtube, video_path, title):

    if youtube is None:
        print("❌ Upload FAILED: No YouTube connection")
        return False

    if not os.path.exists(video_path):
        print("❌ Upload FAILED: Video file missing")
        return False

    try:
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

        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()

        print(f"✅ UPLOAD SUCCESS: {response['id']}")
        return True

    except Exception as e:
        print("❌ UPLOAD ERROR:", e)
        return False


# ----------------------------
# MAIN (NO FAKE SUCCESS)
# ----------------------------
if __name__ == "__main__":

    print("🚀 UPLOAD MODULE STARTED")

    youtube = get_youtube_service()
    video_file = "output/output_video.mp4"

    purge_channel_videos_once(youtube)

    # load title safely
    try:
        if os.path.exists("current_matchup.json"):
            with open("current_matchup.json", "r") as f:
                title = json.load(f).get("title", "Anime Battle")
        else:
            title = "Anime Battle"
    except:
        title = "Anime Battle"

    # REAL EXECUTION LOGIC
    if not youtube:
        print("❌ STOPPED: Missing YouTube auth (fix GitHub secrets)")
        exit(1)

    if not os.path.exists(video_file):
        print("❌ STOPPED: Video not found")
        exit(1)

    success = upload_shorts(youtube, video_file, title)

    if not success:
        print("❌ UPLOAD FAILED (pipeline will stop)")
        exit(1)

    print("🎬 UPLOAD MODULE FINISHED SUCCESSFULLY")
