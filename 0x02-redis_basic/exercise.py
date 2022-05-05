#!/usr/bin/env python3
"""Script with a class for manipulate redis"""

from typing import Union
import redis
import uuid


class Cache:
    """Class with methods for manipulate redis"""

    def __init__(self):
        """Class init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, Union[bytes, Union[int, float]]]) -> str:
        """Method for generate a key and save in cache"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key
