
import requests
import json

class SponsorManager:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def find_safe_spots(self, script):
        """Analyzes script to find brand-safe, retention-preserving ad insertion points."""
        if not self.api_key:
            return [
                {"position": "Early Mid-Roll", "context": "After the initial hook (approx 20% in).", "cue": "transitioning from intro to main story"},
                {"position": "Deep Mid-Roll", "context": "Before the climax (approx 60% in).", "cue": "before the big reveal"}
            ]

        prompt = f"""
        Analyze this script for optimal 'Sponsor Integration' spots.
        Find 2 natural breaks where an ad read (30-60s) would NOT kill retention.
        
        Criteria:
        1. Must be high engagement (don't put it in a boring part).
        2. Must be a "Cliffhanger Break" (e.g., "But before we find out why...").
        3. Must be Brand Safe (not immediately after a gruesome detail).
        
        Script snippet (first 3000 chars):
        {script[:3000]}...
        
        Return JSON list of objects: [{{ "position": "...", "context": "...", "cue": "..." }}]
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
            print(f"Sponsor analysis failed: {e}")
            return [{"position": "Error", "context": "Could not analyze script.", "cue": "N/A"}]
