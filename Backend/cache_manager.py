import time
import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import threading

class CacheManager:
    def __init__(self):
        self.detection_cache = {}
        self.model_cache = {}
        self.frame_cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0
        }
        self.lock = threading.Lock()
        
        # Cache settings
        self.detection_ttl = 300  # 5 minutes
        self.frame_ttl = 60       # 1 minute
        self.max_cache_size = 1000
        
    def _generate_key(self, data: Any) -> str:
        """Generate cache key from data"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _is_expired(self, timestamp: float, ttl: int) -> bool:
        """Check if cache entry is expired"""
        return time.time() - timestamp > ttl
    
    def _cleanup_cache(self, cache_dict: dict, ttl: int):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, value in cache_dict.items()
            if current_time - value["timestamp"] > ttl
        ]
        for key in expired_keys:
            del cache_dict[key]
    
    def get_detection(self, image_hash: str, confidence: float) -> Optional[Dict]:
        """Get cached detection result"""
        with self.lock:
            self.cache_stats["total_requests"] += 1
            
            cache_key = f"{image_hash}_{confidence}"
            
            if cache_key in self.detection_cache:
                entry = self.detection_cache[cache_key]
                if not self._is_expired(entry["timestamp"], self.detection_ttl):
                    self.cache_stats["hits"] += 1
                    print(f"🎯 Cache HIT for detection: {cache_key[:8]}...")
                    return entry["data"]
                else:
                    del self.detection_cache[cache_key]
            
            self.cache_stats["misses"] += 1
            print(f"❌ Cache MISS for detection: {cache_key[:8]}...")
            return None
    
    def set_detection(self, image_hash: str, confidence: float, result: Dict):
        """Cache detection result"""
        with self.lock:
            cache_key = f"{image_hash}_{confidence}"
            
            # Cleanup if cache is too large
            if len(self.detection_cache) >= self.max_cache_size:
                self._cleanup_cache(self.detection_cache, self.detection_ttl)
            
            self.detection_cache[cache_key] = {
                "data": result,
                "timestamp": time.time()
            }
            print(f"💾 Cached detection result: {cache_key[:8]}...")
    
    def get_frame_detection(self, frame_hash: str) -> Optional[Dict]:
        """Get cached frame detection"""
        with self.lock:
            if frame_hash in self.frame_cache:
                entry = self.frame_cache[frame_hash]
                if not self._is_expired(entry["timestamp"], self.frame_ttl):
                    return entry["data"]
                else:
                    del self.frame_cache[frame_hash]
            return None
    
    def set_frame_detection(self, frame_hash: str, result: Dict):
        """Cache frame detection result"""
        with self.lock:
            if len(self.frame_cache) >= self.max_cache_size:
                self._cleanup_cache(self.frame_cache, self.frame_ttl)
            
            self.frame_cache[frame_hash] = {
                "data": result,
                "timestamp": time.time()
            }
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        with self.lock:
            hit_rate = (self.cache_stats["hits"] / max(self.cache_stats["total_requests"], 1)) * 100
            return {
                **self.cache_stats,
                "hit_rate": round(hit_rate, 2),
                "cache_sizes": {
                    "detections": len(self.detection_cache),
                    "frames": len(self.frame_cache)
                }
            }
    
    def clear_cache(self):
        """Clear all caches"""
        with self.lock:
            self.detection_cache.clear()
            self.frame_cache.clear()
            print("🧹 Cache cleared")

# Global cache instance
cache_manager = CacheManager()