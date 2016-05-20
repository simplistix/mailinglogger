# Copyright (c) 2007-2014 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import logging
import os

from mailinglogger.SummarisingLogger import SummarisingLogger
from mailinglogger.tests.shared import DummySMTP, removeHandlers
from unittest import TestCase


class TestSummarisingLogger(TestCase):

    def setUp(self):
        removeHandlers()
        DummySMTP.install(stdout=False)

    def tearDown(self):
        DummySMTP.remove()

    def test_imports(self):
        from mailinglogger.SummarisingLogger import SummarisingLogger
        from mailinglogger import SummarisingLogger

    def create(self, *args, **kw):
        kw['atexit'] = False
        self.handler = SummarisingLogger(*args, **kw)
        self.logger = logging.getLogger('')
        self.logger.addHandler(self.handler)

    def test_do_send_empty(self):
        self.create('from@example.com', ('to@example.com',))
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 1)

    def test_dont_send_empty(self):
        self.create('from@example.com', ('to@example.com',),
                    send_empty_entries=False)
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 0)

    def test_send_level_filters(self):
        self.create('from@example.com', ('to@example.com',),
                    send_level=logging.CRITICAL)
        self.logger.warning('This line will not be sent')
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 0)

    def test_send_level_includes_lower_level(self):
        self.create('from@example.com', ('to@example.com',),
                    send_level=logging.CRITICAL)
        self.logger.warning('a warning')
        self.logger.critical('something critical')
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 1)
        message_text = DummySMTP.sent[0][3]
        self.assertTrue('a warning' in message_text)
        self.assertTrue('something critical' in message_text)

    def test_tmpfile_goes_away(self):
        self.create('from@example.com', ('to@example.com',))
        os.remove(self.handler.filename)
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 1)

    def test_default_charset(self):
        self.create('from@example.com', ('to@example.com',), )
        self.logger.critical(u"accentu\u00E9")
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        # lovely, utf-8 encoded goodness
        self.assertTrue('Subject: Summary of Log Messages (CRITICAL)' in m, m)
        self.assertTrue('Content-Type: text/plain; charset="utf-8"' in m, m)
        self.assertTrue('\nYWNjZW50dcOp' in m, m)

    def test_specified_charset(self):
        self.create('from@example.com', ('to@example.com',),
                    charset='iso-8859-1')
        self.logger.critical(u"accentu\u00E9")
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        # lovely, latin-1 encoded goodness
        self.assertTrue('\naccentu=E9' in m, m)
        self.assertTrue(
            'Content-Type: text/plain; charset="iso-8859-1"' in m, m)
        self.assertTrue('Subject: Summary of Log Messages (CRITICAL)' in m, m)

    def test_template(self):
        self.create('from@example.com', ('to@example.com',),
                    template='<before>%s<after>')
        logging.critical('message')
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        self.assertTrue('Subject: Summary of Log Messages (CRITICAL)' in m, m)
        self.assertTrue('<before>message\n<after>' in m, repr(m))

    def test_specified_content_type(self):
        self.create('from@example.com', ('to@example.com',),
                    content_type='foo/bar')
        self.logger.critical(u"message")
        logging.shutdown()
        m = DummySMTP.sent[0][3]
        # NB: we drop the 'foo'
        self.assertTrue('Content-Type: text/bar' in m, m)

    def test_flood_level_exceeded(self):
        self.create('from@example.com', ('to@example.com', ),
                    flood_level=3)
        self.handler.setFormatter(
            logging.Formatter('%(levelname)s - %(message)s')
        )
        for i in range(10):
            logging.warning('message %s', i)
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 1)
        m = DummySMTP.sent[0][3]
        self.assertTrue('Subject: Summary of Log Messages (WARNING)' in m, m)
        self.assertTrue('\n'.join([
            'WARNING - message 0',
            'WARNING - message 1',
            'WARNING - message 2',
            'CRITICAL - 2 messages not included as flood limit of 3 exceeded',
            'WARNING - message 5',
            'WARNING - message 6',
            'WARNING - message 7',
            'WARNING - message 8',
        ]) in m, repr(m))

    def test_flood_highest_level_still_recorded(self):
        self.create('from@example.com', ('to@example.com', ),
                    flood_level=1)
        self.handler.setFormatter(
            logging.Formatter('%(levelname)s - %(message)s')
        )
        logging.info('included')
        logging.warning('filtered')
        for i in range(5):
            logging.info('after %i', i)
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 1)
        m = DummySMTP.sent[0][3]
        self.assertTrue('Subject: Summary of Log Messages (WARNING)' in m, m)
        self.assertTrue('\n'.join([
            'INFO - included',
            'CRITICAL - 1 messages not included as flood limit of 1 exceeded',
            'INFO - after 0',
        ]) in m, repr(m))

    def test_flood_except_for_tail(self):
        self.create('from@example.com', ('to@example.com', ),
                    flood_level=1)
        self.handler.setFormatter(
            logging.Formatter('%(levelname)s - %(message)s')
        )
        logging.warning('message 1')
        logging.warning('message 2')
        logging.shutdown()
        self.assertEqual(len(DummySMTP.sent), 1)
        m = DummySMTP.sent[0][3]
        self.assertTrue('Subject: Summary of Log Messages (WARNING)' in m, m)
        self.assertTrue('\n'.join([
            'WARNING - message 1',
            'WARNING - message 2',
        ]) in m, repr(m))
