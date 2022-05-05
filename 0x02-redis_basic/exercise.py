#!/usr/bin/env python3
"""Script with a class for manipulate redis"""

from typing import Callable, Optional, Union
from functools import wraps
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """Decorator for count functions calls"""
    @wraps(method)
    def decorator(*args, **kwargs):

        key = method.__qualname__
        cache = args[0]
        cache._redis.incr(key, 1)

        return method(*args, **kwargs)
    return decorator


class Cache:
    """Class with methods for manipulate redis"""

    def __init__(self):
        """Class init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, Union[bytes, Union[int, float]]]) -> str:
        """Method for generate a key and save in cache"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Optional[Union[str, Union[bytes, Union[int, float]]]]:
        """Method to get value from cache"""
        value = self._redis.get(key)
        if value and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> \
            Optional[Union[str, Union[bytes, Union[int, float]]]]:
        """Method to get str value from cache"""
        return self.get(key, str)

    def get_int(self, key: str) -> \
            Optional[Union[str, Union[bytes, Union[int, float]]]]:
        """Method to get int value from cache"""
        return self.get(key, int)
