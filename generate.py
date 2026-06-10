import json
import random
import os

OUTPUT_FILE = "current_matchup.json"


# -----------------------------
# CHARACTER DATABASE
# -----------------------------
CHARACTERS = {
    "Dragon Ball": [
        "Goku", "Vegeta", "Gohan", "Trunks", "Piccolo", "Frieza",
        "Broly", "Beerus", "Whis", "Jiren", "Gogeta", "Vegito"
    ],
    "Naruto": [
        "Naruto", "Sasuke", "Itachi", "Madara", "Obito",
        "Kakashi", "Minato", "Pain", "Jiraiya"
    ],
    "One Piece": [
        "Luffy", "Zoro", "Sanji", "Shanks", "Kaido",
        "Blackbeard", "Law", "Ace"
    ],
    "Bleach": [
        "Ichigo", "Aizen", "Byakuya", "Kenpachi", "Yhwach"
    ],
    "Jujutsu Kaisen": [
        "Gojo", "Sukuna", "Yuji", "Megumi", "Toji"
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
# VIRAL SYSTEMS (EXPANDED ENGINE)
# -----------------------------
HOOKS = [
    "WHO WINS THIS?! 😱",
    "YOU WON'T BELIEVE THIS!",
    "REALITY IS BREAKING!",
    "THIS FIGHT IS ILLEGAL!",
    "ONLY ONE SURVIVES..."
]

SCENARIOS = [
    "WHAT IF BATTLE",
    "TRAPPED IN A DEAD DIMENSION",
    "EVIL VERSION AWAKENS",
    "TIME LOOP WAR",
    "ISSEKAI TRANSPORT",
    "FUSED POWER COLLISION",
    "FINAL GOD AWAKENING",
    "BROKEN REALITY EVENT"
]

ACTIONS = [
    "awakens hidden power",
    "breaks all limits",
    "enters god mode",
    "loses control of power",
    "reaches final evolution",
    "unlocks forbidden form"
]

CLIMAX = [
    "THE FINAL CLASH EXPLODES!",
    "REALITY COLLAPSES!",
    "ONLY ONE REMAINS!",
    "POWER REACHES MAXIMUM!",
    "THE END BEGINS!"
]


# -----------------------------
# FLATTEN POOL
# -----------------------------
def pool():
    return [c for g in CHARACTERS.values() for c in g]


# -----------------------------
# SMART CHARACTER PICKER
# (prevents same-franchise boring fights)
# -----------------------------
def smart_pick(p):
    c1 = random.choice(p)

    # try to pick from different franchise
    filtered = [c for c in p if c != c1]
    c2 = random.choice(filtered) if filtered else c1

    return c1, c2


# -----------------------------
# STORY ENGINE (INFINITE VARIATION)
# -----------------------------
def story(c1, c2):
    scenario = random.choice(SCENARIOS)

    # dynamic intensity variation
    intensity = random.randint(1, 3)

    script = [
        random.choice(HOOKS),
        f"SCENARIO: {scenario}",
        f"{c1} {random.choice(ACTIONS)}..." * intensity,
        f"{c2} {random.choice(ACTIONS)}..." * intensity,
        random.choice(CLIMAX),
        "WHO WILL WIN?!"
    ]

    title = f"{c1} vs {c2} - {scenario}"

    return title, script


# -----------------------------
# MAIN GENERATOR (FAILSAFE)
# -----------------------------
def generate():
    try:
        p = pool()
        c1, c2 = smart_pick(p)

        title, script = story(c1, c2)

        data = {
            "title": title,
            "script": script
        }

    except Exception as e:
        print("⚠️ Fallback triggered:", e)

        data = {
            "title": "Goku vs Naruto - WHAT IF",
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
    print("🎲 STEP 2 VIRAL ENGINE ACTIVE")
    generate()
