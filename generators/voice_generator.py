
import os
import re
import requests
from gtts import gTTS

class VoiceGenerator:
    def __init__(self, api_key=None, lang="en", config_voices=None):
        self.api_key = api_key
        self.lang = lang
        self.voice_presets = config_voices or {}

    def _clean_text(self, text):
        """Removes [Action] and [VISUAL] tags from the script."""
        cleaned = re.sub(r'\[.*?\]', '', text)
        cleaned = re.sub(r'(VISUAL|VOICE|AUDIO|SOUND|INT|EXT):', '', cleaned, flags=re.IGNORECASE)
        cleaned = ' '.join(cleaned.split())
        return cleaned

    def generate_audio(self, text, output_file="output.mp3", voice="onyx"):
        """Generates speech using configured voice settings."""
        cleaned_text = self._clean_text(text)
        if not cleaned_text:
            return None

        preset = self.voice_presets.get(voice, next(iter(self.voice_presets.values()), {"engine": "gtts"}))
        engine = preset.get("engine", "gtts")

        if self.api_key and engine == "openai":
            try:
                print(f"Generating Pro Voice ({voice})...")
                response = requests.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "tts-1",
                        "voice": voice if voice in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"] else "onyx",
                        "input": cleaned_text
                    }
                )
                response.raise_for_status()
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                return output_file
            except Exception as e:
                print(f"Pro Voice failed, falling back to gTTS: {e}")

        # Fallback to gTTS
        try:
            print("Generating Standard Voice (gTTS)...")
            tts = gTTS(text=cleaned_text, lang=self.lang, slow=False)
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"Error generating voice: {e}")
            return None
