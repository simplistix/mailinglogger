# Copyright (c) 2007-2014 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from cgi import escape
from logging import Formatter
from socket import gethostname

class SubjectFormatter(Formatter):
    
    def format(self,record):
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
