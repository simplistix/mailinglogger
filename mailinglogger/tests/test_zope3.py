# Copyright (c) 2007-2010 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
import unittest

from zconfig import setUp,tearDown,Tests
from doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

class Zope3Tests(Tests):

    def getSchemaPath(self):
        import zope.app.twisted
        return os.path.join(
            os.path.dirname(zope.app.twisted.__file__),'schema.xml'
            )
        
    def getConfigPrefix(self):
        return '''
<zodb/>
<accesslog />

%import mailinglogger
<eventlog>
'''

    def getConfigPostfix(self):
        return '\n</eventlog>'

options = REPORT_NDIFF|ELLIPSIS

def test_suite():
    try:
        from zope.app import twisted
    except ImportError:
        # no zope 3
        if os.environ.get('mailinglogger_env')=='zope3':
            raise
        return unittest.TestSuite()
    return unittest.TestSuite((
        DocFileSuite('../docs/zope3.txt',
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        unittest.makeSuite(Zope3Tests),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
