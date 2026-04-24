# Koyeb Deployment Guide (EASIEST Option)

## Why Koyeb?
- ✅ **2GB RAM** (same as Hugging Face)
- ✅ **FREE forever** (3 apps)
- ✅ **Connects to GitHub directly** — just click, no file uploads!
- ✅ **Auto-detects Python** — no Docker needed!

---

## Step-by-Step (5 Minutes)

### Step 1: Sign Up
1. Go to https://app.koyeb.com
2. Click **"Sign up with GitHub"**
3. Authorize Koyeb to access your repos

---

### Step 2: Create App
1. Click the big **"+"** button or **"Create App"**
2. Select **"GitHub"** as source
3. You'll see your repos listed

---

### Step 3: Select Your Repo

| Field | What to Select |
|-------|---------------|
| **Repository** | `anany2905/visionguard-surveillance` |
| **Branch** | `main` |

---

### Step 4: Configure Build

Koyeb auto-detects Python. Just verify these settings:

| Field | Value |
|-------|-------|
| **Builder** | `Buildpack` (auto-selected) |
| **Build command** | `pip install -r requirements.txt` |
| **Run command** | `gunicorn backend.app:app --bind 0.0.0.0:8000` |

---

### Step 5: Select Instance Type

Scroll down to **"Instance type"**:

1. Click **"Free"** (2GB RAM, 1 vCPU)
2. This is the free tier — enough for your ML models!

---

### Step 6: Add Environment Variable

Click **"Advanced"** → **"Add variable"**:

| Key | Value |
|-----|-------|
| `PORT` | `8000` |

---

### Step 7: Name Your App

| Field | Value |
|-------|-------|
| **App name** | `visionguard` |

Your URL will be:
```
https://visionguard-yourusername.koyeb.app
```

---

### Step 8: Deploy!

Click the **"Deploy"** button!

Wait **5-10 minutes** for:
1. Installing Python dependencies
2. Downloading ML models
3. Starting the server

---

### Step 9: Check Status

1. Go to your app dashboard
2. Click on **"visionguard"**
3. Check the **"Logs"** tab
4. Look for: `Running on http://0.0.0.0:8000`

---

### Step 10: Open Your App

Click the **"URL"** link at the top, or visit:
```
https://visionguard-yourusername.koyeb.app
```

---

## 🎉 Done!

Your app is live with:
- ✅ 2GB RAM (models load properly)
- ✅ Free forever
- ✅ HTTPS URL for your professor

---

## If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| Build fails | Check Logs tab for error |
| "Health check failed" | Wait 2-3 more minutes |
| App crashes | Make sure you selected **Free** (2GB) instance |
| 502 error | Restart deployment from dashboard |

---

## Compare: Koyeb vs Hugging Face

| | Koyeb | Hugging Face |
|--|-------|--------------|
| **Setup** | Connect GitHub repo ✅ | Upload files manually |
| **Ease** | Just click Deploy ✅ | Need to understand Docker |
| **RAM** | 2GB ✅ | 2GB ✅ |
| **Price** | Free ✅ | Free ✅ |
| **Best for** | Beginners ✅ | ML researchers |

---

## Quick Start Summary

1. https://app.koyeb.com → Sign up with GitHub
2. Create App → GitHub → Select `visionguard-surveillance`
3. Build: `pip install -r requirements.txt`
4. Run: `gunicorn backend.app:app --bind 0.0.0.0:8000`
5. Instance: **Free** (2GB)
6. Add env: `PORT=8000`
7. Click **Deploy**
8. Wait 5-10 minutes
9. Done! 🎉
