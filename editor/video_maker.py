
import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

class VideoEditor:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


    def create_video(self, audio_path, video_paths, script_text, output_filename="final_video.mp4", background_music_path=None, intro_video_path=None):
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
                    # Resize for standard short format (9:16) if needed
                    # clip = clip.resize(height=1920) 
                    # clip = clip.crop(x1=clip.w/2 - 540, width=1080) 
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

            # Add Text Overlay (Simple)
            txt_clip = TextClip(script_text[:50]+"...", fontsize=70, color='white', size=content_video_clip.size)
            txt_clip = txt_clip.set_pos('center').set_duration(5)
            
            final_content = CompositeVideoClip([content_video_clip, txt_clip])

            # Add Intro Video if provided
            if intro_video_path and os.path.exists(intro_video_path):
                intro_clip = VideoFileClip(intro_video_path)
                # Resize intro to match content if necessary
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
