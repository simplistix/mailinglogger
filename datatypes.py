# Copyright (c) 2004-2005 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from zLOG.datatypes import HandlerFactory, ctrl_char_insert
from Products.MailingLogger.MailingLogger import MailingLogger
from Products.MailingLogger.SummarisingLogger import SummarisingLogger

class MailingLoggerHandlerFactory(HandlerFactory):

    klass = MailingLogger
    
    def create_loghandler(self):
        host, port = self.section.smtp_server
        if not port:
            mailhost = host
        else:
            mailhost = host, port
        return self.klass(mailhost,
                          self.section.fromaddr,
                          self.section.toaddrs,
                          self.section.subject,
                          self.section.send_empty_entries,
                          self.section.flood_level)

class SummarisingLoggerHandlerFactory(MailingLoggerHandlerFactory):

    klass = SummarisingLogger
    
_log_format_variables = {
    'name': '',
    'levelno': '3',
    'levelname': 'DEBUG',
    'pathname': 'apath',
    'filename': 'afile',
    'module': 'amodule',
    'lineno': 1,
    'created': 1.1,
    'asctime': 'atime',
    'msecs': 1,
    'relativeCreated': 1,
    'thread': 1,
    'message': 'amessage',
    'line':'aline',
    }

def subject_log_format(value):
    value = ctrl_char_insert(value)
    try:
        # Make sure the format string uses only names that will be
        # provided, and has reasonable type flags for each, and does
        # not expect positional args.
        value % _log_format_variables
    except (ValueError, KeyError):
        raise ValueError, 'Invalid log format string %s' % value
    return value
