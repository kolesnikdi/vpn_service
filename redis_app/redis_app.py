"""
To use Redis db directly without cache app
Redis.instance
"""

from django.conf import settings

import redis


class Redis:
    """Class for interaction with Redis"""

    instance = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )
