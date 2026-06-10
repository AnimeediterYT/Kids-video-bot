import os
import glob
import json
import requests
from moviepy.editor import *
from PIL import Image

# -----------------------------
# FIX: Pillow + MoviePy compatibility
# -----------------------------
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output/output_video.mp4"

os.makedirs("output", exist_ok=True)

# -----------------------------
# LOAD DATA SAFELY
# -----------------------------
if not os.path.exists("current_matchup.json"):
    print("❌ Missing JSON file")
    exit(0)

try:
    data = json.load(open("current_matchup.json", "r"))
    title = data.get("title", "Anime Battle")
    script = data.get("script", [])
except:
    title = "Anime Battle"
    script = ["Battle starts!", "Power explodes!", "Who wins?"]

# -----------------------------
# AUDIO SAFE LOAD
# -----------------------------
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))

if audio_files:
    audio = AudioFileClip(audio_files[0])
    duration = audio.duration
else:
    audio = None
    duration = 6

# -----------------------------
# CHARACTER SPLIT SAFE
# -----------------------------
if " vs " in title:
    c1, c2 = title.split(" vs ", 1)
else:
    c1, c2 = "Hero", "Villain"

print(f"🎬 Rendering: {c1} vs {c2}")

# -----------------------------
# SAFE IMAGE FETCH
# -----------------------------
def fetch_image(name, filename):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.images(f"{name} anime wallpaper", max_results=1))
            if results:
                img = requests.get(results[0]["image"], timeout=5)
                if img.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(img.content)
                    return filename
    except:
        pass
    return None

img1 = fetch_image(c1, "char1.jpg")
img2 = fetch_image(c2, "char2.jpg")

# -----------------------------
# BASE CANVAS
# -----------------------------
clips = [
    ColorClip((1080, 1920), color=(15, 15, 15)).set_duration(duration)
]

# -----------------------------
# TOP SECTION
# -----------------------------
if img1 and os.path.exists(img1):
    clips.append(
        ImageClip(img1).resize(width=1080).set_duration(duration)
    )
else:
    clips.append(ColorClip((1080, 960), color=(60, 20, 20)).set_duration(duration))

# -----------------------------
# BOTTOM SECTION
# -----------------------------
if img2 and os.path.exists(img2):
    clips.append(
        ImageClip(img2).resize(width=1080).set_duration(duration).set_position(("center", 960))
    )
else:
    clips.append(ColorClip((1080, 960), color=(20, 20, 60)).set_duration(duration).set_position(("center", 960)))

# -----------------------------
# VS TEXT SAFE
# -----------------------------
try:
    clips.append(
        TextClip("VS", fontsize=110, color="red")
        .set_duration(duration)
        .set_position("center")
    )
except:
    pass

# -----------------------------
# SUBTITLES SAFE ENGINE
# -----------------------------
if not script:
    script = ["Fight starts!", "Power explodes!", "Who wins?"]

per = duration / len(script)

for i, line in enumerate(script):
    try:
        clips.append(
            TextClip(
                line,
                fontsize=45,
                color="yellow",
                method="caption",
                size=(1000, None)
            )
            .set_start(i * per)
            .set_duration(per)
            .set_position(("center", 1500))
        )
    except:
        pass

# -----------------------------
# RENDER FINAL VIDEO
# -----------------------------
final = CompositeVideoClip(clips)

if audio:
    final = final.set_audio(audio)

try:
    final.write_videofile(
        OUTPUT_PATH,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )
    print("✅ VIDEO GENERATED SUCCESSFULLY")
except Exception as e:
    print("❌ VIDEO FAILED:", e)
