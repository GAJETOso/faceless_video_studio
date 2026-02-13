
import os
import requests

class ScriptWriter:
    def __init__(self, api_key=None, model="gpt-4o", config_styles=None):
        self.api_key = api_key
        self.model = model
        self.styles = config_styles or {}

    def generate_script(self, topic, style="cinematic_documentary"):
        """Generates a high-stakes script using Viral Psychology & Retention Hooks."""
        if not self.api_key:
            return f"The mystery of {topic} remains unsolved. A journey into the depths of values that matters."

        prompt = f"""
        Write a high-retention, cinematic documentary script for the topic: {topic}.
        
        Rules:
        1. CURIOSITY HOOK: Start with a high-stakes question or a 'Super Hook' that establishes legitimacy immediately.
        2. NON-OBVIOUS TAKE: Avoid the standard narrative; provide a fresh, counter-intuitive perspective.
        3. OPEN LOOPS: Raise multiple information gaps in the beginning. Close some, but keep new ones opening to maintain retention.
        4. LEVERAGE RESEARCH: Cite 'confidential reports', 'historical data', or 'newly uncovered evidence' for credibility.
        5. DOPAMINE PACING: Use short, punchy sentences.
        6. LIP-SYNC OPTIMIZED: Use clear, emotional language suitable for AI dubbing.
        
        Style: {style}
        Return ONLY the script content.
        """

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
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Script generation failed: {e}")
            return f"Error generating script for {topic}"

    def enhance_script(self, script):
        """Enhances a script with dramatic sound effect cues and visual emphasis."""
        if not self.api_key:
            return script + "\n\n[SFX: Dramatic Bass Drop]"

        prompt = f"Analyze the following documentary script and insert dramatic sound effect [SFX] cues and visual [Action] markers to make it more cinematic. Focus on high-stakes delivery. \n\nScript: {script}"

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
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Enhancement failed: {e}")
            return script
    def analyze_tone(self, script):
        """Analyzes script tone and recommends the best voice."""
        if not self.api_key:
            return "onyx"

        prompt = f"Analyze the tone of this documentary script and pick the best voice from this list: [onyx, alloy, echo, fable, nova, shimmer]. Return ONLY the name of the voice. \n\nScript: {script}"

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
            voice = response.json()['choices'][0]['message']['content'].strip().lower()
            return voice if voice in ["onyx", "alloy", "echo", "fable", "nova", "shimmer"] else "onyx"
        except Exception as e:
            print(f"Tone analysis failed: {e}")
            return "onyx"
