
import os
import requests

class ScriptWriter:
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model

    def generate_script(self, topic, prompt=None):
        """Generates a video script based on a topic or source material."""
        if not self.api_key:
            return self._mock_script(topic)

        # Basic prompt template
        if prompt is None:
            prompt = f"Write a 60-second engaging script for a viral video about: {topic}. Keep it punchy, use short sentences. Include [Action] cues for visuals."

        try:
            # Assuming OpenAI-compatible endpoint
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error generating script via API: {e}")
            return self._mock_script(topic)

    def _mock_script(self, topic):
        """Fallback script generator."""
        return f"""
        (Intro)
        Did you know about {topic}? It's absolutely mind-blowing!
        
        (Body)
        Here are three crazy facts.
        Number one: It changes everything you thought you knew.
        Number two: The details are insane.
        Number three: You won't believe how it works.
        
        (Outro)
        Follow for more amazing facts!
        """
