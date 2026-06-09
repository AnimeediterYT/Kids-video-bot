import os
import sys
import json
import requests

PRIMARY_KEY = os.environ.get("PRIMARY_AI_API_KEY")

def has_api_credits():
    """Checks if OpenAI API credits are available without breaking the loop."""
    if not PRIMARY_KEY:
        return False
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {PRIMARY_KEY}", "Content-Type": "application/json"}
    data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
    try:
        res = requests.post(url, json=data, headers=headers, timeout=5)
        if res.status_code == 429:
            return False
        return res.status_code == 200
    except:
        return False

def ask_manager_ai_to_fix(filename, error_message):
    """Asks the Gatekeeper AI to fix the script ONLY if credits are active."""
    if not has_api_credits():
        print("⏳ Gatekeeper Notice: OpenAI account is out of credits. Skipping AI self-healing and maintaining stable layout.")
        return None

    print(f"🤖 Manager AI: Analyzing error inside {filename}...")
    with open(filename, "r") as f:
        original_code = f.read()

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {PRIMARY_KEY}", "Content-Type": "application/json"}
    
    system_instruction = (
        "You are the System Gatekeeper. Your job is to fix a crash error in a Python script. "
        "CRITICAL RULE: You must ONLY fix the exact line causing the problem. Do NOT change the user's style, "
        "do NOT remove their layout rules, and do NOT change how the video looks. Return the complete code file inside a valid JSON object with the key 'code'."
    )
    
    prompt = f"Original Code:\n{original_code}\n\nCrash Error:\n{error_message}\n\nFix the error while keeping everything else identical."
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    try:
        res = requests.post(url, json=data, headers=headers, timeout=30)
        res_json = res.json()
        raw_fix = json.loads(res_json["choices"][0]["message"]["content"])
        return raw_fix.get("code")
    except Exception as e:
        print(f"❌ Gatekeeper: AI processing error: {e}")
        return None

def run_pipeline_with_self_healing():
    print("🚀 Supervisor: Initializing automated content production pipeline...")
    
    # 📦 Run script generator step
    print("📦 Step 1: Executing generate.py...")
    gen_exit = os.system("python generate.py")
    
    # 🎬 Run video rendering step
    print("🎬 Step 2: Executing video.py...")
    video_exit = os.system("python video.py")
    
    # If the video script fails, try to repair it dynamically
    if video_exit != 0:
        print("💥 Crash detected in video compilation! Invoking Self-Healing protocols...")
        error_context = "ImageMagick security policy restriction or image asset handling drop"
        
        fixed_code = ask_manager_ai_to_fix("video.py", error_context)
        if fixed_code:
            # Gatekeeper Validation Rule Layer: Check if it kept your text styling intact
            if "TextClip" in fixed_code and "yellow" in fixed_code:
                print("✅ Gatekeeper: Fix APPROVED! Code changes match user parameters. Rewriting...")
                with open("video.py", "w") as f:
                    f.write(fixed_code)
                print("🔄 Retrying video compilation with fixed code...")
                os.system("python video.py")
            else:
                print("❌ Gatekeeper: Fix DECLINED! The AI attempted unauthorized changes to your video layout design.")
        else:
            print("⚠️ Self-healing bypass: Running with current stable repository parameters.")
            
    print("✅ Supervisor: Pipeline process complete.")

if __name__ == "__main__":
    run_pipeline_with_self_healing()
  
