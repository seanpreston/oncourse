# encoding: utf-8
from django.core.cache import cache
from redis import ConnectionError
import logging

logger = logging.getLogger(__name__)


def get(key, default=None):
    try:
        return cache.get(key, default)
    except ConnectionError:
        logger.error('Redis connection error on cache get for "%s"' % key)
    except Exception as e:
        print e.message
        print e
        print dir(e)
        print key
        logger.error('Cache exception for cache_get "%s": %s' % (key, e))
    return default


def set(key, value, timeout):
    try:
        cache.set(key, value, timeout)
    except ConnectionError:
        logger.error('Redis connection error on cache set for "%s"' % key)
    except Exception as e:
        logger.error('Cache exception for cache_set "%s": %s' % (key, e))


def delete(key):
    try:
        cache.delete(key)
    except ConnectionError:
        logger.error('Redis connection error on cache set for "%s"' % key)
    except Exception as e:
        logger.error('Cache exception for cache_delete "%s": %s' % (key, e))
