from moviepy import *
import os

os.makedirs("videos", exist_ok=True)

audio = AudioFileClip("audio/voice.mp3")

bg = ColorClip(size=(1920,1080), color=(0,0,0), duration=audio.duration)

video = bg.set_audio(audio)

video.write_videofile(
    "videos/final.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
