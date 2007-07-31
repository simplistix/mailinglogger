Mailing Logger

  This provides more flexible and powerful email log handling for
  python's standard logging framework. 

  Two log handlers are provided:

  MailingLogger
  
    This mails out appropriate log entries as they are emitted.

    For more details see mailinglogger.txt in the docs directory of
    the distribution.

  SummarisingLogger

    This mails out a summary of all appropriate log entries at the end
    of the running python script.
  
    For more details see summarisinglogger.txt in the docs directory
    of the distribution.

  Both log handlers have the following features:
 
  - customisable and dynamic subject lines for emails sent

  - emails sent with a header as follows for easy filtering:

    X-Mailer: MailingLogger <version>

  - flood protection to ensure the number of emails sent is not
    excessive

  - configurable log entry filtering

  - fully documented and tested

  The only caveat for using this package is that the smtp server you
  are using must be fast. Email is sent via SMTP and, if using a
  MailingLogger, at the time the message is logged. If your SMTP
  server is slow, your application's performance may suffer.

  Installation

    Extract the .tar.gz which contains this file anywhere on your
    python path.
    
    Additional support is provided if your application is based on one
    of the following frameworks:

    - ZConfig

      Please refer to zconfig.txt in the docs directory of the
      distribution. 

    - Zope 2

      Please refer to zope2.txt in the docs directory of the
      distribution. 
      
    - Zope 3

      Please refer to zope3.txt in the docs directory of the
      distribution. 
      
    Code that enables easier use of this package with other frameworks
    is welcome and will be included in a future release!

  Licensing

     Copyright (c) 2004-2007 Simplistix Ltd
     Copyright (c) 2001-2003 New Information Paradigms Ltd

     This Software is released under the MIT License:
     http://www.opensource.org/licenses/mit-license.html
     See license.txt for more details.

  Changes

     3.2.0

       - Added support for log entry filtering, funded by Campux GmbH

     3.1.0

       - Added support for SMTP servers that require authentication.

     3.0.0

       - Restructured to be used as a python package instead of a Zope
         Product.

       - Added comprehensive documentation and tests.

       - Added support for use ZConfig.

       - Added support for configuration in both Zope 3 and Zope 2.

       - Added support for disutils installation and for egg distribution.


     2.5.0

       - Added compatability for Zope 2.8.x+ at the expense of now
         being incompatible with Zope 2.7.x. 

       - Fixed bug in flood protection that often meant no more mail
         was ever sent after midnight on the day when the flood
         protection was triggered.

       - Correct X-Mailer header which was set with a trailing newline
         which broke any further headers that were set.

       - A date header is now set on all emails sent.

     2.4.0

       - Added sending of X-Mailer header with all emails.

       - Added %(hostname)s for use in subject format.

       - Fixed bug preventing use of summarising logger introduced in
         2.3.0.

     2.3.0

       - Added the ability to limit the number of emails
         sent per hour.

     2.2.0

       - Added ability to mute empty log entries

     2.1.0

       - Added summarising logger functionality

     2.0.1

       - Corrected documentation

       - Fixed bug that caused the subject to include tracebacks,
         which created a broken mail message.

     2.0.0

       - Re-write for Zope 2.7

     1.0.1

       - Fixed python 1.5 incompatability.

     1.0.0

       - Initial Release
