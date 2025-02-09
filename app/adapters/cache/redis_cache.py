import redis
import json
import logging


logger = logging.getLogger(__name__)

class RedisCache:
    def get(self, key):
        try:
            value = self.client.get(key)
            if value: logger.debug(f"Cache HIT: {key}")
            else: logger.debug(f"Cache MISS: {key}")
            return value
        except Exception as e:
            logger.error(f"Cache error: {str(e)}")
            return None

    def set(self, key, value, ex=None):
        try:
            return self.client.set(key, value, ex=ex)
        except redis.RedisError:
            pass

    def delete(self, *keys):
        try:
            return self.client.delete(*keys)
        except redis.RedisError:
            pass