# Hugging Face Spaces - Step-by-Step Setup

## What to Fill in Each Field

### 1. Owner
```
anany29
```
✅ Already filled (your username)

---

### 2. Space Name
```
visionguard
```
**What to type:** `visionguard`

This becomes your URL:
```
https://anany29-visionguard.hf.space
```

---

### 3. Short Description
```
AI-powered surveillance system with real-time face detection, PPE compliance checking, and box counting using computer vision.
```

**Copy-paste exactly this:**

> Intelligent Surveillance System powered by Computer Vision. Features: Face Detection & Recognition, PPE Safety Compliance (Helmet, Vest, Gloves, Boots), and Box Counting for inventory management.

---

### 4. License
Select from dropdown:
```
apache-2.0
```

---

### 5. Select the Space SDK
```
Docker
```

**Click the "Docker" option** (NOT Gradio, NOT Static)

---

### 6. Choose a Docker Template
Select:
```
Blank
```

(or the first/default option - it doesn't matter since we have our own Dockerfile)

---

### 7. Space Hardware
```
Free
```

✅ Already selected correctly (2 CPU, 16GB RAM actually - more than enough!)

---

### 8. Storage Bucket
Leave this **BLANK/UNCHECKED**

You don't need external storage - everything is in your repo.

---

### 9. Space Dev Mode
Leave **DISABLED/UNCHECKED**

This is a PRO feature. You don't need it.

---

### 10. Visibility
Select:
```
Public
```

**Why Public:** Anyone with the URL can use your app (your professor). The code is also visible.

---

## After Creating the Space

### Step 1: Upload Your Files

After clicking **Create Space**, you'll see a file browser.

**Method A: Drag & Drop (Easiest)**
1. Open File Explorer on your laptop
2. Go to `e:/app/surveillance/`
3. Select ALL files and folders
4. Drag and drop into the Hugging Face file browser

**Method B: Upload Button**
1. Click **"Add file"** → **"Upload files"**
2. Select all files from `e:/app/surveillance/`

### Step 2: Wait for Build

- Click **"Commit changes to main"**
- Hugging Face will start building your Docker image
- Go to the **"Logs"** tab to watch progress
- First build takes **10-20 minutes** (downloads PyTorch, etc.)
- You'll see: `Build successful` when done

### Step 3: Access Your App

- Go to the **"App"** tab
- Or visit: `https://anany29-visionguard.hf.space`
- Your app is live! 🎉

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | Check Logs tab for error message |
| Timeout during build | Normal for ML apps, just wait |
| App says "Starting" | First load takes 30-60 seconds |
| 404 error | Wait 2-3 more minutes for build |

---

## Your Final URL

```
https://anany29-visionguard.hf.space
```

**Share this with your professor!**

---

## Quick Reference Card

| Field | Value |
|-------|-------|
| Owner | anany29 |
| Space Name | visionguard |
| Description | AI-powered surveillance system with real-time face detection, PPE compliance checking, and box counting using computer vision. |
| License | apache-2.0 |
| SDK | Docker |
| Template | Blank |
| Hardware | Free |
| Storage | None |
| Dev Mode | Disabled |
| Visibility | Public |
