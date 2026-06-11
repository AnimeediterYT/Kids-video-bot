import json
import random
import os
from system_core import (
    get_intelligence,
    update_memory,
    get_signal,
    get_best_video
)
OUTPUT_FILE = "current_matchup.json"


# =============================
# CORE UNIVERSE
# =============================
CHARACTERS = [
    "Goku", "Vegeta", "Gohan", "Broly", "Frieza",
    "Naruto", "Sasuke", "Itachi", "Madara",
    "Luffy", "Zoro", "Sanji", "Kaido",
    "Ichigo", "Aizen", "Gojo", "Sukuna",
    "Tanjiro", "Muzan", "Saitama", "Killua"
]

SCENARIOS = [
    "What If Battle in Alternate Universe",
    "Final Dimension Collapse Fight",
    "God Level Power Awakening War",
    "Time Rift Death Match",
    "Multiverse Survival Battle",
    "Hidden Power Awakening Clash"
]


# =============================
# PICK SYSTEM (ENHANCED)
# =============================
def pick():
    memory = get_intelligence()
    best_video = get_best_video()

    # bias toward learned best characters if available
    if best_video:
        learned_chars = best_video.get("characters", [])
    else:
        learned_chars = memory.get("characters", [])

    if learned_chars:
        # flatten safely
        flat = []
        for item in learned_chars:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)

        flat = [c for c in flat if c]

        if len(flat) >= 2:
            c1, c2 = random.sample(flat, 2)
            return c1, c2

    # fallback random
    c1 = random.choice(CHARACTERS)
    c2 = random.choice(CHARACTERS)

    while c2 == c1:
        c2 = random.choice(CHARACTERS)

    return c1, c2


# =============================
# TITLE ENGINE (IMPROVED WITH MEMORY)
# =============================
def make_title(c1, c2, scenario):
    memory = get_intelligence()
    best_video = get_best_video()
    best_titles = memory.get("titles", [])

    candidates = best_titles + [
        f"🔥 {c1} vs {c2} | {scenario}",
        f"{c1} ⚡ VS ⚡ {c2} - Ultimate Battle",
        f"WHO IS STRONGER? {c1} or {c2}?",
        f"{c1} vs {c2} - BREAKS REALITY 💥",
        f"INSANE CLASH: {c1} vs {c2}",
        f"LEGENDARY FIGHT: {c1} vs {c2}",
        f"{c1} vs {c2} - FINAL FORM SHOWDOWN"
    ]

    def score(t):
        s = 0
        if "vs" in t.lower(): s += 2
        if "🔥" in t or "⚡" in t: s += 2
        if "?" in t: s += 1
        if len(t) < 60: s += 1
        return s

    best = max(candidates, key=score)
    return best


# =============================
# HOOK ENGINE (LEARNING-BASED)
# =============================
def build_hook(c1, c2):
    memory = get_intelligence()
    learned_hooks = memory.get("hooks", [])

    hooks = learned_hooks + [
        f"WHO WINS THIS?! {c1} vs {c2} 💥",
        f"{c1} vs {c2} JUST BROKE REALITY 😱",
        f"NO ONE EXPECTED THIS FIGHT: {c1} vs {c2}",
        f"WHAT HAPPENS WHEN {c1} FIGHTS {c2}?",
        f"THIS IS NOT POSSIBLE: {c1} vs {c2}",
        f"LEGENDARY CLASH BEGINS: {c1} vs {c2}"
    ]

    def score(h):
        s = 0
        if "WHO" in h or "WHAT" in h: s += 2
        if "vs" in h.lower(): s += 2
        if c1 in h and c2 in h: s += 2
        return s

    return max(hooks, key=score)


# =============================
# DESCRIPTION
# =============================
def make_description(c1, c2, scenario):
    keywords = f"{c1} vs {c2}, anime battle, power scaling, {scenario}"

    return f"""
🔥 {c1} vs {c2} - EPIC ANIME BATTLE

{scenario}

💥 Power scaling | transformations | ultimate clash

COMMENT WHO WINS 👇

{keywords}
""".strip()


def make_hashtags():
    return "#anime #shorts #battle #vs #whatif #powerlevels"


# =============================
# SCRIPT ENGINE
# =============================
def build_script(c1, c2, scenario):
    hook = build_hook(c1, c2)

    return [
        hook,
        f"{c1} enters the battlefield...",
        f"{c2} prepares for impact...",
        f"SCENARIO: {scenario}",
        f"{c1} awakens hidden power...",
        f"{c2} reaches final form...",
        "THE FINAL CLASH SHATTERS REALITY!",
        "WHO WINS THIS FIGHT?!"
    ]


# =============================
# VIRAL SCORE
# =============================
def viral_score(title, script, hook):
    score = 0

    if "vs" in title.lower(): score += 2
    if "🔥" in title or "⚡" in title: score += 2
    if "WHO" in hook or "WHAT" in hook: score += 2
    if any("FINAL" in s.upper() for s in script): score += 2

    return score


def quality_flag(score):
    return "GOOD" if score >= 6 else "RETRY"


# =============================
# MAIN GENERATOR (NOW LEARNING-AWARE)
# =============================
def generate():
  signal = get_signal()
best_video = get_best_video()

if best_video:
    print("🏆 BEST VIDEO:", best_video.get("title", "Unknown"))

    c1, c2 = pick()

if best_video and "characters" in best_video:
    chars = best_video.get("characters", [])

    if len(chars) >= 2:
        c1 = chars[0]
        c2 = chars[1]

        print("🧠 Reusing winning characters:", c1, "vs", c2)
    scenario = random.choice(SCENARIOS)

    title = make_title(c1, c2, scenario)

if best_video and best_video.get("title"):
    old_title = best_video["title"]

    if "🔥" in old_title and "🔥" not in title:
        title = "🔥 " + title

    print("🧠 Learning from title:", old_title)
    script = build_script(c1, c2, scenario)
    hook = script[0]

    description = make_description(c1, c2, scenario)
    hashtags = make_hashtags()

    score = viral_score(title, script, hook)

    data = {
        "title": title,
        "description": description,
        "script": script,
        "hook": hook,
        "hashtags": hashtags,
        "characters": [c1, c2],
        "scenario": scenario,
        "viral_score": score,
        "quality_flag": quality_flag(score),
        "signal": signal
    }

    # =============================
    # SAVE OUTPUT
    # =============================
    os.makedirs(".", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # =============================
    # FEEDBACK TO SYSTEM CORE
    # =============================
    update_memory("uploaded_videos", {
    "title": title,
    "hook": hook,
    "characters": [c1, c2],
    "scenario": scenario,
    "score": score
})

    update_memory("best_titles", title)
    update_memory("best_hooks", hook)
    update_memory("best_characters", [c1, c2])
    update_memory("best_scenarios", scenario)

    print("🚀 TITLE:", title)
    print("🔥 HOOK:", hook)
    print("📊 SCORE:", score)
    print("📡 SIGNAL:", signal)
    print("📌 QUALITY:", data["quality_flag"])


if __name__ == "__main__":
    print("🧠 SELF-LEARNING AGENT RUNNING...")
    generate()
