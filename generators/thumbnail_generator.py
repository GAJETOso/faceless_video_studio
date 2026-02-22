
import os
try:
    from moviepy import ImageClip, TextClip, CompositeVideoClip, ColorClip
except ImportError:
    from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, ColorClip
from generators.media_fetcher import MediaFetcher

class ThumbnailGenerator:
    def __init__(self, config):
        self.config = config
        self.media = MediaFetcher(
            pexels_api_key=config.PEXELS_API_KEY, 
            openai_api_key=config.OPENAI_API_KEY,
            config_styles=config.STYLES
        )

    def generate_ab_concepts(self, topic):
        """Generates two distinct high-performing thumbnail concepts using Intelligence (A/B Test)."""
        prompt = f"""Generate two unique YouTube thumbnail concepts for a video titled '{topic}'.
        
        Concept A should be 'CURIOSITY' driven (mystery, red arrows, zoomed in details).
        Concept B should be 'EMOTION' driven (shocked faces, outcome-based, dramatic lighting).
        
        For each, provide:
        - A 'Visual Description' for an AI Image Generator.
        - A 'Thumb Text' (max 3 words).
        
        Respond in JSON format:
        {{
            "concept_a": {{"type": "CURIOSITY", "visual": "...", "text": "..."}},
            "concept_b": {{"type": "EMOTION", "visual": "...", "text": "..."}}
        }}"""
        
        result = self._call_llm(prompt, "You are a YouTube viral growth expert specializing in CTR optimization.")
        
        if result:
            try:
                # Clean JSON if wrapped in markdown
                import json
                clean_json = result.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json)
            except: pass
            
        # Fallback concepts
        return {
            "concept_a": {
                "type": "CURIOSITY",
                "visual": f"A mysterious silhouette pointing at a hidden detail regarding {topic}",
                "text": "THEY HID THIS"
            },
            "concept_b": {
                "type": "EMOTION",
                "visual": f"A dramatic reaction to a shocking discovery about {topic}",
                "text": "I'M SHOCKED"
            }
        }

    def _call_llm(self, prompt, system):
        import requests
        # 1. Try OpenAI
        if self.config.OPENAI_API_KEY:
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.config.OPENAI_API_KEY}"},
                    json={"model": "gpt-4o-mini", "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
            except: pass
            
        # 2. Try Gemini Fallback
        if self.config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.config.GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system)
                return model.generate_content(prompt).text
            except: pass
        return None

    def generate_thumbnail(self, title, style="cinematic_documentary", concept_visual=None, concept_text=None):
        """Creates a high-end YouTube thumbnail using AI synthesis and professional branding."""
        print(f"--- GENERATING BRANDED THUMBNAIL: {title} ---")
        
        # 1. Generate Backdrop using AI
        style_cfg = self.config.STYLES.get(style, self.config.STYLES["cinematic_documentary"])
        
        # Use provided concept visual if available, otherwise fallback to title-based prompt
        prompt = concept_visual if concept_visual else f"{title}. {style_cfg.get('aesthetic')}. Bold, high-contrast, professional YouTube thumbnail style."
        
        backdrop_path = os.path.join(self.config.ASSETS_DIR, "thumb_backdrop_raw.png")
        backdrop_file = self.media.generate_ai_image(prompt, backdrop_path)
        
        if not backdrop_file:
            print("Failed to generate AI backdrop for thumbnail.")
            return None

        # 2. Design the Thumbnail with MoviePy
        try:
            backdrop = ImageClip(backdrop_file).with_duration(1)
            w, h = backdrop.size
            
            # Add Dark Gradient Overlay for text readability
            gradient = ColorClip(size=(w, h//2), color=(0,0,0)).with_opacity(0.6).with_position(('center', 'bottom'))
            
            # Add Main Title (Punchy & Large)
            # Use provided concept text or take first 4-5 words for thumbnail
            punchy_text = concept_text.upper() if concept_text else " ".join(title.split()[:5]).upper()
            txt_clip = TextClip(
                punchy_text,
                fontsize=120,
                color=style_cfg.get('color', 'white'),
                font=style_cfg.get('font', 'Impact'),
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(w*0.9, None)
            ).with_position(('center', h*0.6)).with_duration(1)

            # Add "Matters of Value" Badge
            badge_text = "MATTERS OF VALUE"
            badge_bg = ColorClip(size=(400, 60), color=(197, 160, 89)).with_position((50, 50)).with_duration(1)  # Gold bar
            badge_txt = TextClip(
                badge_text,
                fontsize=30,
                color='black',
                font='Arial-Bold'
            ).with_position((70, 65)).with_duration(1)

            final_thumb = CompositeVideoClip([backdrop, gradient, txt_clip, badge_bg, badge_txt], size=(w, h))
            
            output_path = os.path.join(self.config.OUTPUT_DIR, f"THUMB_{title.replace(' ', '_')}.png")
            final_thumb.save_frame(output_path, t=0)
            
            print(f"Branded Thumbnail saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"Error creating branded thumbnail: {e}")
            return None
