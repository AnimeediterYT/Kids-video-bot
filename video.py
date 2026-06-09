import os
import glob
import json
import time
import requests
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

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
print(f"🎬 Initiating AI Video generation sequence for: {matchup_title}")

# 2. Grab the generated ElevenLabs audio file
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
if not audio_files:
    print("❌ ERROR: No generated ElevenLabs voice audio found!")
    exit(1)

audio_files.sort(key=os.path.getmtime, reverse=True)
AUDIO_FILE = audio_files[0]
audio_clip = AudioFileClip(AUDIO_FILE)

# 3. Call the Advanced AI Video Generation API (Luma / Runway Layout)
def generate_ai_video_background(prompt_text):
    print("🚀 Sending prompt to AI Animation Engine... This creates custom cinematic footage.")
    
    # Using Luma Dream Machine Developer API framework as our baseline high-fidelity animator
    api_key = os.environ.get("LUMA_AI_API_KEY")
    if not api_key:
        print("❌ ERROR: LUMA_AI_API_KEY is missing from your GitHub secrets!")
        return None
        
    url = "https://api.lumalabs.ai/v1/video"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": f"Cinematic epic anime battle style action scene showing {prompt_text}. Intense fighting visuals, high dynamic range, perfect vertical 9:16 aspect ratio layout for mobile shorts feed.",
        "aspect_ratio": "9:16",
        "duration": 5, # Generate standard 5s cinematic blocks
        "loop": True
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json().get("id")
    except Exception as e:
        print(f"❌ Video API request failed: {e}")
        return None

def download_rendered_ai_video(generation_id):
    api_key = os.environ.get("LUMA_AI_API_KEY")
    url = f"https://api.lumalabs.ai/v1/video/{generation_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    print("⏳ Waiting for AI cloud cluster to render the custom video clip...")
    # Poll the server every 20 seconds until generation finishes
    while True:
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            status = data.get("status")
            
            if status == "completed":
                video_url = data.get("video_url")
                print("✨ Animation finished rendering! Downloading file content...")
                video_content = requests.get(video_url).content
                with open("ai_generated_bg.mp4", "wb") as f:
                    f.write(video_content)
                return "ai_generated_bg.mp4"
                
            elif status == "failed":
                print("❌ AI Animation task failed on the server.")
                return None
                
            time.sleep(20)
        except Exception as e:
            print(f"⚠️ Error checking video status: {e}")
            return None

# 4. Run the rendering pipeline
generation_id = generate_ai_video_background(matchup_title)
bg_video_file = None

if generation_id:
    bg_video_file = download_rendered_ai_video(generation_id)

# Failsafe: If the Video API fails or lacks credits, it builds a placeholder asset safely
if not bg_video_file:
    print("⚠️ Failsafe active: Generating high-contrast background since Video API returned empty.")
    from moviepy.editor import ColorClip
    video_clip = ColorClip(size=(1080, 1920), color=(20, 20, 20)).set_duration(audio_clip.duration)
else:
    video_clip = VideoFileClip(bg_video_file)
    if video_clip.duration < audio_clip.duration:
        from moviepy.video.fx.all import loop
        video_clip = loop(video_clip, duration=audio_clip.duration)
    else:
        video_clip = video_clip.subclip(0, audio_clip.duration)

# 5. Build and Center the Subtitles
subtitle_clips = []
total_lines = len(lines)
duration_per_line = audio_clip.duration / total_lines

for i, line in enumerate(lines):
    start_time = i * duration_per_line
    try:
        txt_clip = TextClip(
            line, 
            fontsize=52, 
            color='yellow', 
            font='Arial-Bold', 
            method='caption', 
            size=(video_clip.w - 120, None)
        )
        txt_clip = txt_clip.set_start(start_time).set_duration(duration_per_line).set_pos('center')
        subtitle_clips.append(txt_clip)
    except Exception as text_error:
        print(f"⚠️ Subtitle rendering skip on line {i}: {text_error}")

# 6. Export everything cleanly
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
print(f"✅ Video engine successfully finished! Output staged at: {OUTPUT_PATH}")

