from django.core.cache import cache

from properties.models import Property


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
