
import os
import sys
from config import settings
from main import FacelessVideoBot
from generators.script_writer import ScriptWriter

class MusicStudio:
    def __init__(self):
        self.bot = FacelessVideoBot()
        self.config = self.bot.config
        
    def produce_music_video(self, topic, genre="hip-hop", output_name="music_video"):
        """
        Produces a high-energy music video by generating lyrics, 
        using a rhythmic voiceover, and applying dynamic cuts.
        """
        print(f"\n--- 🎵 MUSIC STUDIO: STARTING PRODUCTION ---")
        print(f"Topic: {topic} | Genre: {genre}")
        
        # 1. Generate Lyrics instead of a standard script
        lyrics = self.bot.script_engine.generate_lyrics(topic, genre)
        print("\n[LYRICS GENERATED]")
        print(lyrics)
        
        # 2. Pick a high-energy voice for the "vocals"
        voice = genre if genre in ["rnb", "rap", "afrobeat"] else "lyrics"
        
        # 3. Produce the video using the bot's core pipeline but with 'music_video' style
        # Note: We use the existing produce_video but we can extend it for faster cuts
        video_path = self.bot.produce_video(
            title=topic,
            script_content=lyrics,
            style="music_video",
            voice=voice,
            output_prefix=f"music_{topic.replace(' ', '_')}",
            vertical=True # Default to vertical for music videos (TikTok/Reels)
        )
        
        if video_path:
            print(f"\n✅ Music Video ready at: {video_path}")
        else:
            print("\n❌ Music Video production failed.")
            
if __name__ == "__main__":
    studio = MusicStudio()
    
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        genre = sys.argv[2] if len(sys.argv) > 2 else "hip-hop"
        studio.produce_music_video(topic, genre)
    else:
        print("Usage: python music_studio.py <topic> [genre]")
        print("Example: python music_studio.py 'The Future of AI' 'cyberpunk'")
