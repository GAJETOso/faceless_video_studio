
import random

class AnalyticsAggregator:
    def __init__(self):
        # Initial health metrics
        self.health = {
            "total_views": 150000,
            "avg_retention": 68.5,
            "viral_coefficient": 1.2,
            "platforms": {
                "youtube": {"views": 45000, "growth": 12},
                "tiktok": {"views": 98000, "growth": 45},
                "instagram": {"views": 7000, "growth": 5}
            }
        }

    def get_studio_health(self):
        """Aggregates metrics from all connected social platforms."""
        # In a real scenario, we'd fetch live data here.
        # For now, we simulate a 'live' pulse by slightly varying the stats on each call
        self._simulate_live_activity()
        return self.health

    def _simulate_live_activity(self):
        """Simulates real-time viewer activity."""
        # Randomly increment views
        new_views = random.randint(5, 50)
        platform = random.choice(list(self.health["platforms"].keys()))
        self.health["platforms"][platform]["views"] += new_views
        self.health["total_views"] += new_views
        
        # Recalculate viral coefficient based on growth momentum
        # Simplified model: Higher growth on TikTok pulls the coefficient up
        tiktok_growth = self.health["platforms"]["tiktok"]["growth"]
        self.health["viral_coefficient"] = round(1.0 + (tiktok_growth / 100), 2)

    def calculate_viral_coefficient(self, video_stats):
        """
        Calculates the Viral Coefficient (K) for a specific video.
        K = (avg_shares * conversion_rate)
        If K > 1, the video is growing exponentially.
        """
        shares = video_stats.get('shares', 0)
        views = video_stats.get('views', 1)
        
        # Estimation: 1 share leads to X new views. 
        # We use a proxy metric here since we don't have deep pixel tracking.
        engagement_rate = (video_stats.get('likes', 0) + video_stats.get('comments', 0)) / views
        
        # Formula: Base K + Engagement Boost
        k_score = (shares / 100) + (engagement_rate * 5)
        return round(k_score, 2)

    def update_metrics(self, new_video_stats):
        """Updates global health based on a new video's initial performance."""
        self.health["total_views"] += new_video_stats.get("views", 0)
        
        # Update specific platform growth
        platform = new_video_stats.get("platform", "youtube")
        if platform in self.health["platforms"]:
            current_views = self.health["platforms"][platform]["views"]
            # Simple growth calc
            growth_bump = (new_video_stats.get("views", 0) / current_views) * 100
            self.health["platforms"][platform]["growth"] += round(growth_bump, 1)

        return self.health
