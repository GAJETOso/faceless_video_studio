import os
import re
import requests
import asyncio
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

    async def _generate_edge_tts(self, text, output_file, voice):
        """Uses edge-tts for high-quality free voice synthesis."""
        import edge_tts
        # Map some common keywords to edge-tts voices
        voice_map = {
            "onyx": "en-US-GuyNeural",
            "alloy": "en-US-ChristopherNeural",
            "echo": "en-US-EricNeural",
            "shimmer": "en-GB-SoniaNeural",
            "nova": "en-US-JennyNeural"
        }
        edge_voice = voice_map.get(voice, "en-US-ChristopherNeural")
        communicate = edge_tts.Communicate(text, edge_voice)
        await communicate.save(output_file)

    def generate_audio(self, text, output_file="output.mp3", voice="onyx"):
        """Generates speech using configured voice settings."""
        cleaned_text = self._clean_text(text)
        if not cleaned_text:
            return None

        # 1. Try OpenAI Pro Voice if key exists
        preset = self.voice_presets.get(voice, {"engine": "openai"})
        engine = preset.get("engine", "openai")

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
                print(f"Pro Voice failed, falling back to High-Quality Free Voice: {e}")

        # 2. High-Quality Free Fallback (Edge-TTS)
        try:
            print(f"Generating High-Quality Free Voice (Edge-TTS)...")
            asyncio.run(self._generate_edge_tts(cleaned_text, output_file, voice))
            return output_file
        except Exception as e:
            print(f"Edge-TTS failed, falling back to gTTS: {e}")

        # 3. Last Resort Fallback (gTTS)
        try:
            print("Generating Standard Voice (gTTS)...")
            tts = gTTS(text=cleaned_text, lang=self.lang, slow=False)
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"Error generating voice: {e}")
            return None
