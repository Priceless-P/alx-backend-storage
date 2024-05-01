#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
from functools import wraps
from typing import Callable
import requests
import redis

cache = redis.Redis()


def count_access(method: Callable) -> Callable:
    """Increments access count for a URL"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        cache.incr(f"count:{url}")
        cached_content = cache.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode("utf-8")
        data = method(url)
        cache.setex(f"count:{url}", 10, data)
        return data
    return wrapper


@count_access
def get_page(url: str) -> str:
    """Uses requests module to obtain the HTML content
    of a particular URL and returns it"""
    data = requests.get(url=url)
    return data.text
