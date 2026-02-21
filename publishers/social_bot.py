
import os
import requests
import json

class SocialMediaBot:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.platforms = ["YouTube", "TikTok", "Instagram", "Twitter", "Facebook", "WhatsApp"]

    def generate_engagement_package(self, title, script):
        """Generates platform-specific descriptions, tags, and engagement comments."""
        if not self.api_key:
            return {p: "Branded content for " + p for p in self.platforms}

        prompt = f"""
        Create a comprehensive social media engagement package for a high-stakes documentary.
        Title: {title}
        Script Snippet: {script[:500]}...

        Return a JSON object with keys for: YouTube, TikTok, Instagram, Twitter, Facebook, WhatsApp.
        For each, include:
        - A 'description' or 'caption' (optimized for that platform's culture)
        - 5 strategic 'hashtags'
        - A 'pinned_comment' or 'status_update' to drive engagement.
        """

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": { "type": "json_object" }
                }
            )
            response.raise_for_status()
            return json.loads(response.json()['choices'][0]['message']['content'])
        except Exception as e:
            print(f"Engagement generation failed: {e}")
            return None
