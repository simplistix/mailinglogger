# Copyright (c) 2004 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os
import atexit

from logging import FileHandler, Formatter, INFO, LogRecord
from MailingLogger import MailingLogger
from tempfile import mkstemp

class SummarisingLogger(FileHandler):

    def __init__(self, mailhost, fromaddr, toaddrs, subject, send_empty_entries):
        # create the "real" mailinglogger
        self.mailer = MailingLogger(mailhost, fromaddr, toaddrs, subject, send_empty_entries)
        # set the mailing logger's log format
        self.mailer.setFormatter(Formatter('%(message)s'))
        # create a temp file logger to store log entries
        self.fd, self.filename = mkstemp()
        self.mailer_record_level = INFO
        FileHandler.__init__(self,self.filename,'w')
        # register our close method
        self.closed = False
        atexit.register(self.close)

    def setLevel(self,lvl):
        self.mailer.setLevel(lvl)
        FileHandler.setLevel(self,lvl)

    def emit(self,record):
        # keep track of highest level
        if record.levelno > self.level:
            self.mailer_record_level = record.levelno
        # emit to the file
        FileHandler.emit(self,record)

    def close(self):
        if self.closed:
            return
        FileHandler.close(self)
        f = open(self.filename)
        summary = f.read()
        f.close()
        os.close(self.fd)
        os.remove(self.filename)
        self.mailer.handle(
            LogRecord(
                name = 'Summary',
                level = self.level,
                pathname = '',
                lineno = 0,
                msg = summary,
                args = (),
                exc_info = None
                )
            )
        self.closed = True
            

        
