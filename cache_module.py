from functools import wraps, partial
from redis_client import redis_client
import inspect


class cache:
    '''
    Caches function return value.

    Args:
        func: Function and its return value to cache.
        cache_name: Name of the cache, optional. If value is None, then the default value is file and function name.
        ttl: Time to live in seconds. Default value is 30.

    Returns:
        Value from cache by key. If key does not exist in cache, then returs new added value. 
    '''
    def __init__(self, cache_name=None, ttl=30):
        self.cache_name = cache_name
        self.ttl = ttl

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.cache_name is None:
                arg_names = inspect.getfullargspec(func)[0]
                file_name = inspect.stack()[1][1]
                func_name = func.__name__
                arg_names_str = '-'.join(map(str, arg_names)) 
                self.cache_name = '-'.join([file_name, func_name, arg_names_str])
            cache_key = '-'.join(map(str, args))
            result = redis_client.get(self.cache_name, cache_key)
            if result is not None:
                return result
            result = func()
            redis_client.insert_or_update(self.cache_name, cache_key, result, self.ttl)
            return result
        return wrapper


class cache_update:
    '''
    Update cache value by key. Returns new value.

    Args:
        func: Function and its return value to cache.
        cache_name: Name of the cache to update.
        ttl: Time to live in seconds. Default value is 30.

    Returns:
        New value.
    ''' 
    def __init__(self, cache_name, ttl=30):
        self.cache_name = cache_name
        self.ttl = ttl

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func()
            cache_key = '-'.join(map(str, args))
            redis_client.insert_or_update(self.cache_name, cache_key, result, self.ttl)
            return result
        return wrapper


class cache_clear:
    '''
    Removes all key-value pair from cache.
    
    Args:
        cache_key: Name of the cache to remove.
    '''
    def __init__(self, cache_name):
        self.cache_name = cache_name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            redis_client.delete(self.cache_name)
        return wrapper
