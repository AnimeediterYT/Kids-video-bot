import os
import json
import glob
import requests

from moviepy.editor import *
from PIL import Image

from system_core import update_memory, get_intelligence

# -----------------------------
# PIL FIX
# -----------------------------
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS


AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output/output_video.mp4"

os.makedirs("output", exist_ok=True)


# -----------------------------
# LOAD DATA SAFE
# -----------------------------
try:
    with open("current_matchup.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Anime Battle")
    script = data.get("script", [])
    hook = data.get("hook", script[0] if script else "WHO WINS?!")

except Exception as e:
    print("⚠️ JSON LOAD FAILED:", e)
    title = "Anime Battle"
    hook = "WHO WINS THIS?!"
    script = [hook, "Battle starts!", "Who wins?!"]


# -----------------------------
# SYSTEM MEMORY (LEARNING INPUT)
# -----------------------------
memory = get_intelligence()
top_hooks = memory.get("hooks", [])


# -----------------------------
# AUDIO SAFE LOAD
# -----------------------------
audio = None
duration = 6

try:
    audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
    if audio_files:
        audio = AudioFileClip(audio_files[0])
        duration = audio.duration
except:
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
# IMAGE FETCH
# -----------------------------
def fetch_image(name, filename):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.images(f"{name} anime wallpaper", max_results=1))
            if results:
                url = results[0]["image"]
                img = requests.get(url, timeout=5)

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
# BASE LAYER
# -----------------------------
clips = [
    ColorClip((1080, 1920), color=(10, 10, 10)).set_duration(duration)
]


# -----------------------------
# TOP CHARACTER
# -----------------------------
clips.append(
    ImageClip(img1).resize(width=1080).set_duration(duration)
    if img1 and os.path.exists(img1)
    else ColorClip((1080, 960), color=(60, 20, 20)).set_duration(duration)
)


# -----------------------------
# BOTTOM CHARACTER
# -----------------------------
clips.append(
    ImageClip(img2)
    .resize(width=1080)
    .set_duration(duration)
    .set_position(("center", 960))
    if img2 and os.path.exists(img2)
    else ColorClip((1080, 960), color=(20, 20, 60)).set_duration(duration)
)


# -----------------------------
# VS LAYER
# -----------------------------
try:
    clips.append(
        TextClip("VS", fontsize=130, color="red")
        .set_duration(duration)
        .set_position("center")
    )
except:
    pass


# -----------------------------
# 🔥 LEARNING-BASED HOOK LAYER
# -----------------------------
try:
    best_hook = hook

    if top_hooks:
        # reuse strongest learned hook if available
        best_hook = top_hooks[-1]

    clips.append(
        TextClip(
            best_hook,
            fontsize=55,
            color="yellow",
            method="caption",
            size=(1000, None)
        )
        .set_start(0)
        .set_duration(min(2, duration * 0.3))
        .set_position(("center", 200))
    )
except:
    pass


# -----------------------------
# SUBTITLE RETENTION ENGINE
# -----------------------------
if not script:
    script = [hook, "Battle starts!", "Who wins?!"]

body = script[1:] if len(script) > 1 else script

# adaptive pacing (slightly slower for retention)
step = duration / max(len(body), 1)

for i, line in enumerate(body):
    try:
        clips.append(
            TextClip(
                line,
                fontsize=45,
                color="white",
                method="caption",
                size=(1000, None)
            )
            .set_start(i * step)
            .set_duration(step)
            .set_position(("center", 1500))
        )
    except:
        pass


# -----------------------------
# FINAL RENDER
# -----------------------------
try:
    final = CompositeVideoClip(clips)

    if audio:
        final = final.set_audio(audio)

    final.write_videofile(
        OUTPUT_PATH,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    print("✅ VIDEO GENERATED SUCCESSFULLY")

    # -------------------------
    # FEEDBACK TO SYSTEM CORE
    # -------------------------
    update_memory("video_render_styles", {
        "title_style": "vs_split",
        "hook_used": best_hook,
        "duration": duration
    })

except Exception as e:
    print("❌ VIDEO FAILED:", e)

    ColorClip((1080, 1920), color=(0, 0, 0)).set_duration(2).write_videofile(
        OUTPUT_PATH,
        fps=30,
        codec="libx264"
    )

    print("⚠️ FALLBACK VIDEO CREATED")
