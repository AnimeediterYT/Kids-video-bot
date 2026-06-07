from moviepy.editor import *

# background video (black screen)
clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=6)

clip.write_videofile(
    "videos/final.mp4",
    fps=24,
    codec="libx264",
    audio=False
)
