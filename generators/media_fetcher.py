
import os
import requests
import random

class MediaFetcher:
    def __init__(self, pexels_api_key=None):
        self.api_key = pexels_api_key
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {"Authorization": self.api_key} if self.api_key else {}

    def search_videos(self, query, per_page=5):
        """Fetches video URLs from Pexels API."""
        if not self.api_key:
            print("No Pexels API key provided, skipping video download.")
            return []

        try:
            params = {
                "query": query,
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
