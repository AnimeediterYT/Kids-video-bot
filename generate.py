from gtts import gTTS
import random
import os

os.makedirs("stories", exist_ok=True)
os.makedirs("audio", exist_ok=True)

topics = open("topics.txt", encoding="utf-8").read().splitlines()
topic = random.choice([t for t in topics if t.strip()])

script = (
    f"Attention. Stop scrolling. "
    f"Have you ever thought about {topic}? "
    f"Most people ignore it. "
    f"But {topic} can change your life. "
    f"Lesson: {topic} builds discipline and success. "
    f"Remember this."
)

open("stories/story.txt", "w", encoding="utf-8").write(script)

tts = gTTS(script)
tts.save("audio/voice.mp3")
