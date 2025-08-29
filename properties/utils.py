import logging

from django.core.cache import cache
from django_redis import get_redis_connection

from properties.models import Property

logger = logging.getLogger(__name__)


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache metrics including hits, misses, and hit ratio.

    Returns:
        dict: Dictionary containing cache metrics:
            - hits (int): Number of successful key lookups
            - misses (int): Number of failed key lookups
            - hit_ratio (float): Ratio of hits to total requests (hits / (hits + misses))
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")

        # Get Redis info
        info = redis_conn.info("stats")

        # Extract hits and misses
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Calculate hit ratio
        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        # Log metrics
        logger.info(
            f"Cache metrics - Hits: {hits}, Misses: {misses}, "
            f"Hit Ratio: {hit_ratio:.2%}"
        )

        return {"hits": hits, "misses": misses, "hit_ratio": hit_ratio}

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0.0, "error": str(e)}


def get_all_properties():
    """
    Retrieve all properties from cache if available, otherwise fetch from database.
    Caches the queryset for 1 hour (3600 seconds).

    Returns:
        QuerySet: A queryset of all Property objects
    """
    # Try to get properties from cache
    properties = cache.get("all_properties")

    # If not in cache, get from database and cache it
    if properties is None:
        properties = Property.objects.all()
        # Cache for 1 hour (3600 seconds)
        cache.set("all_properties", properties, 3600)

    return properties
