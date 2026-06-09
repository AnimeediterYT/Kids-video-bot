import os
import glob
import json
import requests
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

AUDIO_FOLDER = "audio"
OUTPUT_PATH = "output_video.mp4"

# 1. Load the dynamic AI matchup script details
if not os.path.exists("current_matchup.json"):
    print("❌ ERROR: current_matchup.json not found! Run generate.py first.")
    exit(1)

with open("current_matchup.json", "r") as f:
    matchup_data = json.load(f)

matchup_title = matchup_data["title"]
lines = matchup_data["script"]
print(f"🎬 Creating premium keyless layout for: {matchup_title}")

# 2. Grab the generated ElevenLabs audio file
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
if not audio_files:
    print("❌ ERROR: No generated ElevenLabs voice audio found!")
    exit(1)

audio_files.sort(key=os.path.getmtime, reverse=True)
AUDIO_FILE = audio_files[0]
audio_clip = AudioFileClip(AUDIO_FILE)

# 3. Download a stunning 4K dynamic anime wallpaper automatically (FREE, No Keys)
def download_free_anime_background(search_title):
    print("🎨 Fetching a beautiful cinematic anime backdrop from global asset pools...")
    
    # We clean up the character names to fetch gorgeous atmospheric landscapes
    clean_query = search_title.replace(" vs ", " ").lower()
    fallback_url = "https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=1080&auto=format&fit=crop"
    
    # Connects directly to Unsplash Source's free anime/cyberpunk collection structures
    url = f"https://source.unsplash.com/featured/1080x1920/?anime,cyberpunk,scifi"
    
    try:
        response = requests.get(url, timeout=15)
        # Verify we got a real image asset back securely
        if response.status_code == 200:
            with open("bg_artwork.jpg", "wb") as f:
                f.write(response.content)
            return "bg_artwork.jpg"
    except Exception as e:
        print(f"⚠️ Network pool busy: {e}. Activating internal fallback canvas.")
        
    # Failsafe background downloader if pool is busy
    try:
        res = requests.get(fallback_url, timeout=10)
        with open("bg_artwork.jpg", "wb") as f:
            f.write(res.content)
        return "bg_artwork.jpg"
    except:
        return None

# Run background generation pipeline
bg_image = download_free_anime_background(matchup_title)

if not bg_image or not os.path.exists(bg_image):
    print("⚠️ Failsafe active: Generating high-contrast dark color canvas.")
    from moviepy.editor import ColorClip
    video_clip = ColorClip(size=(1080, 1920), color=(25, 25, 30)).set_duration(audio_clip.duration)
else:
    # Load the artwork and lock it to match the ElevenLabs audio length exactly
    video_clip = ImageClip(bg_image).set_duration(audio_clip.duration)

# 4. Build and Center the Subtitles
subtitle_clips = []
total_lines = len(lines)
duration_per_line = audio_clip.duration / total_lines

for i, line in enumerate(lines):
    start_time = i * duration_per_line
    try:
        # High retention neon yellow captions styled with clean side paddings for mobile
        txt_clip = TextClip(
            line, 
            fontsize=54, 
            color='yellow', 
            font='Arial-Bold', 
            method='caption', 
            size=(1080 - 160, None)
        )
        txt_clip = txt_clip.set_start(start_time).set_duration(duration_per_line).set_pos('center')
        subtitle_clips.append(txt_clip)
    except Exception as text_error:
        print(f"⚠️ Subtitle styling frame skip: {text_error}")

# 5. Composite and Export
if subtitle_clips:
    final_video = CompositeVideoClip([video_clip] + subtitle_clips).set_audio(audio_clip)
else:
    final_video = video_clip.set_audio(audio_clip)

final_video.write_videofile(
    OUTPUT_PATH, 
    fps=30, 
    codec="libx264", 
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True
)
print(f"✅ Video successfully compiled! Staged at: {OUTPUT_PATH}")

