from gtts import gTTS
import random
import os

os.makedirs("stories", exist_ok=True)
os.makedirs("audio", exist_ok=True)

topics = open("topics.txt", encoding="utf-8").read().splitlines()
topic = random.choice([t for t in topics if t.strip()])

script = (
    f"Hook: Have you ever thought about {topic}? "
    f"Story: Many people ignore {topic} in life. "
    f"Lesson: {topic} is important for success. "
    f"Ending: Always respect {topic}."
)

open("stories/story.txt","w",encoding="utf-8").write(script)

tts = gTTS(script)
tts.save("audio/voice.mp3")
