"""
Rate limiting middleware for API endpoints.
"""
import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from collections import defaultdict
import asyncio


class RateLimiter:
    """
    Simple in-memory rate limiter.
    For production, use Redis-based rate limiting.
    """

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()

    async def check_rate_limit(self, identifier: str) -> Tuple[bool, int]:
        """
        Check if the request should be rate limited.
        
        Args:
            identifier: Unique identifier (e.g., IP address or user ID)
            
        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        async with self.lock:
            now = time.time()
            minute_ago = now - 60

            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > minute_ago
            ]

            # Check limit
            current_requests = len(self.requests[identifier])
            
            if current_requests >= self.requests_per_minute:
                return False, 0

            # Add new request
            self.requests[identifier].append(now)
            remaining = self.requests_per_minute - current_requests - 1
            
            return True, remaining

    async def cleanup_old_entries(self):
        """Periodically clean up old entries to prevent memory leak."""
        while True:
            await asyncio.sleep(300)  # Clean every 5 minutes
            async with self.lock:
                now = time.time()
                minute_ago = now - 60
                
                # Remove identifiers with no recent requests
                to_remove = []
                for identifier, requests in self.requests.items():
                    if not requests or all(req_time < minute_ago for req_time in requests):
                        to_remove.append(identifier)
                
                for identifier in to_remove:
                    del self.requests[identifier]


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=100)


async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware.
    Uses IP address as identifier.
    """
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)

    # Get client identifier (IP address)
    client_ip = request.client.host if request.client else "unknown"
    
    # Check rate limit
    is_allowed, remaining = await rate_limiter.check_rate_limit(client_ip)
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )
    
    # Process request
    response = await call_next(request)
    
    # Add rate limit headers
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.requests_per_minute)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    
    return response
