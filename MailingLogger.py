# Copyright (c) 2004 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.


import os,string
from zLOG import severity_string, log_time, format_exception
from mailer import send

class MailingLogger:
    """ a Logger that sends Mail Messages"""

    def __init__(self):
        #get mail address, subject from environment, severity
        self.address=os.environ.get('MAILING_LOGGER_ADDRESS',None)
        self.server=os.environ.get('MAILING_LOGGER_SMTPSERVER',None)
        self.subject=os.environ.get('MAILING_LOGGER_SUBJECT','Zope Server : ')
        self.severity=string.atoi(os.environ.get('MAILING_LOGGER_SEVERITY','100'))
    
    def __call__(self,subsystem, severity, summary, detail, error):

        if self.address is None or self.server is None:
            # no address to send to or server to use...
            return

        if severity < self.severity:
            # below our level of caring
            return

        severity = severity_string(severity)
        
        body = "------\n%s %s %s %s\n%s\n" %(
            log_time(),
            severity,
            subsystem,
            summary,
            detail,
            )
        
        if error:
            try:
                body = body + format_exception(
                    error[0], error[1], error[2],
                    trailer='\n', limit=100)
            except:
                body = body + "%s: %s\n" % error[:2]

        subject = self.subject + severity

        send(self.address,subject,body,smtp_server=self.server)


