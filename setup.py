# Copyright (c) 2007 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
from setuptools import setup, find_packages

this_dir = os.path.dirname(__file__)

setup(
    name='mailinglogger',
    version=file(os.path.join(this_dir,'mailinglogger','version.txt')).read().strip(),
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="Enhanced emailing handlers for the python logging package.",
    long_description=open(os.path.join(this_dir,'mailinglogger','docs','description.txt')).read(),
    url='http://www.simplistix.co.uk/software/python/mailinglogger',
    keywords="logging email",
    classifiers=[
    'Development Status :: 6 - Mature',
    'Framework :: Plone',
    'Framework :: Zope2',
    'Framework :: Zope3',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Topic :: Communications :: Email',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Logging',
    ],    
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    extras_require=dict(
	test_zconfig=['ZConfig'],
	test_zope2=['Zope2'],
	test_zope3=['zope.app.twisted'],
	)
    )

# to build and upload the eggs, do:
# python setup.py sdist register upload
# ...or...
#  bin/buildout setup setup.py sdist register upload
# ...on a unix box!

# To check how things will show on pypi, install docutils and then:
# bin/buildout -q setup setup.py --long-description | rst2html.py --link-stylesheet --stylesheet=http://www.python.org/styles/styles.css > dist/desc.html
