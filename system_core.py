import json
import os

STATE_FILE = "system_state.json"


# =============================
# LOAD STATE
# =============================
def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# =============================
# SAVE STATE
# =============================
def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# =============================
# UPDATE MEMORY
# =============================
def update_memory(key, value):
    state = load_state()

    if key not in state:
        state[key] = []

    if isinstance(state[key], list):
        state[key].append(value)
        state[key] = state[key][-50:]  # keep last 50
    else:
        state[key] = value

    save_state(state)


# =============================
# INTELLIGENCE FEED
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
# SYSTEM SIGNAL
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
