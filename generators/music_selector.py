
import os
import random

class MusicSelector:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = assets_dir
        self.music_dir = os.path.join(assets_dir, "music")
        if not os.path.exists(self.music_dir):
            os.makedirs(self.music_dir)
            
        # Seed some default categories if they don't exist
        self.categories = {
            "mystery": ["suspense.mp3", "dark_ambient.mp3"],
            "finance": ["inspiring.mp3", "corporate.mp3"],
            "action": ["cinematic_drums.mp3", "high_energy.mp3"],
            "peaceful": ["calm_piano.mp3", "nature.mp3"],
            "rhythm": ["beat_lofi.mp3", "trap_beat.mp3", "cyberpunk_core.mp3"],
            "rnb": ["smooth_rnb.mp3", "soulful_beat.mp3"],
            "rap": ["hard_rap_beat.mp3", "boon_bap.mp3"],
            "afrobeat": ["afro_vibes.mp3", "drum_rhythm_africa.mp3"]
        }

    def select_music(self, tone):
        """Selects the best background music based on the analyzed tone."""
        # Map tone to music category
        mapping = {
            "onyx": "mystery",
            "alloy": "finance",
            "echo": "action",
            "nova": "peaceful",
            "shimmer": "peaceful",
            "fable": "mystery",
            "lyrics": "rhythm",
            "rnb": "rnb",
            "rap": "rap",
            "afrobeat": "afrobeat"
        }
        
        category = mapping.get(tone, "mystery")
        print(f"[MUSIC ENGINE] Mapping tone '{tone}' to category '{category}'")
        
        # In a real setup, we'd list files in the category folder
        # For now, we return a path and the system should ensure music exists
        target_dir = os.path.join(self.music_dir, category)
        if os.path.exists(target_dir):
            files = [f for f in os.listdir(target_dir) if f.endswith('.mp3')]
            if files:
                return os.path.join(target_dir, random.choice(files))
        
        # Fallback to a global music file if specific ones aren't found
        global_music = os.path.join(self.music_dir, "default_background.mp3")
        return global_music if os.path.exists(global_music) else None
