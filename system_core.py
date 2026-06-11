import json
import os
from collections import Counter

STATE_FILE = "system_state.json"
MAX_MEMORY = 100


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def update_memory(key, value):
    state = load_state()

    if key not in state:
        state[key] = []

    if isinstance(state[key], list):
        state[key].append(value)
        state[key] = state[key][-MAX_MEMORY:]
    else:
        state[key] = value

    save_state(state)


def set_value(key, value):
    state = load_state()
    state[key] = value
    save_state(state)


def get_value(key, default=None):
    state = load_state()
    return state.get(key, default)


def get_top_items(memory_key, limit=10):
    state = load_state()
    items = state.get(memory_key, [])

    flat = []
    for item in items:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)

    return [v for v, _ in Counter(flat).most_common(limit)]


def get_intelligence():
    state = load_state()

    return {
        "hooks": state.get("best_hooks", []),
        "titles": state.get("best_titles", []),
        "characters": state.get("best_characters", []),
        "scenarios": state.get("best_scenarios", []),
        "uploaded_videos": state.get("uploaded_videos", []),
    }


def get_signal():
    state = load_state()
    videos = state.get("uploaded_videos", [])

    if len(videos) < 5:
        return "LEARNING_PHASE"

    scores = [v.get("score", 0) for v in videos]
    if not scores:
        return "LEARNING_PHASE"

    avg = sum(scores) / len(scores)
    best = max(scores)

    if best > avg * 1.5:
        return "STRONG_WINNERS"
    if avg < 100:
        return "WEAK_CONTENT"

    return "STABLE"
