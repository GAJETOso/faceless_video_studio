
import requests
import json

class SeriesPlanner:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def plan_trilogy(self, topic):
        """Generates a cohesive 3-part documentary arc for a single topic."""
        if not self.api_key:
            return {
                "part_1": {"title": f"{topic}: The hidden Beginning", "synopsis": "Uncovering the origin..."},
                "part_2": {"title": f"{topic}: The Crisis", "synopsis": "When everything went wrong..."},
                "part_3": {"title": f"{topic}: The Aftermath", "synopsis": "What remains today..."}
            }

        prompt = f"""
        Topic: {topic}
        
        Task: Design a 3-Part Documentary Series Arc (Netflix Style).
        The goal is high binge-ability. Each part must end on a cliffhanger leading to the next.
        
        Structure:
        1. PART 1: The Setup / The Mystery (High Curiosity)
        2. PART 2: The Conflict / The Deep Dive (High Stakes/Emotion)
        3. PART 3: The Resolution / The Future (High Impact)
        
        Return JSON with keys: 'part_1', 'part_2', 'part_3'.
        Each part should have 'title' and 'synopsis'.
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
            content = response.json()['choices'][0]['message']['content']
            # Sanitize json string if needed (simple strip)
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
        except Exception as e:
            print(f"Series planning failed: {e}")
            return {
                "part_1": {"title": f"Part 1: {topic}", "synopsis": "Introduction..."},
                "part_2": {"title": f"Part 2: {topic}", "synopsis": "Development..."},
                "part_3": {"title": f"Part 3: {topic}", "synopsis": "Conclusion..."}
            }
