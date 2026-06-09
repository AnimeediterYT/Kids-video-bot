import json
import os
import random
import requests

os.makedirs("stories", exist_ok=True)
os.makedirs("audio", exist_ok=True)

# 💥 MASSIVE EXPANDED ROSTER (50+ Characters)
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

def get_ai_script_primary(prompt_details, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    system_prompt = (
        "You are an expert anime hype scriptwriter. Write a 5-sentence video narration based on the user's request. "
        "Return ONLY a raw JSON object containing a single key named 'script' whose value is an array of exactly 5 short strings. "
        "Example format: {\"script\": [\"Line 1\", \"Line 2\", \"Line 3\", \"Line 4\", \"Line 5\"]}"
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
    raw_content = response.json()["choices"][0]["message"]["content"]
    
    # Foolproof Parsing Layer
    parsed = json.loads(raw_content)
    if "script" in parsed and isinstance(parsed["script"], list):
        return [str(line) for line in parsed["script"][:5]]
    for val in parsed.values():
        if isinstance(val, list):
            return [str(line) for line in val[:5]]
    raise ValueError("Could not extract clean array from OpenAI response structure.")

def build_infinite_concept():
    char1, char2 = random.sample(ROSTER, 2)
    chosen_theme = random.choice(THEMES)
    
    if chosen_theme == "TRAPPED_IN":
        title = f"What if {char1} was in Jujutsu Kaisen?"
        prompt = f"Write an insane scenario where {char1} gets trapped in the Jujutsu Kaisen universe. Max 12 words per line."
    elif chosen_theme == "STOLEN_POWER":
        title = f"What if {char1} unlocked a Domain Expansion?"
        prompt = f"Write a crazy theory script where {char1} combines their signature attacks with an ultimate Domain Expansion. Max 12 words per line."
    elif chosen_theme == "EVIL_SWAP":
        title = f"Evil {char1} Takes Over!"
        prompt = f"Write an alternate universe script where {char1} turns completely evil, betrays everyone, and fights {char2}. Max 12 words per line."
    else:
        title = f"{char1} vs {char2}"
        prompt = f"Write an intense scaling debate script about an all-out deathmatch between {char1} and {char2}. Max 12 words per line."

    return title, prompt

def generate_dynamic_matchup():
    title, prompt = build_infinite_concept()
    script = []
    primary_key = os.environ.get("PRIMARY_AI_API_KEY")
    
    if primary_key:
        try:
            print(f"🎲 Generating Concept: {title}")
            script = get_ai_script_primary(prompt, primary_key)
        except Exception as e:
            print(f"❌ Primary API error: {e}")
            
    if not script or len(script) < 5:
        print("⚠️ Falling back to emergency script script arrays.")
        script = [
            f"What happens when anime universes collide like this?",
            f"Imagine the sheer scale if {title} actually went down.",
            "The scaling community would completely lose their minds over this.",
            "Comment down your real power scaling facts right now.",
            "Subscribe for daily crazy multiverse matchups!"
        ]
        
    payload = {"title": title, "script": script}
    with open("current_matchup.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    full_text = " ".join(script)
    with open("stories/story.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
        
    return full_text

def generate_elevenlabs_voice(text_to_speak):
    el_key = os.environ.get("ELEVENLABS_API_KEY")
    if not el_key:
        print("❌ Error: ELEVENLABS_API_KEY environment secret is missing!")
        return

    print("🎙️ Requesting voice rendering from ElevenLabs...")
    voice_id = "pNInz6obpgLb9nm6EilI"  # High Hype Male Voice (Adam)
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
        print("✅ Voice file written successfully: audio/voice.mp3")
    else:
        print(f"❌ ElevenLabs Server Rejected Request: {response.status_code} - {response.text}")

if __name__ == "__main__":
    audio_text = generate_dynamic_matchup()
    generate_elevenlabs_voice(audio_text)
    
