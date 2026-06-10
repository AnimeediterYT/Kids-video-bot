import json
import random
import os

OUTPUT_FILE = "current_matchup.json"


# =============================
# CHARACTER UNIVERSE (EXPANDABLE)
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


HOOKS = [
    "WHO WINS THIS?!",
    "THIS IS INSANE!",
    "YOU WON’T EXPECT THIS!",
    "REALITY IS BREAKING!",
    "STRONGEST FIGHT EVER!"
]


ACTIONS = [
    "awakens god power",
    "breaks all limits",
    "enters final form",
    "loses control of energy",
    "reaches ultimate evolution"
]


CLIMAX = [
    "THE FINAL CLASH SHATTERS REALITY!",
    "ONLY ONE SURVIVES THIS BATTLE!",
    "POWER LEVELS REACH BEYOND LIMITS!",
    "THE UNIVERSE STARTS COLLAPSING!",
    "VICTORY DECIDED IN ONE MOMENT!"
]


# =============================
# TITLE ENGINE (INFINITE STYLE)
# =============================
def make_title(c1, c2, scenario):
    styles = [
        f"{c1} vs {c2} - {scenario}",
        f"🔥 {c1} vs {c2} | {scenario}",
        f"{c1} ⚡ VS ⚡ {c2} - Ultimate Battle",
        f"WHO IS STRONGER? {c1} or {c2}?",
        f"{c1} vs {c2} - No Limits Fight"
    ]
    return random.choice(styles)


# =============================
# DESCRIPTION ENGINE (150+ CHAR SAFE)
# =============================
def make_description(c1, c2, scenario):
    templates = [
        f"Watch the ultimate battle between {c1} and {c2} in {scenario}. "
        f"This is a fan-made concept fight exploring power levels, abilities, and what-if scenarios. "
        f"Who will dominate this clash of legends?",

        f"{c1} vs {c2} in an insane {scenario}. "
        f"This short explores a hypothetical fight between two powerful characters. "
        f"Experience the intensity and decide the winner yourself!"
    ]

    desc = random.choice(templates)

    # guarantee 150+ chars (safe YouTube style)
    while len(desc) < 150:
        desc += " Watch till the end to see the result!"

    return desc[:500]  # safe limit


# =============================
# STORY ENGINE
# =============================
def build_script(c1, c2, scenario):
    return [
        random.choice(HOOKS),
        f"{c1} enters the battlefield...",
        f"{c2} prepares for impact...",
        f"SCENARIO: {scenario}",
        f"{c1} {random.choice(ACTIONS)}",
        f"{c2} {random.choice(ACTIONS)}",
        random.choice(CLIMAX),
        "WHO WINS THIS FIGHT?!"
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
# MAIN GENERATOR
# =============================
def generate():
    c1, c2 = pick()
    scenario = random.choice(SCENARIOS)

    title = make_title(c1, c2, scenario)
    description = make_description(c1, c2, scenario)
    script = build_script(c1, c2, scenario)

    data = {
        "title": title,
        "description": description,
        "script": script
    }

    os.makedirs(".", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ GENERATED TITLE:", title)
    print("📝 DESCRIPTION LENGTH:", len(description))


# =============================
# RUN
# =============================
if __name__ == "__main__":
    print("🚀 CONTENT ENGINE RUNNING...")
    generate()
