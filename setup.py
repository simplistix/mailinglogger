# Copyright (c) 2005 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os

from distutils.core import setup

base_path = os.path.abspath(os.path.dirname(__file__))
os.chdir('..')

version_path = os.path.join(
    base_path,
    'version.txt'
    )

manifest_path = os.path.join(
    base_path,
    'MANIFEST'
    )

if os.path.exists(manifest_path):
    os.remove(manifest_path)
    
setup(name='MailingLogger',
      version=open(version_path).read().strip(),
      description='Emailing LogHandlers for Python and Zope',
      author='Simplistix',
      author_email='support@simplistix.co.uk',
      url='http://www.simplistix.co.uk',
      packages=['MailingLogger'],
      data_files=[('MailingLogger',['component.xml',
                                    'license.txt',
                                    'version.txt'])]
     )
