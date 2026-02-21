# Values That Matters - Cloud Deployment Guide

This guide explains how to deploy your Professional AI Documentary Studio to the cloud using **Railway.app**.

## 1. Prepare Your Repository
1. Create a new **Private** repository on GitHub.
2. Push your code to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial studio setup"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

## 2. Deploy to Railway
1. Go to [Railway.app](https://railway.app/) and sign in with GitHub.
2. Click **"New Project"** > **"Deploy from GitHub repo"**.
3. Select your `faceless_video_studio` repository.
4. Click **"Deploy Now"**.

## 3. Configure Environment Variables
Once the project is created, go to the **Variables** tab in Railway and add the following:
- `OPENAI_API_KEY`: Your OpenAI key (for scripts and pro voices).
- `PEXELS_API_KEY`: Your Pexels key (for cinematic footage).
- `REDDIT_CLIENT_ID`: (Optional) For auto-discovery.
- `REDDIT_CLIENT_SECRET`: (Optional).

## 4. How to Run Batches in the Cloud
By default, the `Dockerfile` is set to run a Mystery discovery. To run a specific command (like a Finance batch):
1. Go to the **Settings** tab in Railway.
2. Find the **Deploy** section > **Start Command**.
3. Change it to: `python main.py niche finance 5 --no-review`
4. Railway will redeploy and run that batch immediately.

## 5. Downloading Your Videos
After a run completes, your videos will be in the `/output` folder.
- **Option 1**: Check the `publishers/drive_uploader.py` if you have Google Drive sync enabled.
- **Option 2**: Use the Railway CLI to download the folder: `railway volume download output`.

---

*Tip: For 24/7 automation, you can use the **Cron** setting in Railway to trigger these commands daily.*
