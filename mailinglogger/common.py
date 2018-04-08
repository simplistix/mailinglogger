from cgi import escape
from logging import Formatter
from socket import gethostname

import atexit

_AT_EXIT_HANDLERS = []

def register_at_exit_handler(handler):
    _AT_EXIT_HANDLERS.append(handler)
    atexit.register(handler)

def clear_at_exit_handlers():
    if hasattr(atexit,'unregister'):
        [atexit.unregister(f) for f in _AT_EXIT_HANDLERS]
    else:
        atexit._exithandlers[:] = []

class SubjectFormatter(Formatter):

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
        record.msg = escape(record.getMessage())
        record.args = ()
        return True
