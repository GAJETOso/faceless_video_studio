
# Faceless Video Studio

A powerful automation tool to generate faceless videos from Reddit, Nairaland, and other sources, complete with voiceovers, background music, and automatic editing.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: You also need ImageMagick installed and configured for MoviePy to handle text overlays.*

2. **Configure API Keys**
   Open `config/settings.py` or set environment variables for:
   - `OPENAI_API_KEY`: For script generation.
   - `PEXELS_API_KEY`: For background video footage.
   - `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`: For Reddit sourcing.
   - Social Media Keys (Optional for auto-posting).

3. **Prepare Assets**
   Place your default assets in `faceless_video_studio/assets/`:
   - `intro.mp4`: A short intro video (optional).
   - `background_music.mp3`: Background music track (optional).
   - *Note: If these are missing, the video will be generated without them.*

## Usage

### Run Default (Reddit)
```bash
python main.py
```

### Run Specific Mode
```bash
python main.py reddit "AskReddit"
python main.py nairaland "romance"
```

## Features
- **Multi-Source**: Scrape Reddit, Nairaland, or easily add more.
- **Smart Editing**: Auto-mixes voiceover with ducked background music.
- **Intro Support**: Prepend your brand intro automatically.
- **Multi-Publish**: Architecture ready for YouTube, TikTok, Instagram, and Drive.

## Directory Structure
- `config/`: Settings and keys.
- `sources/`: Scrapers for different platforms.
- `generators/`: Logic for script, voice, and media fetching.
- `editor/`: Video processing and assembly.
- `publishers/`: Social media uploaders.
- `assets/`: Your media library.
