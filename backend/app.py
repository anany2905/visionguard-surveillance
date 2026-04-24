from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import cv2
import numpy as np
import sys
import os
import logging
import traceback

# Configure logging for Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import get_config, MODEL_CONFIG

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Log important paths for debugging
logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"Contents of BASE_DIR: {os.listdir(BASE_DIR)}")

# Model paths
ppe_model_path = os.path.join(BASE_DIR, 'ppe_model', 'best.pt')
box_model_path = os.path.join(BASE_DIR, 'box_model', 'best_fixed.pt')
face_dataset_path = os.path.join(BASE_DIR, 'face_model', 'dataset')

logger.info(f"PPE model path: {ppe_model_path} | exists: {os.path.exists(ppe_model_path)}")
logger.info(f"Box model path: {box_model_path} | exists: {os.path.exists(box_model_path)}")
logger.info(f"Face dataset path: {face_dataset_path} | exists: {os.path.exists(face_dataset_path)}")

# Lazy-loaded model instances
_ppe_model = None
_box_model = None
_face_model = None

def get_ppe_model():
    global _ppe_model
    if _ppe_model is None:
        try:
            from models.ppe_detection.ppe_detection_model import PPEDetectionModel
            _ppe_model = PPEDetectionModel(model_path=ppe_model_path)
            logger.info(f"PPE model loaded successfully: {_ppe_model.model is not None}")
        except Exception as e:
            logger.error(f"Failed to load PPE model: {e}")
            logger.error(traceback.format_exc())
            _ppe_model = "ERROR"
    return _ppe_model if _ppe_model != "ERROR" else None

def get_box_model():
    global _box_model
    if _box_model is None:
        try:
            from models.box_counting.box_counting_model import BoxCountingModel
            _box_model = BoxCountingModel(model_path=box_model_path)
            logger.info(f"Box model loaded successfully: {_box_model.model is not None}")
        except Exception as e:
            logger.error(f"Failed to load Box model: {e}")
            logger.error(traceback.format_exc())
            _box_model = "ERROR"
    return _box_model if _box_model != "ERROR" else None

def get_face_model():
    global _face_model
    if _face_model is None:
        try:
            from models.face_detection.face_detection_model import FaceDetectionModel
            _face_model = FaceDetectionModel(dataset_path=face_dataset_path)
            logger.info(f"Face model initialized. Dataset exists: {os.path.exists(face_dataset_path)}")
        except Exception as e:
            logger.error(f"Failed to load Face model: {e}")
            logger.error(traceback.format_exc())
            _face_model = "ERROR"
    return _face_model if _face_model != "ERROR" else None

# ==========================
# Frontend Routes
# ==========================

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'pages'), filename)

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'assets'), filename)

# ==========================
# API Routes
# ==========================

def decode_image(data):
    """Decode base64 image data to OpenCV frame."""
    if not data or 'image' not in data:
        return None, 'No image data provided'
    try:
        image_data = base64.b64decode(data['image'].split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return None, 'Invalid image data'
        return frame, None
    except Exception as e:
        return None, str(e)

@app.route('/api/face_detect', methods=['POST', 'OPTIONS'])
def face_detect():
    if request.method == 'OPTIONS':
        return '', 200
    model = get_face_model()
    if model is None:
        return jsonify({'error': 'Face detection model not available', 'detected': False}), 503
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = model.detect_faces(frame)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Face detection error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/ppe_detect', methods=['POST', 'OPTIONS'])
def ppe_detect():
    if request.method == 'OPTIONS':
        return '', 200
    model = get_ppe_model()
    if model is None or model.model is None:
        return jsonify({'error': 'PPE detection model not available', 'detected': False}), 503
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = model.detect_ppe(frame)
        return jsonify(results)
    except Exception as e:
        logger.error(f"PPE error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/box_count', methods=['POST', 'OPTIONS'])
def box_count():
    if request.method == 'OPTIONS':
        return '', 200
    model = get_box_model()
    if model is None or model.model is None:
        return jsonify({'error': 'Box counting model not available', 'detected': False}), 503
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = model.detect_boxes(frame)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Box error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    ppe = get_ppe_model()
    box = get_box_model()
    face = get_face_model()
    return jsonify({
        'status': 'healthy',
        'base_dir': BASE_DIR,
        'ppe_loaded': ppe is not None and ppe.model is not None,
        'box_loaded': box is not None and box.model is not None,
        'face_loaded': face is not None and face.dataset_path is not None and os.path.exists(face.dataset_path),
        'ppe_path_exists': os.path.exists(ppe_model_path),
        'box_path_exists': os.path.exists(box_model_path),
        'face_path_exists': os.path.exists(face_dataset_path)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
