# Copyright (c) 2004 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from logging.handlers import SMTPHandler
from logging import Formatter

class SubjectFormatter(Formatter):
    
    def format(self,record):
        record.message = record.getMessage()
        if self._fmt.find('%(line)') >= 0:
            record.line = record.message.split('\n')[0]
        if self._fmt.find("%(asctime)") >= 0:
            record.asctime = self.formatTime(record, self.datefmt)
        return self._fmt % record.__dict__
    
class MailingLogger(SMTPHandler):

    def __init__(self, mailhost, fromaddr, toaddrs, subject):
        SMTPHandler.__init__(self,mailhost,fromaddr,toaddrs,subject)
        self.subject_formatter = SubjectFormatter(subject)
        
    def getSubject(self,record):
        return self.subject_formatter.format(record)


