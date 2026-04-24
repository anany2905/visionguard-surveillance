# VisionGuard - Intelligent Surveillance System

## Overview

VisionGuard is a production-ready AI surveillance system with three core detection capabilities:

1. **Face Detection & Authorization** - Real-time facial recognition with name, ID, and authorization status
2. **PPE Detection** - Safety equipment verification (helmet, vest, gloves, boots)
3. **Box Counting** - Real-time detection and counting of boxes in images and video streams

## Project Structure

```
surveillance/
├── index.html                 # Landing page
├── pages/
│   ├── about.html            # About the project & team
│   ├── services.html         # Interactive detection services
│   └── contact.html          # Contact form & info
├── assets/
│   ├── css/style.css         # Main stylesheet (dark/light mode)
│   ├── js/main.js            # Theme, navigation, utilities
│   ├── js/services.js        # Detection UI & API integration
│   └── js/contact.js         # Contact form handling
├── backend/
│   ├── app.py                # Flask API server
│   └── config.py             # Configuration settings
├── models/
│   ├── face_detection/face_detection_model.py
│   ├── ppe_detection/ppe_detection_model.py
│   └── box_counting/box_counting_model.py
├── face_model/dataset/       # Face recognition dataset
├── ppe_model/best.pt         # YOLO PPE detection weights
├── box_model/best_fixed.pt   # YOLO box counting weights
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment entry point
└── README.md                 # This file
```

## Quick Start

### Local Development

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python backend/app.py
```

The application will be available at `http://localhost:5000`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve frontend |
| `/api/face_detect` | POST | Face detection & recognition |
| `/api/ppe_detect` | POST | PPE compliance detection |
| `/api/box_count` | POST | Box counting |
| `/health` | GET | Health check |

### Request Format

All detection endpoints accept JSON with a base64-encoded image:

```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

## Deployment

### Heroku

```bash
# Login and create app
heroku login
heroku create your-app-name

# Set Python buildpack
heroku buildpacks:set heroku/python

# Push to deploy
git push heroku main
```

### Render

1. Connect your GitHub repository
2. Select "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn backend.app:app`
5. Deploy

### Railway

```bash
railway login
railway init
railway up
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Server port |
| `FLASK_ENV` | `development` | Flask environment |
| `SECRET_KEY` | `change-me-in-production` | Flask secret key |

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Flask (Python)
- **Computer Vision**: OpenCV, YOLOv8 (Ultralytics), DeepFace
- **Deep Learning**: TensorFlow, PyTorch

## Team

- **Anany Kanjolia** - Project Lead & Full Stack
- **Sarvagya** - Box Counting Specialist
- **Shaurya** - Face Detection Specialist
- **Om Nimbalkar** - Research Analyst

## License

Created for educational purposes as a final year project.

