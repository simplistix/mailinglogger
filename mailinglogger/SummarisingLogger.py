# Copyright (c) 2004-2005 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import os

from atexit import register
from logging import FileHandler, Formatter, INFO, LogRecord
from mailinglogger.MailingLogger import MailingLogger
from mailinglogger.common import process_ignore
from tempfile import mkstemp

class SummarisingLogger(FileHandler):

    maxlevelno = 0
    
    def __init__(self,
                 fromaddr,
                 toaddrs,
                 mailhost='localhost',
                 subject='Summary of Log Messages (%(levelname)s)',
                 send_empty_entries=True,
                 atexit=True,
                 username=None,
                 password=None,
                 ignore=(),
                 headers=None):
        # create the "real" mailinglogger
        self.mailer = MailingLogger(fromaddr,
                                    toaddrs,
                                    mailhost,
                                    subject,
                                    send_empty_entries,
                                    username=username,
                                    password=password,
                                    headers=headers)
        # set the mailing logger's log format
        self.mailer.setFormatter(Formatter('%(message)s'))
        self.ignore = process_ignore(ignore)
        self.open()
        # register our close method
        if atexit:
            register(self.close)

    def open(self):
        # create a temp file logger to store log entries
        self.fd, self.filename = mkstemp()
        FileHandler.__init__(self,self.filename,'w')
        self.closed = False
        
    def setLevel(self,lvl):
        self.mailer.setLevel(lvl)
        FileHandler.setLevel(self,lvl)

    def emit(self,record):
        if self.closed:
            return

        for criterion in self.ignore:
            if criterion(record.msg):
                return

        if record.levelno>self.maxlevelno:
            self.maxlevelno = record.levelno
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
                level = self.maxlevelno,
                pathname = '',
                lineno = 0,
                msg = summary,
                args = (),
                exc_info = None
                )
            )
        self.closed = True
            
    def reopen(self):
        self.close()
        self.open()
        
        
