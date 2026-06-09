import json
import os
import random
import requests

os.makedirs("stories", exist_ok=True)
os.makedirs("audio", exist_ok=True)

# 💥 MASSIVE EXPANDED ROSTER (50+ Characters across all major universes)
ROSTER = [
    "Goku", "Vegeta", "Gohan", "Frieza", "Broly", "Beerus", 
    "Luffy", "Zoro", "Sanji", "Shanks", "Kaido", "Gear 5 Luffy",
    "Naruto", "Sasuke", "Kakashi", "Itachi", "Madara", "Pain",
    "Saitama", "Genos", "Garou", "Boros",
    "Sukuna", "Gojo", "Yuji Itadori", "Yuta Okkotsu", "Toji Fushiguro",
    "Tanjiro", "Nezuko", "Zenitsu", "Rengoku", "Muzan", "Kokushibo",
    "Ichigo", "Aizen", "Yhwach", "Kenpachi", "Grimmjow",
    "Rimuru Tempest", "Anos Voldigoad", "Saitama", "Mob",
    "Eren Yeager", "Levi Ackerman", "Deku", "Bakugo", "All Might",
    "Alucard", "Light Yagami", "Gon", "Killua", "Hisoka"
]

# 🌌 MULTIVERSE PLOT ARCHETYPES
THEMES = [
    "VS_BATTLE",       # Classic scaling deathmatch
    "TRAPPED_IN",      # What if X was trapped in Y's anime universe?
    "STOLEN_POWER",    # What if X learned Y's ultimate signature technique?
    "EVIL_SWAP"        # What if X became the main villain of another show?
]

def get_ai_script_primary(prompt_details, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    system_prompt = (
        "You are an aggressive, high-hype Anime Short scriptwriter. "
        "Create a fast-paced narration script based on the prompt. "
        "Provide your output ONLY as a clean JSON object containing a key named 'script' "
        "which points to an array of exactly 5 short punchy sentences. Max 12 words per sentence."
    )
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_details}
        ],
        "response_format": {"type": "json_object"}
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=15)
    response.raise_for_status()
    res_json = response.json()
    content = json.loads(res_json["choices"][0]["message"]["content"])
    return content.get("script", list(content.values())[0])

def build_infinite_concept():
    # Pick characters and structure a unique story concept
    char1, char2 = random.sample(ROSTER, 2)
    chosen_theme = random.choice(THEMES)
    
    if chosen_theme == "TRAPPED_IN":
        title = f"What if {char1} was in Jujutsu Kaisen?"
        prompt = f"Write an insane 'What If' anime scenario script where {char1} falls through a portal and gets trapped in the Jujutsu Kaisen universe, immediately running into special grade curses. Make it hype!"
    elif chosen_theme == "STOLEN_POWER":
        title = f"What if {char1} learned Bankai?"
        prompt = f"Write a crazy hypothetical anime theory script where {char1} unlocks a Soul Reaper Bankai or Domain Expansion and combines it with their own signature attacks to achieve god-tier power."
    elif chosen_theme == "EVIL_SWAP":
        title = f"Evil {char1} Takes Over!"
        prompt = f"Write a deep alternate universe script where {char1} turns completely evil, betrays their friends, and fights {char2} who is trying to stop their world domination plans."
    else:
        title = f"{char1} vs {char2}"
        prompt = f"Write an intense scaling debate script about an all-out deathmatch between {char1} and {char2}. Analyze stats, speed blitz potential, and cosmic hax. Who wins?"

    return title, prompt

def generate_dynamic_matchup():
    title, prompt = build_infinite_concept()
    script = []
    
    primary_key = os.environ.get("PRIMARY_AI_API_KEY")
    
    if primary_key:
        try:
            print(f"🎲 Story Selected: {title}")
            script = get_ai_script_primary(prompt, primary_key)
        except Exception as e:
            print(f"Primary API failed: {e}")
            
    if not script:
        print("Fallback frame active...")
        script = [
            f"What happens when anime worlds collide like this?",
            f"Imagine the sheer scale if {title} actually went down.",
            "The scaling community would completely lose their minds over this fight.",
            "Comment down your real power scaling facts right now.",
            "Sub for daily crazy multiverse matchups!"
        ]
        
    payload = {"title": title, "script": script}
    with open("current_matchup.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    full_audio_text = " ".join(script)
    with open("stories/story.txt", "w", encoding="utf-8") as f:
        f.write(full_audio_text)
        
    return full_audio_text

def generate_elevenlabs_voice(text_to_speak):
    print("Generating ElevenLabs voiceover stream...")
    el_key = os.environ.get("ELEVENLABS_API_KEY")
    if not el_key:
        print("Error: Missing ELEVENLABS_API_KEY!")
        return

    voice_id = "pNInz6obpgLb9nm6EilI" # Adam High Hype Voice
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": el_key
    }
    
    data = {
        "text": text_to_speak,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.8}
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("audio/voice.mp3", "wb") as f:
            f.write(response.content)
        print("✅ Voice track successfully saved to audio/voice.mp3")
    else:
        print(f"❌ ElevenLabs Failed: {response.text}")

if __name__ == "__main__":
    audio_text = generate_dynamic_matchup()
    generate_elevenlabs_voice(audio_text)
        
