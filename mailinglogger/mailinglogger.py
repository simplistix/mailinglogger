import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from logging import LogRecord, CRITICAL
from logging.handlers import SMTPHandler
from ssl import SSLContext
from typing import Union

from .common import SubjectFormatter

this_dir = os.path.dirname(__file__)
version = open(os.path.join(this_dir, 'version.txt')).read().strip()
x_mailer = 'MailingLogger ' + version
flood_template = open(os.path.join(this_dir, 'flood_template.txt')).read()


class MailingLogger(SMTPHandler):

    now = datetime.datetime.now

    def __init__(self,
                 fromaddr,
                 toaddrs,
                 mailhost='localhost',
                 subject='%(line)s',
                 send_empty_entries=False,
                 flood_level=10,
                 username=None,
                 password=None,
                 headers=None,
                 template=None,
                 charset='utf-8',
                 content_type='text/plain',
                 secure: Union[bool, SSLContext] = None):
        SMTPHandler.__init__(self, mailhost, fromaddr, toaddrs, subject)
        self.subject_formatter = SubjectFormatter(subject)
        self.send_empty_entries = send_empty_entries
        self.flood_level = flood_level
        self.hour = self.now().hour
        self.sent = 0
        self.username = username
        self.password = password
        self.headers = headers or {}
        self.template = template
        self.charset = charset
        self.content_type = content_type
        self.secure: Union[bool, SSLContext] = secure
        if secure and not (username and password):
            raise TypeError('username and password required for secure')
        if not self.mailport:
            self.mailport = smtplib.SMTP_PORT

    def getSubject(self, record):
        return self.subject_formatter.format(record)

    def emit(self, record):
        msg = record.getMessage()
        if not self.send_empty_entries and not msg.strip():
            return

        current_time = self.now()
        current_hour = current_time.hour
        if current_hour != self.hour:
            self.hour = current_hour
            self.sent = 0
        if self.sent == self.flood_level:
            # send critical error
            record = LogRecord(
                name='flood',
                level=CRITICAL,
                pathname='',
                lineno=0,
                msg=flood_template % (self.sent,
                                      current_time.strftime('%H:%M:%S'),
                                      current_hour + 1),
                args=(),
                exc_info=None)
        elif self.flood_level and self.sent > self.flood_level:
            # do nothing, we've sent too many emails already
            return
        self.sent += 1

        # actually send the mail
        try:
            msg = self.format(record)
            if self.template is not None:
                msg = self.template % msg
            subtype = self.content_type.split('/')[-1]
            try:
                msg = msg.encode('ascii')
                charset = 'ascii'
            except UnicodeEncodeError:
                charset = self.charset
            email = MIMEText(msg, subtype, charset)

            for header, value in self.headers.items():
                email[header] = value
            email['Subject'] = self.getSubject(record)
            email['From'] = self.fromaddr
            email['To'] = ', '.join(self.toaddrs)
            email['X-Mailer'] = x_mailer
            email['X-Log-Level'] = record.levelname
            email['Date'] = formatdate()
            email['Message-ID'] = make_msgid('MailingLogger')
            smtp = smtplib.SMTP(self.mailhost, self.mailport)
            if self.username and self.password:
                if self.secure is not None:
                    if isinstance(self.secure, SSLContext):
                        context=self.secure
                    else:
                        context=None
                    smtp.starttls(context=context)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, email.as_string())
            smtp.quit()
        except:
            self.handleError(record)
