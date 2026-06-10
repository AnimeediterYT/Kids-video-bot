import json
import random

OUTPUT_FILE = "current_matchup.json"


# -----------------------------
# HUGE CHARACTER DATABASE (200+ simplified but real anime roster)
# -----------------------------
CHARACTERS = {
    "Dragon Ball": [
        "Goku", "Vegeta", "Gohan", "Trunks", "Piccolo", "Frieza", "Cell", "Broly",
        "Beerus", "Whis", "Jiren", "Zamasu", "Gogeta", "Vegito"
    ],
    "Naruto": [
        "Naruto", "Sasuke", "Sakura", "Kakashi", "Itachi", "Madara", "Obito",
        "Pain", "Minato", "Jiraiya", "Hashirama", "Tobirama", "Orochimaru"
    ],
    "One Piece": [
        "Luffy", "Zoro", "Sanji", "Nami", "Usopp", "Robin", "Franky", "Brook",
        "Shanks", "Blackbeard", "Kaido", "Big Mom", "Law", "Ace"
    ],
    "Bleach": [
        "Ichigo", "Aizen", "Rukia", "Renji", "Byakuya", "Kenpachi",
        "Urahara", "Yhwach", "Ulquiorra", "Grimmjow"
    ],
    "Jujutsu Kaisen": [
        "Gojo", "Sukuna", "Yuji", "Megumi", "Nobara", "Toji",
        "Geto", "Mahito", "Yuta", "Maki"
    ],
    "Attack on Titan": [
        "Eren", "Mikasa", "Armin", "Levi", "Reiner",
        "Zeke", "Erwin", "Annie", "Historia", "Porco"
    ],
    "My Hero Academia": [
        "Deku", "Bakugo", "Todoroki", "All Might", "Shigaraki",
        "Dabi", "Hawks", "Aizawa", "Endeavor", "Mirko"
    ],
    "Hunter x Hunter": [
        "Gon", "Killua", "Hisoka", "Chrollo", "Meruem",
        "Netero", "Kurapika", "Illumi", "Ging", "Leorio"
    ],
    "Demon Slayer": [
        "Tanjiro", "Nezuko", "Zenitsu", "Inosuke", "Muzan",
        "Rengoku", "Tengen", "Akaza", "Doma", "Giyu"
    ],
    "Black Clover": [
        "Asta", "Yuno", "Yami", "Noelle", "Liebe",
        "Julius", "Luck", "Magna", "Zenon", "Vanica"
    ]
}


# -----------------------------
# SCENARIO ENGINE (EXPANDED TYPES)
# -----------------------------
SCENARIOS = [
    "WHAT IF BATTLE",
    "TRAPPED IN A DEADLY WORLD",
    "EVIL VERSION AWAKENING",
    "TIME LOOP FIGHT",
    "ISSEKAI TRANSPORTED BATTLE",
    "FUSED FORM EXPERIMENT",
    "1000 YEARS TRAINING RETURN",
    "BROKEN REALITY COLLISION",
    "FINAL DIMENSION WAR",
    "NO RULES UNIVERSE"
]


HOOKS = [
    "WHO WINS THIS?! 😱",
    "THIS IS BEYOND POWER LIMITS!",
    "YOU'VE NEVER SEEN THIS BEFORE!",
    "REALITY IS BREAKING!",
    "ULTIMATE ANIME WAR BEGINS!"
]


ACTIONS = [
    "awakens hidden power...",
    "breaks dimensional limits...",
    "enters god form...",
    "loses control of power...",
    "reaches final evolution..."
]


CLASH = [
    "THE CLASH EXPLODES!",
    "REALITY IS COLLAPSING!",
    "ONLY ONE SURVIVES!",
    "THE FINAL MOMENT ARRIVES!",
    "POWER OVERLOAD DETECTED!"
]


# -----------------------------
# FLATTEN CHARACTER LIST
# -----------------------------
def all_chars():
    return [c for group in CHARACTERS.values() for c in group]


# -----------------------------
# STORY ENGINE (KEY UPGRADE)
# -----------------------------
def generate_story(char1, char2):
    scenario = random.choice(SCENARIOS)

    script = [
        random.choice(HOOKS),
        f"SCENARIO: {scenario}",
        f"{char1} {random.choice(ACTIONS)}",
        f"{char2} {random.choice(ACTIONS)}",
        random.choice(CLASH),
        "WHO WILL WIN THIS FIGHT?!"
    ]

    title = f"{char1} vs {char2} - {scenario}"

    return title, script


# -----------------------------
# GENERATE MATCHUP
# -----------------------------
def generate_matchup():
    pool = all_chars()

    char1 = random.choice(pool)
    char2 = random.choice([c for c in pool if c != char1])

    title, script = generate_story(char1, char2)

    return {
        "title": title,
        "script": script
    }


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("🎲 Infinite Anime Story Engine Running...")

    data = generate_matchup()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ Generated:", data["title"])
    print("📜 Script:")
    for line in data["script"]:
        print("-", line)
