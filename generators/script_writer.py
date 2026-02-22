
import os
import requests

class ScriptWriter:
    def __init__(self, api_key=None, model="gpt-4o", config_styles=None):
        self.api_key = api_key
        self.model = model
        self.styles = config_styles or {}

    def generate_script(self, topic, style="cinematic_documentary", structure="cinematic"):
        """Generates a high-stakes script using Viral Psychology & Retention Hooks."""
        if not self.api_key:
            return f"The mystery of {topic} remains unsolved. A journey into the depths of values that matters."

        if structure == "value_driven":
            prompt = f"""
            Write a high-retention, educational video script for the topic: {topic}.

            Follow this EXACT Scaffold:
            1. THE HOOK (0-15s): Stop the scroll. Promise exactly what the viewer will gain. e.g. "By the end of this video, you will..."
            2. THE TRANSITION: Briefly explain why you are the authority or why this information is critical right now.
            3. THE MEAT: Deliver the value using the 'Rule of Three' (Three distinct, actionable points).
            4. THE CTA: Do NOT just say subscribe. Contextual Recommendation: "If you want to achieve [Goal related to topic], watch this next video on [Related Topic]."

            Style: {style}
            Tone: Authoritative, clear, consistent.
            Format: Include [Visual] descriptions for b-roll.
            Return ONLY the script content.
            """
        else:
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

    def generate_from_concept(self, title, concept, style="cinematic_documentary", duration_minutes=2):
        """
        Generates a fully polished, production-ready script from a creative brief/concept.
        The concept can be a free-form description of the video idea, goals, and key points.
        """
        if not self.api_key:
            return f"[INTRO]\nWelcome to Matters of Value. Today we talk about: {title}.\n\n[MAIN CONTENT]\n{concept}\n\n[OUTRO]\nSubscribe for more high-value content."

        word_count = duration_minutes * 130  # ~130 words per minute spoken
        prompt = f"""You are an expert YouTube scriptwriter for the channel "Matters of Value" — a professional content channel about career growth, financial intelligence, and life strategy.

Write a COMPLETE, production-ready video script based on the following creative brief:

TITLE: {title}
TARGET DURATION: {duration_minutes} minutes (~{word_count} words when spoken)
VIDEO STYLE: {style}

CREATIVE BRIEF / CONCEPT:
{concept}

SCRIPT RULES:
1. HOOK (first 15-30 seconds): Open with a bold, pattern-interrupting statement or provocative question. Make the viewer STOP scrolling.
2. CREDIBILITY BRIDGE: In 2-3 sentences, establish why this channel/perspective matters. Do NOT use fluffy language.
3. VALUE DELIVERY: Break the main content into 3 clear, memorable sections. Each section should have 1 actionable insight.
4. Include [VISUAL: description] cues for relevant b-roll footage throughout.
5. Include natural pauses: [PAUSE] where the speaker should breathe for emphasis.
6. CALL TO ACTION: End with a specific, contextual CTA — tell them what to watch NEXT and why.
7. Tone: Authoritative but conversational. Like a wise mentor, not a textbook.

IMPORTANT: Write ONLY the final script text — no meta-commentary, no markdown headers, just the clean spoken script with [VISUAL] and [PAUSE] markers inline.
"""
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": word_count * 2
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            error_msg = f"Concept-to-script generation failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_msg += f" - {e.response.json().get('error', {}).get('message', '')}"
                except:
                    error_msg += f" - {e.response.text}"
            print(error_msg)
            return f"Error: {error_msg}"

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

    def generate_lyrics(self, topic, genre="hip-hop"):
        """Generates rhyming lyrics based on a topic for a music video."""
        if not self.api_key:
            return f"A song about {topic}, a melody of life."

        prompt = f"""
        Write rhyming song lyrics about the topic: {topic}.
        Genre: {genre}
        Format:
        [VERSE 1]
        (4-8 lines)
        [CHORUS]
        (4 lines)
        [VERSE 2]
        (4-8 lines)
        [CHORUS]
        (4 lines)
        [OUTRO]
        (2 lines)
        
        Keep it high energy and suitable for a viral faceless music video.
        Return ONLY the lyrics content.
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
            print(f"Lyrics generation failed: {e}")
            return f"Error generating lyrics for {topic}"
