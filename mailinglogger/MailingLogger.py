# Copyright (c) 2004-2007 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

import datetime
import os
import smtplib
import socket

from email.Utils import formatdate, make_msgid
from email.MIMEText import MIMEText
from logging.handlers import SMTPHandler
from logging import LogRecord, CRITICAL
from mailinglogger.common import SubjectFormatter
from mailinglogger.common import process_ignore

now = datetime.datetime.now

this_dir = os.path.dirname(__file__)
x_mailer = 'MailingLogger '+open(os.path.join(this_dir,'version.txt')).read().strip()
flood_template = open(os.path.join(this_dir,'flood_template.txt')).read()

class MailingLogger(SMTPHandler):

    def __init__(self,
                 fromaddr,
                 toaddrs,
                 mailhost='localhost',
                 subject='%(line)s',
                 send_empty_entries=False,
                 flood_level=10,
                 username=None,
                 password=None,
                 ignore=(),
                 headers=None):
        SMTPHandler.__init__(self,mailhost,fromaddr,toaddrs,subject)
        self.subject_formatter = SubjectFormatter(subject)
        self.send_empty_entries = send_empty_entries
        self.flood_level = flood_level
        self.hour = now().hour
        self.sent = 0
        self.username = username
        self.password = password
        self.ignore = process_ignore(ignore)
        self.headers = headers or {}
        if not self.mailport:
            self.mailport = smtplib.SMTP_PORT

    def getSubject(self,record):
        return self.subject_formatter.format(record)

    def emit(self,record):
        msg = record.getMessage()
        if not self.send_empty_entries and not msg.strip():
            return

        for criterion in self.ignore:
            if criterion(msg):
                return

        current_time = now()
        current_hour = current_time.hour
        if current_hour != self.hour:
            self.hour = current_hour
            self.sent = 0
        if self.sent == self.flood_level:
            # send critical error
            record = LogRecord(
                name = 'flood',
                level = CRITICAL,
                pathname = '',
                lineno = 0,
                msg = flood_template % (self.sent,
                                        current_time.strftime('%H:%M:%S'),
                                        current_hour+1),
                args = (),
                exc_info = None)
        elif self.flood_level and self.sent > self.flood_level:
            # do nothing, we've sent too many emails already
            return
        self.sent += 1

        # actually send the mail
        try:
            msg = self.format(record)
            email = MIMEText(msg)
            for header,value in self.headers.items():
                email[header]=value
            email['Subject']=self.getSubject(record)
            email['From']=self.fromaddr
            email['To']=', '.join(self.toaddrs)
            email['X-Mailer']=x_mailer
            email['Date']=formatdate()
            email['Message-ID']=make_msgid('MailingLogger')
            smtp = smtplib.SMTP(self.mailhost, self.mailport)
            if self.username and self.password:
                smtp.login(self.username,self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, email.as_string())
            smtp.quit()
        except:
            self.handleError(record)
