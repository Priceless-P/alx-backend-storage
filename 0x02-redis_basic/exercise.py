#!/usr/bin/env python3
"""Writing strings to Redis"""
from functools import wraps
from typing import Callable, Optional, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """Count how many times methods of the
    Cache class are called"""
    @wraps(method)
    def increment_count(self, *args, **kwargs):
        """Wrapper function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return increment_count


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs
    for a particular function"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def count_history(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data
    return count_history


def replay(method: Callable) -> None:
    """Replays the history of a function"""
    key = method.__qualname__
    db = redis.Redis()
    calls = db.get(key).decode("utf-8")
    print("{} was called {} times".format(key, calls))
    inputs = db.lrange(key + ":inputs", 0, -1)
    outputs = db.lrange(key + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key, i.decode('utf-8'),
                                     o.decode("utf-8")))


class Cache:
    """"Cache class"""

    def __init__(self):
        """Initializes the cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores input data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Returns data given a key"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Returns str data given a key"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: int) -> int:
        """Returns int data given a key"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
