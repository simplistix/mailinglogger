# Copyright (c) 2004-2014 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os

from atexit import register
from collections import deque
from logging import CRITICAL, FileHandler, Formatter, LogRecord
from mailinglogger.MailingLogger import MailingLogger
from tempfile import mkstemp

flood_template = '%i messages not included as flood limit of %i exceeded'


class SummarisingLogger(FileHandler):

    maxlevelno = 0
    message_count = 0
    tail = None

    def __init__(self,
                 fromaddr,
                 toaddrs,
                 mailhost='localhost',
                 subject='Summary of Log Messages (%(levelname)s)',
                 send_empty_entries=True,
                 atexit=True,
                 username=None,
                 password=None,
                 headers=None,
                 send_level=None,
                 template=None,
                 charset='utf-8',
                 content_type='text/plain',
                 flood_level=100,
                 ):
        # create the "real" mailinglogger
        self.mailer = MailingLogger(fromaddr,
                                    toaddrs,
                                    mailhost,
                                    subject,
                                    send_empty_entries,
                                    username=username,
                                    password=password,
                                    headers=headers,
                                    template=template,
                                    charset=charset,
                                    content_type=content_type)
        # set the mailing logger's log format
        self.mailer.setFormatter(Formatter('%(message)s'))
        self.send_level = send_level
        self.charset = charset
        self.flood_level = flood_level
        self.open()
        # register our close method
        if atexit:
            register(self.close)

    def open(self):
        # create a temp file logger to store log entries
        self.fd, self.filename = mkstemp()
        FileHandler.__init__(self, self.filename, 'w', encoding=self.charset)
        self.closed = False

    def setLevel(self, lvl):
        self.mailer.setLevel(lvl)
        FileHandler.setLevel(self, lvl)

    def emit(self, record):
        if self.closed:
            return

        if record.levelno > self.maxlevelno:
            self.maxlevelno = record.levelno

        self.message_count += 1
        if self.message_count > self.flood_level:
            if self.tail is None:
                self.tail = deque(maxlen=5)
            self.tail.append(record)
        else:
            FileHandler.emit(self, record)

    def close(self):
        if self.closed:
            return

        if self.message_count > self.flood_level:
            hidden = self.message_count - self.flood_level - len(self.tail)
            if hidden:
                # send critical error
                FileHandler.emit(self, LogRecord(
                    name='flood',
                    level=CRITICAL,
                    pathname='',
                    lineno=0,
                    msg=flood_template % (
                        self.message_count - self.flood_level - len(self.tail),
                        self.flood_level
                    ),
                    args=(),
                    exc_info=None
                ))
            for record in self.tail:
                FileHandler.emit(self, record)

        FileHandler.close(self)
        f = os.fdopen(self.fd)
        summary = f.read().decode(self.charset)
        f.close()
        # try and encode in ascii, to keep emails simpler:
        try:
            summary = summary.encode('ascii')
        except UnicodeEncodeError:
            # unicode it is then
            pass
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if self.send_level is None or self.maxlevelno >= self.send_level:
            self.mailer.handle(
                LogRecord(
                    name='Summary',
                    level=self.maxlevelno,
                    pathname='',
                    lineno=0,
                    msg=summary,
                    args=(),
                    exc_info=None
                )
            )
        self.closed = True

    def reopen(self):
        self.close()
        self.open()
