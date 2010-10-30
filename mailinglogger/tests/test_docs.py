# Copyright (c) 2007-2010 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import unittest
from doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS
from os.path import dirname,pardir,join
from shared import setUp,tearDown

docs_dir = join(pardir,pardir,'docs')

options = REPORT_NDIFF|ELLIPSIS
def test_suite():
    return unittest.TestSuite((
        DocFileSuite(join(docs_dir,'mailinglogger.txt'),
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        DocFileSuite(join(docs_dir,'summarisinglogger.txt'),
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        DocFileSuite(join(docs_dir,'subjectformatter.txt'),
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
