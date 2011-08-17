import posixpath

from django.core.exceptions import ImproperlyConfigured

from maintenancemode.utils.settings import AppSettings


class MaintenanceModeSettings(AppSettings):
    CACHE_BACKEND = None

    def configure_cache_backend(self, value):
        # If we are on Django >= 1.3 AND using the new CACHES setting...
        if hasattr(self, "CACHES"):
            if "maintenance_mode" in self.CACHES:
                return "maintenance_mode"
            else:
                return "default"
        if isinstance(value, basestring) and value.startswith("maintenance_mode."):
            raise ImproperlyConfigured("Please upgrade to one of the supported backends "
                                       "for the version of Django you are using as defined in the "
                                       "Django docs: https://docs.djangoproject.com/en/dev/topics/cache/")
        return value

settings = MaintenanceModeSettings("MAINTENANCE_MODE")
