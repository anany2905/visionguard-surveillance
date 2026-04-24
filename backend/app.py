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
from models.ppe_detection.ppe_detection_model import PPEDetectionModel
from models.box_counting.box_counting_model import BoxCountingModel
from models.face_detection.face_detection_model import FaceDetectionModel
from backend.config import get_config, MODEL_CONFIG

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Log important paths for debugging
logger.info(f"BASE_DIR: {BASE_DIR}")
logger.info(f"Contents of BASE_DIR: {os.listdir(BASE_DIR)}")

# Check model files exist before loading
ppe_model_path = os.path.join(BASE_DIR, 'ppe_model', 'best.pt')
box_model_path = os.path.join(BASE_DIR, 'box_model', 'best_fixed.pt')
face_dataset_path = os.path.join(BASE_DIR, 'face_model', 'dataset')

logger.info(f"PPE model path: {ppe_model_path} | exists: {os.path.exists(ppe_model_path)}")
logger.info(f"Box model path: {box_model_path} | exists: {os.path.exists(box_model_path)}")
logger.info(f"Face dataset path: {face_dataset_path} | exists: {os.path.exists(face_dataset_path)}")

# Initialize models with error handling
ppe_model = None
box_model = None
face_model = None

try:
    ppe_model = PPEDetectionModel(model_path=ppe_model_path)
    logger.info(f"PPE model loaded: {ppe_model.model is not None}")
except Exception as e:
    logger.error(f"Failed to load PPE model: {e}")
    logger.error(traceback.format_exc())

try:
    box_model = BoxCountingModel(model_path=box_model_path)
    logger.info(f"Box model loaded: {box_model.model is not None}")
except Exception as e:
    logger.error(f"Failed to load Box model: {e}")
    logger.error(traceback.format_exc())

try:
    face_model = FaceDetectionModel(dataset_path=face_dataset_path)
    logger.info(f"Face model initialized. Dataset exists: {os.path.exists(face_dataset_path) if face_model else False}")
except Exception as e:
    logger.error(f"Failed to load Face model: {e}")
    logger.error(traceback.format_exc())

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
    if face_model is None:
        return jsonify({'error': 'Face detection model not loaded', 'detected': False}), 503
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = face_model.detect_faces(frame)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Face detection error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/ppe_detect', methods=['POST', 'OPTIONS'])
def ppe_detect():
    if request.method == 'OPTIONS':
        return '', 200
    if ppe_model is None or ppe_model.model is None:
        return jsonify({'error': 'PPE detection model not loaded', 'detected': False}), 503
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = ppe_model.detect_ppe(frame)
        return jsonify(results)
    except Exception as e:
        logger.error(f"PPE error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/box_count', methods=['POST', 'OPTIONS'])
def box_count():
    if request.method == 'OPTIONS':
        return '', 200
    if box_model is None or box_model.model is None:
        return jsonify({'error': 'Box counting model not loaded', 'detected': False}), 503
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = box_model.detect_boxes(frame)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Box error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'base_dir': BASE_DIR,
        'ppe_loaded': ppe_model is not None and ppe_model.model is not None,
        'box_loaded': box_model is not None and box_model.model is not None,
        'face_loaded': face_model is not None and face_model.dataset_path is not None and os.path.exists(face_model.dataset_path),
        'ppe_path_exists': os.path.exists(ppe_model_path),
        'box_path_exists': os.path.exists(box_model_path),
        'face_path_exists': os.path.exists(face_dataset_path)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
