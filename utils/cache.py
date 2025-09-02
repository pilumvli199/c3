import time

_cache = {}

def is_duplicate(symbol, action, cooldown=600):
    key = f"{symbol}_{action}"
    now = time.time()
    if key in _cache and (now - _cache[key]) < cooldown:
        return True
    _cache[key] = now
    return False
