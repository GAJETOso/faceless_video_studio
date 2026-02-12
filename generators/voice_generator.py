
import os
import re
import requests
from gtts import gTTS

class VoiceGenerator:
    # Character-based voice presets
    VOICE_PRESETS = {
        "onyx": {"engine": "openai", "desc": "Deep, authoritative, slightly raspy (Perfect for Mysteries)"},
        "alloy": {"engine": "openai", "desc": "Neutral, balanced, professional (Great for Finance)"},
        "echo": {"engine": "openai", "desc": "Energetic, clear, animated (Viral/News style)"},
        "shimmer": {"engine": "openai", "desc": "Soft, inspiring, sophisticated (Motivational)"},
        "gtts": {"engine": "gtts", "desc": "Standard automated voice"}
    }

    def __init__(self, api_key=None, lang="en"):
        self.api_key = api_key
        self.lang = lang

    def _clean_text(self, text):
        """Removes [Action] and [VISUAL] tags from the script."""
        cleaned = re.sub(r'\[.*?\]', '', text)
        cleaned = re.sub(r'(VISUAL|VOICE|AUDIO|SOUND|INT|EXT):', '', cleaned, flags=re.IGNORECASE)
        cleaned = ' '.join(cleaned.split())
        return cleaned

    def generate_audio(self, text, output_file="output.mp3", voice="onyx"):
        """Generates speech using either OpenAI (Pro) or gTTS (Standard)."""
        cleaned_text = self._clean_text(text)
        if not cleaned_text:
            return None

        # Try Professional Voice if API key exists
        if self.api_key and voice in self.VOICE_PRESETS and self.VOICE_PRESETS[voice]["engine"] == "openai":
            try:
                print(f"Generating Pro Voice ({voice})...")
                response = requests.post(
                    "https://api.openai.com/v1/audio/speech",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "tts-1",
                        "voice": voice,
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
