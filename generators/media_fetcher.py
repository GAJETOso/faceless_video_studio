
import os
import requests
import random

class MediaFetcher:
    # Mapping of styles to aesthetic keywords for Pexels search
    STYLE_KEYWORDS = {
        "cinematic_documentary": "cinematic moody lighting, tech server, mysterious dark technology, extreme close up",
        "educational": "minimalist clean workspace, infographic, motion graphics background",
        "motivational": "fitness motivation, sunrise mountain, fast cars, success energy",
        "creepy_pasta": "dark foggy woods, abandoned house, static noise, grainy horror",
        "finance_wealth": "luxury office, wall street trading, gold stacks, corporate skyscraper",
        "breaking_viral": "newsroom background, digital globe, flashing alert lights, emergency siren lights",
        "standard": "vibrant colorful background, abstract moving layers"
    }

    def __init__(self, pexels_api_key=None, stock_dir="assets/stock"):
        self.api_key = pexels_api_key
        self.stock_dir = stock_dir
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {"Authorization": self.api_key} if self.api_key else {}
        
        if not os.path.exists(self.stock_dir):
            os.makedirs(self.stock_dir)

    def _search_local_stock(self, query):
        """Scans the local stock directory for matching clips."""
        local_clips = []
        if not os.path.exists(self.stock_dir):
            return []
            
        # Get all video files in stock dir
        files = [f for f in os.listdir(self.stock_dir) if f.endswith(('.mp4', '.mov', '.avi'))]
        
        # Simple keyword matching
        query_words = query.lower().split()
        for f in files:
            if any(word in f.lower() for word in query_words):
                local_clips.append(os.path.join(self.stock_dir, f))
        
        # If no specific match, just return some random premium clips from the folder if it's not empty
        if not local_clips and files:
            local_clips = [os.path.join(self.stock_dir, f) for f in random.sample(files, min(len(files), 2))]
            
        return local_clips

    def search_videos(self, query, per_page=5, style="standard"):
        """Fetches video URLs, prioritizing local stock database first."""
        # 1. Check Local Stock First
        local_assets = self._search_local_stock(query)
        if len(local_assets) >= per_page:
            return local_assets[:per_page]

        # 2. Fallback to Pexels for remaining clips
        if not self.api_key:
            print("No Pexels API key provided, using local assets only.")
            return local_assets

        # Enhance query with style-based keywords
        aesthetic = self.STYLE_KEYWORDS.get(style, self.STYLE_KEYWORDS["standard"])
        enhanced_query = f"{query} {aesthetic}"

        try:
            params = {
                "query": enhanced_query,
                "per_page": per_page,
                "orientation": "portrait", # For shorts/tiktok
                "size": "medium"
            }
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            videos = response.json().get("videos", [])
            
            # Extract video files (choose highest res available)
            video_files = []
            for video in videos:
                files = video.get("video_files", [])
                best_quality = sorted(files, key=lambda x: x['width'] * x['height'], reverse=True)[0]
                video_files.append(best_quality['link'])
            
            return video_files

        except Exception as e:
            print(f"Error fetching media: {e}")
            return []

    def download_video(self, url, output_path):
        """Downloads a video file."""
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return output_path
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
