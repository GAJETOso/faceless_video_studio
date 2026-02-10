
import os
import praw

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def get_top_post(self, subreddit_name="AskReddit", time_filter="day"):
        """Fetches the top post from a subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            top_post = list(subreddit.top(time_filter=time_filter, limit=1))[0]
            
            # Simple content extraction (title + body)
            content = f"Date: {top_post.created_utc}\nTitle: {top_post.title}\n\n{top_post.selftext}"
            
            return {
                "source": "Reddit",
                "subreddit": subreddit_name,
                "title": top_post.title,
                "author": str(top_post.author),
                "url": top_post.url,
                "content": content
            }
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            return None
