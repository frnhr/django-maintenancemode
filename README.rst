======================
django-maintenancemode
======================

.. image:: https://travis-ci.org/frnhr/django-maintenancemode.svg

django-maintenancemode is a middleware that allows you to temporary shutdown
your site for maintenance work.

When site is in maintenance mode, some user can still access the regular site:
 - logged in users having staff credentials, and
 - users visiting the site from an ip address defined in Django's `INTERNAL_IPS`.

The two points above are just the defaults, configured in `PERMISSION_PROCESSORS` setting
(see below). Custom rules are easy to plug in.

django-maintenancemode works the same way as handling 404 or 500 errors in
Django work. It adds a handler503 which you can override in your main urls.py
or you can add a 503.html to your templates directory.

Forking history:
 - This fork adds the permission processors framework.
 - Older fork moved the maintenance mode property and ignored urls out of settings.py
   and into your database.


Requirements
============
django.contrib.sites

Sites must have at least one domain to work properly.

Plugin is fully tested with:
 - Django 1.7.8
 - Django 1.8.2
 - Python 2.7.9
 - Python 3.4.2


Installation
============

* Download django-maintenancemode from https://github.com/frnhr/django-maintenancemode
* Install using: `python setup.py install`
* In your Django settings file add maintenancemode to your `MIDDLEWARE_CLASSES`.
  Make sure it comes after Django's AuthenticationMiddleware. Like so::

   MIDDLEWARE_CLASSES = (
       # ...
   
       'maintenancemode.middleware.MaintenanceModeMiddleware',
   )
   
* Add ``maintenancemode`` to your `INSTALLED_APPS`.
   
* Run manage.py migrate to create the necessary tables.

* Adding the middleware and running your site creates the necessary records in the database
  to enable/disable maintenance mode and ignored URL patterns.


Configuration
=============

Config section is not up-to-date :(


``MAINTENANCE MODE``
--------------------
Maintenance mode will create a database record per site, read from the domains you have in the
Sites app. There is a boolean property on each Maintenance model, "is_being_performed" that takes
the place of putting the site into "maintnenace mode" from settings.py

``MAINTENANCE IGNORE URLS``
---------------------------
Patterns to ignore are registered as an inline model for each maintenance record created when the
site is first run. Patterns should begin with a forward slash: /, but can end any way you'd like.


Todo
====

* document configuration
* document permission processors
* sort out the ignored urls feature
* tests for admin interface?
* pypi package
* omg make this readme in markdown
