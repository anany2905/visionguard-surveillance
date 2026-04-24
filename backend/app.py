from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.ppe_detection.ppe_detection_model import PPEDetectionModel
from models.box_counting.box_counting_model import BoxCountingModel
from models.face_detection.face_detection_model import FaceDetectionModel
from backend.config import get_config, MODEL_CONFIG

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialize models
ppe_model = PPEDetectionModel(model_path=os.path.join(BASE_DIR, 'ppe_model', 'best.pt'))
box_model = BoxCountingModel(model_path=os.path.join(BASE_DIR, 'box_model', 'best_fixed.pt'))
face_model = FaceDetectionModel(dataset_path=os.path.join(BASE_DIR, 'face_model', 'dataset'))

print("All models initialized successfully")

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
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = face_model.detect_faces(frame)
        return jsonify(results)
    except Exception as e:
        print(f"Face detection error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ppe_detect', methods=['POST', 'OPTIONS'])
def ppe_detect():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = ppe_model.detect_ppe(frame)
        return jsonify(results)
    except Exception as e:
        print(f"PPE error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/box_count', methods=['POST', 'OPTIONS'])
def box_count():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        frame, error = decode_image(request.json)
        if error:
            return jsonify({'error': error}), 400
        results = box_model.detect_boxes(frame)
        return jsonify(results)
    except Exception as e:
        print(f"Box error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'ppe_loaded': ppe_model.model is not None,
        'box_loaded': box_model.model is not None,
        'face_loaded': face_model.dataset_path is not None and os.path.exists(face_model.dataset_path)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')

