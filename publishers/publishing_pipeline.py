from publishers.social_poster import YouTubeUploader, TikTokUploader

class PublishingPipeline:
    def __init__(self, config):
        self.config = config
        self.youtube = YouTubeUploader()
        self.tiktok = TikTokUploader()

    def publish_video(self, video_path, platforms, metadata):
        """Orchestrates the publishing of a video to selected platforms."""
        results = {}
        
        desc = metadata.get('description', f"New video produced by Matters of Value Studio: {metadata['title']}")
        tags = metadata.get('tags', [])

        if "youtube" in platforms:
            results["youtube"] = self.youtube.upload_video(video_path, metadata['title'], desc, tags)
        
        if "tiktok" in platforms:
            results["tiktok"] = self.tiktok.upload_video(video_path, metadata['title'], desc, tags)
            
        return results
