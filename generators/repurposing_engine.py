import os
import re
import json
import google.generativeai as genai

class RepurposingEngine:
    def __init__(self, api_key=None, gemini_api_key=None):
        self.api_key = api_key
        self.gemini_api_key = gemini_api_key
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def identify_viral_shorts(self, script):
        """
        Analyzes a long-form script to identify 15-60 second segments 
        perfect for Shorts/Reels/TikToks.
        """
        print("[REPURPOSING] Analyzing script for viral micro-moments...")
        
        if self.api_key or self.gemini_api_key:
            results = self._ai_identify_shorts(script)
            if results: return results
        
        # Enhanced heuristic fallback (Final layer)
        segments = []
        paragraphs = script.split('\n\n')
        viral_markers = ['secret', 'finally', 'uncovered', 'amazing', 'never', 'shocking', 'truth', 'stop', 'warning', 'exposed', 'hack', 'illegal', 'mystery', 'expensive', 'rich', 'wealth', 'tragedy', 'miracle']
        
        for i, p in enumerate(paragraphs):
            word_count = len(p.split())
            if 30 < word_count < 140:
                p_lower = p.lower()
                score = 0
                if '?' in p: score += 2
                if '!' in p: score += 2
                if any(m in p_lower for m in viral_markers): score += 3
                if p_lower.startswith(('imagine', 'what if', 'did you know', 'this is why', 'never')): score += 4

                if score >= 4:
                    segments.append({
                        "title": f"Viral Clip {len(segments)+1}",
                        "text": p,
                        "score": score,
                        "estimated_duration": round(word_count / 2.5, 1),
                        "rationale": "High-energy keywords detected."
                    })
        return sorted(segments, key=lambda x: x['score'], reverse=True)[:5]

    def _ai_identify_shorts(self, script):
        """Uses LLM (OpenAI -> Gemini) to identify high-retention segments."""
        prompt = f"""Analyze the following script and identify 3-5 segments (50-100 words each) for viral Vertical Shorts. 
        Respond ONLY in JSON format: [{{ "title": "Title", "text": "Exact text...", "score": 9, "rationale": "...Reasoning..." }}]
        
        SCRIPT:
        {script}"""

        # 1. Try OpenAI
        if self.api_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": "You are a viral content strategist."}, {"role": "user", "content": prompt}],
                    response_format={ "type": "json_object" }
                )
                data = json.loads(response.choices[0].message.content)
                shorts = data.get("segments", data if isinstance(data, list) else [])
                for s in shorts: s["estimated_duration"] = round(len(s.get("text", "").split()) / 2.5, 1)
                return shorts
            except Exception as e:
                print(f"[REPURPOSING] OpenAI Fallback: {e}")

        # 2. Try Gemini
        if self.gemini_api_key:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                # Parse JSON from text blocks
                text = response.text
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                data = json.loads(text)
                shorts = data.get("segments", data if isinstance(data, list) else [])
                for s in shorts: s["estimated_duration"] = round(len(s.get("text", "").split()) / 2.5, 1)
                return shorts
            except Exception as e:
                print(f"[REPURPOSING] Gemini Fallback Failed: {e}")

        return None

    def create_viral_hook_variants(self, topic):
        """Generates 3 different hook variations."""
        prompt = f"Generate 3 viral video hooks for: {topic}. Keep under 15 words. Return as plain list."
        
        if self.api_key:
            try:
                import openai
                client = openai.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                return [l.strip() for l in response.choices[0].message.content.split('\n') if l.strip()][:3]
            except: pass

        if self.gemini_api_key:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                return [l.strip() for l in response.text.split('\n') if l.strip()][:3]
            except: pass

        return [f"This changes everything about {topic}.", f"The truth about {topic}.", f"What they don't want you to know: {topic}."]
