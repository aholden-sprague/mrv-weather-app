import time

_cache = {}

def get_from_cache(key, max_age_seconds):
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < max_age_seconds:
            return data
    return None

def set_cache(key, data):
    _cache[key] = (data, time.time())
