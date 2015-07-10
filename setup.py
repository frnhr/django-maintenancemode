import os
from distutils.core import setup

version = '0.9.4.1'

def read_file(name):
    return open(os.path.join(os.path.dirname(__file__), 
                             name)).read()    

readme = read_file('README.rst')
changes = read_file('CHANGES')

setup(
    name='tocka-django-maintenancemode',
    version=version,
    description='Django-maintenancemode allows you to temporary shutdown your site for maintenance work',
    long_description='\n\n'.join([readme, changes]),
    author='Fran Hrzenjak',
    author_email='fran.hrzenjak@gmail.com',
    license="BSD",
    platforms=["any"],
    url='https://github.com/frnhr/django-maintenancemode/',
    packages=[
        'maintenancemode',
        'maintenancemode.views',
        'maintenancemode.migrations',
    ],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities',
    ],
)
