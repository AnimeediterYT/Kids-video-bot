import random
import asyncio
import edge_tts
import os

os.makedirs("stories", exist_ok=True)
os.makedirs("audio", exist_ok=True)

topics = open("topics.txt", encoding="utf-8").read().splitlines()
topic = random.choice([t for t in topics if t.strip()])

script = (
    f"Attention. Stop scrolling. "
    f"Have you ever thought about {topic}? "
    f"Most people ignore it. "
    f"But {topic} can change your life completely. "
    f"Lesson: {topic} builds discipline, success and future growth. "
    f"Remember this."
)

open("stories/story.txt","w",encoding="utf-8").write(script)

async def main():
    voice = edge_tts.Communicate(script, "en-US-AriaNeural")
    await voice.save("audio/voice.mp3")

asyncio.run(main())
