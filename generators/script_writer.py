
import os
import requests

class ScriptWriter:
    STYLES = {
        "cinematic_documentary": {
            "description": "Professional documentary style, high-stakes, mysterious, and tense.",
            "prompt_instructions": "Write a 90-second professional documentary script. Use short, punchy sentences. Build suspense. Start with a hook (the 'what if' or the 'moment of impact'). Tone: Explanatory but tense. Use [Action] cues for cinematic visuals."
        },
        "educational": {
            "description": "Clear, informative, and engaging.",
            "prompt_instructions": "Write a 60-second educational script. Explain complex concepts in simple terms. Use a friendly, knowledgeable tone. Include [Action] cues for diagrams or clear footage."
        },
        "motivational": {
            "description": "High-energy, fast-paced, and inspiring.",
            "prompt_instructions": "Write a 60-second motivational script. Fast-paced, high impact. Use powerful metaphors and direct calls to action. [Action] cues should focus on dynamic movement and success."
        },
        "creepy_pasta": {
            "description": "Slow, unsettling, and atmospheric horror.",
            "prompt_instructions": "Write a 90-second horror script. Slow buildup, unsettling details. Use a whispery or monotone cadence in instructions. [Action] cues for dark, grainy, or disturbing visuals."
        },
        "finance_wealth": {
            "description": "Slick, sophisticated, and focused on money, scandals, or success.",
            "prompt_instructions": "Write a 60-second high-energy financial script. Focus on power, wealth, or corporate scandals. Use sophisticated but aggressive language. [Action] cues for premium high-rise offices, luxury cars, and stock charts."
        },
        "breaking_viral": {
            "description": "Urgent, fast-paced news flash style.",
            "prompt_instructions": "Write a 45-second urgent news flash. Start with 'BREAKING' or 'ALERT'. Use high-impact, short phrases. [Action] cues for flashing lights, digital maps, and rapid news-room style movement."
        },
        "standard": {
            "description": "General viral video style.",
            "prompt_instructions": "Write a 60-second engaging script for a viral video. Keep it punchy, use short sentences. Include [Action] cues for visuals."
        }
    }

    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model

    def generate_script(self, topic, prompt=None, style="standard"):
        """Generates a video script based on a topic or source material and chosen style."""
        if not self.api_key:
            return self._mock_script(topic, style)

        # Build prompt based on style
        style_config = self.STYLES.get(style, self.STYLES["standard"])
        
        if prompt is None:
            prompt = f"{style_config['prompt_instructions']}\nTopic: {topic}"

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
            return self._mock_script(topic, style)

    def _mock_script(self, topic, style="standard"):
        """Fallback script generator."""
        if style == "cinematic_documentary":
            return f"""
            [Action: Dark screen with blinking cursor]
            In the heart of the digital age, a shadow was growing.
            
            [Action: Server rack glowing with blue lights]
            {topic}. A name whispered in the deepest corners of the web.
            
            [Action: Cinematic montage of data flowing]
            But what was hidden behind the code? And who was pulling the strings?
            
            [Action: Title card appears]
            This is the investigation.
            """
        
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
