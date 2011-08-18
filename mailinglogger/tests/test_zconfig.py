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
    
def test_suite():
    try:
        import ZConfig
    except ImportError:
        # no ZConfig
        if os.environ.get('mailinglogger_env')=='zconfig':
            raise
        return unittest.TestSuite()
    m =  doctest.Manuel(optionflags=REPORT_NDIFF|ELLIPSIS)
    m += codeblock.Manuel()
    m += Files('tempdir')
    return unittest.TestSuite((
        TestSuite(m,
                  os.path.join(docs_dir, 'zconfig.txt'),
                  setUp=setUp,
                  tearDown=tearDown
                  ),
        unittest.makeSuite(ZConfigTests),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
