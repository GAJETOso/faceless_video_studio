
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
        self.voice_engine = VoiceGenerator(api_key=self.config.OPENAI_API_KEY, lang="en")
        self.media_engine = MediaFetcher(pexels_api_key=self.config.PEXELS_API_KEY)
        self.editor = VideoEditor(output_dir=self.config.OUTPUT_DIR)


    def produce_video(self, title, script_content, content_source_name="generic", output_prefix="video", style="standard", voice="alloy", sign_off=True):
        """Shared pipeline to generate, edit, and publish a video with a specific style."""
        print(f"Producing video for: {title} (Style: {style}, Voice: {voice})")
        
        # Add Brand Signature if requested
        if sign_off:
            signature = "\n\n[Action: Brand Logo Appears]\nThis is Values That Matters."
            if signature not in script_content:
                script_content += signature

        # 1. Generate Audio (Voiceover)
        audio_file = os.path.join(self.config.ASSETS_DIR, f"voiceover_{output_prefix}.mp3")
        if not os.path.exists(self.config.ASSETS_DIR):
            os.makedirs(self.config.ASSETS_DIR)
            
        audio_path = self.voice_engine.generate_audio(text=script_content, output_file=audio_file, voice=voice)
        if not audio_path:
            print("Failed to generate audio. Exiting.")
            return
        
        print(f"Generated Audio at: {audio_path}")

        # 2. Fetch Visuals (Background Video)
        # Try to find relevant visuals, or fallback to generic nature/abstract
        query = title if len(title) < 20 else "abstract background" 
        video_sources = self.media_engine.search_videos(query=query, per_page=3, style=style)
        video_clips = []
        
        for i, source in enumerate(video_sources):
            # If it's already a local path from our stock database, use it directly
            if os.path.exists(source):
                video_clips.append(source)
                continue
                
            # Otherwise, download from the URL (Pexels)
            path = os.path.join(self.config.ASSETS_DIR, f"bg_{output_prefix}_{i}.mp4")
            local_path = self.media_engine.download_video(source, path)
            if local_path:
                video_clips.append(local_path)
        
        if not video_clips:
            print("No video clips found/downloaded. Cannot proceed.")
            return

        # 3. Prepare Assets (Intro & Music)
        intro_path = os.path.join(self.config.ASSETS_DIR, "intro.mp4")
        if not os.path.exists(intro_path): intro_path = None
        
        music_path = os.path.join(self.config.ASSETS_DIR, "background_music.mp3")
        if not os.path.exists(music_path): music_path = None

        # 4. Edit Video
        final_video = self.editor.create_video(
            audio_path=audio_path, 
            video_paths=video_clips, 
            script_text=title, 
            output_filename=f"{output_prefix}_final.mp4",
            background_music_path=music_path,
            intro_video_path=intro_path,
            style=style
        )
        
        if final_video:
            print(f"Video created successfully: {final_video}")
            self.publish_content(final_video, title, script_content)
        else:
            print("Video creation failed.")

    NICHE_MAP = {
        "mystery": {
            "subreddits": ["UnresolvedMysteries", "InternetMysteries", "DeepWeb"],
            "style": "cinematic_documentary",
            "voice": "onyx" # Placeholder for pro voice ID
        },
        "finance": {
            "subreddits": ["finance", "WallStreetBets", "CryptoCurrency", "wealth"],
            "style": "finance_wealth",
            "voice": "alloy"
        },
        "viral": {
            "subreddits": ["todayIlearned", "worldnews", "trending"],
            "style": "breaking_viral",
            "voice": "echo"
        },
        "motivational": {
            "subreddits": ["getmotivated", "success"],
            "style": "motivational",
            "voice": "shimmer"
        }
    }

    def run_niche_pipeline(self, niche="mystery", count=1, interactive=True):
        """Automatically discovers topics and produces videos in batches with optional manual review."""
        if niche not in self.NICHE_MAP:
            print(f"Error: Niche '{niche}' not recognized.")
            return

        config = self.NICHE_MAP[niche]
        print(f"--- Starting {niche.upper()} Batch Production ({count} videos) ---")
        
        # 1. Fetch multiple posts
        import random
        subreddit = random.choice(config["subreddits"])
        posts = self.reddit.get_top_posts(subreddit_name=subreddit, limit=count)
        
        for i, post in enumerate(posts):
            print(f"\n[Video {i+1}/{count}] Topic Discovered: {post['title']}")
            
            # Step A: Generate Script
            script = self.script_engine.generate_script(topic=post['title'], style=config["style"])
            
            # Step B: Interactive Review (The "Modify at any point" option)
            if interactive:
                print("\n--- SCRIPT REVIEW ---")
                print(script)
                print("---------------------")
                choice = input("\nOptions: [P]roceed, [E]dit, [S]kip, [Q]uit: ").lower()
                
                if choice == 'q':
                    break
                elif choice == 's':
                    continue
                elif choice == 'e':
                    print("Enter/Paste your modified script below (Type 'DONE' on a new line when finished):")
                    lines = []
                    while True:
                        line = input()
                        if line.strip().upper() == 'DONE':
                            break
                        lines.append(line)
                    script = "\n".join(lines)
                    print("Script updated.")
            
            # Step C: Produce Video
            self.produce_video(
                title=post['title'],
                script_content=script,
                content_source_name="NicheDiscovery",
                output_prefix=f"niche_{niche}_{i}",
                style=config["style"],
                voice=config["voice"]
            )

    def run_reddit_pipeline(self, subreddit="AskReddit", count=1, style="standard"):
        """Runs the pipeline for Reddit content."""
        print(f"Starting Reddit Bot execution for r/{subreddit} (Style: {style})...")

        # 1. Fetch Content
        post = self.reddit.get_top_post(subreddit_name=subreddit)
        if not post:
            return

        print(f"Found post: {post['title']}")

        # 2. Generate Script
        script = self.script_engine.generate_script(topic=post['title'], prompt=None, style=style)
        if not script:
            return
        
        self.produce_video(
            title=post['title'],
            script_content=script,
            content_source_name="Reddit",
            output_prefix=f"reddit_{subreddit}",
            style=style
        )

    def run_nairaland_pipeline(self, category="romance", style="standard"):
        """Runs pipeline for Nairaland content."""
        from sources.nairaland_scraper import NairalandScraper
        self.nairaland = NairalandScraper()
        
        print(f"Starting Nairaland Bot execution for {category} (Style: {style})...")
        
        # 1. Fetch Topic
        topics = self.nairaland.get_trending_topics(limit=5)
        if not topics:
            print("No topics found.")
            return

        topic = topics[0]  # Pick first
        print(f"Topic: {topic['title']}")
        
        # 2. Generate Content
        script = self.script_engine.generate_script(topic=topic['title'], style=style)
        if not script:
            return

        self.produce_video(
            title=topic['title'],
            script_content=script,
            content_source_name="Nairaland",
            output_prefix=f"nairaland_{category}",
            style=style
        )

    def run_documentary_pipeline(self, topic, style="cinematic_documentary"):
        """Specialized pipeline for professional documentary-style videos."""
        print(f"Starting Documentary Pipeline for: {topic}...")
        
        # 1. Generate Script with Documentary Style
        script = self.script_engine.generate_script(topic=topic, style=style)
        if not script:
            return

        # 2. Produce Video
        self.produce_video(
            title=topic,
            script_content=script,
            content_source_name="Documentary",
            output_prefix=f"doc_{topic[:10].replace(' ', '_')}",
            style=style
        )

    def run_custom_script_pipeline(self, script_path, style="cinematic_documentary"):
        """Runs the pipeline using a custom script provided in a file."""
        if not os.path.exists(script_path):
            print(f"Error: Script file not found at {script_path}")
            return

        print(f"Starting Custom Script Pipeline for: {script_path} (Style: {style})...")

        # 1. Read Script Content
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
        except Exception as e:
            print(f"Error reading script file: {e}")
            return

        # 2. Extract Title (Use first line or filename)
        first_line = script_content.strip().split('\n')[0]
        title = first_line.replace('#', '').strip() if first_line.startswith('#') else os.path.basename(script_path)
        
        # 3. Produce Video
        self.produce_video(
            title=title,
            script_content=script_content,
            content_source_name="CustomScript",
            output_prefix=f"custom_{os.path.basename(script_path).split('.')[0]}",
            style=style
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
        topic_or_path = sys.argv[2] if len(sys.argv) > 2 else "AskReddit"
        style = sys.argv[3] if len(sys.argv) > 3 else "standard"
        
        if mode == "reddit":
            bot.run_reddit_pipeline(subreddit=topic_or_path, style=style)
        elif mode == "nairaland":
            bot.run_nairaland_pipeline(category=topic_or_path, style=style)
        elif mode == "documentary":
            bot.run_documentary_pipeline(topic=topic_or_path, style=style)
        elif mode == "niche":
            niche = topic_or_path
            count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            # Check for --no-review flag
            interactive = "--no-review" not in sys.argv
            bot.run_niche_pipeline(niche=niche, count=count, interactive=interactive)
        else:
            print("Unknown mode. Use 'reddit', 'nairaland', 'documentary', 'script', or 'niche'.")
    else:
        # Default behavior for testing
        print("No args provided. Running default Reddit bot...")
        bot.run_reddit_pipeline()
