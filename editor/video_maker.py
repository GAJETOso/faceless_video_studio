
import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip, ColorClip

class VideoEditor:
    # Font/Style configurations for different moods
    STYLE_CONFIGS = {
        "cinematic_documentary": {
            "font": "Courier-Bold",
            "fontsize": 60,
            "color": "white",
            "stroke_color": "black",
            "stroke_width": 1,
            "method": "caption",
            "pos": ("center", "bottom"),
            "padding": 50,
            "overlay_color": (0, 0, 0), # Deep black base
            "grain": True,
            "vignette": True
        },
        "finance_wealth": {
            "font": "Georgia-Bold",
            "fontsize": 75,
            "color": "#FFD700", # Gold
            "stroke_color": "black",
            "stroke_width": 2,
            "method": "caption",
            "pos": ("center", 100),
            "overlay_color": (10, 20, 30), # Midnight blue tint
            "vignette": True
        },
        "breaking_viral": {
            "font": "Helvetica-Bold",
            "fontsize": 90,
            "color": "white",
            "bg_color": "red",
            "method": "caption",
            "pos": "bottom",
            "vignette": False
        },
        "standard": {
            "font": "Arial-Bold",
            "fontsize": 70,
            "color": "white",
            "method": "label",
            "pos": "center"
        }
    }

    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


    def create_video(self, audio_path, video_paths, script_text, output_filename="final_video.mp4", background_music_path=None, intro_video_path=None, style="standard"):
        """Creates a video by combining audio with background clips, text, music, and intro."""
        try:
            # Load voiceover audio
            voiceover = AudioFileClip(audio_path)
            duration = voiceover.duration

            # Load background music if provided
            final_audio = voiceover
            if background_music_path and os.path.exists(background_music_path):
                bg_music = AudioFileClip(background_music_path)
                # Loop music if shorter than voiceover, trim if longer
                if bg_music.duration < duration:
                    bg_music = bg_music.loop(duration=duration + 2) # slightly longer padding
                else:
                    bg_music = bg_music.subclip(0, duration + 2)
                
                # Lower volume of background music
                bg_music = bg_music.volumex(0.1)
                final_audio = CompositeAudioClip([voiceover, bg_music])

            # Load content video clips
            clips = []
            if not video_paths:
                print("No video paths provided. Cannot generate video.")
                return None
            
            for path in video_paths:
                try:
                    clip = VideoFileClip(path)
                    # For a professional look, ensure clips are covering the screen
                    # resize/crop logic would go here
                    clips.append(clip)
                except Exception as e:
                    print(f"Error loading clip {path}: {e}")

            if not clips:
                return None

            # Concatenate content clips
            content_video_clip = concatenate_videoclips(clips, method="compose")
            
            # Adjust video length to audio
            if content_video_clip.duration < duration:
                content_video_clip = content_video_clip.loop(duration=duration)
            else:
                content_video_clip = content_video_clip.subclip(0, duration)
            
            # Set audio for content
            content_video_clip = content_video_clip.set_audio(final_audio)

            # Add Text Overlay based on Style
            style_cfg = self.STYLE_CONFIGS.get(style, self.STYLE_CONFIGS["standard"])
            
            # 1. Overlay & Filters
            final_layers = [content_video_clip]
            
            # Add Grain Overlay if requested
            if style_cfg.get("grain"):
                grain = self._create_grain_overlay(content_video_clip.size, duration)
                final_layers.append(grain)
            
            # Show a portion of the text or the title
            display_text = script_text[:80].upper() if style == "motivational" else script_text[:80] + "..."
            
            txt_clip = TextClip(
                display_text, 
                fontsize=style_cfg.get("fontsize", 70), 
                color=style_cfg.get("color", "white"),
                font=style_cfg.get("font", "Arial-Bold"),
                stroke_color=style_cfg.get("stroke_color"),
                stroke_width=style_cfg.get("stroke_width", 0),
                size=(content_video_clip.w * 0.8, None),
                method='caption' 
            )
            
            txt_clip = txt_clip.set_pos(style_cfg.get("pos", "center")).set_duration(min(duration, 7))
            final_layers.append(txt_clip)
            
            final_content = CompositeVideoClip(final_layers)

    def _create_grain_overlay(self, size, duration):
        """Creates a subtle moving grain/noise layer for cinematic texture."""
        import numpy as np
        from moviepy.editor import ImageClip
        
        # Create a single frame of noise
        w, h = size
        noise = np.random.randint(0, 50, (h, w, 3), dtype='uint8')
        grain_clip = ImageClip(noise).set_duration(duration).set_opacity(0.1)
        return grain_clip

            # Add Intro Video if provided
            if intro_video_path and os.path.exists(intro_video_path):
                intro_clip = VideoFileClip(intro_video_path)
                if intro_clip.size != final_content.size:
                    intro_clip = intro_clip.resize(final_content.size)
                
                final_video = concatenate_videoclips([intro_clip, final_content], method="compose")
            else:
                final_video = final_content

            output_path = os.path.join(self.output_dir, output_filename)
            final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
            
            return output_path

        except Exception as e:
            print(f"Error creating video: {e}")
            return None
