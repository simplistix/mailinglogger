# Copyright (c) 2007-2011 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import logging

from mailinglogger.common import RegexConversion
from mailinglogger.SummarisingLogger import SummarisingLogger
from shared import DummySMTP, removeHandlers
from unittest import TestSuite,makeSuite,TestCase,main

class TestSummarisingLogger(TestCase):

    def setUp(self):
        removeHandlers()
        DummySMTP.install(stdout=False)

    def tearDown(self):
        DummySMTP.remove()
        
    def test_imports(self):
        from mailinglogger.SummarisingLogger import SummarisingLogger
        from mailinglogger import SummarisingLogger

    def create(self,*args,**kw):
        kw['atexit']=False
        self.handler = SummarisingLogger(*args,**kw)
        self.logger = logging.getLogger('')
        self.logger.addHandler(self.handler)
        
    def test_send_empty(self):
        self.create('from@example.com',('to@example.com',))
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent),1)
        
    def test_send_empty(self):
        self.create('from@example.com',('to@example.com',),
                    send_empty_entries=False)
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent),0)

    def test_send_empty_with_filtering(self):
        self.create('from@example.com',('to@example.com',),
                    send_empty_entries=False,
                    ignore='rubbish')
        self.logger.critical('This Line Contains rubbish.')
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent),0)
        
def test_suite():
    return TestSuite((
        makeSuite(TestSummarisingLogger),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
