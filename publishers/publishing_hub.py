
import os
import json
import time
from publishers.social_bot import SocialMediaBot

class PublishingHub:
    def __init__(self, output_dir="output", api_key=None):
        self.output_dir = output_dir
        self.log_file = os.path.join(output_dir, "publishing_log.json")
        self.social_bot = SocialMediaBot(api_key=api_key)

    def publish_video(self, video_path, title, script="", platforms=["youtube", "tiktok", "twitter", "instagram", "facebook", "whatsapp"]):
        """Distributes the video and its AI-generated engagement package."""
        print(f"--- INITIALIZING GLOBAL DISTRIBUTION HUB: {title} ---")
        
        # 1. Generate Social Assets
        print("Generating platform-specific descriptions and tags...")
        social_package = self.social_bot.generate_engagement_package(title, script)
        
        results = {}
        for platform in platforms:
            print(f"Publishing to {platform.upper()}...")
            time.sleep(0.5) 
            
            # Simulated Upload Logic
            results[platform] = {
                "status": "Published",
                "timestamp": time.ctime(),
                "url": f"https://www.{platform}.com/ValuesThatMatters/status/...",
                "metadata": social_package.get(platform.capitalize(), {}) if social_package else {}
            }
            print(f"[{platform.upper()}] Success: {results[platform]['url']}")

        self._log_publish(video_path, title, results)
        return results

    def _log_publish(self, video_path, title, results):
        log_entry = {
            "title": title,
            "file": os.path.basename(video_path),
            "distribution": results
        }
        
        current_logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                try:
                    current_logs = json.load(f)
                except: pass
        
        current_logs.append(log_entry)
        with open(self.log_file, 'w') as f:
            json.dump(current_logs, f, indent=4)
