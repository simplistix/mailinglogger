import logging
import smtplib
from collections import namedtuple
from ssl import SSLContext

from testfixtures import Replacer, test_datetime, test_time
from testfixtures.mock import call


SentMessage = namedtuple('SentMessage', ['to_addr', 'from_addr', 'host', 'port', 'msg', 'username', 'password'])


class DummySMTP:

    broken = False

    sent = []
    calls = []

    stdout = True

    old_smtp = None

    username = None
    password = None

    @staticmethod
    def install(stdout=False):
        if DummySMTP.old_smtp is None:
            DummySMTP.old_smtp = smtplib.SMTP
            smtplib.SMTP = DummySMTP
        DummySMTP.sent = []
        DummySMTP.calls = []
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
        self.calls.append(call.login(username, password))
        self.username = username
        self.password = password

    def sendmail(self, fromaddr, toaddrs, msg):
        sent = SentMessage(
            to_addr=toaddrs,
            from_addr=fromaddr,
            host=self.mailhost,
            port=self.port,
            msg=msg.replace('\r\n', '\n'),
            username=self.username,
            password=self.password,
        )
        self.calls.append(call.sendmail(fromaddr, toaddrs, '...'))
        if self.stdout:
            print('sending to %r from %r using %r' % (
                toaddrs, fromaddr, (self.mailhost, self.port)
            ))
            if self.username and self.password:
                print('(authenticated using username:%r and password:%r)' % (
                    self.username,
                    self.password,
                ))
            parts = msg.split('\n\n', 1)
            if len(parts)>1:
                headers, body = parts
                headers = '\n'.join(sorted(headers.split('\n')))
                print(headers, end='')
                print('\n\n', end='')
                print(body)
            else:
                print(msg)
        else:
            self.sent.append(sent)

    def quit(self):
        self.calls.append(call.quit())

    def starttls(self, context=None):
        if context:
            assert isinstance(context, SSLContext)
        self.calls.append(call.starttls(context=context))

    def ehlo(self):
        self.calls.append(call.ehlo())


class Dummy:

    def __init__(self, value):
        self.value = value

    def __call__(self, *args):
        return self.value


def removeHandlers():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    hl = getattr(logging, '_handlerList', None)
    if hl:
        hl[:] = []


def _setUp(d, stdout=True):
    removeHandlers()
    DummySMTP.install(stdout=stdout)

    atexit_handlers = []
    datetime = test_datetime(2007, 1, 1, 10, delta=0)
    time = test_time(2007, 1, 1, 10, delta=0)
    r = Replacer()
    r.replace('atexit.register', atexit_handlers.append)
    r.replace('mailinglogger.MailingLogger.now', datetime.now)
    r.replace('mailinglogger.common.gethostname', Dummy('host.example.com'))
    r.replace('time.time', time)
    r.replace('os.environ.TZ', 'GMT', strict=False)

    d['atexit_handlers'] = atexit_handlers
    d['r'] = r
    d['smtp'] = DummySMTP
    d['datetime'] = datetime
    d['time'] = time
    d['removeHandlers'] = removeHandlers


def _tearDown(d):
    # restore stuff we've mocked out
    d['r'].restore()
    # make sure we have no dummy smtp
    DummySMTP.remove()
