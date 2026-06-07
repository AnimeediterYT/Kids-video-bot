from moviepy.editor import *

audio = AudioFileClip("audio/voice.mp3")

bg = ColorClip((1080,1920), color=(0,0,0), duration=audio.duration)

txt = TextClip("Moral Story", fontsize=70, color='white')
txt = txt.set_duration(audio.duration).set_position("center")

video = CompositeVideoClip([bg, txt]).set_audio(audio)

video.write_videofile("videos/final.mp4", fps=24, codec="libx264")
