
# Configuration for Faceless Video Studio
import os

class Config:
    # APIs
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_key")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_key")
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "your_pexels_key")
    UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "your_unsplash_key")
    YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secret.json")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "your_reddit_client_id")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "your_reddit_client_secret")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "FacelessVideoBot/1.0")

    # Paths
    ASSETS_DIR = os.path.join(os.getcwd(), "assets")
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")

    # Defaults
    DEFAULT_VOICE = "en-US-JennyNeural"  # EdgeTTS voice
    VIDEO_RESOLUTION = (1080, 1920)  # YouTube Shorts / TikTok / Reels format (vertical)
    FPS = 30
