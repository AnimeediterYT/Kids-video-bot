import json
import os
import random
import requests

os.makedirs("stories", exist_ok=True)
os.makedirs("audio", exist_ok=True)

# 💥 THE ULTIMATE ANIME ROSTER (50+ Legends)
ROSTER = [
    "Goku", "Vegeta", "Gohan", "Frieza", "Broly", "Beerus", 
    "Luffy", "Zoro", "Sanji", "Shanks", "Kaido", "Gear 5 Luffy",
    "Naruto", "Sasuke", "Kakashi", "Itachi", "Madara", "Pain",
    "Saitama", "Genos", "Garou", "Boros",
    "Sukuna", "Gojo", "Yuji Itadori", "Yuta Okkotsu", "Toji Fushiguro",
    "Tanjiro", "Nezuko", "Zenitsu", "Rengoku", "Muzan", "Kokushibo",
    "Ichigo", "Aizen", "Yhwach", "Kenpachi", "Grimmjow",
    "Rimuru Tempest", "Anos Voldigoad", "Mob",
    "Eren Yeager", "Levi Ackerman", "Deku", "Bakugo", "All Might",
    "Alucard", "Light Yagami", "Gon", "Killua", "Hisoka"
]

THEMES = ["VS_BATTLE", "TRAPPED_IN", "STOLEN_POWER", "EVIL_SWAP"]

def build_infinite_concept():
    char1, char2 = random.sample(ROSTER, 2)
    chosen_theme = random.choice(THEMES)
    
    if chosen_theme == "TRAPPED_IN":
        title = f"What if {char1} was in Jujutsu Kaisen?"
        script = [
            f"What happens if {char1} gets trapped in Jujutsu Kaisen?",
            "Cursed energy floods the atmosphere instantly.",
            f"Special grade curses launch a massive ambush.",
            f"But {char1} activates a god tier counter attack!",
            "The jujutsu world has never seen power like this."
        ]
    elif chosen_theme == "STOLEN_POWER":
        title = f"What if {char1} unlocked a Domain Expansion?"
        script = [
            f"What if {char1} combined their skills with a Domain Expansion?",
            "The reality barrier completely shatters under pressure.",
            "An absolute, unavoidable critical hit is locked in.",
            "Even the strongest anime gods cannot escape this layout.",
            "This combination completely breaks the scaling charts!"
        ]
    elif chosen_theme == "EVIL_SWAP":
        title = f"Evil {char1} Takes Over!"
        script = [
            f"What if {char1} turned completely evil and betrayed everyone?",
            "A dark cloud falls over the entire universe.",
            f"Only one warrior steps up to stop the destruction: {char2}!",
            "The final clash of titans begins right now.",
            f"Comment down below who survives this betrayal!"
        ]
    else:
        title = f"{char1} vs {char2}"
        script = [
            f"Who actually wins this ultimate deathmatch showdown?",
            f"{char1} brings insane speed blitz potential and cosmic hacks.",
            f"Stop coping! {char2} completely outclasses them in raw IQ.",
            "One definitive strike completely shatters their defense system.",
            "Debate down below with your real scaling facts!"
        ]

    return title, script

def generate_dynamic_matchup():
    title, script = build_infinite_concept()
    
    # Check if OpenAI key is alive, use it to get unique text variations if credits ever return
    primary_key = os.environ.get("PRIMARY_AI_API_KEY")
    if primary_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            prompt = f"Write an alternate anime universe script about: {title}. Format ONLY as a clean JSON list of 5 short strings."
            data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
            res = requests.post(url, headers=headers, json=data, timeout=5)
            if res.status_code == 200:
                parsed = json.loads(res.json()["choices"][0]["message"]["content"])
                if isinstance(parsed, list): script = parsed[:5]
        except:
            print("🤖 OpenAI Credits empty! Utilizing local infinite universe generation engine.")

    payload = {"title": title, "script": script}
    with open("current_matchup.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    full_text = " ".join(script)
    with open("stories/story.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"🎲 Concept generated successfully: {title}")
    return full_text

def generate_free_voice(text_to_speak):
    print("🎙️ Activating free high-hype AI voice generation via native systems...")
    
    # We use Microsoft's premium aggressive male news voice (Christopher) - completely free and infinite
    voice_name = "en-US-ChristopherNeural"
    output_audio = "audio/voice.mp3"
    
    # Command line calling edge-tts framework directly inside the system container
    command = f'edge-tts --voice {voice_name} --text "{text_to_speak}" --write-media {output_audio}'
    os.system(command)
    
    if os.path.exists(output_audio) and os.path.getsize(output_audio) > 0:
        print("✅ Free voice track successfully written to: audio/voice.mp3")
    else:
        print("❌ CRITICAL: Free voice generator stream failed.")

if __name__ == "__main__":
    audio_text = generate_dynamic_matchup()
    generate_free_voice(audio_text)
    
