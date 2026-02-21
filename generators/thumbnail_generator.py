
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
        """Generates two distinct high-performing thumbnail concepts (A/B Test)."""
        # Mock response for speed if no API key in this specific class (usually inherited or passed)
        return {
            "concept_a": {
                "type": "CURIOSITY",
                "visual": f"A magnifying glass hovering over a redacted document about {topic}",
                "text": "SECRET FOUND"
            },
            "concept_b": {
                "type": "EMOTION",
                "visual": f"A dramatic split screen of {topic} before and after a crisis",
                "text": "TOTAL COLLAPSE"
            }
        }

    def generate_thumbnail(self, title, style="cinematic_documentary"):
        """Creates a high-end YouTube thumbnail using AI synthesis and professional branding."""
        print(f"--- GENERATING BRANDED THUMBNAIL: {title} ---")
        
        # 1. Generate Backdrop using AI
        style_cfg = self.config.STYLES.get(style, self.config.STYLES["cinematic_documentary"])
        prompt = f"{title}. {style_cfg.get('aesthetic')}. Bold, high-contrast, professional YouTube thumbnail style."
        
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
            # Take first 4-5 words for thumbnail
            punchy_text = " ".join(title.split()[:5]).upper()
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
