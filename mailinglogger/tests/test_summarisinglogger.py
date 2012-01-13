# Copyright (c) 2007-2011 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import logging
import os

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
        
    def test_do_send_empty(self):
        self.create('from@example.com',('to@example.com',))
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent),1)
        
    def test_dont_send_empty(self):
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
        
    def test_send_level_filters(self):
        self.create('from@example.com',('to@example.com',),
                    send_level=logging.CRITICAL)
        self.logger.warning('This line will not be sent')
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent),0)
        
    def test_send_level_includes_lower_level(self):
        self.create('from@example.com',('to@example.com',),
                    send_level=logging.CRITICAL)
        self.logger.warning('a warning')
        self.logger.critical('something critical')
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent),1)
        message_text = DummySMTP.sent[0][3]
        self.assertTrue('a warning' in message_text)
        self.assertTrue('something critical' in message_text)

    def test_tmpfile_goes_away(self):
        self.create('from@example.com',('to@example.com',))
        os.remove(self.handler.filename)
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent),1)
        
    def test_default_charset(self):
        self.create('from@example.com', ('to@example.com',), )
        self.logger.critical(u"accentu\u00E9")
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        # lovely, utf-8 encoded goodness
        self.failUnless('Subject: Summary of Log Messages (CRITICAL)' in m, m)
        self.failUnless('Content-Type: text/plain; charset="utf-8"' in m, m)
        self.failUnless('\nYWNjZW50dcOp' in m, m)

    def test_specified_charset(self):
        self.create('from@example.com', ('to@example.com',),
                    charset='iso-8859-1')
        self.logger.critical(u"accentu\u00E9")
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        # lovely, latin-1 encoded goodness
        self.failUnless('\naccentu=E9' in m, m)
        self.failUnless('Content-Type: text/plain; charset="iso-8859-1"' in m, m)
        self.failUnless('Subject: Summary of Log Messages (CRITICAL)' in m, m)

    def test_template(self):
        self.create('from@example.com',('to@example.com',),
                    template='<before>%s<after>')
        logging.critical('message')
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        self.failUnless('Subject: Summary of Log Messages (CRITICAL)' in m, m)
        self.failUnless('<before>message\n<after>' in m, repr(m))
        
    def test_specified_content_type(self):
        self.create('from@example.com', ('to@example.com',),
                    content_type='foo/bar')
        self.logger.critical(u"message")
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        # NB: we drop the 'foo'
        self.failUnless('Content-Type: text/bar' in m, m)

def test_suite():
    return TestSuite((
        makeSuite(TestSummarisingLogger),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
