from testfixtures import Replacer, test_datetime, test_time
from time import tzset

import atexit
import logging
import smtplib


class DummySMTP:

    broken = False

    sent = []

    stdout = True

    old_smtp = None

    username = None
    password = None

    @staticmethod
    def install(stdout=True):
        if DummySMTP.old_smtp is None:
            DummySMTP.old_smtp = smtplib.SMTP
            smtplib.SMTP = DummySMTP
        DummySMTP.sent = []
        DummySMTP.stdout = stdout

    @staticmethod
    def remove():
        if DummySMTP.old_smtp is not None:
            smtplib.SMTP = DummySMTP.old_smtp
            DummySMTP.old_smtp = None
        DummySMTP.stdout = True

    def __init__(self, mailhost, port=25):
        self.mailhost = mailhost
        self.port = port

    def login(self, username, password):
        self.username = username
        self.password = password

    def sendmail(self, fromaddr, toaddrs, msg):
        msg = msg.replace('\r\n', '\n')
        if self.stdout:
            print('sending to %r from %r using %r' % (
                toaddrs, fromaddr, (self.mailhost, self.port)
            ))
            if self.username and self.password:
                print('(authenticated using username:%r and password:%r)' % (
                    self.username,
                    self.password,
                ))
            print(msg)
        else:
            self.sent.append((
                toaddrs,
                fromaddr,
                (self.mailhost, self.port),
                msg,
                self.username,
                self.password
            ))

    def quit(self):
        pass


class Dummy:

    def __init__(self, value):
        self.value = value

    def __call__(self, *args):
        return self.value


def removeHandlers():
    to_handle = [logging.getLogger()]
    for logger in to_handle:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
    hl = getattr(logging, '_handlerList', None)
    if hl:
        hl[:] = []


def _setUp(d, stdout=True):
    removeHandlers()
    DummySMTP.install(stdout=stdout)

    datetime = test_datetime(2007, 1, 1, 10, delta=0)
    time = test_time(2007, 1, 1, 10, delta=0)
    r = Replacer()
    r.replace('mailinglogger.MailingLogger.now', datetime.now)
    r.replace('mailinglogger.common.gethostname', Dummy('host.example.com'))
    r.replace('time.time', time)
    r.replace('os.environ.TZ', 'GMT', strict=False)
    tzset()

    d['r'] = r
    d['smtp'] = DummySMTP
    d['datetime'] = datetime
    d['time'] = time
    d['removeHandlers'] = removeHandlers


def _tearDown(d):
    # restore stuff we've mocked out
    d['r'].restore()
    tzset()
    # make sure we have no dummy smtp
    DummySMTP.remove()
    # make sure we haven't registered any atexit funcs
    atexit._exithandlers[:] = []
