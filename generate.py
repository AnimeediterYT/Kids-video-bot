import json
import random
import os

OUTPUT_FILE = "current_matchup.json"


# -----------------------------
# CHARACTER DATABASE (expanded + safer pool)
# -----------------------------
CHARACTERS = {
    "Dragon Ball": [
        "Goku", "Vegeta", "Gohan", "Trunks", "Piccolo", "Frieza",
        "Cell", "Broly", "Beerus", "Whis", "Jiren", "Gogeta", "Vegito"
    ],
    "Naruto": [
        "Naruto", "Sasuke", "Itachi", "Madara", "Obito",
        "Kakashi", "Minato", "Pain", "Jiraiya"
    ],
    "One Piece": [
        "Luffy", "Zoro", "Sanji", "Shanks", "Kaido",
        "Blackbeard", "Law", "Ace", "Big Mom"
    ],
    "Bleach": [
        "Ichigo", "Aizen", "Byakuya", "Kenpachi", "Yhwach", "Ulquiorra"
    ],
    "Jujutsu Kaisen": [
        "Gojo", "Sukuna", "Yuji", "Megumi", "Toji", "Geto"
    ],
    "Attack on Titan": [
        "Eren", "Levi", "Mikasa", "Reiner", "Zeke"
    ],
    "My Hero Academia": [
        "Deku", "Bakugo", "Todoroki", "Shigaraki", "All Might"
    ],
    "Hunter x Hunter": [
        "Gon", "Killua", "Hisoka", "Chrollo", "Meruem"
    ],
    "Demon Slayer": [
        "Tanjiro", "Nezuko", "Zenitsu", "Inosuke", "Muzan"
    ]
}


# -----------------------------
# VIRAL SCENARIOS (expanded + retention focused)
# -----------------------------
SCENARIOS = [
    "WHAT IF BATTLE",
    "TRAPPED IN A DEADLY DIMENSION",
    "EVIL VERSION AWAKENING",
    "TIME LOOP FIGHT",
    "ISSEKAI TRANSPORT",
    "FUSED POWER EXPLOSION",
    "FINAL GOD FORM UNLOCK",
    "BROKEN REALITY COLLISION",
    "NO RULES DEATH MATCH",
    "HIDDEN POWER REVEALED"
]


# -----------------------------
# VIRAL HOOK ENGINE (stronger YouTube Shorts hooks)
# -----------------------------
HOOKS = [
    "WHO WINS THIS?! 😱",
    "YOU WON'T BELIEVE THIS FIGHT!",
    "REALITY IS BREAKING APART!",
    "THIS IS THE STRONGEST BATTLE!",
    "ONLY 1 SURVIVES THIS..."
]


# -----------------------------
# ACTION ENGINE (dynamic storytelling)
# -----------------------------
ACTIONS = [
    "awakens hidden power",
    "breaks all limits",
    "enters god mode",
    "loses control of power",
    "reaches final evolution"
]


# -----------------------------
# CLIMAX ENGINE (retention booster)
# -----------------------------
CLIMAX = [
    "THE FINAL CLASH EXPLODES!",
    "REALITY COLLAPSES!",
    "ONLY ONE REMAINS STANDING!",
    "POWER REACHES MAXIMUM!",
    "THE END BEGINS!"
]


# -----------------------------
# FLATTEN CHARACTER POOL
# -----------------------------
def get_pool():
    return [c for group in CHARACTERS.values() for c in group]


# -----------------------------
# STORY BUILDER (core upgrade)
# -----------------------------
def build_story(c1, c2):
    scenario = random.choice(SCENARIOS)

    script = [
        random.choice(HOOKS),
        f"SCENARIO: {scenario}",
        f"{c1} {random.choice(ACTIONS)}...",
        f"{c2} {random.choice(ACTIONS)}...",
        random.choice(CLIMAX),
        "WHO WILL WIN THIS FIGHT?!"
    ]

    title = f"{c1} vs {c2} - {scenario}"

    return title, script


# -----------------------------
# MAIN GENERATOR (FAILSAFE + VIRAL)
# -----------------------------
def generate():
    try:
        pool = get_pool()

        c1 = random.choice(pool)
        c2 = random.choice([c for c in pool if c != c1])

        title, script = build_story(c1, c2)

        data = {
            "title": title,
            "script": script
        }

    except Exception as e:
        # HARD FALLBACK (NEVER BREAK PIPELINE)
        print("⚠️ Generator fallback triggered:", e)

        data = {
            "title": "Goku vs Naruto - WHAT IF BATTLE",
            "script": [
                "WHO WINS THIS?! 😱",
                "Battle begins...",
                "Power explodes...",
                "FINAL CLASH!",
                "WHO WILL WIN?!"
            ]
        }

    os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ Generated:", data["title"])


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    print("🎲 VIRAL SHORTS ENGINE RUNNING...")
    generate()
