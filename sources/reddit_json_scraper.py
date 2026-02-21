
import requests
import time
import random

class RedditJSONScraper:
    def __init__(self, user_agent="FacelessVideoStudio/1.0 (Public JSON mode)"):
        self.user_agent = user_agent
        self.headers = {"User-Agent": self.user_agent}

    def get_top_posts(self, subreddit_name="AskReddit", time_filter="day", limit=5):
        """Fetches posts using the public .json endpoint (No API keys required)."""
        url = f"https://www.reddit.com/r/{subreddit_name}/top.json?t={time_filter}&limit={limit}"
        print(f"[REDDIT JSON] Fetching: {url}")
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 429:
                print("[REDDIT JSON] Rate limited (429). Try again later or use API keys.")
                return []
            
            response.raise_for_status()
            data = response.json()
            
            posts = []
            children = data.get('data', {}).get('children', [])
            
            for child in children:
                post_data = child.get('data', {})
                content = f"Date: {post_data.get('created_utc')}\nTitle: {post_data.get('title')}\n\n{post_data.get('selftext')}"
                
                posts.append({
                    "source": "Reddit (JSON)",
                    "subreddit": subreddit_name,
                    "title": post_data.get('title'),
                    "author": post_data.get('author'),
                    "url": f"https://reddit.com{post_data.get('permalink')}",
                    "content": content
                })
            
            return posts
        except Exception as e:
            print(f"[REDDIT JSON] Error: {e}")
            return []

    def get_top_post(self, subreddit_name="AskReddit", time_filter="day"):
        posts = self.get_top_posts(subreddit_name, time_filter, limit=1)
        return posts[0] if posts else None
