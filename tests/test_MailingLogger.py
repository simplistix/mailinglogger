# Copyright (c) 2007 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import logging

from mailinglogger.MailingLogger import MailingLogger
from shared import DummySMTP,setTime,resumeTime
from unittest import TestSuite,makeSuite,TestCase,main

class TestMailingLogger(TestCase):

    handler = None
    
    def getLogger(self):
        return logging.getLogger('')
    
    def setUp(self):
        DummySMTP.install(stdout=False)
        setTime()

    def tearDown(self):
        if self.handler:
            self.getLogger().removeHandler(self.handler)
        resumeTime()
        DummySMTP.remove()
        
    def test_default_flood_limit(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',))
        logger = self.getLogger()
        logger.addHandler(self.handler)
        # log 11 entries
        for i in range(12):
            logger.critical('message')
        # only 1st 10 should get sent
        # +1 for the final warning
        self.assertEqual(len(DummySMTP.sent),11)
        
    def test_flood_protection_bug(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',),
                                     flood_level=1)
        logger = self.getLogger()
        logger.addHandler(self.handler)
        # make it 11pm
        setTime('2007-03-15 23:00:00')
        # paranoid check
        self.assertEqual(len(DummySMTP.sent),0)
        # log until flood protection kicked in
        logger.critical('message1')
        logger.critical('message2')
        # check - 1 logged, 1 final warning
        self.assertEqual(len(DummySMTP.sent),2)
        # check nothing emitted
        logger.critical('message3')
        self.assertEqual(len(DummySMTP.sent),2)
        # advance time past midnight
        setTime('2007-03-15 00:00:00')
        # log again
        logger.critical('message4')
        # check we are emitted now!
        self.assertEqual(len(DummySMTP.sent),3)
        
def test_suite():
    return TestSuite((
        makeSuite(TestMailingLogger),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
