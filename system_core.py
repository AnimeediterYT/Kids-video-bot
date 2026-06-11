import json
import os
from system_core import load_state, save_state, update_memory


# =============================
# LOAD UPLOADED DATA
# =============================
def get_uploaded_videos():
    state = load_state()
    return state.get("uploaded_videos", [])


# =============================
# SIMPLE PERFORMANCE SIMULATOR
# (replace later with YouTube API stats)
# =============================
def estimate_performance(video):
    score = 0

    title = video.get("title", "")
    signal = video.get("signal", "")

    if "🔥" in title:
        score += 2
    if "VS" in title.upper() or "vs" in title.lower():
        score += 2
    if signal == "STRONG_WINNERS":
        score += 3

    # fake randomness to simulate real world variance
    import random
    score += random.randint(0, 2)

    return score


# =============================
# ANALYSIS ENGINE
# =============================
def analyze():
    videos = get_uploaded_videos()

    if not videos:
        print("⚠️ No videos to analyze")
        return

    results = []

    for v in videos:
        score = estimate_performance(v)

        results.append({
            "video_id": v.get("video_id"),
            "title": v.get("title"),
            "score": score
        })

    # sort best to worst
    results.sort(key=lambda x: x["score"], reverse=True)

    best = results[:3]
    worst = results[-3:]

    # =============================
    # FEEDBACK LOOP INTO MEMORY
    # =============================
    update_memory("best_performing_videos", best)
    update_memory("worst_performing_videos", worst)

    # extract patterns
    for b in best:
        update_memory("winning_titles", b["title"])

    for w in worst:
        update_memory("avoid_titles", w["title"])

    print("📊 ANALYTICS COMPLETE")
    print("🏆 BEST:", best)
    print("⚠️ WORST:", worst)


# =============================
# RUN
# =============================
if __name__ == "__main__":
    print("🧠 ANALYTICS BRAIN RUNNING...")
    analyze()
