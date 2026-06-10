import os
import time
import requests

# ----------------------------
# ENV KEYS (YOU SET THESE)
# ----------------------------
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
PIKA_API_KEY = os.getenv("PIKA_API_KEY")


# ----------------------------
# RUNWAY AI VIDEO GENERATION
# ----------------------------
def runway_generate(prompt):
    print("🎬 Runway AI generating...")

    if not RUNWAY_API_KEY:
        print("⚠️ Runway API key missing")
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
            data = res.json()
            print("✅ Runway video created")
            return data.get("video_url")

        print("❌ Runway failed:", res.text)
        return None

    except Exception as e:
        print("❌ Runway error:", e)
        return None


# ----------------------------
# PIKA AI VIDEO GENERATION
# ----------------------------
def pika_generate(prompt):
    print("🎬 Pika AI generating...")

    if not PIKA_API_KEY:
        print("⚠️ Pika API key missing")
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
            data = res.json()
            print("✅ Pika video created")
            return data.get("video_url")

        print("❌ Pika failed:", res.text)
        return None

    except Exception as e:
        print("❌ Pika error:", e)
        return None


# ----------------------------
# SMART AI ROUTER (MAIN SYSTEM)
# ----------------------------
def generate_ai_video(prompt):
    print("🧠 AI VIDEO ROUTER STARTED")

    # 1. Try Runway first
    video = runway_generate(prompt)
    if video:
        return video

    # 2. Wait before fallback
    time.sleep(2)

    # 3. Try Pika
    video = pika_generate(prompt)
    if video:
        return video

    # 4. Fallback system
    print("⚠️ AI VIDEO FAILED → fallback mode activated")
    return None
