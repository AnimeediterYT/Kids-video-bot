import os
import glob
import json
import requests
from moviepy.editor import ColorClip, ImageClip, AudioFileClip, TextClip, CompositeVideoClip

AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output_video.mp4"

with open("current_matchup.json", "r") as f:
    matchup_data = json.load(f)

matchup_title = matchup_data["title"]
lines = matchup_data["script"]

if " vs " in matchup_title:
    char1, char2 = matchup_title.split(" vs ", 1)
elif " Takes Over!" in matchup_title:
    char1 = matchup_title.replace("Evil ", "").replace(" Takes Over!", "")
    char2 = "Anime"
elif " trapped in " in matchup_title.lower():
    char1 = matchup_title.split(" was in ")[0].replace("What if ", "")
    char2 = "Gojo"
else:
    char1, char2 = "Goku", "Anime"

print(f"🎬 Building high-accuracy split-screen for: {char1} vs {char2}")

audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
audio_clip = AudioFileClip(audio_files[0])
duration = audio_clip.duration

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
                    with open(filename, "wb") as f: f.write(res.content)
                    return filename
    except Exception as e:
        print(f"⚠️ Search fallback for {name}: {e}")
    return None

img1 = fetch_character_artwork(char1, "char1.jpg")
img2 = fetch_character_artwork(char2, "char2.jpg")

canvas = ColorClip(size=(1080, 1920), color=(10, 10, 14)).set_duration(duration)
clips = [canvas]

# Top Half Placement
if img1 and os.path.exists(img1):
    try:
        c1_clip = ImageClip(img1).set_duration(duration).resize(width=1080).set_pos(('center', 0))
        clips.append(c1_clip)
    except:
        clips.append(ColorClip(size=(1080, 960), color=(30, 15, 15)).set_duration(duration).set_pos(('center', 0)))
else:
    clips.append(ColorClip(size=(1080, 960), color=(30, 15, 15)).set_duration(duration).set_pos(('center', 0)))

# Bottom Half Placement
if img2 and os.path.exists(img2):
    try:
        c2_clip = ImageClip(img2).set_duration(duration).resize(width=1080).set_pos(('center', 960))
        clips.append(c2_clip)
    except:
        clips.append(ColorClip(size=(1080, 960), color=(15, 15, 30)).set_duration(duration).set_pos(('center', 960)))
else:
    clips.append(ColorClip(size=(1080, 960), color=(15, 15, 30)).set_duration(duration).set_pos(('center', 960)))

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
        ).set_start(start_time).set_duration(duration_per_line).set_pos(('center', 1500))
        clips.append(txt_clip)
    except Exception as e:
        print(f"Subtitle processing error: {e}")

final_video = CompositeVideoClip(clips).set_audio(audio_clip)
final_video.write_videofile(OUTPUT_PATH, fps=30, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
    
