from sys import version_info
from html import escape

from logging import Formatter
from socket import gethostname


class SubjectFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None):
        if version_info >= (3, 8):
            super().__init__(fmt, datefmt, validate=False)
        else:
            Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        record.message = record.getMessage()
        if self._fmt.find('%(line)') >= 0:
            record.line = record.message.split('\n')[0]
        if self._fmt.find("%(asctime)") >= 0:
            record.asctime = self.formatTime(record, self.datefmt)
        if self._fmt.find("%(hostname)") >= 0:
            record.hostname = gethostname()
        return self._fmt % record.__dict__


class HTMLFilter(object):

    def filter(self, record):
        record.msg = escape(record.getMessage(), quote=True)
        record.args = ()
        return True
