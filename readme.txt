Mailing Logger

  This is a simple plugin module that will mail certain log messages 
  to a specified address.

  Installation

    Just extract the .tar.gz which contains this file in the 
    Products directory of your Zope instance.

  Setup Instructions

    Mailing Logger gets its configuration from the following
    environment variables:

     MAILING_LOGGER_ADDRESS
       
       The address to send the mail to. This must be specified.

     MAILING_LOGGER_SMTPSERVER
  
       The SMTP server to use to send the mail. This must be 
       specified.

     MAILING_LOGGER_SUBJECT
 
       This is used to prefix the Subject of the messages sent.
       It defaults to 'Zope Server : '

     MAILING_LOGGER_SEVERITY

       This is the minimum severity of a log message that will 
       trigger a mail. See the Zope documentation for log severity.
       The default value is 100 which should suffice for most people.

    To set these variables on Unix, add the following lines to your
    start script:

      MAILING_LOGGER_ADDRESS=your.address@your.domain
      export MAILING_LOGGER_ADDRESS
      MAILING_LOGGER_SMTPSERVER=your.smtp.server
      export MAILING_LOGGER_SMTPSERVER
      MAILING_LOGGER_SUBJECT="My Message"
      export MAILING_LOGGER_SUBJECT
      MAILING_LOGGER_SEVERITY=0
      export MAILING_LOGGER_SEVERITY

    To set these variables on Windows, add the following lines to your
    start.bat script:

      set MAILING_LOGGER_ADDRESS=your.address@your.domain
      set MAILING_LOGGER_SMTPSERVER=your.smtp.server
      set MAILING_LOGGER_SUBJECT="My Message"
      set MAILING_LOGGER_SEVERITY=0         

  Licensing

     Copyright (c) 2001 New Information Paradigms Ltd

     This Software is released under the MIT License:
     http://www.opensource.org/licenses/mit-license.html
     See license.txt for more details.

  Changes

     1.0.1

       - Fixed python 1.5 incompatability.

     1.0.0

       - Initial Release
