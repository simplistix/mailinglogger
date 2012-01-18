# Copyright (c) 2012 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from logging import getLogger
from mailinglogger.common import HTMLFilter
from unittest import TestCase
from testfixtures import LogCapture

class TestHTMLFilter(TestCase):

    def setUp(self):
        self.log = LogCapture()
        self.logger = getLogger()
        self.log.addFilter(HTMLFilter())

    def tearDown(self):
        self.log.uninstall()
        
    def test_plain_string(self):
        self.logger.info('foo')
        self.log.check(('root', 'INFO', 'foo'),)

    def test_html_string(self):
        self.logger.info('<foo &bar>')
        self.log.check(('root', 'INFO', '&lt;foo &amp;bar&gt;'),)

    def test_with_params_string(self):
        self.logger.info('%s', 'foo')
        self.log.check(('root', 'INFO', 'foo'),)

    def test_plain_unicode(self):
        self.logger.info(u"accentu\u00E9")
        self.log.check(('root', 'INFO', u'accentu\xe9'),)

    def test_html_unicode(self):
        self.logger.info(u"<u\u00E9 &bar>")
        self.log.check(('root', 'INFO', u'&lt;u\xe9 &amp;bar&gt;'),)

    def test_with_params_unicode(self):
        self.logger.info(u"\u00E9%s", u"accentu\u00E9")
        self.log.check(('root', 'INFO', u'\xe9accentu\xe9'),)

    def test_some_object(self):
        class AnObject(object):
            def __repr__(self):
                return 'obj'
            __str__ = __repr__
        self.logger.info(AnObject())
        self.log.check(('root', 'INFO', 'obj'),)
