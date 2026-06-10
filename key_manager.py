import os
import json

class KeyManager:
    """
    Central system for managing all API keys safely.
    Prevents missing-key crashes and enables auto fallback modes.
    """

    def __init__(self):
        self.keys = {
            "YOUTUBE_CLIENT_SECRETS": os.environ.get("YOUTUBE_CLIENT_SECRETS"),
            "YOUTUBE_REFRESH_TOKEN": os.environ.get("YOUTUBE_REFRESH_TOKEN"),
            "OPENAI_KEY": os.environ.get("PRIMARY_AI_API_KEY"),
            "RUNWAY_KEY": os.environ.get("RUNWAY_API_KEY")
        }

    def is_available(self, key_name):
        return self.keys.get(key_name) is not None

    def youtube_ready(self):
        return self.is_available("YOUTUBE_CLIENT_SECRETS") and self.is_available("YOUTUBE_REFRESH_TOKEN")

    def ai_ready(self):
        return self.is_available("OPENAI_KEY")

    def runway_ready(self):
        return self.is_available("RUNWAY_KEY")

    def system_mode(self):
        """
        Returns current safe operating mode:
        FULL_AI / HYBRID / OFFLINE
        """
        if self.ai_ready() and self.youtube_ready():
            return "FULL_AI"
        elif self.youtube_ready():
            return "HYBRID"
        else:
            return "OFFLINE"

    def debug_report(self):
        print("🔐 KEY STATUS REPORT:")
        for k, v in self.keys.items():
            print(f"- {k}: {'OK' if v else 'MISSING'}")

        print("⚙️ SYSTEM MODE:", self.system_mode())
