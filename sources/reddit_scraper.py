import os
from .reddit_json_scraper import RedditJSONScraper

class RedditScraper:
    def __init__(self, client_id=None, client_secret=None, user_agent="FacelessVideoStudio/1.0"):
        self.use_praw = client_id and client_secret and client_id != "your_reddit_client_id"
        
        if self.use_praw:
            print("[REDDIT] Initializing API mode (PRAW)...")
            import praw
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
        else:
            print("[REDDIT] Client keys missing. Initializing Public JSON mode...")
            self.json_scraper = RedditJSONScraper(user_agent=user_agent)

    def get_top_post(self, subreddit_name="AskReddit", time_filter="day"):
        """Fetches the top post from a subreddit."""
        posts = self.get_top_posts(subreddit_name, time_filter, limit=1)
        return posts[0] if posts else None

    def get_top_posts(self, subreddit_name="AskReddit", time_filter="day", limit=5):
        """Fetches multiple top posts from a subreddit."""
        if not self.use_praw:
            return self.json_scraper.get_top_posts(subreddit_name, time_filter, limit)
            
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            for top_post in subreddit.top(time_filter=time_filter, limit=limit):
                content = f"Date: {top_post.created_utc}\nTitle: {top_post.title}\n\n{top_post.selftext}"
                posts.append({
                    "source": "Reddit",
                    "subreddit": subreddit_name,
                    "title": top_post.title,
                    "author": str(top_post.author),
                    "url": top_post.url,
                    "content": content
                })
            return posts
        except Exception as e:
            print(f"Error scraping Reddit with PRAW: {e}")
            print("Attempting JSON fallback...")
            fallback = RedditJSONScraper()
            return fallback.get_top_posts(subreddit_name, time_filter, limit)
