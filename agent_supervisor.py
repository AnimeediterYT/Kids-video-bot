import json
import random
import os

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
# PICK SYSTEM
# =============================
def pick():
    c1 = random.choice(CHARACTERS)
    c2 = random.choice(CHARACTERS)
    while c2 == c1:
        c2 = random.choice(CHARACTERS)
    return c1, c2


# =============================
# TITLE ENGINE v2
# =============================
def make_title(c1, c2, scenario):
    candidates = [
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
        if "FINAL" in t.upper() or "INSANE" in t.upper(): s += 1
        return s

    best_score = max(score(t) for t in candidates)
    best = [t for t in candidates if score(t) == best_score]

    return random.choice(best)


# =============================
# HOOK ENGINE v2 (RETENTION CORE)
# =============================
def build_hook(c1, c2):
    hooks = [
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
        if any(x in h for x in ["💥", "🔥", "😱"]): s += 2
        if c1 in h and c2 in h: s += 2
        return s

    best_score = max(score(h) for h in hooks)
    best = [h for h in hooks if score(h) == best_score]

    return random.choice(best)


# =============================
# DESCRIPTION + SEO + HASHTAGS
# =============================
def make_description(c1, c2, scenario):
    keywords = f"{c1} vs {c2}, anime battle, what if fight, power scaling, {scenario}"

    desc = f"""
🔥 {c1} vs {c2} - EPIC ANIME BATTLE

A what-if scenario where two legendary fighters collide in:
{scenario}

💥 Power scaling | transformations | ultimate clash

COMMENT WHO WINS 👇

{keywords}
""".strip()

    return desc[:1000]


def make_hashtags():
    base = ["#anime", "#shorts", "#battle", "#vs", "#whatif", "#powerlevels"]
    return " ".join(base)


# =============================
# SCRIPT ENGINE v2 (3-ACT STRUCTURE)
# =============================
def build_script(c1, c2, scenario):
    hook = build_hook(c1, c2)

    return [
        hook,  # ACT 1
        f"{c1} enters the battlefield...",
        f"{c2} prepares for impact...",
        f"SCENARIO: {scenario}",  # ACT 2 BUILD
        f"{c1} awakens hidden power...",
        f"{c2} reaches final form...",
        "THE FINAL CLASH SHATTERS REALITY!",  # ACT 3 CLIMAX
        "WHO WINS THIS FIGHT?!"
    ]


# =============================
# VIRAL SCORE v2 (PREDICTIVE)
# =============================
def viral_score(title, script, hook):
    score = 0

    if "vs" in title.lower(): score += 2
    if "🔥" in title or "⚡" in title: score += 2
    if "WHO" in hook or "WHAT" in hook: score += 2
    if any("FINAL" in s.upper() for s in script): score += 2
    if len(script) >= 7: score += 1

    return score


def quality_flag(score):
    return "GOOD" if score >= 6 else "RETRY"


# =============================
# MAIN GENERATOR
# =============================
def generate():
    c1, c2 = pick()
    scenario = random.choice(SCENARIOS)

    title = make_title(c1, c2, scenario)
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
        "quality_flag": quality_flag(score)
    }

    os.makedirs(".", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("🚀 TITLE:", title)
    print("🔥 HOOK:", hook)
    print("📊 SCORE:", score)
    print("📌 QUALITY:", data["quality_flag"])


if __name__ == "__main__":
    print("🚀 CONTENT ENGINE (FULL SYSTEM) RUNNING...")
    generate()
