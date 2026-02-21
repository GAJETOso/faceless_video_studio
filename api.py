
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from main import FacelessVideoBot

app = FastAPI(title="Matters of Value Studio API")
bot = FacelessVideoBot()

# Serve static files for the dashboard
app.mount("/dashboard", StaticFiles(directory="public", html=True), name="static")
# Serve video outputs for the Cinema Feed
app.mount("/exports", StaticFiles(directory="output"), name="exports")

class VideoRequest(BaseModel):
    niche: str
    count: Optional[int] = 1
    style: Optional[str] = "cinematic_documentary"

class ScriptRequest(BaseModel):
    title: str
    script: Optional[str] = ""
    style: str
    voice: str
    structure: Optional[str] = "cinematic"
    generate_thumb: Optional[bool] = True
    enhance_script: Optional[bool] = False
    publish: Optional[bool] = False
    vertical: Optional[bool] = False

class ConceptRequest(BaseModel):
    title: str
    concept: str
    style: Optional[str] = "cinematic_documentary"
    duration_minutes: Optional[int] = 2

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

@app.post("/api/script/from-concept")
async def script_from_concept(request: ConceptRequest):
    """Generates a full production script from a free-form creative brief/concept."""
    script = bot.script_engine.generate_from_concept(
        title=request.title,
        concept=request.concept,
        style=request.style,
        duration_minutes=request.duration_minutes
    )
    return {"title": request.title, "script": script, "style": request.style}

@app.get("/api/settings")
async def get_settings():
    return bot.config.defaults # Returns all keys with current values

@app.post("/api/settings")
async def update_settings(settings: dict):
    bot.config.update(settings)
    # Re-initialize bot modules with new keys
    bot.__init__() 
    return {"status": "Settings updated and engine re-initialized"}

@app.get("/api/videos")
async def list_videos():
    """Lists all produced videos in the output directory."""
    output_dir = bot.config.OUTPUT_DIR
    if not os.path.exists(output_dir):
        return []
    
    videos = []
    for f in os.listdir(output_dir):
        if f.endswith(".mp4"):
            videos.append({
                "name": f,
                "path": f"/api/video/download/{f}",
                "size": os.path.getsize(os.path.join(output_dir, f))
            })
    return videos

@app.post("/api/produce/niche")
async def produce_niche(request: VideoRequest, background_tasks: BackgroundTasks):
    """Triggers the niche autopilot pipeline."""
    # We run it in the background as video production takes time
    background_tasks.add_task(bot.run_niche_pipeline, niche=request.niche, count=request.count, interactive=False)
    return {"status": "Production started on autopilot", "niche": request.niche}

@app.post("/api/produce/custom")
async def produce_custom(request: ScriptRequest, background_tasks: BackgroundTasks):
    """Triggers production with a custom script."""
    # If script is empty, generate it using the selected structure
    script_content = request.script
    if not script_content:
        script_content = bot.script_engine.generate_script(topic=request.title, style=request.style, structure=request.structure)
    
    background_tasks.add_task(
        bot.produce_video, 
        title=request.title, 
        script_content=script_content, 
        style=request.style, 
        voice=request.voice,
        generate_thumb=request.generate_thumb,
        enhance_script=request.enhance_script,
        publish=request.publish,
        vertical=request.vertical
    )
    return {"status": "Custom production started"}

@app.post("/api/produce/long")
async def produce_long(request: ScriptRequest, background_tasks: BackgroundTasks):
    """Triggers long-form chapter-based documentary production."""
    # If script is empty, generate it using the selected structure
    script_content = request.script
    if not script_content:
        script_content = bot.script_engine.generate_script(topic=request.title, style=request.style, structure=request.structure)

    background_tasks.add_task(
        bot.produce_long_form, 
        title=request.title, 
        full_script=script_content, 
        style=request.style, 
        voice=request.voice,
        generate_thumb=request.generate_thumb,
        enhance_script=request.enhance_script,
        publish=request.publish
    )
@app.get("/api/calendar/current")
async def get_calendar():
    "Returns the current AI-generated content plan."
    plan = bot.calendar.get_current_plan()
    return plan or {"message": "No active plan found"}

@app.post("/api/calendar/generate")
async def generate_calendar():
    "Triggers the AI to generate a new 7-day content schedule."
    plan = bot.calendar.generate_weekly_plan()
    return {"status": "Weekly plan generated", "plan": plan}

@app.post("/api/produce/intl")
async def produce_intl(request: ScriptRequest, background_tasks: BackgroundTasks):
    "Generates international dubbed versions of the video."
    background_tasks.add_task(bot.produce_dubbed_variants, title=request.title, script_content=request.script)
    return {"status": "International dubbing sequence initiated (5+ languages)"}

@app.post("/api/produce/test")
async def produce_test(request: ScriptRequest, background_tasks: BackgroundTasks):
    "Tests every possible demographic angle/hook for a topic."
    background_tasks.add_task(bot.run_angle_test, topic=request.title)
    return {"status": "Angle-Testing & Demographic Optimization initiated"}

@app.post("/api/produce/bulk")
async def produce_bulk(background_tasks: BackgroundTasks):
    "Triggers background render for the entire weekly calendar."
    background_tasks.add_task(bot.run_bulk_production)
    return {"status": "Bulk production for weekly calendar initiated"}

from publishers.analytics_aggregator import AnalyticsAggregator
aggregator = AnalyticsAggregator()

@app.get("/api/analytics/health")
async def get_analytics_health():
    "Returns aggregated cross-platform studio health metrics."
    return aggregator.get_studio_health()

@app.get("/api/analytics/pivot")
async def get_strategic_pivot():
    "Recommends a niche shift based on viral coefficients and world trends."
    health = aggregator.get_studio_health()
    return bot.get_strategic_pivot(health)

@app.post("/api/produce/intro-hook")
async def generate_intro_hook(request: dict):
    "Designs a high-impact CGI-style intro hook for a topic."
    topic = request.get("topic")
    design = bot.intro_engine.generate_cgi_hook(topic)
    return {"design": design}

@app.post("/api/analytics/simulate-video-launch")
async def simulate_video_launch(request: dict):
    "Simulates the launch of a video and updates studio metrics."
    # Mock stats for a new "viral" video
    platform = request.get("platform", "tiktok")
    views = request.get("views", 5000)
    shares = request.get("shares", 200)
    likes = request.get("likes", 1500)
    comments = request.get("comments", 300)
    
    video_stats = {
        "platform": platform,
        "views": views,
        "shares": shares,
        "likes": likes,
        "comments": comments
    }
    
    # Update global health
    new_health = aggregator.update_metrics(video_stats)
    
    # Calculate specific K-score for this video
    k_score = aggregator.calculate_viral_coefficient(video_stats)
    
    return {
        "status": "Video Launch Simulated",
        "video_k_score": k_score,
        "new_studio_health": new_health
    }

@app.post("/api/produce/series-plan")
async def plan_series(request: dict):
    "Generates a 3-Part Documentary Trilogy plan."
    topic = request.get("topic")
    plan = bot.generate_series_plan(topic)
    return {"plan": plan}

@app.post("/api/produce/thumbnail-ab")
async def test_thumbnail_ab(request: dict):
    "Generates two distinct thumbnail concepts for A/B testing."
    topic = request.get("topic")
    concepts = bot.get_thumbnail_ab(topic)
    return {"concepts": concepts}

@app.post("/api/monetization/sponsors")
async def analyze_sponsors(request: dict):
    "Analyzes the script for optimal sponsor integration spots."
    script = request.get("script")
    spots = bot.analyze_for_sponsors(script)
    return {"spots": spots}

@app.post("/api/distribution/repurpose")
async def repurpose_content(request: dict):
    "Identifies viral segments for Shorts/Reels repurposing."
    script = request.get("script")
    shorts = bot.analyze_for_repurposing(script)
    return {"shorts": shorts}

@app.post("/api/personalization/clone-voice")
async def clone_voice(request: dict):
    "Clones a voice or lists available cloned voices."
    action = request.get("action")
    name = request.get("name")
    sample_path = request.get("sample_path")
    result = bot.manage_voice_cloning(action, name, sample_path)
    return result

@app.post("/api/distribution/publish")
async def publish_video(request: dict):
    "Publishes a video to selected platforms."
    video_path = request.get("video_path")
    platforms = request.get("platforms", ["youtube", "tiktok"])
    metadata = request.get("metadata", {"title": "New Video"})
    result = bot.orchestrate_publishing(video_path, platforms, metadata)
    return result

@app.post("/api/engage/comment")
async def engage_comment(request: dict):
    "Generates a strategic AI response to a viewer comment."
    topic = request.get("topic")
    script = request.get("script")
    comment = request.get("comment")
    response = bot.auto_respond_to_viewer(topic, script, comment)
    return {"reply": response}

@app.post("/api/community/draft")
async def draft_community(request: dict):
    "Generates a viral engagement kit for social community tabs."
    topic = request.get("topic")
    script = request.get("script")
    kit = bot.generate_community_kit(topic, script)
    return {"kit": kit}

@app.get("/api/news/trending")
async def get_news_trending():
    "Returns AI-curated news opportunities from the World Pulse engine."
    return bot.get_trending_opportunities()

from music_studio import MusicStudio
studio_engine = MusicStudio()

@app.post("/api/produce/music")
async def produce_music(request: dict, background_tasks: BackgroundTasks):
    "Triggers the Music Studio to generate a song and music video."
    topic = request.get("topic")
    genre = request.get("genre", "hip-hop")
    background_tasks.add_task(studio_engine.produce_music_video, topic=topic, genre=genre)
    return {"status": "Music video production started in the background"}
@app.get("/api/video/download/{filename}")
async def download_video(filename: str):
    file_path = os.path.join(bot.config.OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
