# Copyright (c) 2004-2007 Simplistix Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from ZConfig.components.logger.handlers import HandlerFactory
from ZConfig.components.logger.handlers import ctrl_char_insert
from mailinglogger.MailingLogger import MailingLogger
from mailinglogger.SummarisingLogger import SummarisingLogger

class MailingLoggerHandlerFactory(HandlerFactory):

    def mailhost(self):
        host, port = self.section.smtp_server
        if not port:
            return host
        else:
            return host, port

    def headers(self):
        if self.section.headers:
            return self.section.headers.values
        else:
            return {}
        
    def create_loghandler(self):
        return MailingLogger(self.section.fromaddr,
                             self.section.toaddrs,
                             self.mailhost(),
                             self.section.subject,
                             self.section.send_empty_entries,
                             self.section.flood_level,
                             self.section.username,
                             self.section.password,
                             self.section.ignore,
                             self.headers())

class SummarisingLoggerHandlerFactory(MailingLoggerHandlerFactory):

    def create_loghandler(self):        
        return SummarisingLogger(self.section.fromaddr,
                                 self.section.toaddrs,
                                 self.mailhost(),
                                 self.section.subject,
                                 self.section.send_empty_entries,
                                 self.section.atexit,
                                 self.section.username,
                                 self.section.password,
                                 self.section.ignore,
                                 self.headers())

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
    'hostname':'ahost',
    'funcName':'a func'
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
