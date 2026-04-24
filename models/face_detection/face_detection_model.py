"""
Face Detection Model Integration using DeepFace
===============================================
Real-time facial recognition with name, ID, and confidence score.

Expected Output:
{
    "detected": True,
    "faces": [
        {
            "name": "John Doe",
            "id": "EMP_001",
            "authorized": True,
            "confidence": 0.98,
            "bbox": [100, 50, 300, 400]
        }
    ]
}
"""

import cv2
import numpy as np
import math
import os
import warnings

# Redirect DeepFace home to project-local writable directory
os.environ['DEEPFACE_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'face_model', '.deepface')
os.makedirs(os.environ['DEEPFACE_HOME'], exist_ok=True)

# Suppress TensorFlow warnings for cleaner output
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class FaceDetectionModel:
    def __init__(self, dataset_path=None):
        """
        Initialize face detection model with DeepFace
        
        Args:
            dataset_path: Path to the face dataset directory containing person folders
        """
        self.dataset_path = dataset_path
        self.person_ids = {
            "Shaurya": "1032221748",
            "Anany": "1032222541",
            "Sarvagya": "1032222788",
            "Om": "1032222696"
        }
        self.confidence_threshold = 0.5
        
        # Verify dataset exists
        if dataset_path and os.path.exists(dataset_path):
            print(f"Face dataset loaded from: {dataset_path}")
        else:
            print(f"Warning: Face dataset not found at {dataset_path}")
    
    def detect_faces(self, frame):
        """
        Detect and recognize faces in frame using DeepFace
        
        Args:
            frame: Input video frame (BGR format from OpenCV)
            
        Returns:
            Dictionary with detection results
        """
        try:
            from deepface import DeepFace
            
            if not self.dataset_path or not os.path.exists(self.dataset_path):
                return {
                    "detected": False,
                    "error": "Face dataset not found"
                }
            
            # Convert BGR to RGB for DeepFace
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Step 1: Detect all faces with bounding boxes
            try:
                faces = DeepFace.extract_faces(
                    img_path=rgb_frame,
                    detector_backend='opencv',
                    enforce_detection=False,
                    align=True
                )
            except Exception as e:
                print(f"Face extraction error: {e}")
                faces = []
            
            if not faces or len(faces) == 0:
                return {
                    "detected": False,
                    "message": "No faces detected"
                }
            
            # Step 2: Recognize each detected face
            detected_faces = []
            
            for face_data in faces:
                # Get face region coordinates
                facial_area = face_data.get('facial_area', {})
                x = facial_area.get('x', 0)
                y = facial_area.get('y', 0)
                w = facial_area.get('w', 0)
                h = facial_area.get('h', 0)
                
                # Ensure bounds are valid
                h_frame, w_frame = frame.shape[:2]
                x1 = max(0, x)
                y1 = max(0, y)
                x2 = min(w_frame, x + w)
                y2 = min(h_frame, y + h)
                
                if x2 <= x1 or y2 <= y1:
                    continue
                
                # Crop face region from RGB frame
                face_crop = rgb_frame[y1:y2, x1:x2]
                
                if face_crop.size == 0:
                    continue
                
                # Step 3: Identify face using DeepFace.find
                try:
                    result = DeepFace.find(
                        img_path=face_crop,
                        db_path=self.dataset_path,
                        detector_backend='opencv',
                        enforce_detection=False,
                        silent=True,
                        model_name='Facenet'
                    )
                    
                    if len(result) > 0 and len(result[0]) > 0:
                        # Extract best match
                        best_match = result[0].iloc[0]
                        identity = best_match.get('identity', '')
                        distance = best_match.get('distance', float('inf'))
                        
                        # Extract name from identity path
                        identity_path = str(identity).replace('\\', '/')
                        path_parts = identity_path.split('/')
                        
                        # Find the person name from the path
                        name = "Unknown"
                        for part in path_parts:
                            if part in self.person_ids:
                                name = part
                                break
                        
                        # Calculate confidence using exponential decay
                        if distance != float('inf'):
                            confidence = math.exp(-distance * 0.5)
                        else:
                            confidence = 0
                        
                        # Check confidence threshold
                        if confidence < self.confidence_threshold:
                            name = "Unknown"
                            person_id = "UNKNOWN"
                            authorized = False
                            confidence = 0
                        else:
                            person_id = self.person_ids.get(name, "UNKNOWN")
                            authorized = True
                    else:
                        name = "Unknown"
                        person_id = "UNKNOWN"
                        authorized = False
                        confidence = 0
                        
                except Exception as e:
                    print(f"Face recognition error: {e}")
                    name = "Unknown"
                    person_id = "UNKNOWN"
                    authorized = False
                    confidence = 0
                
                detected_faces.append({
                    "name": name,
                    "id": person_id,
                    "authorized": authorized,
                    "confidence": round(confidence, 3),
                    "bbox": [int(x1), int(y1), int(x2), int(y2)]
                })
            
            if not detected_faces:
                return {
                    "detected": False,
                    "message": "No recognizable faces found"
                }
            
            return {
                "detected": True,
                "faces": detected_faces
            }
            
        except ImportError as e:
            return {
                "detected": False,
                "error": f"DeepFace not installed: {str(e)}"
            }
        except Exception as e:
            print(f"Error in face detection: {str(e)}")
            return {
                "detected": False,
                "error": str(e)
            }
    
    def draw_results(self, frame, detections):
        """
        Draw detection results on frame
        
        Args:
            frame: Input frame
            detections: Detection results
            
        Returns:
            Frame with drawn results
        """
        for face in detections.get("faces", []):
            x1, y1, x2, y2 = face["bbox"]
            
            # Draw bounding box - green for authorized, red for unknown
            color = (0, 255, 0) if face["authorized"] else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw name and ID
            text = f"{face['name']} ({face['id']})"
            (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Draw background rectangle for text
            cv2.rectangle(frame, (x1, y1 - text_h - 10), (x1 + text_w, y1), color, -1)
            cv2.putText(frame, text, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Draw confidence below box
            conf_text = f"Conf: {face['confidence']:.2f}"
            cv2.putText(frame, conf_text, (x1, y2 + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame

