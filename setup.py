# Copyright (c) 2007-2010 Simplistix Ltd
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
    long_description=open(os.path.join(this_dir,'docs','description.txt')).read(),
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
    )
