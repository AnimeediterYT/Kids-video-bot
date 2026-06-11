import json
import random
import os

OUTPUT_FILE = "current_matchup.json"


# =============================
# CHARACTER UNIVERSE
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
# PICK CHARACTERS
# =============================
def pick():
    c1 = random.choice(CHARACTERS)
    c2 = random.choice(CHARACTERS)

    while c2 == c1:
        c2 = random.choice(CHARACTERS)

    return c1, c2


# =============================
# TITLE ENGINE (VIRAL SYSTEM)
# =============================
def make_title(c1, c2, scenario):
    candidates = [
        f"{c1} vs {c2} - {scenario}",
        f"🔥 {c1} vs {c2} | {scenario}",
        f"{c1} ⚡ VS ⚡ {c2} - Ultimate Battle",
        f"WHO IS STRONGER? {c1} or {c2}?",
        f"{c1} vs {c2} - No Limits Fight",
        f"INSANE FIGHT: {c1} vs {c2}",
        f"{c1} vs {c2} - FINAL FORM SHOWDOWN",
        f"UNSTOPPABLE WAR: {c1} vs {c2}",
        f"{c1} vs {c2} - BREAKS REALITY 💥",
        f"LEGENDARY CLASH: {c1} vs {c2}"
    ]

    def score(t):
        s = 0
        if "vs" in t.lower():
            s += 2
        if "🔥" in t or "⚡" in t:
            s += 2
        if "?" in t:
            s += 1
        if len(t) < 60:
            s += 1
        if "FINAL" in t.upper() or "INSANE" in t.upper():
            s += 1
        return s

    scored = [(t, score(t)) for t in candidates]
    scored.sort(key=lambda x: x[1], reverse=True)

    best = scored[0][1]
    best_titles = [t for t, s in scored if s == best]

    return random.choice(best_titles)


# =============================
# HOOK ENGINE (RETENTION OPTIMIZED)
# =============================
def build_hook(c1, c2):
    hooks = [
        f"WHO WINS THIS?! {c1} vs {c2} 💥",
        f"{c1} VS {c2} — THIS IS NOT POSSIBLE...",
        f"THE STRONGEST FIGHT EVER: {c1} vs {c2}",
        f"{c1} vs {c2} JUST BROKE REALITY 😱",
        f"NO ONE EXPECTED THIS: {c1} vs {c2}",
        f"WHAT HAPPENS WHEN {c1} FIGHTS {c2}?",
        f"THIS BATTLE DEFIES LOGIC: {c1} vs {c2}"
    ]

    def score(h):
        s = 0
        if "WHO" in h or "WHAT" in h:
            s += 2
        if "vs" in h.lower():
            s += 2
        if any(x in h for x in ["💥", "🔥", "😱"]):
            s += 2
        if c1 in h and c2 in h:
            s += 2
        return s

    scored = [(h, score(h)) for h in hooks]
    scored.sort(key=lambda x: x[1], reverse=True)

    top = scored[0][1]
    best = [h for h, s in scored if s == top]

    return random.choice(best)


# =============================
# DESCRIPTION ENGINE (SEO OPTIMIZED)
# =============================
def make_description(c1, c2, scenario):
    keywords = f"{c1} vs {c2}, anime battle, what if fight, power scaling, {scenario}"

    templates = [
        f"""🔥 EPIC ANIME BATTLE

{c1} vs {c2} in a {scenario}.

This is a fan-made what-if battle exploring power levels, transformations, and ultimate abilities.

💥 COMMENT WHO WINS
⚡ SUBSCRIBE FOR MORE BATTLES

#Anime #Battle #VS #WhatIf #Shorts""",

        f"""{c1} vs {c2} — Ultimate Fight

A legendary what-if scenario where {c1} faces {c2}.

This video explores hypothetical power scaling and battle outcomes.

{keywords}

👇 Who wins this fight?"""
    ]

    desc = random.choice(templates).strip()

    if len(desc) < 250:
        desc += f"\n\n{keywords}"

    return desc[:1000]


# =============================
# STORY ENGINE
# =============================
def build_script(c1, c2, scenario):
    return [
        build_hook(c1, c2),
        f"{c1} enters the battlefield...",
        f"{c2} prepares for impact...",
        f"SCENARIO: {scenario}",
        f"{c1} awakens hidden power...",
        f"{c2} enters final form...",
        "THE FINAL CLASH SHATTERS REALITY!",
        "WHO WINS THIS FIGHT?!"
    ]


# =============================
# VIRAL SCORE SYSTEM
# =============================
def viral_score(script):
    score = 0
    if any("FINAL" in s.upper() for s in script):
        score += 2
    if any("POWER" in s.upper() for s in script):
        score += 1
    if len(script) >= 7:
        score += 1
    return score


# =============================
# MAIN GENERATOR
# =============================
def generate():
    c1, c2 = pick()
    scenario = random.choice(SCENARIOS)

    title = make_title(c1, c2, scenario)
    description = make_description(c1, c2, scenario)
    script = build_script(c1, c2, scenario)

    score = viral_score(script)

    data = {
        "title": title,
        "description": description,
        "script": script,
        "characters": [c1, c2],
        "scenario": scenario,
        "hook": script[0],
        "viral_score": score
    }

    os.makedirs(".", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("🚀 TITLE:", title)
    print("🔥 HOOK:", script[0])
    print("📊 SCORE:", score)


if __name__ == "__main__":
    print("🚀 CONTENT ENGINE RUNNING...")
    generate()
