
# Faceless Video Studio: Operational Roadmap

To make this studio **fully operational**, the following steps are required.

## 1. API Credentials & Configuration
Most modules are built to work with external APIs. You need to provide valid keys in `config/settings.json`:
- **OpenAI API Key**: Used for script writing, tone analysis, and AI image synthesis.
- **Pexels API Key**: Crucial for fetching high-quality stock video footage.
- **Reddit/Nairaland Auth**: Credentials to scrape trending topics automatically.
- **YouTube/TikTok/Instagram APIs**: Client secrets and OAuth tokens for automated publishing.

## 2. System Dependencies
- **ImageMagick**: MoviePy (the video engine) requires ImageMagick installed on Windows to render text overlays. You must set the path to the ImageMagick binary in your environment or MoviePy config.
    *   *Tip: Set the `IMAGEMAGICK_BINARY` environment variable to the path of `magick.exe` (e.g., `C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe`).*
- **FFmpeg**: Ensure FFmpeg is in your system PATH for video encoding.

## 3. Missing Infrastructure (Placeholders)
- [x] **Reddit JSON Scraper**: (Just Added) The bot now works for Reddit content WITHOUT needing API keys!
- [x] **Repurposing Engine**: (Just Added) Logic to split long-form content into viral Shorts.
- [ ] **Social Poster Implementations**: Currently, `publishers/social_poster.py` contains simulations. Real API integration code for each platform needs to be finalized.
- [ ] **Asset Library**: You should populate `assets/music/` and `assets/stock/` with premium licensed content to fallback on when API results are low.

## 4. UI/UX Dashboard
- The current `public/index.html` is a static placeholder. A full React/Vite or Next.js dashboard would be ideal for monitoring render queues and publishing stats.

## 5. Song & Music Video Process
- [ ] **Music Studio**: (In Progress) A separate process to generate lyrics and produce rhythmic music videos.

---

### Recently Completed:
- Added `RepurposingEngine` to identify viral segments.
- Integrated `RepurposingEngine` into the main `FacelessVideoBot`.
