# Copyright (c) 2007-2010 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
import unittest

from zconfig import setUp,tearDown,Tests
from doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

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
''' % self.globs['dir']

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
    return unittest.TestSuite((
        DocFileSuite('../docs/zope2.txt',
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        unittest.makeSuite(Zope2Tests),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
