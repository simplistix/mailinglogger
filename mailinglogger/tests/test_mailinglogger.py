# Copyright (c) 2007-2012 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import logging
import time

from email.charset import Charset
from mailinglogger.common import RegexConversion
from mailinglogger.MailingLogger import MailingLogger
from shared import DummySMTP, setUp, tearDown
from unittest import TestSuite,makeSuite,TestCase,main

class TestMailingLogger(TestCase):

    def getLogger(self):
        return logging.getLogger('')
    
    def setUp(self):
        setUp(None, self, stdout=False)

    def tearDown(self):
        tearDown(None,self)
        
    def test_imports(self):
        from mailinglogger.MailingLogger import MailingLogger
        from mailinglogger import MailingLogger
    
    def test_tls_secure_option_1(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',), username='x', password='y', secure='')
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical('message')
        self.assertEqual(len(DummySMTP.sent),1)

    def test_tls_secure_option_2(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',), username='x', password='y', secure='keyfile')
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical('message')
        self.assertEqual(len(DummySMTP.sent),1)

    def test_tls_secure_option_3(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',), username='x', password='y', secure='keyfile certfile')
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical('message')
        self.assertEqual(len(DummySMTP.sent),1)

    def test_tls_secure_option_exception(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',), username='x', password='y', secure='keyfile certfile other')
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical('message')
        self.assertEqual(len(DummySMTP.sent),0)

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
        self.datetime.set(2007,3,15,23)
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
        self.datetime.set(2007,3,15)
        # log again
        logger.critical('message4')
        # check we are emitted now!
        self.assertEqual(len(DummySMTP.sent),3)

    def test_ignore(self):
        ignored = [ RegexConversion('^bad start')
                  , RegexConversion('(.*)Some String')
                  , RegexConversion('(.*)http:(.*)\/view')
                  ]
        self.handler = MailingLogger( 'from@example.com'
                                    , ('to@example.com',)
                                    , ignore=ignored
                                    )
        logger = self.getLogger()
        logger.addHandler(self.handler)
        # paranoid check
        self.assertEqual(len(DummySMTP.sent),0)

        # Now test a few variations
        logger.critical('This Line Contains Some String.')
        self.assertEqual(len(DummySMTP.sent),0)

        logger.critical('bad starts and terrible endings')
        self.assertEqual(len(DummySMTP.sent),0)

        logger.critical('NotFoundError: http://my.site.com/some/path/view')
        self.assertEqual(len(DummySMTP.sent),0)

        # Interpolations are also ignored
        logger.critical('NotFoundError: %s',
                        'http://my.site.com/some/path/view')
        self.assertEqual(len(DummySMTP.sent),0)

        # Non-matching stuff still gets through
        logger.critical('message1')
        self.assertEqual(len(DummySMTP.sent),1)

    def test_headers_supplied_get_added_to_those_generated(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',),
                                     headers={'From':'someidiot',
                                              'to':'someidiot'})
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical('message')
        self.assertEqual(len(DummySMTP.sent),1)
        m = DummySMTP.sent[0][3]
        # the headers specified in the `headers` parameter get added
        # to those generated by mailinglogger - be careful!
        self.failUnless('From: from@example.com' in m)
        self.failUnless('From: someidiot' in m)
        # however, if you try hard you *can* break things :-S
        self.failUnless('To: to@example.com' in m)
        self.failUnless('to: someidiot' in m)
        
    def test_subject_contains_date(self):
        # set up logger
        self.handler = MailingLogger('from@example.com',('to@example.com',),
                                     subject="%(asctime)s")
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical('message')
        self.assertEqual(len(DummySMTP.sent),1)
        m = DummySMTP.sent[0][3]
        self.failUnless('Subject: 2007-01-01 10:00:00,000' in m, m)

    def test_non_string_error_messages_dont_break_logging(self):
        self.handler = MailingLogger('from@example.com',('to@example.com',),)
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical(object())
        self.assertEqual(len(DummySMTP.sent),1)

    def test_template(self):
        self.handler = MailingLogger('from@example.com',('to@example.com',),
                                     template="<before>%s<after>")
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical('message')
        m = DummySMTP.sent[0][3]
        self.failUnless('Subject: message' in m, m)
        self.failUnless('<before>message<after>' in m, m)

    def test_default_charset(self):
        self.handler = MailingLogger('from@example.com', ('to@example.com',), )
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical(u"accentu\u00E9")
        m = DummySMTP.sent[0][3]
        # lovely, utf-8 encoded goodness
        self.failUnless('Subject: =?utf-8?b?YWNjZW50dcOp?=' in m, m)
        self.failUnless('Content-Type: text/plain; charset="utf-8"' in m, m)
        self.failUnless('\nYWNjZW50dcOp' in m, m)

    def test_specified_charset(self):
        self.handler = MailingLogger('from@example.com', ('to@example.com',),
                                     charset='iso-8859-1')
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical(u"accentu\u00E9")
        m = DummySMTP.sent[0][3]
        # lovely, latin-1 encoded goodness
        self.failUnless('\naccentu=E9' in m, m)
        self.failUnless('Content-Type: text/plain; charset="iso-8859-1"' in m, m)
        # no idea why MIMEText doesn't use iso-8859-1 here, best not to
        # argue...
        self.failUnless('Subject: =?utf-8?b?YWNjZW50dcOp?=' in m, m)

    def test_specified_content_type(self):
        self.handler = MailingLogger('from@example.com', ('to@example.com',),
                                     content_type='foo/bar')
        logger = self.getLogger()
        logger.addHandler(self.handler)
        logger.critical(u"message")
        m = DummySMTP.sent[0][3]
        # NB: we drop the 'foo'
        self.failUnless('Content-Type: text/bar' in m, m)

def test_suite():
    return TestSuite((
        makeSuite(TestMailingLogger),
        ))

if __name__ == '__main__':
    unittest.main(default='test_suite')
