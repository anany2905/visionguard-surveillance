import cv2
import numpy as np
from ultralytics import YOLO

class BoxCountingModel:
    def __init__(self, model_path=None):
        self.model = None
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        try:
            self.model = YOLO(model_path)
            print(f"Box model loaded from {model_path}")
        except Exception as e:
            print(f"Error loading box model: {e}")
    
    def detect_boxes(self, frame):
        try:
            if self.model is None:
                return {"detected": False, "count": 0, "confidence": 0.0}
            
            results = self.model.predict(frame, conf=0.5, verbose=False)
            count = 0
            confidences = []
            
            for r in results:
                if r.boxes is not None:
                    count += len(r.boxes)
                    confidences.extend(r.boxes.conf.cpu().numpy())
            
            avg_conf = np.mean(confidences) if confidences else 0.0
            
            return {
                "detected": count > 0,
                "count": int(count),
                "confidence": float(avg_conf)
            }
        except Exception as e:
            print(f"Box detection error: {e}")
            return {"detected": False, "error": str(e), "count": 0, "confidence": 0.0}

