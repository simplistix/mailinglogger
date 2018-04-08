import logging
import smtplib
from email.parser import Parser
from time import tzset

from six import PY3
from testfixtures import Replacer, test_datetime, test_time, compare, StringComparison

from mailinglogger.common import exit_handler_manager


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

    def compare_sent_message(self, expected_message):
        latest_sent_message = self.sent[-1][3]
        actual_email = Parser().parsestr(latest_sent_message)
        expected_email = Parser().parsestr(expected_message.replace('<BLANKLINE>', ''))
        actual_header_keys = set(actual_email.keys())
        expected_header_keys = set(expected_email.keys())
        assert actual_header_keys == expected_header_keys, "Headers differ\nExpected headers:\n%s\nActual headers:\n%s" % (
            expected_header_keys, actual_header_keys)
        for key in expected_header_keys:
            actual_header = actual_email[key]
            expected_header = expected_email[key]
            if '...' in expected_header:
                for fragment in actual_header.split('...'):
                    assert fragment in actual_header, '\nExpected fragment %s not found in:\n%s\nwhen comparing header: %s' % (
                        fragment, actual_header, key)
            else:
                assert actual_header == expected_header, "Headers %s differs.\nExpected: %s\nActual:%s" % (
                    key, expected_header,
                    actual_header)

        expected_payload = expected_email.get_payload().strip()
        actual_payload = actual_email.get_payload().strip()
        for line_number, (expected, actual) in enumerate(
                zip(expected_payload.split('\n'), actual_payload.split('\n'))):
            if '...' in expected:
                for fragment in actual.split('...'):
                    assert fragment in actual, '\nExpected fragment %s not found in:\n%s\nwhen comparing line: %s' % (
                        fragment, actual, line_number)
            elif len(expected) == 0:
                assert not actual.strip(), '\nExpected line: %s to be blank in message:\n%s' % (
                    line_number, actual_payload)
            else:
                assert expected.strip() == actual.strip(), '\nExpected:%s\nActual:%s\nWhen comparing line:%i with actual message: %s' % (
                    expected, actual, line_number,
                    actual_payload)
        return True


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


def _check_sent_message(expected_message, m):
    sent_email = Parser().parsestr(m)
    sent_message = sent_email.get_payload(decode=True)
    if PY3:
        sent_message = sent_message.decode(sent_email.get_content_charset())
    assert expected_message in sent_message, "Expected: %s to be in sent email:\n%s" % (expected_message, sent_message)
