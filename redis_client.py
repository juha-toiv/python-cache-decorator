import redis


class Redis_Client:

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def insert_or_update(self, cache_name, key, value, ttl=None):
        '''
        Adds a new key-value pair to cache or updates existing key value pair.
        '''
        self.r.hset(cache_name, key, value)
        if ttl is not None:
            self.r.expire(cache_name, ttl)

    def get(self, cache_name, key):
        '''
        Returns value from cache by key, if key is not found in cache then returns None.
        '''
        return self.r.hget(cache_name, key)

    def delete(self, cache_name):
        '''
        Removes all key-value pairs from cache.
        '''
        key_value_pairs = self.r.hgetall(cache_name)
        for key in key_value_pairs.keys():
            self.r.hdel(cache_name, key)


redis_client = Redis_Client()
