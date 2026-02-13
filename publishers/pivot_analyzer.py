
import requests

class PivotAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def analyze_pivot_opportunity(self, current_stats, trending_news):
        """Analyzes viral performance vs. world trends to suggest a strategic niche pivot."""
        if not self.api_key:
            return {
                "current_niche": "Finance",
                "recommended_pivot": "AI Sovereignty",
                "rationale": "High viral coefficient in tech news vs. plateauing finance engagement.",
                "confidence": "85%"
            }

        prompt = f"""
        Current Studio Performance: {current_stats}
        Global Trending News: {trending_news}
        
        Analyze the data and recommend a 'Strategic Niche Pivot'.
        1. Identify if the current niche is 'Saturated', 'Stable', or 'Declining'.
        2. Suggest a 'High-Growth Sub-Niche' that aligns with current viral coefficients.
        3. Provide a 'Rationale' based on the intersection of world pulse and studio health.
        
        Return JSON with keys: [sentiment, recommended_pivot, rationale, confidence_score].
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
            print(f"Pivot analysis failed: {e}")
            return {"error": "Analysis offline."}
