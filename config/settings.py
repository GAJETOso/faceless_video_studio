import os
import json

class Config:
    # Keys that can be overridden via environment variables
    ENV_KEYS = [
        "OPENAI_API_KEY",
        "PEXELS_API_KEY",
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USER_AGENT",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "YOUTUBE_CLIENT_SECRET",
        "OUTPUT_DIR",
        "ASSETS_DIR",
    ]

    def __init__(self, config_file="config/settings.json"):
        self.config_file = config_file
        self.defaults = {
            "OPENAI_API_KEY": "",
            "PEXELS_API_KEY": "",
            "REDDIT_CLIENT_ID": "your_reddit_client_id",
            "REDDIT_CLIENT_SECRET": "your_reddit_client_secret",
            "REDDIT_USER_AGENT": "FacelessVideoBot/1.0",
            "TELEGRAM_BOT_TOKEN": "",
            "TELEGRAM_CHAT_ID": "",
            "YOUTUBE_CLIENT_SECRET": "",
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
                },
                "breaking_viral": {
                    "font": "Impact", "fontsize": 70, "color": "#FF4500", "pos": "top", "grain": False,
                    "prompt": "Breaking news script. High urgency. Short punchy lines.",
                    "aesthetic": "breaking news studio, flashing red alerts, global map background"
                },
                "motivational": {
                    "font": "Arial-Bold", "fontsize": 65, "color": "#FFFFFF", "pos": "center", "grain": False,
                    "prompt": "Inspirational motivational script. Action-driving. Emotional peaks.",
                    "aesthetic": "sunrise mountain, athlete running, golden hour light"
                },
                "music_video": {
                    "font": "Impact", "fontsize": 80, "color": "#00FF00", "pos": "center", "grain": True, 
                    "aesthetic": "neon city, fast cars, abstract glitch, rave party, strobe lights"
                }
            },
            "VOICES": {
                "onyx": {"engine": "openai", "desc": "Deep/Mystery"},
                "alloy": {"engine": "openai", "desc": "Finance/Neutral"},
                "echo": {"engine": "openai", "desc": "Viral/Energetic"},
                "shimmer": {"engine": "openai", "desc": "Peaceful/Calm"},
                "nova": {"engine": "openai", "desc": "Upbeat/Female"}
            },
            "NICHES": {
                "mystery": {"subreddits": ["UnresolvedMysteries", "InternetMysteries"], "style": "cinematic_documentary", "voice": "onyx", "structure": "cinematic"},
                "finance": {"subreddits": ["finance", "WallStreetBets", "CryptoCurrency"], "style": "finance_wealth", "voice": "alloy", "structure": "value_driven"},
                "viral": {"subreddits": ["todayIlearned", "worldnews"], "style": "breaking_viral", "voice": "echo", "structure": "cinematic"},
                "motivational": {"subreddits": ["getmotivated", "success"], "style": "motivational", "voice": "shimmer", "structure": "cinematic"}
            }
        }
        self.load()
        self._apply_env_overrides()

    def load(self):
        """Load from JSON config file, or write defaults on first run."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                try:
                    data = json.load(f)
                    for k, v in data.items():
                        setattr(self, k, v)
                except Exception:
                    pass
        # Always set keys that aren't set yet from defaults
        for k, v in self.defaults.items():
            if not hasattr(self, k):
                setattr(self, k, v)

    def _apply_env_overrides(self):
        """Railway / Docker: environment variables take highest priority."""
        for key in self.ENV_KEYS:
            env_val = os.environ.get(key)
            if env_val:
                setattr(self, key, env_val)
                print(f"[CONFIG] Loaded '{key}' from environment.")

    def save(self):
        data = {k: getattr(self, k, self.defaults[k]) for k in self.defaults.keys()}
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=4)

    def update(self, new_settings):
        for k, v in new_settings.items():
            if k in self.defaults:
                setattr(self, k, v)
        self.save()
