import traceback
import functools
import inspect
import asyncio
from typing import Optional
import pickle
from typing import Callable, Any
import hashlib


# Configure Redis connection settings
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Initialize Redis client
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def redis_cache(expiration: int = 3600):
    def decorator_cache(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper_cache(*args, **kwargs) -> Any:
            # Generate a unique key based on the function arguments
            key = generate_key(func.__name__, args, kwargs)

            # Check if the result is in the cache
            cached_result = redis_client.get(key)
            if cached_result:
                return pickle.loads(cached_result)  # Unpickle the result

            # Call the actual function
            result = func(*args, **kwargs)

            # Cache the result for future use
            redis_client.setex(key, expiration, pickle.dumps(result))  # Pickle the result
            return result

        return wrapper_cache

    return decorator_cache
