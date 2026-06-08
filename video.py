from moviepy import *
from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("videos", exist_ok=True)

audio = AudioFileClip("audio/voice.mp3")
text = open("stories/story.txt", encoding="utf-8").read()

# Create simple background image
img = Image.new("RGB", (1920,1080), (0,0,0))
draw = ImageDraw.Draw(img)

draw.text((100,500), text[:200], fill=(255,255,255))

img_path = "assets/bg.png"
img.save(img_path)

bg = ImageClip(img_path).set_duration(audio.duration)

video = bg.set_audio(audio)

video.write_videofile(
    "videos/final.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
