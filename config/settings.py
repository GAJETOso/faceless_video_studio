
import os
import json

class Config:
    def __init__(self, config_file="config/settings.json"):
        self.config_file = config_file
        self.defaults = {
            "OPENAI_API_KEY": "your_openai_key",
            "PEXELS_API_KEY": "your_pexels_key",
            "REDDIT_CLIENT_ID": "your_reddit_client_id",
            "REDDIT_CLIENT_SECRET": "your_reddit_client_secret",
            "REDDIT_USER_AGENT": "FacelessVideoBot/1.0",
            "ASSETS_DIR": "assets",
            "OUTPUT_DIR": "output",
            "STOCK_DIR": "assets/stock",
            "DOC_TITLE_TEMPLATE": "VALUES THAT MATTERS: {title}",
            "CHAPTER_LENGTH_MINUTES": 5,
            "STYLES": {
                "cinematic_documentary": {
                    "font": "Courier-Bold", "fontsize": 60, "color": "white", "pos": "bottom", "grain": True, "vignette": True,
                    "prompt": "Write a 90-second professional documentary script. Short sentences. High suspense.",
                    "aesthetic": "cinematic moody lighting, tech server, mysterious dark technology"
                },
                "finance_wealth": {
                    "font": "Georgia-Bold", "fontsize": 75, "color": "#FFD700", "pos": "top", "vignette": True,
                    "prompt": "Professional finance script. Sophisticated and wealth-focused.",
                    "aesthetic": "luxury office, stock market charts, gold bars, city skyline"
                }
            },
            "VOICES": {
                "onyx": {"engine": "openai", "desc": "Deep/Mystery"},
                "alloy": {"engine": "openai", "desc": "Finance/Neutral"},
                "echo": {"engine": "openai", "desc": "Viral/Energetic"}
            },
            "NICHES": {
                "mystery": {"subreddits": ["UnresolvedMysteries"], "style": "cinematic_documentary", "voice": "onyx", "structure": "cinematic"},
                "finance": {"subreddits": ["finance", "WallStreetBets"], "style": "finance_wealth", "voice": "alloy", "structure": "value_driven"}
            }
        }
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    setattr(self, k, v)
        else:
            for k, v in self.defaults.items():
                setattr(self, k, v)
            self.save()

    def save(self):
        data = {k: getattr(self, k) for k in self.defaults.keys()}
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=4)

    def update(self, new_settings):
        for k, v in new_settings.items():
            if k in self.defaults:
                setattr(self, k, v)
        self.save()
