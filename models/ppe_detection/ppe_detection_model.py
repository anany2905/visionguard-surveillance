"""
PPE (Personal Protective Equipment) Detection Model Integration
==============================================================
This is a placeholder for your trained PPE detection model.

Expected Model Characteristics:
- Input: Video frame or image
- Output: Detection of helmet, vest, gloves, and boots

Integration Steps:
1. Load your trained model weights
2. Implement preprocessing pipeline
3. Process input through model
4. Classify PPE equipment for each person

Example Output:
{
    "detected": True,
    "people": [
        {
            "personId": "PERSON_001",
            "ppe": {
                "helmet": True,
                "vest": True,
                "gloves": False,
                "boots": True
            },
            "complianceStatus": "PARTIAL",
            "confidence": 0.96,
            "bbox": [50, 30, 400, 600]
        }
    ]
}
"""

import cv2
import numpy as np
from ultralytics import YOLO

class PPEDetectionModel:
    def __init__(self, model_path=None):
        """
        Initialize PPE detection model
        
        Args:
            model_path: Path to your trained model (YOLO .pt)
        """
        self.model = None
        self.ppe_classes = ['helmet', 'vest', 'gloves', 'boots']
        self.class_map = {}
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load YOLO model weights and build dynamic class map"""
        try:
            self.model = YOLO(model_path)
            print(f"Model loaded successfully from {model_path}")
            # Build dynamic class map from model.names
            self.class_map = {}
            print(f"Model class names: {self.model.names}")
            
            # Filter out negative/non-PPE classes (no_helmet, no_gloves, etc.)
            valid_classes = {}
            for idx, name in self.model.names.items():
                clean = name.lower().strip()
                if clean.startswith('no_') or clean in ('none', 'person'):
                    continue
                valid_classes[idx] = clean
            
            # First pass: exact match
            for idx, clean in valid_classes.items():
                for ppe in self.ppe_classes:
                    if clean == ppe:
                        self.class_map[ppe] = idx
                        break
            
            # Second pass: partial match for remaining unmapped classes
            for idx, clean in valid_classes.items():
                for ppe in self.ppe_classes:
                    if ppe not in self.class_map:
                        if ppe in clean or clean in ppe:
                            self.class_map[ppe] = idx
                            break
            
            print(f"PPE class map: {self.class_map}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.model = None


    
    def preprocess(self, frame):
        """
        Preprocess the input frame for YOLO
        
        Args:
            frame: Input video frame or image
            
        Returns:
            RGB frame (YOLO expects RGB)
        """
        # Convert BGR to RGB
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    def detect_ppe(self, frame):
        """
        Detect PPE equipment in frame using YOLO
        
        Args:
            frame: Input video frame
            
        Returns:
            Dictionary with PPE detection results
        """
        try:
            if self.model is None:
                return {"detected": False, "error": "Model not loaded"}
            
            # Run YOLO inference (YOLOv8 handles preprocessing internally)
            results = self.model.predict(frame, conf=0.25, verbose=False)
            
            # Collect actual PPE detections
            detected_items = []
            confidences = []
            bboxes = []
            
            for r in results:
                boxes = r.boxes
                if boxes is not None:
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        # Map class to PPE item
                        if cls in self.class_map.values():
                            item = [k for k, v in self.class_map.items() if v == cls][0]
                            detected_items.append(item)
                            confidences.append(conf)
                            # Get actual bounding box
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            bboxes.append([x1, y1, x2, y2])
            
            # Only create person entry if PPE items were actually detected
            if not detected_items:
                return {
                    "detected": False,
                    "people": []
                }
            
            # Build PPE status dictionary
            person_ppe = {k: False for k in self.ppe_classes}
            for item in detected_items:
                person_ppe[item] = True
            
            # Calculate actual average confidence
            avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
            
            # Compute overall bounding box from all detections
            if bboxes:
                x1 = min(b[0] for b in bboxes)
                y1 = min(b[1] for b in bboxes)
                x2 = max(b[2] for b in bboxes)
                y2 = max(b[3] for b in bboxes)
                overall_bbox = [x1, y1, x2, y2]
            else:
                h, w = frame.shape[:2]
                overall_bbox = [0, 0, w, h]
            
            detections = [{
                "personId": "PERSON_001",
                "ppe": person_ppe,
                "complianceStatus": self.get_compliance_status(person_ppe),
                "confidence": round(avg_conf, 3),
                "bbox": overall_bbox
            }]
            
            return {
                "detected": True,
                "people": detections
            }
            
        except Exception as e:
            print(f"Error in PPE detection: {str(e)}")
            return {"detected": False, "error": str(e)}

    
    def get_compliance_status(self, ppe_dict):
        """
        Determine compliance status based on PPE worn
        
        Args:
            ppe_dict: Dictionary with PPE detection results
            
        Returns:
            Compliance status: "FULL", "PARTIAL", or "NONE"
        """
        worn_items = sum(1 for v in ppe_dict.values() if v)
        total_items = len(ppe_dict)
        
        if worn_items == total_items:
            return "FULL"
        elif worn_items > 0:
            return "PARTIAL"
        else:
            return "NONE"
    
    def draw_results(self, frame, detections):
        """
        Draw PPE detection results on frame
        
        Args:
            frame: Input frame
            detections: Detection results
            
        Returns:
            Frame with drawn results
        """
        for person in detections.get("people", []):
            x1, y1, x2, y2 = person["bbox"]
            ppe = person["ppe"]
            status = person["complianceStatus"]
            
            # Color based on compliance
            if status == "FULL":
                color = (0, 255, 0)  # Green
            elif status == "PARTIAL":
                color = (0, 165, 255)  # Orange
            else:
                color = (0, 0, 255)  # Red
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw person ID and status
            cv2.putText(frame, f"{person['personId']} - {status}", 
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw PPE status
            ppe_text = f"H:{ppe['helmet']} V:{ppe['vest']} G:{ppe['gloves']} B:{ppe['boots']}"
            cv2.putText(frame, ppe_text, (x1, y2+25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return frame
    
    def check_compliance_alert(self, detections):
        """
        Check if any non-compliance alert should be triggered
        
        Args:
            detections: Detection results
            
        Returns:
            List of alerts for non-compliant personnel
        """
        alerts = []
        
        for person in detections.get("people", []):
            if person["complianceStatus"] != "FULL":
                missing_ppe = [item for item, worn in person["ppe"].items() if not worn]
                alerts.append({
                    "personId": person["personId"],
                    "missing": missing_ppe,
                    "severity": "HIGH" if person["complianceStatus"] == "NONE" else "MEDIUM"
                })
        
        return alerts


# Usage Example:
if __name__ == "__main__":
    # Initialize model
    model = PPEDetectionModel(model_path="path/to/model")
    
    # Process video
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect PPE
        detections = model.detect_ppe(frame)
        
        # Draw results
        frame = model.draw_results(frame, detections)
        
        # Check for alerts
        alerts = model.check_compliance_alert(detections)
        for alert in alerts:
            print(f"ALERT: {alert['personId']} missing {alert['missing']}")
        
        # Display
        cv2.imshow("PPE Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
