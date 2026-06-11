import json
import os
from collections import Counter

STATE_FILE = "system_state.json"
MAX_MEMORY = 100


# =============================
# LOAD STATE
# =============================
def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
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
        state[key] = state[key][-MAX_MEMORY:]
    else:
        state[key] = value

    save_state(state)


# =============================
# SET VALUE
# =============================
def set_value(key, value):
    state = load_state()
    state[key] = value
    save_state(state)


# =============================
# GET VALUE
# =============================
def get_value(key, default=None):
    state = load_state()
    return state.get(key, default)


# =============================
# TOP ITEMS
# =============================
def get_top_items(memory_key, limit=10):
    state = load_state()

    items = state.get(memory_key, [])

    flat = []

    for item in items:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)

    return [
        value
        for value, _
        in Counter(flat).most_common(limit)
    ]


# =============================
# INTELLIGENCE FEED
# =============================
def get_intelligence():
    return {
    "hooks": state.get("best_hooks", []),
    "titles": state.get("best_titles", []),
    "characters": state.get("best_characters", []),
    "scenarios": state.get("best_scenarios", []),
    "uploaded_videos": state.get("uploaded_videos", []),
    "video_urls": state.get("video_urls", [])
    }


# =============================
# ANALYTICS STORAGE
# =============================
def record_video_analytics(
    video_id,
    views=0,
    likes=0,
    comments=0,
    score=0,
):
    update_memory(
        "analytics_history",
        {
            "video_id": video_id,
            "views": views,
            "likes": likes,
            "comments": comments,
            "score": score,
        },
    )


# =============================
# PERFORMANCE SCORE
# =============================
def calculate_score(
    views=0,
    likes=0,
    comments=0,
):
    return (
        views
        + (likes * 5)
        + (comments * 10)
    )


# =============================
# TREND ENGINE
# =============================
def get_trend_signal():
    history = get_value("analytics_history", [])

    if len(history) < 3:
        return "LEARNING_PHASE"

    scores = [
        item.get("score", 0)
        for item in history
    ]

    avg = sum(scores) / len(scores)
    latest = scores[-1]

    if latest > avg * 1.5:
        return "TRENDING_UP"

    if latest < avg * 0.75:
        return "TRENDING_DOWN"

    return "STABLE"


# =============================
# CONTENT SIGNAL
# =============================
def get_signal():
    trend = get_trend_signal()

    if trend == "TRENDING_UP":
        return "STRONG_WINNERS"

    if trend == "TRENDING_DOWN":
        return "WEAK_CONTENT"

    if trend == "LEARNING_PHASE":
        return "LEARNING_PHASE"

    return "STABLE"


# =============================
# BEST CONTENT DETECTOR
# =============================
def get_best_performers():
    history = get_value("analytics_history", [])

    if not history:
        return []

    ranked = sorted(
        history,
        key=lambda x: x.get("score", 0),
        reverse=True,
    )

    return ranked[:10]


# =============================
# SYSTEM REPORT
# =============================
def get_system_report():
    return {
        "signal": get_signal(),
        "trend": get_trend_signal(),
        "best_titles": get_top_items("best_titles", 5),
        "best_hooks": get_top_items("best_hooks", 5),
        "best_characters": get_top_items("best_characters", 5),
        "best_scenarios": get_top_items("best_scenarios", 5),
        "analytics_count": len(
            get_value("analytics_history", [])
        ),
    }
