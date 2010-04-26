# Copyright (c) 2007-2010 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
import unittest

from zconfig import setUp,tearDown,Tests
from doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

schema_text = '''
<schema>
  <import package="ZConfig.components.logger" file="eventlog.xml"/>
  <import package="ZConfig.components.logger" file="handlers.xml"/>
  <import package="mailinglogger"/>
  <section type="eventlog" name="*" attribute="eventlog"/>
</schema>
'''

class ZConfigTests(Tests):

    def getSchemaPath(self):
        f = open('schema.xml','w')
        f.write(schema_text)
        f.close()
        return 'schema.xml'
        
    def getConfigPrefix(self):
        return '<eventlog>\n'

    def getConfigPostfix(self):
        return '\n</eventlog>'
    
options = REPORT_NDIFF|ELLIPSIS
def test_suite():
    try:
        import ZConfig
    except ImportError:
        # no ZConfig
        if os.environ.get('mailinglogger_env')=='zconfig':
            raise
        return unittest.TestSuite()
    return unittest.TestSuite((
        DocFileSuite('../docs/zconfig.txt',
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        unittest.makeSuite(ZConfigTests),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
