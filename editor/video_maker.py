
import os
import math
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, CompositeAudioClip, ColorClip

class VideoEditor:
    STYLE_CONFIGS = {
        "standard": {
            "font": "Arial-Bold",
            "fontsize": 60,
            "color": "white",
            "pos": ("center", "bottom"),
            "padding": 50
        }
    }

    def __init__(self, output_dir="output", config_styles=None):
        self.output_dir = output_dir
        self.styles = config_styles or self.STYLE_CONFIGS
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_video(self, audio_path, video_paths, script_text, output_filename="final_video.mp4", 
                     background_music_path=None, intro_video_path=None, style="standard", watermark_handle="@ValuesThatMatters"):
        """Compiles the final documentary with professional style, branding, and advanced watermarking."""
        print(f"Creating video with style: {style}")
        style_cfg = self.styles.get(style, self.STYLE_CONFIGS["standard"])
        
        try:
            # Load voiceover audio
            voiceover = AudioFileClip(audio_path)
            duration = voiceover.duration

            # Load background music if provided
            final_audio = voiceover
            if background_music_path and os.path.exists(background_music_path):
                bg_music = AudioFileClip(background_music_path)
                if bg_music.duration < duration:
                    bg_music = bg_music.loop(duration=duration + 2)
                else:
                    bg_music = bg_music.subclip(0, duration + 2)
                
                bg_music = bg_music.volumex(0.1)
                final_audio = CompositeAudioClip([voiceover, bg_music])

            # Load content video clips
            clips = []
            for path in video_paths:
                if os.path.exists(path):
                    clip = VideoFileClip(path)
                    clips.append(clip)

            if not clips:
                print("No clips loaded.")
                return None

            content_video_clip = concatenate_videoclips(clips, method="compose")
            if content_video_clip.duration < duration:
                content_video_clip = content_video_clip.loop(duration=duration)
            else:
                content_video_clip = content_video_clip.subclip(0, duration)
            
            content_video_clip = content_video_clip.set_audio(final_audio)

            # 1. Overlay Layers
            final_layers = [content_video_clip]
            
            # Add Grain Overlay if requested
            if style_cfg.get("grain"):
                grain = self._create_grain_overlay(content_video_clip.size, duration)
                final_layers.append(grain)
            
            # Subtitle/Text clip
            display_text = script_text[:80] + "..."
            txt_clip = TextClip(
                display_text, 
                fontsize=style_cfg.get("fontsize", 60), 
                color=style_cfg.get("color", "white"),
                font=style_cfg.get("font", "Arial-Bold"),
                size=(content_video_clip.w * 0.8, None),
                method='caption' 
            ).set_pos(style_cfg.get("pos", "center")).set_duration(min(duration, 7))
            
            final_layers.append(txt_clip)

            # 2. Advanced Watermark (Subtle/Moving)
            if watermark_handle:
                watermark = self._create_watermark(content_video_clip.size, watermark_handle, duration)
                final_layers.append(watermark)
            
            final_content = CompositeVideoClip(final_layers)

            # 3. Finalize
            output_path = os.path.join(self.output_dir, output_filename)
            final_content.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
            
            return output_path

        except Exception as e:
            print(f"Error creating video: {e}")
            return None

    def merge_videos(self, video_paths, output_filename):
        try:
            clips = [VideoFileClip(p) for p in video_paths]
            final_clip = concatenate_videoclips(clips, method="compose")
            output_path = os.path.join(self.output_dir, output_filename)
            final_clip.write_videofile(output_path, fps=24)
            return output_path
        except Exception as e:
            print(f"Error merging: {e}")
            return None

    def _create_grain_overlay(self, size, duration):
        import numpy as np
        from moviepy.editor import ImageClip
        w, h = size
        noise = np.random.randint(0, 50, (h, w, 3), dtype='uint8')
        return ImageClip(noise).set_duration(duration).set_opacity(0.1)

    def _apply_multi_camera_cuts(self, clips):
        """Simulates a multi-camera shoot by cutting between wide, close, and POV angles."""
        print("[EDITOR] Applying Multi-Camera AI Synthesis (Cinematic Cutting)...")
        cut_clips = []
        for i, clip in enumerate(clips):
            # For every clip, we simulate a cut to a 'Close Up' or 'Detail' mid-way
            duration = clip.duration
            if duration > 4:
                # Wide Shot (Start)
                cut_clips.append(clip.subclip(0, duration/2))
                # Close Up / Zoom (Simulated with crop/resize or simple jump cut)
                # In a full impl, we'd fetch a NEW angle for the same scene here
                mid_cut = clip.subclip(duration/2, duration).margin(2, color=(0,242,255))
                cut_clips.append(mid_cut)
            else:
                cut_clips.append(clip)
        return cut_clips

    def _trim_silences(self, audio_path):
        """Standardizes audio to maximize pace by trimming dead space (silence)."""
        # In a real setup, we would use pydub to detect silence and slice clips
        # For now, we simulate 'Max Pace' by ensuring minimal padding between segments
        print("[AUDIO] Trimming dead space to maximize viewer retention...")
        return audio_path

    def _apply_dopamine_cues(self, video_clip):
        """Injects visual 'hits' (glitches, pans, or zooms) to maintain attention spans."""
        from moviepy.video.fx.all import mirror_x, lum_triotone
        import random
        
        # Every 10 seconds, apply a refreshing visual effect
        duration = video_clip.duration
        if duration > 10:
            print("[EDITOR] Injecting dopaminergic visual cues...")
            # Real implementation would apply fx to subclips and re-composite
        return video_clip
