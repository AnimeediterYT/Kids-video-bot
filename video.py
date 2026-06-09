import os
import glob
import json
import requests
from moviepy.editor import ColorClip, ImageClip, AudioFileClip, TextClip, CompositeVideoClip

AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output_video.mp4"

# 1. Load context manifests
if not os.path.exists("current_matchup.json"):
    print("❌ ERROR: current_matchup.json not found!")
    exit(1)

with open("current_matchup.json", "r") as f:
    matchup_data = json.load(f)

matchup_title = matchup_data["title"]
lines = matchup_data["script"]

if " vs " in matchup_title:
    char1, char2 = matchup_title.split(" vs ", 1)
elif " Takes Over!" in matchup_title:
    char1 = matchup_title.replace("Evil ", "").replace(" Takes Over!", "")
    char2 = "Anime Universe"
elif " trapped in " in matchup_title.lower():
    char1 = matchup_title.split(" was in ")[0].replace("What if ", "")
    char2 = "Jujutsu Kaisen"
else:
    char1, char2 = "Goku", "Anime"

print(f"🎬 Building split-screen layout for: {char1} vs {char2}")

# 2. Extract sound layers
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
audio_clip = AudioFileClip(audio_files[0])
duration = audio_clip.duration

# 3. Secure Asset Image Scraper
def fetch_character_artwork(name, filename):
    print(f"🔍 Searching live web assets for: {name}")
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            search_results = list(ddgs.images(f"{name} anime vertical mobile wallpaper", max_results=1))
            if search_results:
                img_url = search_results[0]['image']
                res = requests.get(img_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                if res.status_code == 200:
                    with open(filename, "wb") as f: 
                        f.write(res.content)
                    return filename
    except Exception as e:
        print(f"⚠️ Search engine rate limit or error for {name}: {e}")
    return None

img1 = fetch_character_artwork(char1, "char1.jpg")
img2 = fetch_character_artwork(char2, "char2.jpg")

# 4. Assemble Canvas System
canvas = ColorClip(size=(1080, 1920), color=(14, 14, 18)).set_duration(duration)
clips = [canvas]

# Top Half Layout Setup
if img1 and os.path.exists(img1):
    try:
        c1_clip = ImageClip(img1).set_duration(duration).resize(width=1080).set_pos(('center', 0))
        clips.append(c1_clip)
    except:
        pass
else:
    # Stylized Top Poster Fallback if Web Image is Ratelimited
    block1 = ColorClip(size=(1080, 960), color=(35, 18, 18)).set_duration(duration).set_pos(('center', 0))
    clips.append(block1)
    try:
        txt_b1 = TextClip(char1.upper(), fontsize=75, color='white', font='Arial-Bold').set_duration(duration).set_pos(('center', 400))
        clips.append(txt_b1)
    except:
        pass

# Bottom Half Layout Setup
if img2 and os.path.exists(img2):
    try:
        c2_clip = ImageClip(img2).set_duration(duration).resize(width=1080).set_pos(('center', 960))
        clips.append(c2_clip)
    except:
        pass
else:
    # Stylized Bottom Poster Fallback if Web Image is Ratelimited
    block2 = ColorClip(size=(1080, 960), color=(18, 18, 35)).set_duration(duration).set_pos(('center', 960))
    clips.append(block2)
    try:
        txt_b2 = TextClip(char2.upper(), fontsize=75, color='white', font='Arial-Bold').set_duration(duration).set_pos(('center', 1360))
        clips.append(txt_b2)
    except:
        pass

# 5. Global Typography & Timing Control Overlay
try:
    vs_tag = TextClip("VS", fontsize=110, color='red', font='Arial-Bold', stroke_color='black', stroke_width=4).set_duration(duration).set_pos('center')
    clips.append(vs_tag)
except:
    pass

duration_per_line = duration / len(lines)
for i, line in enumerate(lines):
    start_time = i * duration_per_line
    try:
        txt_clip = TextClip(
            line, 
            fontsize=52, 
            color='yellow', 
            font='Arial-Bold', 
            method='caption', 
            size=(1080 - 120, None)
        ).set_start(start_time).set_duration(duration_per_line).set_pos(('center', 1550))
        clips.append(txt_clip)
    except Exception as e:
        print(f"⚠️ Subtitle render pass note: {e}")

# 6. Composite & Compile
final_video = CompositeVideoClip(clips).set_audio(audio_clip)
final_video.write_videofile(
    OUTPUT_PATH, 
    fps=30, 
    codec="libx264", 
    audio_codec="aac", 
    temp_audiofile="temp-audio.m4a", 
    remove_temp=True
)
print("✅ Split layout engine execution finalized successfully!")

