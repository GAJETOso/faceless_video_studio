
import requests
from bs4 import BeautifulSoup

class NairalandScraper:
    def __init__(self):
        self.base_url = "https://www.nairaland.com"

    def get_trending_topics(self, limit=5):
        """Scrapes trending topics from Nairaland homepage."""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract links from the "Latest News" or relevant section
            # Nairaland structure is usually table-based.
            links = []
            
            # Example selector - needs verification
            for link in soup.select('td.bold a')[:limit]:
                href = link.get('href')
                if href.startswith("/"):
                    href = self.base_url + href
                links.append({
                    "title": link.text,
                    "url": href
                })
            
            return links
        except Exception as e:
            print(f"Error scraping Nairaland: {e}")
            return []

    def get_post_content(self, url):
        """Scrapes the content of a specific post."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main post content
            # Usually the first post in the thread
            post_body = soup.find('div', class_='narrow')
            if post_body:
                return post_body.get_text(strip=True)
            return ""
        except Exception as e:
            print(f"Error reading post content: {e}")
            return ""
