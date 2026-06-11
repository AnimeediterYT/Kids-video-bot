import json
import os

STATE_FILE = "system_state.json"

os.makedirs(".", exist_ok=True)


# =============================
# LOAD SYSTEM STATE
# =============================
def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "best_hooks": [],
            "best_titles": [],
            "best_characters": [],
            "best_scenarios": [],
            "video_memory": []
        }

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# =============================
# SAVE SYSTEM STATE
# =============================
def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# =============================
# UPDATE MEMORY (USED BY ALL FILES)
# =============================
def update_memory(key, value):
    state = load_state()

    if key not in state:
        state[key] = []

    if isinstance(state[key], list):
        state[key].append(value)

        # keep only last 20 entries
        state[key] = state[key][-20:]
    else:
        state[key] = value

    save_state(state)


# =============================
# GET INTELLIGENCE
# =============================
def get_intelligence():
    state = load_state()

    return {
        "hooks": state.get("best_hooks", []),
        "titles": state.get("best_titles", []),
        "characters": state.get("best_characters", []),
        "scenarios": state.get("best_scenarios", [])
    }


# =============================
# FEEDBACK SIGNAL
# =============================
def get_signal():
    state = load_state()

    videos = state.get("video_memory", [])

    if len(videos) < 3:
        return "LEARNING_PHASE"

    scores = [v.get("score", 0) for v in videos]

    avg = sum(scores) / len(scores)
    best = max(scores)

    if best > avg * 1.5:
        return "STRONG_WINNERS"
    elif best < avg:
        return "WEAK_CONTENT"
    else:
        return "STABLE"
