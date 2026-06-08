import os
import glob
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

VIDEOS_FOLDER = "videos"
AUDIO_FOLDER = "audio"

# Create folders automatically if they don't exist
os.makedirs(VIDEOS_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# 1. Grab generated audio and background clips from your repository folder
audio_files = glob.glob(os.path.join(AUDIO_FOLDER, "*.mp3"))
bg_videos = glob.glob(os.path.join(VIDEOS_FOLDER, "*.mp4"))

# Safety check: If you forgot to put background clips, stop neatly
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

# 2. Stitch and Edit Video
audio_clip = AudioFileClip(AUDIO_FILE)
video_clip = VideoFileClip(BG_VIDEO)

# Loop the video if it is shorter than the audio, or cut it if it's longer
if video_clip.duration < audio_clip.duration:
    # If video is too short, loop it to match the audio length
    from moviepy.video.fx.all import loop
    video_clip = loop(video_clip, duration=audio_clip.duration)
else:
    video_clip = video_clip.subclip(0, audio_clip.duration)

# 3. Add Subtitles Overlay
try:
    subtitle_text = "Watch till the end for a valuable life lesson..."
    subtitle = TextClip(subtitle_text, fontsize=28, color='white', font='Arial', 
                        method='caption', size=(video_clip.w - 40, None), bg_color='black')
    subtitle = subtitle.set_pos('center').set_duration(audio_clip.duration)
    final_video = CompositeVideoClip([video_clip, subtitle]).set_audio(audio_clip)
except Exception as e:
    print(f"⚠️ Subtitle styling skipped: {e}. Outputting plain audio sync.")
    final_video = video_clip.set_audio(audio_clip)

# 4. Save EXACTLY where Upload.py looks for it
OUTPUT_PATH = "output_video.mp4"
final_video.write_videofile(
    OUTPUT_PATH, 
    fps=24, 
    codec="libx264", 
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a", # Safe file write handling
    remove_temp=True
)

print(f"✅ Video creation successful! Target file: {OUTPUT_PATH}")
                                         
