from django.contrib.sites.models import Site
from django.core.cache import get_cache
from django.template.defaultfilters import slugify

from maintenancemode.conf.app_settings import settings


def get_cache_backend():
    return get_cache(settings.MAINTENANCE_MODE_CACHE_BACKEND)

cache = get_cache_backend()


def get_cache_key(display_name):
    current_site = Site.objects.get_current()
    return 'maintenancemode::%s::%s' % (slugify(display_name), current_site.pk)

def add_ignore_urls_to_cache(instance, **kwargs):
    """
    Called via Django's signals to cache ignored urls, if any were
    added or changed in the database.
    """
    cache.set(get_cache_key(instance.display_name), instance.pattern)

def remove_ignore_urls_from_cache(instance, **kwargs):
    """
    Called via Django's signals to remove cached ignore urls, if any were
    added, changed or deleted in the database.
    """
    try:
        original_instance = instance.__class__.objects.get(pk=instance.id)
        cache_key = get_cache_key(original_instance.display_name)
        cache.delete(cache_key)
    except instance.__class__.DoesNotExist:
        pass
