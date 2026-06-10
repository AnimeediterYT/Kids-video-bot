import os
import glob
import json
import requests
from moviepy.editor import ColorClip, ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from PIL import Image

# -----------------------------
# FIX: Pillow compatibility for MoviePy
# -----------------------------
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output/output_video.mp4"

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# -----------------------------
# Load script data
# -----------------------------
if not os.path.exists("current_matchup.json"):
    print("❌ ERROR: current_matchup.json not found!")
    exit(1)

with open("current_matchup.json", "r") as f:
    matchup_data = json.load(f)

matchup_title = matchup_data["title"]
lines = matchup_data["script"]

# -----------------------------
# Character parsing
# -----------------------------
if " vs " in matchup_title:
    char1, char2 = matchup_title.split(" vs ", 1)
else:
    char1, char2 = "Hero", "Villain"

print(f"🎬 Building video for: {char1} vs {char2}")

# -----------------------------
# Audio loading
# -----------------------------
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))

if not audio_files:
    print("❌ No audio found!")
    exit(1)

audio_clip = AudioFileClip(audio_files[0])
duration = audio_clip.duration

# -----------------------------
# Image fetch (safe fallback)
# -----------------------------
def fetch_character_artwork(name, filename):
    print(f"🔍 Searching image: {name}")
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.images(f"{name} anime wallpaper", max_results=1))
            if results:
                url = results[0]["image"]
                img = requests.get(url, timeout=10)
                if img.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(img.content)
                    return filename
    except:
        pass
    return None

img1 = fetch_character_artwork(char1, "char1.jpg")
img2 = fetch_character_artwork(char2, "char2.jpg")

# -----------------------------
# Canvas setup
# -----------------------------
canvas = ColorClip(size=(1080, 1920), color=(10, 10, 10)).set_duration(duration)
clips = [canvas]

# -----------------------------
# Top character
# -----------------------------
if img1 and os.path.exists(img1):
    clips.append(
        ImageClip(img1).set_duration(duration).resize(width=1080).set_position(("center", 0))
    )
else:
    clips.append(ColorClip((1080, 960), color=(50, 20, 20)).set_duration(duration).set_position(("center", 0)))

# -----------------------------
# Bottom character
# -----------------------------
if img2 and os.path.exists(img2):
    clips.append(
        ImageClip(img2).set_duration(duration).resize(width=1080).set_position(("center", 960))
    )
else:
    clips.append(ColorClip((1080, 960), color=(20, 20, 50)).set_duration(duration).set_position(("center", 960)))

# -----------------------------
# VS text
# -----------------------------
try:
    clips.append(
        TextClip("VS", fontsize=120, color="red")
        .set_duration(duration)
        .set_position("center")
    )
except:
    pass

# -----------------------------
# Subtitles
# -----------------------------
per_line = duration / max(len(lines), 1)

for i, line in enumerate(lines):
    try:
        clips.append(
            TextClip(
                line,
                fontsize=50,
                color="yellow",
                method="caption",
                size=(1000, None)
            )
            .set_start(i * per_line)
            .set_duration(per_line)
            .set_position(("center", 1500))
        )
    except:
        pass

# -----------------------------
# Render video
# -----------------------------
final = CompositeVideoClip(clips).set_audio(audio_clip)

final.write_videofile(
    OUTPUT_PATH,
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ VIDEO GENERATED SUCCESSFULLY")
