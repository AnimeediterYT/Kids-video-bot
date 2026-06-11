import os
import json
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

print("🚀 UPLOAD MODULE STARTED (PHASE COMPLETE)")


# =============================
# ENV LOADER
# =============================
def get_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"⚠️ Missing env: {name}")
    return value


# =============================
# YOUTUBE CLIENT
# =============================
def get_youtube():
    client_json = get_env("YOUTUBE_CLIENT_SECRETS")
    refresh_token = get_env("YOUTUBE_REFRESH_TOKEN")

    if not client_json or not refresh_token:
        print("❌ Upload BLOCKED: Missing YouTube credentials")
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


# =============================
# LOAD DATA SAFE
# =============================
def load_data():
    try:
        with open("current_matchup.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("⚠️ JSON LOAD FAILED:", e)
        return {}


# =============================
# BUILD METADATA (PHASE COMPLETE)
# =============================
def build_metadata(data):
    title = data.get("title", "Anime Battle")[:95]

    description = data.get("description", "Anime battle shorts")
    hashtags = data.get("hashtags", "#anime #shorts #battle #vs #whatif")

    script = data.get("script", [])

    # safety enrichment
    if "#shorts" not in title.lower():
        title = title + " #shorts"

    full_description = f"""
{description}

{hashtags}

🔥 What if anime battle scenario
⚡ Power scaling fight simulation
💥 Who wins? Comment below!

#anime #shorts
""".strip()

    pinned_comment = f"👇 Who wins this fight?\n{title}"

    return {
        "title": title,
        "description": full_description[:5000],
        "tags": ["anime", "shorts", "battle", "vs", "whatif"],
        "pinned_comment": pinned_comment
    }


# =============================
# UPLOAD FUNCTION
# =============================
def upload(video_path, metadata, youtube):

    if not youtube:
        print("❌ STOPPED: No YouTube connection")
        return False

    if not os.path.exists(video_path):
        print("❌ STOPPED: Video file missing")
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
        retry = 0

        while response is None and retry < 10:
            try:
                status, response = request.next_chunk()
            except Exception as e:
                print("⚠️ Upload chunk error:", e)
                retry += 1
                time.sleep(2)

        if not response:
            print("❌ UPLOAD FAILED AFTER RETRIES")
            return False

        video_id = response.get("id")
        print("✅ UPLOAD SUCCESS:", video_id)

        # future phase hook (NOT ACTIVE YET)
        print("📌 PINNED COMMENT READY:", metadata["pinned_comment"])

        return True

    except Exception as e:
        print("❌ UPLOAD FAILED:", e)
        return False


# =============================
# MAIN
# =============================
if __name__ == "__main__":

    video_file = "output/output_video.mp4"

    youtube = get_youtube()
    data = load_data()

    metadata = build_metadata(data)

    success = upload(video_file, metadata, youtube)

    if not success:
        print("❌ UPLOAD FAILED (NO FAKE SUCCESS)")
        exit(1)

    print("🎬 UPLOAD MODULE FINISHED (PHASE COMPLETE)")
