# Copyright (c) 2007 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import logging

from mailinglogger.common import RegexConversion
from mailinglogger.SummarisingLogger import SummarisingLogger
from shared import DummySMTP,setTime,resumeTime
from unittest import TestSuite,makeSuite,TestCase,main

class TestSummarisingLogger(TestCase):

    def setUp(self):
        DummySMTP.install(stdout=False)
        setTime()

    def tearDown(self):
        self.logger.removeHandler(self.handler)
        resumeTime()
        DummySMTP.remove()
        
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
