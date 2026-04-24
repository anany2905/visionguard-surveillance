---
title: VisionGuard Surveillance
emoji: 🛡️
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
---

# VisionGuard - Free Deployment on Hugging Face Spaces

## Why Hugging Face Spaces?

| Feature | Render Free | Hugging Face Free |
|---------|-------------|-------------------|
| **RAM** | 512 MB | **2 GB** ✅ |
| **Disk** | 512 MB | **20 GB** ✅ |
| **Timeout** | 15 min | **24 hours** ✅ |
| **Custom Domain** | ❌ | ✅ |
| **ML Models** | May OOM | **Works perfectly** ✅ |

## Deployment Steps

### 1. Create Hugging Face Account
- Go to https://huggingface.co/join
- Sign up (free, no credit card)

### 2. Create New Space
1. Go to https://huggingface.co/new-space
2. Space name: `visionguard` (or your choice)
3. Select **Docker** as SDK
4. Visibility: **Public**
5. Click **Create Space**

### 3. Upload Code
In your new Space, click **Files** → **Upload files**:
- Upload all files from this `surveillance/` folder
- Or use Git:
  ```bash
  git clone https://huggingface.co/spaces/YOUR_USERNAME/visionguard
  cd visionguard
  # Copy all files from your surveillance/ folder here
  git add .
  git commit -m "Initial deployment"
  git push
  ```

### 4. Wait for Build
- Hugging Face will automatically build the Docker image
- First build takes ~10-15 minutes (downloads ML libraries)
- Watch progress in the **Logs** tab

### 5. Access Your App
- URL: `https://YOUR_USERNAME-visionguard.hf.space`
- The app will be live 24/7 on the free tier!

## Troubleshooting

### Build fails with timeout
- Hugging Face free tier builds have a 1-hour limit
- If it times out, try removing version pins from requirements.txt
- Or upgrade to **Pro** ($9/month) for longer builds

### Models not loading
- Check **Logs** tab for error messages
- The Dockerfile installs all system dependencies OpenCV needs
- 2GB RAM is enough for all 3 models

### App is slow on first request
- First request loads ML models into memory
- Subsequent requests are fast
- This is normal for ML apps

## Local Testing (Docker)

```bash
cd surveillance
docker build -t visionguard .
docker run -p 7860:7860 visionguard
```

Visit: http://localhost:7860
