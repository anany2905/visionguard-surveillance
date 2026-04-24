# Free Deployment Platforms with Enough RAM for ML Models

## Why Render Fails
- Render Free: **512 MB RAM** ❌
- Your models need: **~1.5 GB RAM** 
- Result: Server crashes with 502 error

---

## ✅ Option 1: Hugging Face Spaces (BEST - 2GB RAM)

| Feature | Details |
|---------|---------|
| **RAM** | **2 GB** ✅ |
| **Price** | **FREE forever** ✅ |
| **Setup** | Easy (Docker) |
| **URL** | `https://yourname-visionguard.hf.space` |

### Deploy Now:
1. Go to https://huggingface.co/join → Sign up
2. Go to https://huggingface.co/new-space
3. Name: `visionguard`
4. SDK: **Docker**
5. Upload ALL files from `surveillance/` folder
6. Click **Create** → Wait 10-15 minutes
7. Done! Your app is live.

**Files already prepared:** `Dockerfile`, `README_HF.md`

---

## ✅ Option 2: Koyeb (2GB RAM)

| Feature | Details |
|---------|---------|
| **RAM** | **2 GB** ✅ |
| **Price** | **FREE** (3 apps) |
| **Setup** | GitHub connect |

### Deploy:
1. Go to https://app.koyeb.com → Sign up with GitHub
2. Click **Create App** → **GitHub**
3. Select your repo: `anany2905/visionguard-surveillance`
4. Branch: `main`
5. Build command: `pip install -r requirements.txt`
6. Run command: `gunicorn backend.app:app --bind 0.0.0.0:8000`
7. Instance type: **Free (2GB RAM)**
8. Click **Deploy**

---

## ✅ Option 3: Google Cloud Run ($300 Free Credit)

| Feature | Details |
|---------|---------|
| **RAM** | Up to **32 GB** |
| **Price** | **$300 free** for 90 days |
| **Setup** | Medium |

### Deploy:
```bash
# 1. Install Google Cloud SDK
# 2. Login
gcloud auth login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID

# 4. Deploy
gcloud run deploy visionguard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 300
```

**Note:** Requires credit card (won't be charged with free tier)

---

## ✅ Option 4: Railway ($5 Free Credit)

| Feature | Details |
|---------|---------|
| **RAM** | **2 GB** |
| **Price** | $5 free credit, then ~$5/month |
| **Setup** | Very Easy |

### Deploy:
1. Go to https://railway.app → Sign up with GitHub
2. Click **New Project** → **Deploy from GitHub repo**
3. Select `anany2905/visionguard-surveillance`
4. Add environment variable: `PORT=5000`
5. Railway auto-detects Python and installs requirements
6. Click **Deploy**

---

## ✅ Option 5: Fly.io ($5 Free Credit)

| Feature | Details |
|---------|---------|
| **RAM** | **256 MB** (Free) / **1GB** ($1.94/mo) |
| **Price** | $5 free credit |
| **Setup** | Medium |

### Deploy:
```bash
# Install flyctl
# Login
flyctl auth login

# Launch
flyctl launch --name visionguard

# Deploy
flyctl deploy
```

---

## 🏆 RECOMMENDATION

| Use Case | Platform | Why |
|----------|----------|-----|
| **Quick demo** | **Hugging Face** | 2GB RAM, truly free, no credit card |
| **Long-term** | **Koyeb** | 2GB RAM, 3 free apps forever |
| **Professional** | **Google Cloud** | $300 credit, scales to production |

---

## 🚀 My Pick: Hugging Face Spaces

I already created `Dockerfile` and `README_HF.md`. Just:

1. Go to https://huggingface.co/new-space
2. Select **Docker**
3. Drag-drop all files from `e:/app/surveillance/`
4. Wait for build
5. **Done!**

Your app will be at: `https://yourusername-visionguard.hf.space`
