import os
import random
import json

class MusicSelector:
    def __init__(self, assets_dir="assets", api_key=None, gemini_api_key=None):
        self.assets_dir = assets_dir
        self.api_key = api_key
        self.gemini_api_key = gemini_api_key
        self.music_dir = os.path.join(assets_dir, "music")
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)
            
        self.categories = {
            "mystery": ["suspense.mp3", "dark_ambient.mp3"],
            "finance": ["inspiring.mp3", "corporate.mp3"],
            "action": ["cinematic_drums.mp3", "high_energy.mp3"],
            "peaceful": ["calm_piano.mp3", "nature.mp3"],
            "rhythm": ["beat_lofi.mp3", "trap_beat.mp3", "cyberpunk_core.mp3"],
            "rnb": ["smooth_rnb.mp3", "soulful_beat.mp3"],
            "rap": ["hard_rap_beat.mp3", "boon_bap.mp3"],
            "afrobeat": ["afro_vibes.mp3", "drum_rhythm_africa.mp3"]
        }

    def analyze_script_for_music(self, script):
        """Uses AI to generate a detailed music production brief for a given script."""
        prompt = f"""Analyze the following video script and describe the IDEAL background music theme. 
        Provide:
        1. Genre & Mood.
        2. Instrumentation (e.g., Deep Bass, Acoustic Guitar).
        3. Energy Arc (how it should change over time).
        4. A 'Music Prompt' for an AI music generator (Suno/Udio).
        
        SCRIPT:
        {script}
        """
        
        # Use a simple direct LLM call or reference ScriptWriter logic
        # For simplicity in this module, we'll implement a basic fallback call
        result = self._call_llm(prompt, "You are a professional Music Supervisor for cinematic content.")
        return result or "Cinematic suspenseful theme with steady pacing."

    def _call_llm(self, prompt, system):
        import requests
        # Try OpenAI
        if self.api_key:
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"model": "gpt-4o-mini", "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
            except: pass
            
        # Try Gemini Fallback
        if self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system)
                return model.generate_content(prompt).text
            except: pass
        return None

    def select_music(self, tone):
        """Selects the best background music based on the analyzed tone."""
        mapping = {
            "onyx": "mystery", "alloy": "finance", "echo": "action", 
            "nova": "peaceful", "shimmer": "peaceful", "fable": "mystery",
            "lyrics": "rhythm", "rnb": "rnb", "rap": "rap", "afrobeat": "afrobeat"
        }
        
        category = mapping.get(tone, "mystery")
        print(f"[MUSIC ENGINE] Mapping tone '{tone}' to category '{category}'")
        
        target_dir = os.path.join(self.music_dir, category)
        if os.path.exists(target_dir):
            files = [f for f in os.listdir(target_dir) if f.endswith('.mp3')]
            if files:
                return os.path.join(target_dir, random.choice(files))
        
        global_music = os.path.join(self.music_dir, "default_background.mp3")
        return global_music if os.path.exists(global_music) else None
