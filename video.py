import os
import glob
import random
import json
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

VIDEOS_FOLDER = "videos"
AUDIO_FOLDER = "audio"

# Create folders automatically if they don't exist
os.makedirs(VIDEOS_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# 1. Load the dynamic AI script data
if not os.path.exists("current_matchup.json"):
    print("❌ ERROR: current_matchup.json not found! Run generate.py first.")
    exit(1)

with open("current_matchup.json", "r") as f:
    matchup_data = json.load(f)

lines = matchup_data["script"]
print(f"🔥 Loaded script for subtitles: {matchup_data['title']}")

# 2. Grab generated audio and background clips
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
bg_videos = glob.glob(os.path.join(VIDEOS_FOLDER, "*.mp4"))

if not bg_videos:
    print("❌ ERROR: Your 'videos' folder on GitHub is empty!")
    print("Please upload 2-3 generic vertical background videos (.mp4) into your 'videos' folder on GitHub.")
    exit(1)

if not audio_files:
    print("❌ ERROR: No generated AI voice audio found in the audio folder!")
    exit(1)

# Pick the newest audio track and a random background video
audio_files.sort(key=os.path.getmtime, reverse=True)
AUDIO_FILE = audio_files[0]
BG_VIDEO = random.choice(bg_videos)

print(f"🎙️ Found Audio Track: {AUDIO_FILE}")
print(f"🎬 Selected Background Video: {BG_VIDEO}")

# 3. Stitch and Edit Video Base
audio_clip = AudioFileClip(AUDIO_FILE)
video_clip = VideoFileClip(BG_VIDEO)

# Loop or cut the background video to match the ElevenLabs audio length exactly
if video_clip.duration < audio_clip.duration:
    from moviepy.video.fx.all import loop
    video_clip = loop(video_clip, duration=audio_clip.duration)
else:
    video_clip = video_clip.subclip(0, audio_clip.duration)

# 4. Generate Dynamic Timing-Matched Subtitles
subtitle_clips = []
total_lines = len(lines)
duration_per_line = audio_clip.duration / total_lines  # Split time perfectly across all lines

print(f"⏱️ Total video duration: {audio_clip.duration:.2f}s | Per line: {duration_per_line:.2f}s")

for i, line in enumerate(lines):
    start_time = i * duration_per_line
    
    try:
        # Professional high-retention subtitle design: Bold yellow caption text
        txt_clip = TextClip(
            line, 
            fontsize=50, 
            color='yellow', 
            font='Arial-Bold', 
            method='caption', 
            size=(video_clip.w - 120, None)  # Ensures text never cuts off on mobile sides
        )
        
        # Position perfectly in the center of the vertical video frame
        txt_clip = txt_clip.set_start(start_time).set_duration(duration_per_line).set_pos('center')
        subtitle_clips.append(txt_clip)
        
    except Exception as text_error:
        print(f"⚠️ Could not generate text clip for line {i}: {text_error}")

# 5. Composite everything together
if subtitle_clips:
    final_video = CompositeVideoClip([video_clip] + subtitle_clips).set_audio(audio_clip)
else:
    print("⚠️ Subtitles failed completely. Exporting plain video synced with audio.")
    final_video = video_clip.set_audio(audio_clip)

# 6. Save EXACTLY where Upload.py looks for it
OUTPUT_PATH = "output_video.mp4"
final_video.write_videofile(
    OUTPUT_PATH, 
    fps=30,  # 30fps looks smoother for fast-paced short content
    codec="libx264", 
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True
)

print(f"✅ Video creation successful! Target file: {OUTPUT_PATH}")

