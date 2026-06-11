import os
import json
import time

 from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

from system_core import (
    update_memory,
    get_intelligence,
    get_signal,
    record_video_analytics,
    calculate_score,
)
print("🚀 UPLOAD MODULE STARTED (AI GROWTH ENGINE)")


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
# LOAD DATA
# =============================
def load_data():
    try:
        with open("current_matchup.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("⚠️ JSON LOAD FAILED:", e)
        return {}


# =============================
# GROWTH METADATA ENGINE
# =============================
def build_metadata(data):
    signal = get_signal()
    memory = get_intelligence()

    title = data.get("title", "Anime Battle")
    description = data.get("description", "")
    hashtags = data.get("hashtags", "#anime #shorts #battle #vs #whatif")

    if "🔥" not in title:
        title = "🔥 " + title

    if "#shorts" not in title.lower():
        title += " #shorts"

    if signal == "STRONG_WINNERS":
        title = title.upper() if len(title) < 80 else title

    full_description = f"""
{description}

💥 Anime Battle Simulation
⚡ Power scaling test
🔥 What if scenario

COMMENT WHO WINS 👇

#anime #shorts #battle #vs #whatif
""".strip()

    pinned_comment = f"👇 Who wins?\n🔥 {title}"

    return {
        "title": title[:100],
        "description": full_description[:4500],
        "tags": ["anime", "shorts", "battle", "vs", "whatif"],
        "pinned_comment": pinned_comment,
        "signal": signal
    }


# =============================
# UPLOAD ENGINE
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
set_value(
    "latest_video_id",
    video_id
)

set_value(
    "latest_video_url",
    f"https://youtube.com/watch?v={video_id}"
)
video_url = f"https://www.youtube.com/watch?v={video_id}"

update_memory("video_urls", {
    "video_id": video_id,
    "url": video_url,
    "timestamp": time.time()
})

print("🔗 VIDEO URL:", video_url)

        update_memory("uploaded_videos", {
    "video_id": video_id,
    "video_url": f"https://youtube.com/watch?v={video_id}",
    "title": metadata["title"],
    "signal": metadata.get("signal", "UNKNOWN"),
    "score": 0,
    "views": 0,
    "likes": 0,
    "comments": 0,
    "timestamp": time.time()
})

        update_memory("best_titles", metadata["title"])

        print("📌 PINNED COMMENT:", metadata["pinned_comment"])

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

    print("🎬 UPLOAD MODULE FINISHED (AI SYSTEM ACTIVE)")
