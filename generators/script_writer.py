import os
import requests
import google.generativeai as genai

class ScriptWriter:
    def __init__(self, api_key=None, gemini_api_key=None, model="gpt-4o", config_styles=None):
        self.api_key = api_key
        self.gemini_api_key = gemini_api_key
        self.model = model
        self.styles = config_styles or {}
        
        # Configure Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def _call_llm(self, prompt, system_instruction="You are a professional video scriptwriter for 'Matters of Value'.", max_tokens=1000):
        """Unified LLM caller with OpenAI -> Gemini fallback."""
        
        # 1. Try OpenAI
        if self.api_key:
            try:
                print(f"[LLM] Attempting OpenAI ({self.model})...")
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": max_tokens
                    },
                    timeout=60
                )
                if response.status_code == 429:
                    print("[LLM] OpenAI Quota Exceeded (429). Falling back...")
                else:
                    response.raise_for_status()
                    return response.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"[LLM] OpenAI Error: {e}")
        
        # 2. Try Gemini Fallback
        if self.gemini_api_key:
            try:
                print("[LLM] Attempting Gemini Fallback...")
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=0.7
                    )
                )
                return response.text
            except Exception as e:
                print(f"[LLM] Gemini Fallback Error: {e}")
        
        return None

    def generate_script(self, topic, style="cinematic_documentary", structure="cinematic"):
        """Generates a high-stakes script using Viral Psychology & Retention Hooks."""
        if not self.api_key and not self.gemini_api_key:
            return f"The mystery of {topic} remains unsolved. A journey into the depths of values that matters."

        if structure == "value_driven":
            prompt = f"Write a high-retention, educational video script for the topic: {topic}. Style: {style}. Follow HOOK, TRANSITION, MEAT (Rule of 3), and CTA."
            system = "You are an expert YouTube scriptwriter. Return ONLY the script content with [Visual] cues."
        else:
            prompt = f"Write a high-retention, cinematic documentary script for the topic: {topic}. Style: {style}. Use CURIOSITY HOOK, NON-OBVIOUS TAKE, and OPEN LOOPS."
            system = "You are a professional documentary scriptwriter. Focus on high-stakes delivery and non-obvious takes. Return ONLY the script content."

        result = self._call_llm(prompt, system_instruction=system)
        return result or f"Error generating script for {topic}"

    def generate_from_concept(self, title, concept, style="cinematic_documentary", duration_minutes=2):
        """Generates a fully polished, production-ready script from a creative brief/concept."""
        word_count = duration_minutes * 130
        prompt = f"""Write a COMPLETE, production-ready video script:
        TITLE: {title}
        DURATION: {duration_minutes}m (~{word_count} words)
        STYLE: {style}
        CONCEPT: {concept}
        Include [VISUAL] cues and [PAUSE] markers. End with a contextual CTA."""
        
        system = "You are an expert YouTube scriptwriter for 'Matters of Value'. Write ONLY the spoken script text."
        
        result = self._call_llm(prompt, system_instruction=system, max_tokens=word_count * 2)
        if result:
            return result
        
        if not self.api_key and not self.gemini_api_key:
            return f"[INTRO]\nWelcome to Matters of Value. Today we talk about: {title}.\n\n[MAIN CONTENT]\n{concept}\n\n[OUTRO]\nSubscribe for more high-value content."
        
        return "Error: Both OpenAI and Gemini generation failed. Please check your API keys."

    def enhance_script(self, script):
        """Enhances a script with dramatic sound effect cues and visual emphasis."""
        prompt = f"Analyze the following documentary script and insert dramatic sound effect [SFX] cues and visual [Action] markers. \n\nScript: {script}"
        system = "You are a cinematic editor. Enhance the script's drama and pacing. Return ONLY the enhanced script."
        
        result = self._call_llm(prompt, system_instruction=system, max_tokens=len(script.split()) * 2)
        return result or script

    def analyze_tone(self, script):
        """Analyzes script tone and recommends the best voice."""
        prompt = f"Analyze script tone and pick best voice: [onyx, alloy, echo, fable, nova, shimmer]. Return ONLY the name. \n\nScript: {script}"
        system = "Pick the best voice from the list based on the script's emotional weight. Return only the single word name."
        
        result = self._call_llm(prompt, system_instruction=system, max_tokens=10)
        if result:
            voice = result.strip().lower()
            return voice if voice in ["onyx", "alloy", "echo", "fable", "nova", "shimmer"] else "onyx"
        return "onyx"

    def generate_lyrics(self, topic, genre="hip-hop"):
        """Generates rhyming lyrics based on a topic for a music video."""
        prompt = f"Write rhyming {genre} lyrics for a music video about: {topic}. Include [VERSE], [CHORUS], and [OUTRO]."
        system = "You are a viral music composer. Write high-energy rhyming lyrics for a faceless channel. Return ONLY the lyrics."
        
        result = self._call_llm(prompt, system_instruction=system)
        return result or f"Error generating lyrics for {topic}"
