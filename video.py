from moviepy.editor import *
import os

os.makedirs("videos", exist_ok=True)

audio = AudioFileClip("audio/voice.mp3")

# simple solid background (NO TextClip = NO ERRORS)
bg = ColorClip((1920,1080), color=(0,0,0), duration=audio.duration)

video = bg.set_audio(audio)

video.write_videofile(
    "videos/final.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
