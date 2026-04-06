
import os
import requests
import random
from sources.youtube_trends import YouTubeTrends

class NewsIntegrator:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # High-stakes news categories
        self.categories = ["finance", "technology", "geopolitics", "mystery", "motivational"]
        self.yt_engine = YouTubeTrends(api_key=api_key)

    def fetch_trending_topics(self):
        """Fetches breaking news opportunities, merging AI mocks and real YouTube research."""
        base_topics = [
            {"title": "The Silicon Shield: Taiwan's Semiconductor Monopoly", "niche": "Technology", "urgency": "High"},
            {"title": "The Petrodollar Pivot: A New World Order?", "niche": "Geopolitics", "urgency": "Breaking"},
            {"title": "Quantum Supremacy: The End of Encryption", "niche": "Mystery", "urgency": "Trending"},
            {"title": "The Lithium Rush: Mining the Andes", "niche": "Finance", "urgency": "Global"}
        ]
        
        # Inject real YouTube motivational research
        yt_topics = self.yt_engine.fetch_trending_motivation()
        
        # Merge and shuffle
        combined = base_topics + yt_topics
        random.shuffle(combined)
        
        return combined[:6] # Return top 6 high-stakes opportunities
