# VisionGuard - Professor Demo Guide

## ⚡ QUICK START (For Your Laptop)

### Option A: Local Only (Fastest)
```bash
# Double-click this file:
start.bat
```
- Opens browser automatically at `http://localhost:5000`
- Works instantly, no internet needed for you

### Option B: Share with Professor (Recommended)
```bash
# 1. Install ngrok first (one-time):
#    Download from https://ngrok.com/download
#    Extract ngrok.exe to this folder

# 2. Double-click:
start_with_ngrok.bat
```
- Shows a public URL like `https://abc123.ngrok-free.app`
- Professor can open this on their phone/laptop
- Works from anywhere

---

## 📱 What Your Professor Will See

1. **Home Page** - Beautiful landing with dark/light mode
2. **Services Page** - 3 detection cards:
   - Face Detection (live camera + upload)
   - PPE Detection (helmet, vest, gloves, boots)
   - Box Counting (inventory counting)
3. **About Page** - Team info and tech stack
4. **Contact Page** - Working contact form

---

## 🎯 Demo Script (2-3 minutes)

1. **Open Services page**
2. **Click PPE Detection card** → "Upload Image"
3. **Upload a photo** of someone wearing a helmet
4. **Watch real-time detection** with checkmarks ✅
5. **Show Box Counting** with a warehouse image
6. **Show Face Detection** with team member photos

---

## 🛠️ If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| "Python not found" | Install from https://python.org |
| "Module not found" | Delete `venv` folder, re-run `start.bat` |
| Port 5000 in use | Close other apps, or change port in `backend/app.py` |
| ngrok not working | Check internet connection, restart `start_with_ngrok.bat` |

---

## 📁 Project Files

```
surveillance/
├── start.bat              ← Double-click to run locally
├── start_with_ngrok.bat   ← Double-click to share
├── backend/app.py         ← Flask server
├── pages/services.html    ← Detection UI
├── assets/js/services.js  ← API calls
├── ppe_model/best.pt      ← PPE detection model
├── box_model/best_fixed.pt ← Box counting model
└── face_model/dataset/    ← Face recognition data
```

---

## 🎓 Submission Ready

✅ All code is in the `surveillance/` folder  
✅ GitHub repo: https://github.com/anany2905/visionguard-surveillance  
✅ Runs on your laptop with one double-click  
✅ Can be shared via ngrok for remote viewing  
✅ All 3 ML models work (tested locally)

**For online deployment**, use Hugging Face Spaces (2GB RAM, free):
- See `README_HF.md` for instructions
