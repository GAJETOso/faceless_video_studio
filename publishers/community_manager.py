
import requests

class CommunityManager:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def draft_community_package(self, topic, script):
        """Generates a high-engagement community tab package (Polls, Teasers, Questions)."""
        if not self.api_key:
            return {
                "poll": "Which part of this mystery shocked you most?",
                "teaser": "New deep dive coming soon. Stay tuned.",
                "engagement_question": "What should we cover next?"
            }

        prompt = f"""
        Topic: {topic}
        Context: {script[:1000]}
        
        Generate a 'Viral Community Package' for YouTube/TikTok Community tabs:
        1. RELEVANT POLL: A 4-option poll that sparks debate related to the topic.
        2. CURIOSITY TEASER: A short, high-stakes text update that opens a loop about the next video.
        3. PERSPECTIVE QUESTION: A deep, value-based question to drive 50+ comments.
        
        Return JSON with keys: [poll_question, poll_options, teaser, engagement_question].
        """

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            # In a real scenario, use json.loads. Mocking here.
            content = response.json()['choices'][0]['message']['content']
            return content
        except Exception as e:
            print(f"Community drafting failed: {e}")
            return {"status": "error", "message": str(e)}
