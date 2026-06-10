import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

print("🚀 UPLOAD MODULE STARTED")


# ----------------------------
# ENV CHECKER (CLEAR + SIMPLE)
# ----------------------------
def get_env(name):
    value = os.environ.get(name)

    if not value:
        print(f"⚠️ Missing env: {name}")
        return None

    return value


# ----------------------------
# YOUTUBE LOGIN
# ----------------------------
def get_youtube():
    client_json = get_env("YOUTUBE_CLIENT_SECRETS")
    refresh_token = get_env("YOUTUBE_REFRESH_TOKEN")

    if not client_json or not refresh_token:
        print("❌ Upload BLOCKED: Missing YouTube authentication")
        return None

    try:
        data = json.loads(client_json)

        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=data["web"]["client_id"],
            client_secret=data["web"]["client_secret"],
        )

        return build("youtube", "v3", credentials=creds)

    except Exception as e:
        print("❌ AUTH ERROR:", e)
        return None


# ----------------------------
# UPLOAD VIDEO
# ----------------------------
def upload(video_path, title, youtube):

    if not youtube:
        print("❌ STOPPED: No YouTube connection")
        return False

    if not os.path.exists(video_path):
        print("❌ STOPPED: Video file not found")
        return False

    try:
        body = {
            "snippet": {
                "title": (title + " #shorts")[:100],
                "description": title[:200],
                "tags": ["anime", "shorts"],
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

        print("✅ UPLOAD SUCCESS:", response["id"])
        return True

    except Exception as e:
        print("❌ UPLOAD FAILED:", e)
        return False


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    video_file = "output/output_video.mp4"

    youtube = get_youtube()

    # load title safely
    try:
        if os.path.exists("current_matchup.json"):
            with open("current_matchup.json", "r") as f:
                title = json.load(f).get("title", "Anime Battle")
        else:
            title = "Anime Battle"
    except:
        title = "Anime Battle"

    # FINAL DECISION
    success = upload(video_file, title, youtube)

    if not success:
        print("❌ UPLOAD FAILED (NO FAKE SUCCESS)")
        exit(1)

    print("🎬 UPLOAD MODULE FINISHED")
