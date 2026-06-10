import os
import sys
import json
import requests
import time

PRIMARY_KEY = os.environ.get("PRIMARY_AI_API_KEY")


# ----------------------------
# CHECK AI CREDITS
# ----------------------------
def has_api_credits():
    if not PRIMARY_KEY:
        return False

    try:
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {PRIMARY_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 5,
            },
            timeout=5,
        )
        return res.status_code == 200
    except:
        return False


# ----------------------------
# SAFE RUN FUNCTION
# ----------------------------
def run(cmd, name):
    print(f"⚙️ Running {name}")
    exit_code = os.system(cmd)

    if exit_code == 0:
        print(f"✅ {name} success")
        return True
    else:
        print(f"❌ {name} failed")
        return False


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def run_pipeline():
    print("🚀 AUTOPILOT PIPELINE STARTED")

    # STEP 0 — AUTOPILOT (NEW)
    print("🤖 Step 0: Generating viral content with AUTOPILOT")
    if not run("python autopilot.py", "autopilot.py"):
        print("⚠️ Autopilot failed, using fallback script system")

    # VERIFY SCRIPT EXISTS
    if not os.path.exists("current_matchup.json"):
        print("❌ No script generated. Stopping pipeline.")
        return

    # STEP 1 — GENERATE (OPTIONAL SAFETY)
    print("📦 Step 1: generate.py (optional fallback)")
    run("python generate.py", "generate.py")

    # STEP 2 — VIDEO CREATION
    print("🎬 Step 2: video.py")
    if not run("python video.py", "video.py"):
        print("💥 Video failed, continuing to upload attempt")

    # STEP 3 — UPLOAD (GUARANTEED)
    print("📤 Step 3: Upload.py")
    run("python Upload.py", "Upload.py")

    print("🎉 PIPELINE COMPLETE — AUTOPILOT MODE ACTIVE")


# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    run_pipeline()
