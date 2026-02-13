
import os
import json
import requests
from datetime import datetime, timedelta

class ContentCalendar:
    def __init__(self, api_key=None, config=None):
        self.api_key = api_key
        self.config = config
        self.calendar_path = os.path.join("config", "content_calendar.json")

    def generate_weekly_plan(self):
        """Uses AI to plan a strategic week of content based on active niches."""
        if not self.api_key:
            return []

        active_niches = list(self.config.NICHES.keys())
        prompt = f"""Create a week-long content calendar (7 days) for a faceless video studio.
        Active Niches: {active_niches}. 
        For each day, provide:
        - Day (e.g., Monday)
        - Niche
        - Viral Topic Idea
        - Aesthetic Style
        
        Return the result as a JSON array of objects.
        """

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": { "type": "json_object" }
                }
            )
            response.raise_for_status()
            plan_data = json.loads(response.json()['choices'][0]['message']['content'])
            
            # Save the plan
            with open(self.calendar_path, 'w') as f:
                json.dump(plan_data, f, indent=4)
            
            return plan_data
        except Exception as e:
            print(f"Failed to generate calendar: {e}")
            return None

    def get_current_plan(self):
        if os.path.exists(self.calendar_path):
            with open(self.calendar_path, 'r') as f:
                return json.load(f)
        return None
