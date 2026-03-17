"""
Redis cache utilities for caching frequently accessed data.
"""
import json
import redis.asyncio as redis
from typing import Optional, Any, Callable
from functools import wraps
import hashlib

from app.core import settings

# Redis client
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get Redis client instance."""
    global redis_client
    if redis_client is None:
        redis_client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
        )
    return redis_client


async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


class Cache:
    """Redis cache manager."""

    def __init__(self, prefix: str = "aiworkos"):
        self.prefix = prefix

    def _make_key(self, key: str) -> str:
        """Create cache key with prefix."""
        return f"{self.prefix}:{key}"

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        client = await get_redis()
        value = await client.get(self._make_key(key))
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None

    async def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds (default: 5 minutes)
        """
        client = await get_redis()
        if not isinstance(value, str):
            value = json.dumps(value)
        return await client.set(self._make_key(key), value, ex=expire)

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        client = await get_redis()
        return await client.delete(self._make_key(key)) > 0

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        client = await get_redis()
        return await client.exists(self._make_key(key)) > 0

    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern."""
        client = await get_redis()
        keys = await client.keys(self._make_key(pattern))
        if keys:
            await client.delete(*keys)


# Global cache instance
cache = Cache()


def cache_response(expire: int = 300, key_prefix: str = ""):
    """
    Decorator to cache function responses.
    
    Args:
        expire: Cache expiration in seconds
        key_prefix: Prefix for cache key
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix or func.__name__]
            
            # Add args to key
            for arg in args:
                if isinstance(arg, (str, int, float, bool)):
                    key_parts.append(str(arg))
            
            # Add kwargs to key
            for k, v in sorted(kwargs.items()):
                if isinstance(v, (str, int, float, bool)):
                    key_parts.append(f"{k}:{v}")
            
            # Create hash of key parts
            key_str = ":".join(key_parts)
            cache_key = hashlib.md5(key_str.encode()).hexdigest()
            
            # Try to get from cache
            cached = await cache.get(cache_key)
            if cached is not None:
                return cached
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            await cache.set(cache_key, result, expire)
            
            return result
        
        return wrapper
    return decorator
