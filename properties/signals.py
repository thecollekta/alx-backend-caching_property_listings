from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Property


@receiver([post_save, post_delete], sender=Property)
def invalidate_properties_cache(sender, **kwargs):
    """
    Invalidate the 'all_properties' cache when a Property is created, updated, or deleted.
    This ensures the cached queryset is refreshed on the next request.
    """
    cache.delete("all_properties")
