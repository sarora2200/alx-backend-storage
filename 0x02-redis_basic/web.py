#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import requests
import time
from functools import wraps

def cache_with_expiry(expiry_time):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            if url in cache and time.time() - cache[url]['timestamp'] < expiry_time:
                return cache[url]['content']

            result = func(*args, **kwargs)
            cache[url] = {'content': result, 'timestamp': time.time()}
            return result

        return wrapper

    return decorator

@cache_with_expiry(10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

# Test the function
url = 'http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com'
print(get_page(url))
# This call should be cached
print(get_page(url))
# Wait for cache expiry (more than 10 seconds)
time.sleep(11)
# Cache expired, should fetch again
print(get_page(url))
