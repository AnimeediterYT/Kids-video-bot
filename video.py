import os
import glob
import json
import requests
from moviepy.editor import ColorClip, ImageClip, AudioFileClip, TextClip, CompositeVideoClip

AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output_video.mp4"

# 1. Load context manifests
with open("current_matchup.json", "r") as f:
    matchup_data = json.load(f)

matchup_title = matchup_data["title"]
lines = matchup_data["script"]

# Attempt to split character names out safely
if " vs " in matchup_title:
    char1, char2 = matchup_title.split(" vs ", 1)
else:
    char1, char2 = "Anime Hero", "Anime Villain"

print(f"🎬 Building splitscreen layout for faceoff: {char1} vs {char2}")

# 2. Extract sound layers
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
audio_clip = AudioFileClip(audio_files[0])
duration = audio_clip.duration

# 3. Dynamic Image Scraper: Automatically pulls aesthetic wallpaper assets for specific characters
def fetch_character_artwork(name, filename):
    print(f"🎨 Fetching visual portrait assets for: {name}")
    url = f"https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=1080&auto=format&fit=crop"
    try:
        # Connects to open global creative commons images using character tags
        res = requests.get(f"https://source.unsplash.com/featured/1080x960/?{name},anime", timeout=10)
        if res.status_code == 200:
            with open(filename, "wb") as f: f.write(res.content)
            return filename
    except:
        pass
    return None

img1 = fetch_character_artwork(char1, "char1.jpg")
img2 = fetch_character_artwork(char2, "char2.jpg")

# 4. Assemble the Vertical Split Screen Visuals
# Standard layout background canvas
canvas = ColorClip(size=(1080, 1920), color=(10, 10, 14)).set_duration(duration)
clips = [canvas]

# Top Half Layout Layer (Character 1)
if img1 and os.path.exists(img1):
    c1_clip = ImageClip(img1).set_duration(duration).resize(width=1080).set_pos(('center', 0))
    clips.append(c1_clip)
else:
    clips.append(ColorClip(size=(1080, 960), color=(40, 20, 20)).set_duration(duration).set_pos(('center', 0)))

# Bottom Half Layout Layer (Character 2)
if img2 and os.path.exists(img2):
    c2_clip = ImageClip(img2).set_duration(duration).resize(width=1080).set_pos(('center', 960))
    clips.append(c2_clip)
else:
    clips.append(ColorClip(size=(1080, 960), color=(20, 20, 40)).set_duration(duration).set_pos(('center', 960)))

# 5. Overlay Subtitles and Title Banners
try:
    # VS Middle Divider Tag Graphic
    vs_tag = TextClip("VS", fontsize=90, color='red', font='Arial-Bold').set_duration(duration).set_pos('center')
    clips.append(vs_tag)
except:
    pass

duration_per_line = duration / len(lines)
for i, line in enumerate(lines):
    start_time = i * duration_per_line
    try:
        txt_clip = TextClip(
            line, 
            fontsize=56, 
            color='yellow', 
            font='Arial-Bold', 
            method='caption', 
            size=(1080 - 120, None)
        ).set_start(start_time).set_duration(duration_per_line).set_pos(('center', 1400))
        clips.append(txt_clip)
    except Exception as e:
        print(f"Subtitle processing error: {e}")

# 6. Composite & Render
final_video = CompositeVideoClip(clips).set_audio(audio_clip)
final_video.write_videofile(
    OUTPUT_PATH, 
    fps=30, 
    codec="libx264", 
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True
)
print("✅ Split layout compilation step complete!")

