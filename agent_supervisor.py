import os
import sys
import json
import requests
import time

PRIMARY_KEY = os.environ.get("PRIMARY_AI_API_KEY")


def has_api_credits():
    """Checks if OpenAI API credits are available without breaking the loop."""
    if not PRIMARY_KEY:
        return False

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {PRIMARY_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5,
    }

    try:
        res = requests.post(url, json=data, headers=headers, timeout=5)
        if res.status_code == 429:
            return False
        return res.status_code == 200
    except:
        return False


# ----------------------------
# NEW: SAFE RETRY WRAPPER (ADDED ONLY)
# ----------------------------
def run_with_retry(cmd, name, retries=2):
    for i in range(retries + 1):
        print(f"⚙️ Running {name} (attempt {i+1})")
        exit_code = os.system(cmd)

        if exit_code == 0:
            print(f"✅ {name} success")
            return True

        print(f"⚠️ {name} failed")
        time.sleep(2)

    print(f"❌ {name} failed after retries")
    return False


def ask_manager_ai_to_fix(filename, error_message):
    """Asks the Gatekeeper AI to fix the script ONLY if credits are active."""
    if not has_api_credits():
        print("⏳ Gatekeeper Notice: No credits. Skipping AI self-heal.")
        return None

    print(f"🤖 Manager AI: Fixing {filename}...")

    with open(filename, "r") as f:
        original_code = f.read()

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {PRIMARY_KEY}",
        "Content-Type": "application/json",
    }

    system_instruction = (
        "You are a strict code fixer. Only fix the error line. "
        "Do NOT change design, layout, or structure. "
        "Return JSON: {\"code\": \"full fixed file\"}"
    )

    prompt = f"Code:\n{original_code}\n\nError:\n{error_message}"

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }

    try:
        res = requests.post(url, json=data, headers=headers, timeout=30)
        res_json = res.json()
        raw_fix = json.loads(res_json["choices"][0]["message"]["content"])
        return raw_fix.get("code")

    except Exception as e:
        print(f"❌ AI error: {e}")
        return None


def run_pipeline_with_self_healing():
    print("🚀 Supervisor: Starting pipeline...")

    # ----------------------------
    # STEP 1 (IMPROVED WITH RETRY)
    # ----------------------------
    print("📦 Step 1: Running generate.py")
    if not run_with_retry("python generate.py", "generate.py"):
        print("⚠️ generate.py failed → continuing anyway (fallback mode)")

    # ----------------------------
    # STEP 2 (VIDEO + SELF HEAL KEPT SAME)
    # ----------------------------
    print("🎬 Step 2: Running video.py")
    video_exit = os.system("python video.py")

    if video_exit != 0:
        print("💥 video.py crashed, attempting self-heal...")

        error_context = "Video rendering failure (MoviePy/Image/audio issue)"

        fixed_code = ask_manager_ai_to_fix("video.py", error_context)

        if fixed_code:
            if "TextClip" in fixed_code:
                print("✅ Fix accepted, updating video.py")

                with open("video.py", "w") as f:
                    f.write(fixed_code)

                print("🔄 Retrying video.py")
                os.system("python video.py")
            else:
                print("❌ Fix rejected (layout modified)")
        else:
            print("⚠️ No fix applied")

        return

    # ----------------------------
    # STEP 3 (UPLOAD GUARANTEED WITH RETRY)
    # ----------------------------
    print("📤 Step 3: Running Upload.py")

    if not run_with_retry("python Upload.py", "Upload.py"):
        print("❌ Upload failed after retries")
        return

    print("🎉 Pipeline complete successfully!")


if __name__ == "__main__":
    run_pipeline_with_self_healing()
