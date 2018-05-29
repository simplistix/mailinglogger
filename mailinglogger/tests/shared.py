import logging
import smtplib
from collections import namedtuple
from email.parser import Parser
from time import tzset

from six import PY3
from testfixtures import Replacer, test_datetime, test_time, compare

from mailinglogger.common import exit_handler_manager

SentMessage = namedtuple('SentMessage', ['to_addr', 'from_addr', 'host', 'port', 'msg', 'username', 'password'])


class DummySMTP:

    broken = False

    sent = []

    stdout = True

    old_smtp = None

    username = None
    password = None

    @staticmethod
    def install():
        if DummySMTP.old_smtp is None:
            DummySMTP.old_smtp = smtplib.SMTP
            smtplib.SMTP = DummySMTP
        DummySMTP.sent = []

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
        self.sent.append(SentMessage(
            to_addr=toaddrs,
            from_addr=fromaddr,
            host=self.mailhost,
            port=self.port,
            msg=msg,
            username=self.username,
            password=self.password,
        ))

    def quit(self):
        pass

    def check_sent_message_matches(self, expected_message, hostname='localhost', to_addr=None,
                                   from_addr='from@example.com', port=25, username=None, password=None):

        last_sent_email = self.sent[-1]
        self._check_server_configuration(from_addr, hostname, last_sent_email, password, port, to_addr, username)

        actual_email = Parser().parsestr(last_sent_email.msg)
        expected_email = Parser().parsestr(expected_message.replace('<BLANKLINE>', ''))

        self._check_headers_match(actual_email, expected_email)
        self._check_bodies_match(actual_email, expected_email)
        return True

    def _check_server_configuration(self, from_addr, hostname, last_sent_email, password, port, to_addr, username):
        to_addr = to_addr or ['to@example.com']
        compare(actual=last_sent_email.to_addr, expected=to_addr)
        compare(actual=last_sent_email.from_addr, expected=from_addr)
        compare(actual=last_sent_email.host, expected=hostname)
        compare(actual=last_sent_email.port, expected=port)
        compare(actual=last_sent_email.username, expected=username)
        compare(actual=last_sent_email.password, expected=password)

    def _check_bodies_match(self, actual_email, expected_email):
        expected_payload = expected_email.get_payload().strip()
        actual_payload = actual_email.get_payload().strip()
        for line_number, (expected, actual) in enumerate(
                zip(expected_payload.split('\n'), actual_payload.split('\n'))):
            if '...' in expected:
                self._check_line_containing_ellipsis(actual, expected, 'line', line_number)
            elif len(expected) == 0:
                assert not actual.strip(), '\nExpected line: %s to be blank in message:\n%s' % (
                    line_number, actual_payload)
            else:
                assert expected.strip() == actual.strip(), '\nExpected:%s\nActual:%s\nWhen comparing line:%i with actual message: %s' % (
                    expected, actual, line_number,
                    actual_payload)

    def _check_headers_match(self, actual_email, expected_email):
        actual_header_keys = set(actual_email.keys())
        expected_header_keys = set(expected_email.keys())
        assert actual_header_keys == expected_header_keys, "Headers differ\nExpected headers:\n%s\nActual headers:\n%s" % (
            expected_header_keys, actual_header_keys)
        for key in expected_header_keys:
            actual_header = actual_email[key]
            expected_header = expected_email[key]
            if '...' in expected_header:
                self._check_line_containing_ellipsis(actual_header, expected_header, 'header', key)
            else:
                assert actual_header == expected_header, "Headers %s differs.\nExpected: %s\nActual:%s" % (
                    key, expected_header,
                    actual_header)

    def _check_line_containing_ellipsis(self, actual_header, expected_header, identifier, key):
        for fragment in expected_header.split('...'):
            assert fragment in actual_header, '\nExpected fragment %s not found in:\n%s\nwhen comparing header: %s' % (
                fragment, actual_header, identifier, key)


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


def _setUp(d):
    removeHandlers()
    DummySMTP.install()

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
    exit_handler_manager.clear_at_exit_handlers()
