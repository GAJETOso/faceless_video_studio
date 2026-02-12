
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from main import FacelessVideoBot

app = FastAPI(title="Values That Matters Studio API")
bot = FacelessVideoBot()

# Serve static files for the dashboard
app.mount("/dashboard", StaticFiles(directory="public", html=True), name="static")

class VideoRequest(BaseModel):
    niche: str
    count: Optional[int] = 1
    style: Optional[str] = "cinematic_documentary"

class ScriptRequest(BaseModel):
    title: str
    script: str
    style: str
    voice: str

@app.get("/")
async def root():
    return {"message": "Values That Matters API is running"}

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
    background_tasks.add_task(
        bot.produce_video, 
        title=request.title, 
        script_content=request.script, 
        style=request.style, 
        voice=request.voice
    )
    return {"status": "Custom production started"}

@app.get("/api/video/download/{filename}")
async def download_video(filename: str):
    file_path = os.path.join(bot.config.OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
