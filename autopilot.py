import json
import random

# ----------------------------
# VIRAL CHARACTER POOL
# ----------------------------
CHARACTERS = [
    "Goku", "Naruto", "Sasuke", "Ichigo", "Gojo",
    "Sukuna", "Luffy", "Zoro", "Madara", "Itachi",
    "Kokushibo", "Tanjiro", "Aizen", "Killua", "Saitama"
]

# ----------------------------
# VIRAL SCENARIOS
# ----------------------------
SCENARIOS = [
    "vs battle begins",
    "awakens hidden power",
    "gets transported to another world",
    "final form transformation",
    "betrayal twist happens",
    "god mode unlocked"
]

# ----------------------------
# HOOK LINES (FIRST 2 SECONDS IMPACT)
# ----------------------------
HOOKS = [
    "THIS IS INSANE 🔥",
    "WHO WINS THIS?! 😱",
    "YOU WON’T EXPECT THIS!",
    "STRONGEST FIGHT EVER!",
    "FINAL BATTLE BEGINS!"
]

# ----------------------------
# SCRIPT BUILDER
# ----------------------------
def generate_script(c1, c2):
    return [
        random.choice(HOOKS),
        f"{c1} enters the battlefield...",
        f"{c2} prepares for impact!",
        random.choice(SCENARIOS),
        "THE CLASH STARTS NOW!",
        "WHO WILL WIN?"
    ]

# ----------------------------
# GENERATE MATCHUP
# ----------------------------
def generate():
    c1 = random.choice(CHARACTERS)
    c2 = random.choice(CHARACTERS)

    while c2 == c1:
        c2 = random.choice(CHARACTERS)

    title = f"{c1} vs {c2} - Viral Battle"

    data = {
        "title": title,
        "script": generate_script(c1, c2)
    }

    return data

# ----------------------------
# SAVE TO SYSTEM FILE
# ----------------------------
def run():
    data = generate()

    with open("current_matchup.json", "w") as f:
        json.dump(data, f, indent=4)

    print("🤖 AUTOPILOT GENERATED CONTENT")
    print("TITLE:", data["title"])
    print("SCRIPT:")
    for line in data["script"]:
        print("-", line)

# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    run()
