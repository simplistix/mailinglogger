Mailing Logger

  This provides more flexible and powerful email log handling for
  python's standard logging framework. 

  Two log handlers are provided:

  MailingLogger
  
    This mails out appropriate log entries as they are emitted.

    For more details, see mailinglogger.txt in the docs directory of
    the package.

  SummarisingLogger

    This mails out a summary of all appropriate log entries at the end
    of the running python script.
  
    For more details, see summarisinglogger.txt in the docs directory
    of the package.

  Both log handlers have the following features:
 
  - customisable and dynamic subject lines for emails sent
    For more details, see subjectformatter.txt in the docs directory
    of the package.

  - emails sent with a header as follows for easy filtering:

    X-Mailer: MailingLogger <version>

    In addition, other headers can be easilly configured.

  - flood protection to ensure the number of emails sent is not
    excessive

  - support for SMTP servers that require authentication

  - configurable log entry filtering

  - fully documented and tested

  The only caveat for using this package is that the smtp server you
  are using must be fast. Email is sent via SMTP and, if using a
  MailingLogger, at the time the message is logged. If your SMTP
  server is slow, your application's performance may suffer.

  Installation

    To install, either:

    - Extract the .tar.gz and do the usual:
    
      python setup.py install
    
    - use easy_install mailinglogger

    NB: Due to an bug in Python 2.5.0, SummarisingLogger requires a
        any version of Python with the logging framework present
        *other* than 2.5.0

    Additional support is provided if your application is based on one
    of the following frameworks:

    - ZConfig

      Please refer to zconfig.txt in the docs directory of the
      package. 

    - Zope 2

      Please refer to zope2.txt in the docs directory of the
      package. 
      
    - Zope 3

      Please refer to zope3.txt in the docs directory of the
      package. 
      
    Code that enables easier use of this package with other frameworks
    is welcome and will be included in a future release!

  Licensing

     Copyright (c) 2004-2010 Simplistix Ltd
     Copyright (c) 2001-2003 New Information Paradigms Ltd

     This Software is released under the MIT License:
     http://www.opensource.org/licenses/mit-license.html
     See license.txt for more details.

  Changes

    3.3.2 (27 Apr 2010)

       - Ignores are processed on the interpolated error message.

       - Check for empty error messages is done on the interpolated error
         message which in all cases is a string.

       Thanks to Christian Zagrodnick for these changes.

     3.3.1 (12 Dec 2008)
  
       - Fix bug that occurred when subject format used %(asctime)s

     3.3.0 (11 Dec 2008)
  
       - Tweak installation documentation

       - Add specific test runners for ZConfig, Zope 2 and Zope 3
         support
  
       - %(levelname)s in the subject of a SummarisingLogger summary
         is now the highest level message handled by that logger

       - Add support for specifying additional headers to the mails
         sent

     3.2.2 (4 Nov 2008)

       - Removed hard dependency on ZConfig

       - Moved to zc.buildout-based development model

       - Fix some doctests for newer versions of zope.testing

     3.2.1 (14 Aug 2007)

       - Fixed egg distribution.

     3.2.0 (31 Jul 2007)

       - Added support for log entry filtering.
         Thanks to Jens Vagelpohl for the work which was funded by
         Campux GmbH.

     3.1.0 (18 May 2007)

       - Added support for SMTP servers that require authentication.

     3.0.0 (9 May 2007)

       - Restructured to be used as a python package instead of a Zope
         Product.

       - Added comprehensive documentation and tests.

       - Added support for use ZConfig.

       - Added support for configuration in both Zope 3 and Zope 2.

       - Added support for disutils installation and for egg distribution.

     2.5.0 (5 Oct 2005)

       - Added compatability for Zope 2.8.x+ at the expense of now
         being incompatible with Zope 2.7.x. 

       - Fixed bug in flood protection that often meant no more mail
         was ever sent after midnight on the day when the flood
         protection was triggered.

       - Correct X-Mailer header which was set with a trailing newline
         which broke any further headers that were set.

       - A date header is now set on all emails sent.

     2.4.0 (13 May 2005)

       - Added sending of X-Mailer header with all emails.

       - Added %(hostname)s for use in subject format.

       - Fixed bug preventing use of summarising logger introduced in
         2.3.0.

     2.3.0 (25 Jan 2005)

       - Added the ability to limit the number of emails
         sent per hour.

     2.2.0 (13 Oct 2004)

       - Added ability to mute empty log entries

     2.1.0 (11 Oct 2004)

       - Added summarising logger functionality

     2.0.1 (1 Aug 2004)

       - Corrected documentation

       - Fixed bug that caused the subject to include tracebacks,
         which created a broken mail message.

     2.0.0 (28 Jul 2004)

       - Re-write for Zope 2.7

     1.0.1

       - Fixed python 1.5 incompatability.

     1.0.0

       - Initial Release
