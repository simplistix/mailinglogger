# Copyright (c) 2007 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from setuptools import setup, find_packages

setup(
    name='mailinglogger',
    version='svn',
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="Enhanced emailing handlers for the python logging package.",
    long_description="""
    This package contains two handlers for the python logging
    framework that enable important log entries to be sent by email.

    This can either be as the entries are logged or as a summary at
    the end of the running process.

    The handlers have the following features:
    
    - customisable and dynamic subject lines for emails sent

    - emails sent with an X-Mailer header for easy filtering
    
    - flood protection to ensure the number of emails sent is not
      excessive

    - fully documented and tested
    
    In addition, extra support is provided for configuring the
    handlers when using ZConfig, Zope 2 or Zope 3.  
    """,
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
    )
