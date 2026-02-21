
import os
from config import settings
from sources.reddit_scraper import RedditScraper
from generators.script_writer import ScriptWriter
from generators.voice_generator import VoiceGenerator
from generators.media_fetcher import MediaFetcher
from editor.video_maker import VideoEditor

from generators.news_integrator import NewsIntegrator
from generators.translation_engine import TranslationEngine
from generators.hook_optimizer import HookOptimizer
from publishers.sentiment_tracker import SentimentTracker
from generators.lipsync_engine import LipSyncEngine
from publishers.comment_responder import CommentResponder
from publishers.community_manager import CommunityManager
from publishers.pivot_analyzer import PivotAnalyzer
from generators.intro_generator import IntroHookGenerator
from generators.series_planner import SeriesPlanner
from generators.voice_cloning import VoiceCloningEngine
from publishers.publishing_pipeline import PublishingPipeline
from generators.branding_engine import BrandingEngine
from generators.music_selector import MusicSelector
from generators.content_calendar import ContentCalendar
from generators.thumbnail_generator import ThumbnailGenerator
from generators.sponsor_manager import SponsorManager
from publishers.publishing_hub import PublishingHub
from generators.repurposing_engine import RepurposingEngine

class FacelessVideoBot:
    def __init__(self):
        self.config = settings.Config()
        
        # Initialize modules
        self.reddit = RedditScraper(client_id=self.config.REDDIT_CLIENT_ID, 
                                   client_secret=self.config.REDDIT_CLIENT_SECRET,
                                   user_agent=self.config.REDDIT_USER_AGENT)
        
        self.script_engine = ScriptWriter(api_key=self.config.OPENAI_API_KEY, config_styles=self.config.STYLES)
        self.branding_engine = BrandingEngine(api_key=self.config.OPENAI_API_KEY)
        self.translation_engine = TranslationEngine(api_key=self.config.OPENAI_API_KEY)
        self.hook_engine = HookOptimizer(api_key=self.config.OPENAI_API_KEY)
        self.sentiment_engine = SentimentTracker(api_key=self.config.OPENAI_API_KEY)
        self.news_engine = NewsIntegrator(api_key=self.config.OPENAI_API_KEY)
        self.community_engine = CommunityManager(api_key=self.config.OPENAI_API_KEY)
        
        # Strategic Intelligence & Visual Hooks
        self.pivot_engine = PivotAnalyzer(api_key=self.config.OPENAI_API_KEY)
        self.intro_engine = IntroHookGenerator(api_key=self.config.OPENAI_API_KEY)
        self.series_engine = SeriesPlanner(api_key=self.config.OPENAI_API_KEY)
        self.sync_engine = LipSyncEngine(api_key=self.config.OPENAI_API_KEY)
        self.comment_bot = CommentResponder(api_key=self.config.OPENAI_API_KEY)
        
        # Monetization, Distribution, & Personalization
        self.sponsor_engine = SponsorManager(api_key=self.config.OPENAI_API_KEY)
        self.repurpose_engine = RepurposingEngine(api_key=self.config.OPENAI_API_KEY)
        self.voice_cloning_engine = VoiceCloningEngine(api_key=self.config.OPENAI_API_KEY)
        self.publishing_pipeline = PublishingPipeline(config=self.config)
        
        self.voice_engine = VoiceGenerator(api_key=self.config.OPENAI_API_KEY, config_voices=self.config.VOICES)
        self.music_engine = MusicSelector(assets_dir=self.config.ASSETS_DIR)
        self.media_engine = MediaFetcher(
            pexels_api_key=self.config.PEXELS_API_KEY, 
            openai_api_key=self.config.OPENAI_API_KEY,
            config_styles=self.config.STYLES
        )
        self.editor = VideoEditor(output_dir=self.config.OUTPUT_DIR, config_styles=self.config.STYLES)
        self.calendar = ContentCalendar(api_key=self.config.OPENAI_API_KEY, config=self.config)
        self.thumbnailer = ThumbnailGenerator(self.config)
        self.publisher = PublishingHub(output_dir=self.config.OUTPUT_DIR, api_key=self.config.OPENAI_API_KEY)

    def generate_series_plan(self, topic):
        """Generates a 3-part documentary arc."""
        print(f"[SERIES] Planning trilogy for: {topic}")
        return self.series_engine.plan_trilogy(topic)

    def get_thumbnail_ab(self, topic):
        """Generates A/B thumbnail concepts."""
        return self.thumbnailer.generate_ab_concepts(topic)

    def analyze_for_sponsors(self, script):
        """Finds safe spots for ad integration."""
        print("[MONETIZATION] Analyzing script for brand-safe ad slots...")
        return self.sponsor_engine.find_safe_spots(script)

    def analyze_for_repurposing(self, script):
        """Identifies viral segments for Shorts/Reels."""
        print("[DISTRIBUTION] Scanning script for viral micro-moments...")
        if not self.repurpose_engine:
            return []
        return self.repurpose_engine.identify_viral_shorts(script)

    def orchestrate_publishing(self, video_path, platforms, metadata):
        """Orchestrates multi-platform publishing."""
        return self.publishing_pipeline.publish_video(video_path, platforms, metadata)

    def manage_voice_cloning(self, action, name=None, sample_path=None):
        """Manages voice cloning operations."""
        if action == "clone":
            return self.voice_cloning_engine.clone_voice(name, sample_path)
        elif action == "list":
            return self.voice_cloning_engine.list_cloned_voices()
        return {}

    def get_strategic_pivot(self, current_stats):
        """Recommends a high-growth niche shift using AI analysis."""
        trending = self.news_engine.fetch_trending_topics()
        print("[STRATEGY] Calculating optimal niche pivot...")
        return self.pivot_engine.analyze_pivot_opportunity(current_stats, trending)

    def generate_community_kit(self, topic, script):
        """Generates a viral engagement kit for community tabs."""
        print(f"[COMMUNITY] Drafting social engagement kit for: {topic}")
        return self.community_engine.draft_community_package(topic, script)

    def auto_respond_to_viewer(self, topic, script, comment):
        """Strategic automated response to maximize viral engagement."""
        print(f"[ENGAGEMENT] Drafting strategic reply for topic: {topic}")
        return self.comment_bot.draft_response(topic, script, comment)

    def get_trending_opportunities(self):
        """Returns the latest high-stakes topics from the news engine."""
        return self.news_engine.fetch_trending_topics()

    def produce_dubbed_variants(self, title, script_content, languages=["Spanish", "French"]):
        """Generates international versions of a video automatically."""
        print(f"--- GLOBAL DUBBING INITIATED: {title} ---")
        for lang in languages:
            print(f"Translating and voicing for {lang}...")
            translated_script = self.translation_engine.translate_script(script_content, lang)
            self.produce_video(
                title=f"{title} ({lang})",
                script_content=translated_script,
                output_prefix=f"intl_{lang.lower()}_{title[:10].replace(' ', '_')}",
                voice="auto", # AI will pick best multi-lang voice if configured
                publish=True
            )

    def run_angle_test(self, topic):
        """Dupes and tests every possible angle/hook for a specific topic."""
        print(f"--- ANGLE TESTING & DEMOGRAPHIC OPTIMIZATION: {topic} ---")
        variants = self.hook_engine.generate_variants(topic, "")
        for angle_name, hook_text in variants.items():
            print(f"Testing Angle: {angle_name}")
            full_script = hook_text + "\n\n" + self.script_engine.generate_script(topic)
            self.produce_video(
                title=f"{topic} [{angle_name}]",
                script_content=full_script,
                output_prefix=f"test_{angle_name}_{topic[:10].replace(' ', '_')}",
                publish=True
            )

    def run_bulk_production(self):
        """Processes the entire weekly calendar in one massive background render."""
        plan = self.calendar.get_current_plan()
        if not plan or "days" not in plan:
            print("No strategic plan found for bulk production.")
            return

        print(f"--- INITIALIZING BULK RENDER FOR {len(plan['days'])} PRODUCTIONS ---")
        for i, day_plan in enumerate(plan['days']):
            print(f"\n[Bulk {i+1}/{len(plan['days'])}] Targeting: {day_plan['topic']}")
            
            # Auto-generate script if not provided
            script = self.script_engine.generate_script(topic=day_plan['topic'], style=day_plan['style'])
            
            self.produce_video(
                title=day_plan['topic'],
                script_content=script,
                output_prefix=f"bulk_{day_plan['day'].lower()}",
                style=day_plan['style'],
                voice="auto",
                generate_thumb=True,
                enhance_script=True,
                publish=True
            )

    def produce_video(self, title, script_content, content_source_name="generic", output_prefix="video", 
                      style="cinematic_documentary", voice="auto", sign_off=True,
                      generate_thumb=True, enhance_script=False, publish=False, vertical=False):
        """Standard pipeline with AI Tone Analysis, Music Selection, Custom Branding & Social Bot."""
        print(f"Producing branded video: {title} (Vertical: {vertical})")
        
        # 0. Custom Branding
        slogan = self.branding_engine.generate_slogan(title)
        branding_intro = f"[Action: Cinematic Title Overlay: {title}]\n[{slogan}]\n\n"
        script_content = branding_intro + script_content

        # 1. AI Tone & Voice Selection
        if voice == "auto":
            print("Analyzing script tone for automatic voice selection...")
            voice = self.script_engine.analyze_tone(script_content)
            print(f"AI Recommended Voice: {voice}")

        # 2. Dynamic Music Selection
        bg_music = self.music_engine.select_music(voice)
        print(f"AI Recommended Music: {bg_music}")

        # 3. Optional AI Enhancement
        if enhance_script:
            print("Enhancing script with AI SFX cues...")
            script_content = self.script_engine.enhance_script(script_content)

        # Add Brand Signature if requested
        if sign_off:
            signature = "\n\n[Action: Brand Logo Appears]\nThis is Matters of Value."
            if signature not in script_content:
                script_content += signature

        # 1. Generate Audio
        audio_file = os.path.join(self.config.ASSETS_DIR, f"voiceover_{output_prefix}.mp3")
        audio_path = self.voice_engine.generate_audio(text=script_content, output_file=audio_file, voice=voice)
        
        # 2. Fetch Visuals
        keywords = self.media_engine.extract_keywords_from_script(script_content)
        query = " ".join(keywords) if keywords else title
        
        # Determine orientation for stock search
        orientation = "portrait" if vertical else "landscape"
        video_sources = self.media_engine.search_videos(query=query, per_page=10, style=style)
        
        # If no videos found, synthesize an AI image
        if not video_sources:
            img_path = os.path.join(self.config.ASSETS_DIR, f"ai_synthesis_{output_prefix}.png")
            fallback_img = self.media_engine.generate_ai_image(query, img_path)
            video_sources = [fallback_img] if fallback_img else []

        # 4. Create Video
        final_video = self.editor.create_video(
            audio_path=audio_path,
            video_paths=video_sources,
            script_text=script_content,
            output_filename=f"{output_prefix}_final.mp4",
            background_music_path=bg_music,
            style=style,
            vertical=vertical
        )
        
        if final_video:
            print(f"Video created successfully: {final_video}")
            # 4. Optional: Generate Branded Thumbnail
            if generate_thumb:
                self.thumbnailer.generate_thumbnail(title, style)

            # 5. Optional: Automated Publishing
            if publish:
                self.publisher.publish_video(video_path=final_video, title=title, script=script_content)
        else:
            print("Video creation failed.")
        
        return final_video

    def produce_long_form(self, title, full_script, style="cinematic_documentary", voice="onyx", 
                          generate_thumb=True, enhance_script=False, publish=False):
        """Splits a long script into chapters, renders them, and merges into a feature documentary."""
        print(f"--- INITIALIZING LONG-FORM PRODUCTION: {title} ---")
        
        # 0. Optional AI Enhancement for the ENTIRE script first
        if enhance_script:
            print("Enhancing long-form script with AI SFX cues...")
            full_script = self.script_engine.enhance_script(full_script)

        # 1. Split script into chapters
        # [Existing split logic...]
        paragraphs = full_script.split('\n\n')
        chapters = []
        current_chapter = []
        words_per_chapter = 500
        
        count = 0
        for p in paragraphs:
            current_chapter.append(p)
            count += len(p.split())
            if count >= words_per_chapter:
                chapters.append("\n\n".join(current_chapter))
                current_chapter = []
                count = 0
        if current_chapter:
            chapters.append("\n\n".join(current_chapter))

        chapter_files = []
        for i, chapter_text in enumerate(chapters):
            filename = f"long_{title[:10].replace(' ', '_')}_ch{i}_final.mp4"
            self.produce_video(
                title=f"{title} - Part {i+1}",
                script_content=chapter_text,
                output_prefix=f"long_{title[:10].replace(' ', '_')}_ch{i}",
                style=style,
                voice=voice,
                sign_off=(i == len(chapters)-1),
                generate_thumb=False, # Don't generate thumb for individual chapters
                publish=False # Don't publish individual chapters
            )
            
            chapter_path = os.path.join(self.config.OUTPUT_DIR, filename)
            if os.path.exists(chapter_path):
                chapter_files.append(chapter_path)

        # 2. Merge and Finalize
        if chapter_files:
            final_filename = f"FEATURE_{title.replace(' ', '_')}.mp4"
            final_path = self.editor.merge_videos(chapter_files, final_filename)
            
            if final_path:
                if generate_thumb:
                    self.thumbnailer.generate_thumbnail(title, style)
                if publish:
                    self.publisher.publish_video(video_path=final_path, title=title)
            return final_path
        return None

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
        niche_config = self.config.NICHES.get(niche)
        if not niche_config:
            print(f"Error: Niche '{niche}' not recognized.")
            return

        print(f"--- Starting {niche.upper()} Batch Production ({count} videos) ---")
        
        # 1. Fetch multiple posts
        import random
        subreddit = random.choice(niche_config["subreddits"])
        posts = self.reddit.get_top_posts(subreddit_name=subreddit, limit=count)
        
        for i, post in enumerate(posts):
            print(f"\n[Video {i+1}/{count}] Topic Discovered: {post['title']}")
            
            # Step A: Generate Script
            structure = niche_config.get("structure", "cinematic")
            script = self.script_engine.generate_script(topic=post['title'], style=niche_config["style"], structure=structure)
            
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
                style=niche_config["style"],
                voice=niche_config["voice"]
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
