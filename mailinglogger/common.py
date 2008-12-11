# Copyright (c) 2007-2008 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import re

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
    
class RegexConversion:

    def __init__(self, regex):
        self._rx = re.compile(regex)

    def __call__(self, value):
        return bool(self._rx.search(value))

def process_ignore(ignore):
    if isinstance(ignore,basestring):
        ignore = [ignore]
    result = []
    for i in ignore:
        if not isinstance(i,RegexConversion):
            i = RegexConversion(i)
        result.append(i)
    return result
