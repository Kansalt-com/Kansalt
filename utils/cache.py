"""
Cache manager with file-based and DB storage options.
"""
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from utils.logger import get_logger

logger = get_logger(__name__)

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

CACHE_TTL_MINUTES = 20  # 20 minutes default


class CacheManager:
    """Simple file-based cache with TTL."""

    @staticmethod
    def _get_cache_file(key: str) -> str:
        """Get cache file path for key."""
        safe_key = key.replace("/", "_").replace("\\", "_")
        return os.path.join(CACHE_DIR, f"{safe_key}.json")

    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        try:
            cache_file = CacheManager._get_cache_file(key)
            if not os.path.exists(cache_file):
                return None

            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check expiry
            expires_at = datetime.fromisoformat(data.get("expires_at", ""))
            if datetime.now(timezone.utc) > expires_at:
                os.remove(cache_file)
                logger.debug(f"Cache expired for key: {key}")
                return None

            logger.debug(f"Cache HIT for key: {key}")
            return data.get("value")

        except Exception as e:
            logger.error(f"Cache GET error for {key}: {e}")
            return None

    @staticmethod
    def set(key: str, value: Any, ttl_minutes: int = CACHE_TTL_MINUTES) -> bool:
        """Set value in cache with TTL."""
        try:
            cache_file = CacheManager._get_cache_file(key)
            expires_at = (datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)).isoformat()

            data = {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": expires_at,
                "value": value,
            }

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, default=str)

            logger.debug(f"Cache SET for key: {key} (TTL: {ttl_minutes}m)")
            return True

        except Exception as e:
            logger.error(f"Cache SET error for {key}: {e}")
            return False

    @staticmethod
    def clear(key: Optional[str] = None) -> bool:
        """Clear cache. If key is None, clear all."""
        try:
            if key:
                cache_file = CacheManager._get_cache_file(key)
                if os.path.exists(cache_file):
                    os.remove(cache_file)
                    logger.debug(f"Cache cleared for key: {key}")
            else:
                for file in os.listdir(CACHE_DIR):
                    os.remove(os.path.join(CACHE_DIR, file))
                logger.debug("Cache cleared (all)")
            return True
        except Exception as e:
            logger.error(f"Cache CLEAR error: {e}")
            return False
