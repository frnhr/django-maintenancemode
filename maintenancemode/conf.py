
class Settings(object):

    prefix = 'MAINTENANCE_MODE'

    defaults = {
        'PERMISSION_PROCESSORS': (
            'maintenancemode.permission_processors.is_staff',
        ),
    }

    def __getattr__(self, item):
        from django.conf import settings
        if item in self.defaults:
            return getattr(settings, '{}_{}'.format(self.prefix, item), self.defaults[item])
        raise AttributeError

settings = Settings()
