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
        self = args[0]
        self._redis.incr(key, 1)

        return method(*args, **kwargs)
    return decorator


def call_history(method: Callable) -> Callable:
    """Decorator for save call history"""
    @wraps(method)
    def decorator(*args, **kwargs):

        key_input = f'{method.__qualname__}:inputs'
        key_output = f'{method.__qualname__}:outputs'
        self = args[0]
        self._redis.rpush(key_input, str(args[1:]))
        output = method(*args, **kwargs)
        self._redis.rpush(key_output, str(output))

        return output
    return decorator


class Cache:
    """Class with methods for manipulate redis"""

    def __init__(self):
        """Class init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
        return self.get(key, lambda x: x.decode('UTF-8'))

    def get_int(self, key: str) -> \
            Optional[Union[str, Union[bytes, Union[int, float]]]]:
        """Method to get int value from cache"""
        return self.get(key, int)


def replay(method: Callable):
    """Function that display the history of calls of a particular function"""
    _redis = redis.Redis()

    key_count = method.__qualname__
    counts = int(_redis.get(key_count))

    key_input = f'{method.__qualname__}:inputs'
    key_output = f'{method.__qualname__}:outputs'

    inputs = _redis.lrange(key_input, 0, counts)
    outputs = _redis.lrange(key_output, 0, counts)

    print(f"{key_count} was called {counts} times:")
    for in_, out in zip(inputs, outputs):
        print(f"{key_count}(*{in_.decode('UTF-8')}) -> {out.decode('UTF-8')}")
