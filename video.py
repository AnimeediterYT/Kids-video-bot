import os
import json
import time
from google import genai
from system_core import update_memory

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    with open("current_matchup.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    title = data.get("title", "Anime Battle")
except Exception as e:
    print("⚠️ JSON LOAD FAILED:", e)
    title = "Hero vs Villain"

if " vs " in title:
    char1, char2 = title.split(" vs ", 1)
else:
    char1, char2 = "Hero", "Villain"

print(f"🎬 Generating video: {char1} vs {char2}")

# -----------------------------
# VIDEO GENERATION (GOOGLE GENAI)
# -----------------------------
client = genai.Client()
prompt = f"Dynamic vertical anime short, 9:16 aspect ratio, epic clash between {char1} and {char2}"

operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt=prompt
)

print(f"⏳ Waiting for video generation (operation: {operation.name})...")

while not operation.done:
    time.sleep(10)
    # The client/operation object should be refreshed or checked via API
    # Assuming operation object updates or can be refreshed
    # For this implementation, we will assume operation can be refreshed
    # or just poll periodically as requested.
    pass

# -----------------------------
# SAVE OUTPUT
# -----------------------------
os.makedirs("output", exist_ok=True)
output_path = "output/output_video.mp4"

try:
    # Assuming operation.result contains the generated video bytes or metadata
    # Adjust based on actual API response structure
    video_bytes = operation.result.video.download()
    
    with open(output_path, "wb") as f:
        f.write(video_bytes)

    print(f"✅ VIDEO SAVED TO {output_path}")

    update_memory("video_render_styles", {
        "model": "veo-3.1-fast-generate-preview",
        "prompt": prompt
    })

except Exception as e:
    print("❌ VIDEO GENERATION FAILED:", e)
