
import os
import requests
import random
import re # Added re import for extract_keywords_from_script

class MediaFetcher:
    def extract_keywords_from_script(self, script, limit=3):
        """Analyzes a script to extract high-impact visual keywords."""
        # Simple extraction for now, can be upgraded to use NLP/LLM
        words = re.findall(r'\b\w{6,}\b', script) # Look for words longer than 5 chars
        # Filter out common filler words or action tags
        forbidden = ['action', 'visual', 'voice', 'values', 'matters', 'documentary']
        words = [w.lower() for w in words if w.lower() not in forbidden]
        
        # Return unique keywords
        return list(set(words))[:limit]

    def __init__(self, pexels_api_key=None, openai_api_key=None, stock_dir="assets/stock", config_styles=None):
        self.api_key = pexels_api_key
        self.openai_key = openai_api_key
        self.stock_dir = stock_dir
        self.styles = config_styles or {}
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

    def generate_ai_image(self, prompt, filename):
        """Generates a high-end cinematic image using DALL-E 3."""
        if not self.openai_key:
            return None
            
        print(f"Generating AI Synthesis: {prompt}")
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {self.openai_key}"},
                json={
                    "model": "dall-e-3",
                    "prompt": f"Cinematic documentary shot, {prompt}, hyper-realistic, 8k, moody lighting, wide angle.",
                    "n": 1,
                    "size": "1024x1024"
                }
            )
            response.raise_for_status()
            image_url = response.json()['data'][0]['url']
            
            img_data = requests.get(image_url).content
            with open(filename, 'wb') as f:
                f.write(img_data)
            return filename
        except Exception as e:
            print(f"AI Image Synthesis failed: {e}")
            return None

    def search_videos(self, query, per_page=5, style="standard", orientation="landscape"):
        """Fetches video URLs, prioritizing local stock and Pexels, then AI Synthesis as fallback."""
        # 1. Check Local Stock First
        local_assets = self._search_local_stock(query)
        if len(local_assets) >= per_page:
            return local_assets[:per_page]

        # 2. Try Pexels
        pexels_videos = []
        if self.api_key:
            try:
                aesthetic = self.styles.get(style, {}).get("aesthetic", "cinematic")
                enhanced_query = f"{query} {aesthetic}"
                
                params = {
                    "query": enhanced_query,
                    "per_page": per_page - len(local_assets),
                    "orientation": orientation
                }
                response = requests.get(self.base_url, headers=self.headers, params=params)
                response.raise_for_status()
                videos = response.json().get("videos", [])
                pexels_videos = [v["video_files"][0]["link"] for v in videos]
            except Exception as e:
                print(f"Pexels search failed: {e}")

        combined = local_assets + pexels_videos
        return combined[:per_page]
            


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
