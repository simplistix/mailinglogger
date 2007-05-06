# base stuff for all zconfig-based (ZConfig, Zope 2, Zope 3) based tests
import atexit
import logging
import os
import shutil
import unittest
from mailinglogger.MailingLogger import MailingLogger
from mailinglogger.SummarisingLogger import SummarisingLogger
from shared import setUp as shared_setUp
from shared import tearDown as shared_tearDown
from tempfile import mkdtemp
from ZConfig import loadSchema,loadConfig
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF,ELLIPSIS

def setUp(test):
    shared_setUp(test)
    dir = test.globs['dir'] = mkdtemp()
    os.mkdir(os.path.join(dir,'etc'))
    test.globs['startdir'] = os.getcwd()
    test.globs['os'] = os
    test.globs['INSTANCE_HOME'] = dir
    os.chdir(dir) 
    
def tearDown(test):
    shared_tearDown(test)
    os.chdir(test.globs['startdir'])
    shutil.rmtree(test.globs['dir'])

class Tests(unittest.TestCase):

    def setUp(self):
        self.globs = {}
        setUp(self)
        self.schema = loadSchema(self.getSchemaPath())
        
    def tearDown(self):
        tearDown(self)

    def _loadConfig(self,text):
        f = open('test.conf','w')
        f.write(self.getConfigPrefix())
        f.write(text)
        f.write(self.getConfigPostfix())
        f.close()
        config, handlers = loadConfig(self.schema, 'test.conf')
        return config

    def _checkHandler(self,h,
                      klass,
                      normal_format,
                      date_format,
                      **expected):
        # class
        self.failUnless(isinstance(h,klass))
        # formatter
        f = h.formatter
        self.assertEqual(f._fmt,normal_format)
        self.assertEqual(f.datefmt,date_format)
        self.assertEqual(f.datefmt,date_format)
        # the rest
        for name,value in expected.items():
            self.assertEqual(getattr(h,name),value)
        
    def _check(self,c,
               logger_level,
               handler_level,
               klass,
               normal_format,
               date_format,
               **expected):
        logger = c.eventlog()
        # logger
        self.assertEqual(logger.level,logger_level)
        self.assertEqual(len(logger.handlers),1)
        self._checkHandler(
            logger.handlers[0],
            klass,
            normal_format,
            date_format,
            level=handler_level,
            **expected)
        return logger
            
    def test_all_keys_mailinglogger(self):
        # load config
        c = self._loadConfig('''
  level     info
  <mailing-logger>
    dateformat  %H:%M:%S on %Y-%m-%d 
    level       warning
    from        logging@example.com
    to          receiver@example.com
    to          support@example.com
    smtp-server mail.example.com
    subject     [MyApp] %(line)s
    format      %(levelname)s - %(message)s
    send-empty-entries yes
    flood-level        13
  </mailing-logger>    
        ''')
        # check resulting logger
        self._check(c,
                    logger_level=logging.INFO,
                    handler_level=logging.WARNING,
                    klass=MailingLogger,
                    normal_format='%(levelname)s - %(message)s',
                    date_format='%H:%M:%S on %Y-%m-%d',
                    mailhost='mail.example.com',
                    mailport=None,
                    fromaddr='logging@example.com',
                    toaddrs=['receiver@example.com','support@example.com'],
                    subject='[MyApp] %(line)s',
                    send_empty_entries=True,
                    flood_level=13
                    )

    def test_minimal_config_mailinglogger(self):
        # load config
        c = self._loadConfig('''
  <mailing-logger>
    from        logging@example.com
    to          support@example.com
  </mailing-logger>    
        ''')
        # check resulting logger
        self._check(c,
                    logger_level=logging.INFO,
                    handler_level=0,
                    klass=MailingLogger,
                    normal_format='%(message)s',
                    date_format='%Y-%m-%dT%H:%M:%S',
                    mailhost='localhost',
                    mailport=None,
                    fromaddr='logging@example.com',
                    toaddrs=['support@example.com'],
                    subject='[%(hostname)s] %(levelname)s - %(line)s',
                    send_empty_entries=False,
                    flood_level=10
                    )

    def test_all_keys_summarisinglogger(self):
        # load config
        c = self._loadConfig('''
  level     info
  <summarising-logger>
    dateformat  %H:%M:%S on %Y-%m-%d 
    level       warning
    from        logging@example.com
    to          receiver@example.com
    to          support@example.com
    smtp-server mail.example.com
    subject     [MyApp] %(line)s
    format      %(levelname)s - %(message)s
    send-empty-entries no
    atexit             no
  </summarising-logger>    
        ''')
        # check resulting logger
        l = self._check(c,
                        logger_level=logging.INFO,
                        handler_level=logging.WARNING,
                        klass=SummarisingLogger,
                        normal_format='%(levelname)s - %(message)s',
                        date_format='%H:%M:%S on %Y-%m-%d',
                        )
        # check mailer stored as attribure of summariser
        self._checkHandler(l.handlers[0].mailer,
                           klass=MailingLogger,
                           # This format is hardcoded and means we send
                           # the whole of the summary
                           normal_format='%(message)s',
                           # We leave this as is, since it's never
                           # actuallly used.
                           date_format=None,
                           mailhost='mail.example.com',
                           mailport=None,
                           fromaddr='logging@example.com',
                           toaddrs=['receiver@example.com','support@example.com'],
                           subject='[MyApp] %(line)s',
                           send_empty_entries=False,
                           # flood level doesn't matter so is left as default.
                           # This mailer will only send one message.
                           flood_level=10
                           )
        # check atexit
        self.assertEqual(atexit._exithandlers,[])
        
    def test_minimal_config_summarisinglogger(self):
        # load config
        c = self._loadConfig('''
  <summarising-logger>
    from        logging@example.com
    to          receiver@example.com
  </summarising-logger>    
        ''')
        # check resulting logger
        l = self._check(c,
                        logger_level=logging.INFO,
                        handler_level=0,
                        klass=SummarisingLogger,
                        normal_format='%(asctime) - %(levelname)s - %(message)s',
                        date_format='%Y-%m-%dT%H:%M:%S',
                        )
        # check mailer stored as attribure of summariser
        self._checkHandler(l.handlers[0].mailer,
                           klass=MailingLogger,
                           normal_format='%(message)s',
                           date_format=None,
                           mailhost='localhost',
                           mailport=None,
                           fromaddr='logging@example.com',
                           toaddrs=['receiver@example.com'],
                           subject='Summary of Log Messages',
                           send_empty_entries=True,
                           flood_level=10
                           )
        # check atexit
        self.assertEqual(atexit._exithandlers,[(l.handlers[0].close,(),{})])

    def test_port_in_mailhost(self):
        # test for mailinglogger only as summarisinglogger uses the same code
        # load config
        c = self._loadConfig('''
  <mailing-logger>
    from        logging@example.com
    to          support@example.com
    smtp-server localhost:2525
  </mailing-logger>    
        ''')
        # check resulting logger
        self._check(c,
                    logger_level=logging.INFO,
                    handler_level=0,
                    klass=MailingLogger,
                    normal_format='%(message)s',
                    date_format='%Y-%m-%dT%H:%M:%S',
                    mailhost='localhost',
                    mailport=2525,
                    )
    
