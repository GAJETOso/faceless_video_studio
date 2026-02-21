
import requests

class IntroHookGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def generate_cgi_hook(self, topic):
        """Generates a high-quality visual prompt for an ultra-high-stakes 5-second CGI intro."""
        if not self.api_key:
            return "A golden futuristic vault opening in deep space, hyper-realistic, 8k."

        prompt = f"""
        Topic: {topic}
        
        Task: Design a 5-second 'Super Hook' CGI intro concept.
        1. VISUAL: Describe a hyper-realistic, cinematic visual (CGI style).
        2. SFX: Recommend high-stakes sound effects (e.g., 'Deep cinematic thud', 'Digital shimmer').
        3. OVERLAY: A powerful 3-word title overlay.
        
        Return a 'Visual Prompt' that can be used for AI Video/Image generation.
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
            return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Intro hook generation failed: {e}")
            return f"Cinematic landscape of {topic}, atmospheric lightning, 4k."
