# Copyright (c) 2007-2010 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import unittest
from shared import setUp,tearDown
from doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

options = REPORT_NDIFF|ELLIPSIS
def test_suite():
    return unittest.TestSuite((
        DocFileSuite('../docs/mailinglogger.txt',
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        DocFileSuite('../docs/summarisinglogger.txt',
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        DocFileSuite('../docs/subjectformatter.txt',
                     optionflags=options,
                     setUp=setUp,
                     tearDown=tearDown),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
