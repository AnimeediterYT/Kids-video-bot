import os
import time
import requests

# ----------------------------
# API KEYS (already expected in environment)
# ----------------------------
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
PIKA_API_KEY = os.getenv("PIKA_API_KEY")

# ----------------------------
# SIMPLE RATE CONTROL (prevents 429 crashes)
# ----------------------------
_last_call_time = 0
MIN_DELAY = 12  # prevents spam requests


def _allow_request():
    global _last_call_time
    now = time.time()

    if now - _last_call_time < MIN_DELAY:
        print("⏳ AI cooldown active — skipping request")
        return False

    _last_call_time = now
    return True


# ----------------------------
# RUNWAY (AI VIDEO)
# ----------------------------
def runway_generate(prompt):
    print("🎬 Runway request...")

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

        print("❌ Runway failed:", res.text)
        return None

    except Exception as e:
        print("❌ Runway error:", e)
        return None


# ----------------------------
# PIKA (AI VIDEO)
# ----------------------------
def pika_generate(prompt):
    print("🎬 Pika request...")

    if not PIKA_API_KEY:
        print("⚠️ Missing Pika API key")
        return None

    try:
        url = "https://api.pika.art/generate"

        headers = {
            "Authorization": f"Bearer {PIKA_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt,
            "aspect_ratio": "9:16"
        }

        res = requests.post(url, json=payload, headers=headers, timeout=60)

        if res.status_code == 200:
            return res.json().get("video_url")

        print("❌ Pika failed:", res.text)
        return None

    except Exception as e:
        print("❌ Pika error:", e)
        return None


# ----------------------------
# MAIN AI ROUTER
# ----------------------------
def generate_ai_video(prompt):
    print("🧠 AI VIDEO ROUTER START")

    # STEP 1: safety lock
    if not _allow_request():
        return None

    # STEP 2: try Runway
    video = runway_generate(prompt)
    if video:
        return video

    time.sleep(2)

    # STEP 3: safety lock again
    if not _allow_request():
        return None

    # STEP 4: try Pika
    video = pika_generate(prompt)
    if video:
        return video

    print("⚠️ AI failed → fallback mode")
    return None
