import re
import os.path
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.test import TestCase
from django.test.client import Client
from maintenancemode.models import Maintenance


class MaintenanceModeMiddlewareTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.TEMPLATES_WITH = [spec.copy() for spec in settings.TEMPLATES]
        cls.TEMPLATES_WITH[0]['DIRS'] = (
            os.path.join(settings.BASE_DIR, 'templates/'),
        )
        cls.TEMPLATES_WITHOUT = [spec.copy() for spec in settings.TEMPLATES]
        cls.TEMPLATES_WITHOUT[0]['DIRS'] = ()

    def setUp(self):
        """ Reset config options adapted in the individual tests """
        settings.INTERNAL_IPS = ()
        settings.TEMPLATES = self.TEMPLATES_WITH
        self.site = Site.objects.get_current()
        self.maintenance = Maintenance.objects.get_or_create(
            site=self.site,
        )[0]  # (obj, created)[0]
        self._set_model_to(False)

    def _set_model_to(self, is_being_performed):
        """ Set setting model value """
        Maintenance.objects.filter(id=self.maintenance.id).update(
            is_being_performed=is_being_performed,
        )

    def test_implicitly_disabled_middleware(self):
        """ Middleware should default to being disabled """
        self.maintenance.delete()
        response = self.client.get('/')
        self.assertContains(response, text='Rendered response page', count=1, status_code=200)

    def test_disabled_middleware(self):
        """ Explicitly disabling the MAINTENANCE_MODE should work """
        self.assertFalse(self.maintenance.is_being_performed)
        response = self.client.get('/')
        self.assertContains(response, text='Rendered response page', count=1, status_code=200)

    def test_enabled_middleware_without_template(self):
        """ Enabling the middleware without a proper 503 template should raise a template error """
        self._set_model_to(True)
        with self.settings(TEMPLATES=self.TEMPLATES_WITHOUT):
            self.assertRaises(TemplateDoesNotExist, self.client.get, '/')

    def test_enabled_middleware_with_template(self):
        """ Enabling the middleware having a 503.html in any of the template
            locations should return the rendered template
        """
        self._set_model_to(True)
        with self.settings(TEMPLATES=self.TEMPLATES_WITH):
            response = self.client.get('/')
        self.assertContains(response, text='Temporary unavailable', count=1, status_code=503)

    def test_middleware_with_non_staff_user(self):
        """ A logged in user that is not a staff user should see the 503 message """
        self._set_model_to(True)
        from django.contrib.auth.models import User
        User.objects.create_user(username='maintenance',
                                 email='maintenance@example.org',
                                 password='maintenance_pw')
        self.client.login(username='maintenance', password='maintenance_pw')
        response = self.client.get('/')
        self.assertContains(response, text='Temporary unavailable', count=1, status_code=503)
    
    def test_middleware_with_staff_user(self):
        """ A logged in user that _is_ a staff user should be able to use the site normally """
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='maintenance',
                                        email='maintenance@example.org',
                                        password='maintenance_pw')
        user.is_staff = True
        user.save()
        self.client.login(username='maintenance', password='maintenance_pw')
        response = self.client.get('/')
        self.assertContains(response, text='Rendered response page', count=1, status_code=200)
        
    def test_middleware_with_internal_ips(self):
        """ A user that visits the site from an IP in INTERNAL_IPS
            should be able to use the site normally
        """
        # Use a new Client instance to be able to set the REMOTE_ADDR used by INTERNAL_IPS
        client = Client(REMOTE_ADDR='127.0.0.1')
        with self.settings(INTERNAL_IPS=('127.0.0.1', )):
            response = client.get('/')
        self.assertContains(response, text='Rendered response page', count=1, status_code=200)

    def test_ignored_path(self):
        """ A path is ignored when applying the maintenance mode and
            should be reachable normally
        """
        with self.settings(IGNORE_URLS=(re.compile(r'^/ignored.*'),)):
            response = self.client.get('/ignored/')
        self.assertContains(response, text='Rendered response page', count=1, status_code=200)
