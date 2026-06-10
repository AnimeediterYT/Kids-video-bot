import os
import time
import requests

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

_last_call = 0
MIN_DELAY = 12


def _rate_limit():
    global _last_call
    now = time.time()

    if now - _last_call < MIN_DELAY:
        print("⏳ AI cooldown active")
        return False

    _last_call = now
    return True


# ----------------------------
# RUNWAY ONLY (REAL AI)
# ----------------------------
def runway_generate(prompt):
    print("🎬 Runway generating...")

    if not RUNWAY_API_KEY:
        print("⚠️ Missing Runway API key")
        return None

    try:
        url = "https://api.runwayml.com/v1/video"

        headers = {
            "Authorization": f"Bearer {RUNWAY_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt,
            "duration": 4,
            "aspect_ratio": "9:16"
        }

        res = requests.post(url, json=payload, headers=headers, timeout=60)

        if res.status_code == 200:
            return res.json().get("video_url")

        print("❌ Runway error:", res.text)
        return None

    except Exception as e:
        print("❌ Runway exception:", e)
        return None


# ----------------------------
# MAIN ROUTER (NO PIKA)
# ----------------------------
def generate_ai_video(prompt):
    print("🧠 AI VIDEO ENGINE START")

    if not _rate_limit():
        return None

    video = runway_generate(prompt)

    if video:
        return video

    print("⚠️ AI FAILED → fallback to MoviePy system")
    return None
