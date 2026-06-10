import os
import glob
import json
import requests
from moviepy.editor import (
    ColorClip,
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    VideoFileClip
)

from ai_video_engine import generate_ai_video

AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output/output_video.mp4"

os.makedirs("output", exist_ok=True)


# ----------------------------
# LOAD SCRIPT
# ----------------------------
if not os.path.exists("current_matchup.json"):
    print("❌ ERROR: current_matchup.json not found!")
    exit(1)

with open("current_matchup.json", "r") as f:
    data = json.load(f)

title = data["title"]
lines = data["script"]


# ----------------------------
# CHARACTER SPLIT
# ----------------------------
if " vs " in title:
    char1, char2 = title.split(" vs ", 1)
else:
    char1, char2 = "Hero", "Enemy"

print(f"🎬 AI VIDEO ENGINE: {char1} vs {char2}")


# ----------------------------
# AUDIO
# ----------------------------
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))

if not audio_files:
    print("❌ No audio found!")
    exit(1)

audio = AudioFileClip(audio_files[0])
duration = audio.duration


# ----------------------------
# DOWNLOAD AI VIDEO
# ----------------------------
def download_video(url, filename="ai_video.mp4"):
    try:
        print("⬇️ Downloading AI video...")

        r = requests.get(url, stream=True, timeout=60)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

            print("✅ AI video downloaded")
            return filename

    except Exception as e:
        print("❌ Download error:", e)

    return None


# ----------------------------
# IMAGE FALLBACK SYSTEM
# ----------------------------
def fetch_image(name, filename):
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.images(f"{name} anime wallpaper", max_results=1))
            if results:
                url = results[0]["image"]
                img = requests.get(url, timeout=10).content

                with open(filename, "wb") as f:
                    f.write(img)

                return filename
    except:
        return None


img1 = fetch_image(char1, "c1.jpg")
img2 = fetch_image(char2, "c2.jpg")


# ----------------------------
# AI VIDEO GENERATION SLOT
# ----------------------------
ai_url = generate_ai_video(f"{char1} vs {char2} anime cinematic battle")

ai_clip = None

if ai_url:
    ai_file = download_video(ai_url)
    if ai_file and os.path.exists(ai_file):
        try:
            ai_clip = VideoFileClip(ai_file).subclip(0, min(4, duration))
            print("🎬 AI VIDEO CLIP READY")
        except:
            print("⚠️ AI video load failed")


# ----------------------------
# BASE CANVAS
# ----------------------------
canvas = ColorClip(size=(1080, 1920), color=(10, 10, 15)).set_duration(duration)
clips = [canvas]


# ----------------------------
# PRIORITY SYSTEM
# ----------------------------

# TOP LAYER (AI VIDEO FIRST)
if ai_clip:
    ai_clip = ai_clip.resize(height=1920)
    clips.append(ai_clip)

else:
    # fallback image system
    if img1:
        c1 = ImageClip(img1).set_duration(duration).resize(width=1080).set_position(("center", 0))
        clips.append(c1)

    if img2:
        c2 = ImageClip(img2).set_duration(duration).resize(width=1080).set_position(("center", 960))
        clips.append(c2)


# ----------------------------
# VS TEXT
# ----------------------------
try:
    vs = TextClip(
        "VS",
        fontsize=130,
        color="red",
        font="Arial-Bold",
        stroke_color="black",
        stroke_width=5
    ).set_duration(duration).set_position("center")

    clips.append(vs)
except:
    pass


# ----------------------------
# SUBTITLES
# ----------------------------
time_per_line = duration / max(len(lines), 1)

for i, line in enumerate(lines):
    start = i * time_per_line

    try:
        txt = TextClip(
            line,
            fontsize=50,
            color="yellow",
            font="Arial-Bold",
            method="caption",
            size=(900, None)
        ).set_start(start).set_duration(time_per_line).set_position(("center", 1500))

        clips.append(txt)

    except:
        pass


# ----------------------------
# FINAL RENDER
# ----------------------------
final = CompositeVideoClip(clips).set_audio(audio)

final.write_videofile(
    OUTPUT_PATH,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True
)


# ----------------------------
# VERIFY OUTPUT
# ----------------------------
if os.path.exists(OUTPUT_PATH):
    size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"✅ VIDEO CREATED: {size:.2f} MB")
else:
    print("❌ VIDEO FAILED")

print("🎬 AI VIDEO ENGINE COMPLETE")
