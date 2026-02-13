
import requests
import json

class RepurposingEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def identify_viral_shorts(self, script):
        """Identifies the top 3 'Viral Hooks' in a script suitable for vertical Shorts/Reels."""
        if not self.api_key:
            return [
                {"title": "The Hook", "segment": "00:00 - 00:45", "reason": "High curiosity opening."},
                {"title": "The Shock", "segment": "03:20 - 04:00", "reason": "Emotional peak of the story."},
                {"title": "The Twist", "segment": "08:15 - 08:50", "reason": "Unexpected conclusion."}
            ]

        prompt = f"""
        Analyze this documentary script and identify 3 segments that would go viral as standalone TikToks/Reels (Vertical Format).
        
        Criteria:
        1. Standalone Value: Must make sense without the rest of the video.
        2. High Energy/Shock: Must happen quickly.
        3. < 60 Seconds estimated duration.
        
        Script snippet (first 4000 chars):
        {script[:4000]}...
        
        Return JSON list: [{{ "title": "...", "segment": "approx timestamps or text cue", "reason": "..." }}]
        """

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        except Exception as e:
            print(f"Repurposing sizing failed: {e}")
            return []
