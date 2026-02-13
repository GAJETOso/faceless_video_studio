
import requests
import json

class SentimentTracker:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def analyze_feedback(self, comments_list):
        """Analyzes a list of viewer comments to extract strategic sentiment and suggestions."""
        if not self.api_key or not comments_list:
            return "Neutral sentiment. Maintain current production standards."

        prompt = f"""
        Analyze these viewer comments for a documentary series:
        {json.dumps(comments_list)}

        What is the overall sentiment? What specific topics or 'hooks' are viewers asking for?
        Provide a concise 'Strategic Directive' for the next script writer.
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
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Sentiment analysis failed: {e}")
            return "Unable to analyze sentiment. Continue with viral trends."
