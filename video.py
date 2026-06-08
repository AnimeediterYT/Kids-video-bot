from moviepy.editor import AudioFileClip, ColorClip, TextClip, CompositeVideoClip
import os

os.makedirs("videos", exist_ok=True)

audio = AudioFileClip("audio/voice.mp3")

text = open("stories/story.txt", encoding="utf-8").read()

bg = ColorClip(size=(1920,1080), color=(0,0,0), duration=audio.duration)

subtitle = TextClip(
    text,
    fontsize=50,
    color='white',
    method='caption',
    size=(1800,800)
)

subtitle = subtitle.set_position("center").set_duration(audio.duration)

video = CompositeVideoClip([bg, subtitle]).set_audio(audio)

video.write_videofile(
    "videos/final.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
