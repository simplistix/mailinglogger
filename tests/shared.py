import atexit
import datetime
import logging
import smtplib
import time

from mailinglogger.MailingLogger import MailingLogger
from mailinglogger.SummarisingLogger import SummarisingLogger

class DummySMTP:

    broken = False

    sent = []

    stdout=True
    
    old_smtp = None

    @staticmethod
    def install(stdout=True):
        if DummySMTP.old_smtp is None:
            DummySMTP.old_smtp = smtplib.SMTP
            smtplib.SMTP = DummySMTP
        DummySMTP.sent = []
        DummySMTP.stdout=stdout

    @staticmethod
    def remove():
        if DummySMTP.old_smtp is not None:
            smtplib.SMTP = DummySMTP.old_smtp
            DummySMTP.old_smtp = None
        DummySMTP.stdout=True
    
    def __init__(self,mailhost,port):
        if self.broken:
            raise RuntimeError
        self.mailhost = mailhost
        self.port = port
        
    def sendmail(self,fromaddr,toaddrs,msg):
        msg = msg.replace('\r\n','\n')
        if self.stdout:
            print 'sending to %r from %r using %r' % (
                toaddrs,fromaddr,(self.mailhost,self.port)
                )
            print msg
        else:
            self.sent.append((
                toaddrs,fromaddr,(self.mailhost,self.port),msg
                ))
        
    def quit(self):
        pass

class Dummy:

    def __init__(self,value):
        self.value = value

    def __call__(self):
        return self.value
    
old_time = None
old_now = None

def setTime(ts='2007-01-01 10:00:00'):
    global old_time,old_now
    from mailinglogger import MailingLogger
    if old_now is None:
        old_now = MailingLogger.now
    if old_time is None:
        old_time = time.time
    t = datetime.datetime(*time.strptime(ts,"%Y-%m-%d %H:%M:%S")[0:6])
    MailingLogger.now = Dummy(t)
    time.time = Dummy(time.mktime(t.timetuple()))

def resumeTime():
    global old_time,old_now
    from mailinglogger import MailingLogger
    if old_now is not None:
        MailingLogger.now = old_now
        old_now = None
    if old_time is not None:
        time.time = old_time
        old_time = None

old_hostname = None
def setHostName(name):
    global old_hostname
    from mailinglogger import common
    if old_hostname is None:
        old_hostname = common.gethostname
    common.gethostname = Dummy(name)
    
def unsetHostName():
    global old_hostname
    from mailinglogger import common
    if old_hostname is not None:
        common.gethostname = old_hostname

def setUp(test):
    to_handle = [logging.getLogger()]
    for logger in logging.Logger.manager.loggerDict.values():
        to_handle.append(logger)
    for logger in to_handle:
        if isinstance(logger,logging.PlaceHolder):
            continue
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
    DummySMTP.install()
    test.globs['smtp']=DummySMTP
    test.globs['setHostName']=setHostName
    test.globs['setTime']=setTime
    test.globs['resumeTime']=resumeTime
    
def tearDown(test):
    # make sure we have no dummy smtp
    DummySMTP.remove()
    # just in case ;-)
    resumeTime()
    # make sure we haven't registered any atexit funcs
    atexit._exithandlers[:] = []
    
