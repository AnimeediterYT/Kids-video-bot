import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

print("🚀 UPLOAD MODULE STARTED")


# ----------------------------
# ENV CHECKER
# ----------------------------
def get_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"⚠️ Missing env: {name}")
        return None
    return value


# ----------------------------
# YOUTUBE CLIENT
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
# BUILD SEO METADATA (NEW SAFE LAYER)
# ----------------------------
def build_metadata(data):
    title = data.get("title", "Anime Battle")[:95]

    description = data.get("description", "")
    script = data.get("script", [])

    hashtags = "#shorts #anime #battle #vs"

    # pinned comment PREPARATION (not auto-posting yet)
    pinned_comment = f"Who wins this fight? 👇\n{title}"

    return {
        "title": title + " #shorts",
        "description": f"{description}\n\n{hashtags}",
        "tags": ["anime", "shorts", "battle", "whatif"],
        "pinned_comment": pinned_comment
    }


# ----------------------------
# UPLOAD VIDEO
# ----------------------------
def upload(video_path, metadata, youtube):

    if not youtube:
        print("❌ STOPPED: No YouTube connection")
        return False

    if not os.path.exists(video_path):
        print("❌ STOPPED: Video file not found")
        return False

    try:
        body = {
            "snippet": {
                "title": metadata["title"],
                "description": metadata["description"],
                "tags": metadata["tags"],
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

        video_id = response.get("id")
        print("✅ UPLOAD SUCCESS:", video_id)

        # NOTE: pinned comment NOT executed yet (safe roadmap stage)
        print("📌 PINNED COMMENT READY:", metadata["pinned_comment"])

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

    try:
        if os.path.exists("current_matchup.json"):
            with open("current_matchup.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
    except:
        data = {}

    metadata = build_metadata(data)

    success = upload(video_file, metadata, youtube)

    if not success:
        print("❌ UPLOAD FAILED (NO FAKE SUCCESS)")
        exit(1)

    print("🎬 UPLOAD MODULE FINISHED")
