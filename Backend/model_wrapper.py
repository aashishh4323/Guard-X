import torch
import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import time
from PIL import Image
import asyncio
import hashlib
from cache_manager import cache_manager

class ModelWrapper:
    def __init__(self):
        self.models = {}
        self.active_model_name = None
        self.confidence_threshold = 0.5
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    def _get_image_hash(self, image) -> str:
        """Generate hash for image caching"""
        try:
            img_array = np.array(image)
            return hashlib.md5(img_array.tobytes()).hexdigest()
        except Exception as e:
            print(f"⚠️ Hash generation failed: {e}")
            return str(time.time())
    
    async def load_models(self):
        """Load both custom and fallback models"""
        print("🔄 Loading AI models...")
        
        # Try to load custom trained model first
        custom_model_path = Path("models/best.pt")
        if custom_model_path.exists():
            try:
                self.models['custom'] = YOLO(str(custom_model_path))
                self.active_model_name = 'custom'
                print(f"✅ Custom model loaded: {custom_model_path}")
            except Exception as e:
                print(f"❌ Custom model failed: {e}")
        
        # Load fallback YOLO model
        try:
            self.models['yolo'] = YOLO('yolov8n.pt')
            if not self.active_model_name:
                self.active_model_name = 'yolo'
            print("✅ YOLO fallback model loaded")
        except Exception as e:
            print(f"❌ YOLO model failed: {e}")
            
        print(f"🎯 Active model: {self.active_model_name}")
    
    async def detect_humans(self, image, confidence=None):
        """Enhanced human detection with caching"""
        try:
            print(f"🔄 Starting detection with model: {self.active_model_name}")
            
            if not self.models:
                raise Exception("No models loaded")
                
            if self.active_model_name not in self.models:
                raise Exception(f"Active model {self.active_model_name} not available")
            
            conf = confidence or self.confidence_threshold
            
            # Generate image hash for caching
            image_hash = self._get_image_hash(image)
            
            # Check cache first
            cached_result = cache_manager.get_detection(image_hash, conf)
            if cached_result:
                return cached_result
            
            model = self.models[self.active_model_name]
            start_time = time.time()
            
            # Convert PIL to numpy array
            img_array = np.array(image)
            
            # Run detection
            results = model(img_array, conf=conf, classes=[0])
            processing_time = time.time() - start_time
            
            # Extract results
            boxes = []
            confidences = []
            
            if results and len(results) > 0:
                result = results[0]
                if hasattr(result, 'boxes') and result.boxes is not None:
                    for box in result.boxes:
                        if hasattr(box, 'xyxy') and hasattr(box, 'conf'):
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            confidence_score = float(box.conf[0].cpu().numpy())
                            
                            boxes.append([float(x1), float(y1), float(x2), float(y2)])
                            confidences.append(confidence_score)
            
            detection_result = {
                "boxes": boxes,
                "count": len(boxes),
                "confidences": confidences,
                "model_type": self.active_model_name,
                "processing_time": round(processing_time, 3),
                "confidence_threshold": conf
            }
            
            # Cache the result
            cache_manager.set_detection(image_hash, conf, detection_result)
            
            return detection_result
            
        except Exception as e:
            print(f"❌ Detection error: {e}")
            # Return safe fallback
            return {
                "boxes": [],
                "count": 0,
                "confidences": [],
                "model_type": self.active_model_name or "unknown",
                "processing_time": 0.0,
                "confidence_threshold": conf,
                "error": str(e)
            }
    
    async def detect_realtime_frame(self, frame):
        """Optimized detection with frame caching"""
        try:
            if not self.models or self.active_model_name not in self.models:
                return {"boxes": [], "count": 0, "confidences": []}
            
            # Generate frame hash
            frame_hash = hashlib.md5(frame.tobytes()).hexdigest()
            
            # Check cache
            cached_result = cache_manager.get_frame_detection(frame_hash)
            if cached_result:
                return cached_result
            
            model = self.models[self.active_model_name]
            
            # Resize for performance
            height, width = frame.shape[:2]
            if width > 640:
                scale_factor = 640 / width
                new_width = 640
                new_height = int(height * scale_factor)
                frame = cv2.resize(frame, (new_width, new_height))
            else:
                scale_factor = 1.0
            
            # Run detection
            results = model(frame, conf=0.3, classes=[0])
            
            boxes = []
            confidences = []
            
            if results and len(results) > 0:
                result = results[0]
                if hasattr(result, 'boxes') and result.boxes is not None:
                    for box in result.boxes:
                        if hasattr(box, 'xyxy') and hasattr(box, 'conf'):
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            confidence_score = float(box.conf[0].cpu().numpy())
                            
                            # Scale back to original size
                            if scale_factor != 1.0:
                                x1, x2 = x1 / scale_factor, x2 / scale_factor
                                y1, y2 = y1 / scale_factor, y2 / scale_factor
                            
                            boxes.append([float(x1), float(y1), float(x2), float(y2)])
                            confidences.append(confidence_score)
            
            result = {
                "boxes": boxes,
                "count": len(boxes),
                "confidences": confidences
            }
            
            # Cache frame result
            cache_manager.set_frame_detection(frame_hash, result)
            
            return result
            
        except Exception as e:
            print(f"❌ Frame detection error: {e}")
            return {"boxes": [], "count": 0, "confidences": []}
    
    async def get_health_status(self):
        """Get model health status"""
        return {
            "models_loaded": len(self.models) > 0,
            "active_model": self.active_model_name,
            "available_models": list(self.models.keys()),
            "device": self.device,
            "confidence_threshold": self.confidence_threshold,
            "models": {
                name: {
                    "loaded": True,
                    "type": "YOLO" if name == "yolo" else "Custom",
                    "status": "OPERATIONAL"
                } for name in self.models.keys()
            }
        }
    
    async def get_models_info(self):
        """Get information about available models"""
        return [
            {
                "name": name,
                "type": info["type"],
                "path": info["path"],
                "loaded": info["loaded"],
                "active": name == self.active_model_name
            }
            for name, info in self.models.items()
        ]






