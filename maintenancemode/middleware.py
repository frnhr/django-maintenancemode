import re

from django.conf import settings as django_settings
from django.db.utils import DatabaseError
from django.core import urlresolvers
from django.utils.module_loading import import_string
from django.contrib.sites.models import Site
import django.conf.urls as urls

from maintenancemode.models import Maintenance, IgnoredURL

urls.handler503 = 'maintenancemode.views.defaults.temporary_unavailable'
urls.__all__.append('handler503')


class MaintenanceModeMiddleware(object):
    def process_request(self, request):
        """
        Get the maintenance mode from the database.
        If a Maintenance value doesn't already exist in the database, we'll create one.
        "has_add_permission" and "has_delete_permission" are overridden in admin
        to prevent the user from adding or deleting a record, as we only need one
        to affect multiple sites managed from one instance of Django admin.
        """
        site = Site.objects.get_current()
        maintenance = None

        try:
            maintenance = Maintenance.objects.get(site=site)
        except (Maintenance.DoesNotExist, DatabaseError):
            for site in Site.objects.all():
                maintenance = Maintenance.objects.create(site=site, is_being_performed=False)

        # Allow access if maintenance is not being performed
        if not maintenance.is_being_performed:
            return None

        # Allow access if remote ip is in INTERNAL_IPS
        if request.META.get('REMOTE_ADDR') in django_settings.INTERNAL_IPS:
            return None

        # Cycle trough PERMISSION_PROCESSORS to see if this user has the right to access the site
        for processor in self._permission_processors():
            if processor(request):
                return None

        # Check if a path is explicitly excluded from maintenance mode
        urls_to_ignore = IgnoredURL.objects.filter(maintenance=maintenance)
        ignore_urls = tuple([re.compile(r'%s' % str(url.pattern)) for url in urls_to_ignore])
        for url in ignore_urls:
            if url.match(request.path_info):
                return None

        # Otherwise show the user the 503 page
        resolver = urlresolvers.get_resolver(None)

        callback, param_dict = resolver.resolve_error_handler('503')
        return callback(request, **param_dict)

    def _permission_processors(self):
        processor_modules = getattr(django_settings, 'MAINTENANCE_MODE_PERMISSION_PROCESSORS', ())
        for processor_module in processor_modules:
            yield import_string(processor_module)
