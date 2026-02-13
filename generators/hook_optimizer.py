
import requests
import json

class HookOptimizer:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def generate_variants(self, topic, base_script):
        """Generates multiple 'Angle' variants (hooks) for the same topic to test different demographics."""
        if not self.api_key:
            return [base_script]

        prompt = f"""
        For the topic: {topic}, create 3 distinct opening 'Hooks' targeting different demographics:
        1. The 'Fear of Missing Out' Angle (Gen Z / Investors)
        2. The 'Deep Mystery' Angle (Documentary fans)
        3. The 'Controversial Truth' Angle (Viral / Debaters)

        Return a JSON object with keys: angle_fomo, angle_mystery, angle_controversy.
        Each should be a powerful 30-second opening script.
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
            print(f"Hook optimization failed: {e}")
            return {"default": base_script}
