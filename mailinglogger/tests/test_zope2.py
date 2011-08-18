# Copyright (c) 2007-2011 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
import unittest

from doctest import REPORT_NDIFF, ELLIPSIS
from mailinglogger.tests.test_docs import docs_dir
from manuel import doctest, codeblock
from manuel.testing import TestSuite
from testfixtures.manuel import Files
from zconfig import setUp, tearDown, Tests

class Zope2Tests(Tests):

    def getSchemaPath(self):
        import Zope2.Startup
        return os.path.join(os.path.dirname(
            os.path.realpath(Zope2.Startup.__file__)
            ),'zopeschema.xml')
        
    def getConfigPrefix(self):
        return '''
instancehome %s
%%import mailinglogger
<eventlog>
''' % self.globs['INSTANCE_HOME']

    def getConfigPostfix(self):
        return '\n</eventlog>'

options = REPORT_NDIFF|ELLIPSIS

def test_suite():
    try:
        from Zope2 import app
    except ImportError:
        # no zope 2
        if os.environ.get('mailinglogger_env')=='zope2':
            raise
        return unittest.TestSuite()
    m =  doctest.Manuel(optionflags=REPORT_NDIFF|ELLIPSIS)
    m += codeblock.Manuel()
    m += Files('tempdir')
    return unittest.TestSuite((
        TestSuite(m,
                  os.path.join(docs_dir, 'zope2.txt'),
                  setUp=setUp,
                  tearDown=tearDown
                  ),
        unittest.makeSuite(Zope2Tests),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
