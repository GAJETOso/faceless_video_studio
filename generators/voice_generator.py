
import os
from gtts import gTTS

class VoiceGenerator:
    def __init__(self, lang="en"):
        self.lang = lang

    def generate_audio(self, text, output_file="output.mp3"):
        """Generates speech from text using gTTS."""
        try:
            tts = gTTS(text=text, lang=self.lang, slow=False)
            tts.save(output_file)
            return output_file
        except Exception as e:
            print(f"Error generating voice: {e}")
            return None
