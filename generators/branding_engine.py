
import requests

class BrandingEngine:
    def __init__(self, api_key=None, model="gpt-4o"):
        self.api_key = api_key
        self.model = model

    def generate_slogan(self, topic_or_niche):
        """Generates a high-stakes, cinematic slogan for a specific niche or video."""
        if not self.api_key:
            return "Matters of Value: Truth Unveiled."

        prompt = f"Generate a short, powerful, high-stakes cinematic slogan for a documentary series centered on: {topic_or_niche}. It should be pithy and evoke mystery, power, or deep human values. Return ONLY the slogan."

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip().replace('"', '')
        except Exception as e:
            print(f"Slogan generation failed: {e}")
            return "Matters of Value: The Core of Everything."
