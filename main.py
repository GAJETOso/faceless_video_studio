
import os
from config import settings
from sources.reddit_scraper import RedditScraper
from generators.script_writer import ScriptWriter
from generators.voice_generator import VoiceGenerator
from generators.media_fetcher import MediaFetcher
from editor.video_maker import VideoEditor

class FacelessVideoBot:
    def __init__(self):
        self.config = settings.Config()
        
        # Initialize modules
        self.reddit = RedditScraper(client_id=self.config.REDDIT_CLIENT_ID, 
                                   client_secret=self.config.REDDIT_CLIENT_SECRET,
                                   user_agent=self.config.REDDIT_USER_AGENT)
        
        self.script_engine = ScriptWriter(api_key=self.config.OPENAI_API_KEY)
        self.voice_engine = VoiceGenerator(lang="en")  # Use gTTS or edge-tts if integrated
        self.media_engine = MediaFetcher(pexels_api_key=self.config.PEXELS_API_KEY)
        self.editor = VideoEditor(output_dir=self.config.OUTPUT_DIR)


    def produce_video(self, title, script_content, content_source_name="generic", output_prefix="video"):
        """Shared pipeline to generate, edit, and publish a video."""
        print(f"Producing video for: {title}")
        
        # 1. Generate Audio (Voiceover)
        audio_file = os.path.join(self.config.ASSETS_DIR, f"voiceover_{output_prefix}.mp3")
        if not os.path.exists(self.config.ASSETS_DIR):
            os.makedirs(self.config.ASSETS_DIR)
            
        audio_path = self.voice_engine.generate_audio(text=script_content, output_file=audio_file)
        if not audio_path:
            print("Failed to generate audio. Exiting.")
            return
        
        print(f"Generated Audio at: {audio_path}")

        # 2. Fetch Visuals (Background Video)
        # Try to find relevant visuals, or fallback to generic nature/abstract
        query = title if len(title) < 20 else "abstract background" 
        video_urls = self.media_engine.search_videos(query=query, per_page=3)
        video_clips = []
        
        for i, url in enumerate(video_urls):
            path = os.path.join(self.config.ASSETS_DIR, f"bg_{output_prefix}_{i}.mp4")
            local_path = self.media_engine.download_video(url, path)
            if local_path:
                video_clips.append(local_path)
        
        if not video_clips:
            print("No video clips found/downloaded. Cannot proceed.")
            return

        # 3. Prepare Assets (Intro & Music)
        # Look for 'intro.mp4' and 'music.mp3' in assets, or specific ones.
        intro_path = os.path.join(self.config.ASSETS_DIR, "intro.mp4")
        if not os.path.exists(intro_path): intro_path = None
        
        music_path = os.path.join(self.config.ASSETS_DIR, "background_music.mp3")
        # Todo: implementations could pick random music from a folder
        if not os.path.exists(music_path): music_path = None

        # 4. Edit Video
        final_video = self.editor.create_video(
            audio_path=audio_path, 
            video_paths=video_clips, 
            script_text=title, 
            output_filename=f"{output_prefix}_final.mp4",
            background_music_path=music_path,
            intro_video_path=intro_path
        )
        
        if final_video:
            print(f"Video created successfully: {final_video}")
            self.publish_content(final_video, title, script_content)
        else:
            print("Video creation failed.")

    def run_reddit_pipeline(self, subreddit="AskReddit", count=1):
        """Runs the pipeline for Reddit content."""
        print(f"Starting Reddit Bot execution for r/{subreddit}...")

        # 1. Fetch Content
        post = self.reddit.get_top_post(subreddit_name=subreddit)
        if not post:
            return

        print(f"Found post: {post['title']}")

        # 2. Generate Script
        script = self.script_engine.generate_script(topic=post['title'], prompt=None)
        if not script:
            return
        
        self.produce_video(
            title=post['title'],
            script_content=script,
            content_source_name="Reddit",
            output_prefix=f"reddit_{subreddit}"
        )

    def run_nairaland_pipeline(self, category="romance"):
        """Runs pipeline for Nairaland content."""
        from sources.nairaland_scraper import NairalandScraper
        self.nairaland = NairalandScraper()
        
        print(f"Starting Nairaland Bot execution for {category}...")
        
        # 1. Fetch Topic
        topics = self.nairaland.get_trending_topics(limit=5)
        if not topics:
            print("No topics found.")
            return

        topic = topics[0]  # Pick first
        print(f"Topic: {topic['title']}")
        
        # 2. Generate Content
        script = self.script_engine.generate_script(topic=topic['title'])
        if not script:
            return

        self.produce_video(
            title=topic['title'],
            script_content=script,
            content_source_name="Nairaland",
            output_prefix=f"nairaland_{category}"
        )

    def publish_content(self, video_path, title, description):
        """Uploads to all configured platforms."""
        from publishers.social_poster import YouTubeUploader, TikTokUploader, InstagramUploader, DriveUploader
        
        uploaders = [
            YouTubeUploader(),
            TikTokUploader(),
            InstagramUploader(), # Requires Instagram Graph API
            DriveUploader()
        ]
        
        for uploader in uploaders:
            try:
                uploader.upload_video(video_path, title, description)
            except Exception as e:
                print(f"Failed to upload using {uploader.platform}: {e}")

if __name__ == "__main__":
    bot = FacelessVideoBot()
    
    import sys
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        topic = sys.argv[2] if len(sys.argv) > 2 else "AskReddit"
        
        if mode == "reddit":
            bot.run_reddit_pipeline(subreddit=topic)
        elif mode == "nairaland":
            bot.run_nairaland_pipeline(category=topic)
        else:
            print("Unknown mode. Use 'reddit' or 'nairaland'.")
    else:
        # Default behavior for testing
        print("No args provided. Running default Reddit bot...")
        bot.run_reddit_pipeline()
