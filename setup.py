import os
from setuptools import setup
 
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
 
# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
 
setup(
    name = 'django-app',
    version = '0.0',
    packages = ['app'],
    include_package_data = True,
    license = '',
    description = '',
    long_description = README,
    url = 'https://github.com/degreeworkunivalle/Services',
    author = 'Miguel Angel Bernal Colonia, Aslhey Ramirez',
    author_email = 'miguel.angel.bernal@correounivalle.edu.co, aslhey.ramirez@correounivalle.edu.co',
    classifiers =[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License ::',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)