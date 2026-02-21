
import requests

class TranslationEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.target_languages = {
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Portuguese": "pt",
            "Chinese": "zh"
        }

    def translate_script(self, script, target_lang_name):
        """Translates a script into a target language using GPT-4o context."""
        if not self.api_key:
            return script

        prompt = f"Translate the following documentary script into fluent, cinematic {target_lang_name}. Maintain the high-stakes tone and all [SFX] or [Action] markers. \n\nScript: {script}"

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
            print(f"Translation to {target_lang_name} failed: {e}")
            return script
