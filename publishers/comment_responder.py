
import requests

class CommentResponder:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def draft_response(self, topic, script, viewer_comment):
        """Generates a high-engagement response that maintains the 'Non-Obvious Take'."""
        if not self.api_key:
            return "Thank you for watching! Stay tuned for more."

        prompt = f"""
        A viewer commented on our documentary about: {topic}.
        Our Original Script (Context): {script[:1000]}
        
        Viewer Comment: "{viewer_comment}"
        
        Task: Draft a response that:
        1. Maintains our professional, high-stakes 'Matters of Value' brand voice.
        2. Uses our 'Non-Obvious Take' from the script to engage or debate respectfully.
        3. Opens a new loop or asks a question to drive further comments.
        
        Return ONLY the response text.
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
            print(f"Comment response failed: {e}")
            return "Perspective is everything. What's yours?"
