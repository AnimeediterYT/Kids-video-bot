import json
import os
import random
import requests

os.makedirs("stories", exist_ok=True)
os.makedirs("audio", exist_ok=True)

ROSTER = ["Goku", "Zoro", "Saitama", "Naruto", "Luffy", "Sukuna", "Gojo", "Ichigo", "Vegeta", "Madara"]

def get_ai_script_primary(char1, char2, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    prompt = f"Create a highly aggressive debate script about who wins a fight between {char1} and {char2}. Format your response exactly as a JSON array of 5 short strings representing fast arguments. Max 15 words per line."
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=15)
    response.raise_for_status()
    res_json = response.json()
    content = json.loads(res_json["choices"][0]["message"]["content"])
    return content.get("script", list(content.values())[0])

def get_ai_script_backup(char1, char2, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    prompt = f"Create an aggressive debate script about a fight between {char1} and {char2}. Format as a JSON object containing a list named 'lines' with 5 short argument sentences."
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=15)
    response.raise_for_status()
    res_json = response.json()
    text_content = res_json["candidates"][0]["content"]["parts"][0]["text"]
    content = json.loads(text_content)
    return content.get("lines", list(content.values())[0])

def generate_dynamic_matchup():
    char1, char2 = random.sample(ROSTER, 2)
    title = f"{char1} vs {char2}"
    script = []
    
    primary_key = os.environ.get("PRIMARY_AI_API_KEY")
    backup_key = os.environ.get("BACKUP_AI_API_KEY")
    
    if primary_key:
        try:
            print("Attempting generation via Primary AI API...")
            script = get_ai_script_primary(char1, char2, primary_key)
        except Exception as e:
            print(f"Primary API failed: {e}. Routing to backup...")
            
    if not script and backup_key:
        try:
            print("Attempting generation via Backup AI API...")
            script = get_ai_script_backup(char1, char2, backup_key)
        except Exception as e:
            print(f"Backup API failed: {e}")
            
    if not script:
        print("All APIs failed. Using fallback framework library.")
        script = [
            f"Who actually wins this showdown? {char1} vs {char2} is wild.",
            f"{char1} brings insane speed and scaling feats.",
            f"Stop coping! {char2} completely outclasses them in raw IQ.",
            f"One structural technique from {char2} breaks their entire kit.",
            "Debate down below with real facts!"
        ]
        
    payload = {"title": title, "script": script}
    with open("current_matchup.json", "w") as f:
        json.dump(payload, f, indent=4)
        
    full_audio_text = " ".join(script)
    with open("stories/story.txt", "w", encoding="utf-8") as f:
        f.write(full_audio_text)
        
    print(f"Successfully finalized dynamic manifest processing for: {title}")
    return full_audio_text

def generate_elevenlabs_voice(text_to_speak):
    print("Generating ElevenLabs high-retention audio file...")
    el_key = os.environ.get("ELEVENLABS_API_KEY")
    if not el_key:
        print("Error: ELEVENLABS_API_KEY is missing from the environment variables!")
        return

    # Using 'Adam' voice ID
    voice_id = "pNInz6obpgLb9nm6EilI"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": el_key
    }
    
    data = {
        "text": text_to_speak,
        "model_id": "eleven_multilingual_v2", # Upgraded from old deprecated v1 engine
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("audio/voice.mp3", "wb") as f:
            f.write(response.content)
        print("Audio processing complete: audio/voice.mp3")
    else:
        print(f"ElevenLabs API Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    audio_text = generate_dynamic_matchup()
    generate_elevenlabs_voice(audio_text)

