Mailing Logger

  This adds a more flexible and powerful email log handler. It has
  both customisable log format and subject line.

  Installation

    Extract the .tar.gz which contains this file in the 
    Products directory of your Zope instance.
    
  Setup Instructions

    You will need to import Mailing Logger into your zope.conf and add
    a mailing-logger section in one or more of the logger sections.

    For example:

    %import Products.MailingLogger

    <eventlog>
      level info
      <mailing-logger>
        level   critical
        from    logging@example.com
        to      receiver@example.com
        to      support@example.com
        subject [Zope] ${line}
      </mailing-logger>    
    </eventlog>

    NB: For the %import to work, INSTANCE_HOME must be available in
    the environment!

    A full description of the possible keys and defaults for the
    email-notifier section are given below:

      dateformat

        The date format to use in log entries. This will be used
        wherever the %(asctime)s substitution is used.

	default: %Y-%m-%dT%H:%M:%S

      level

        The level at or above which an email log notification will be
        sent.

        This can either be a numeric level or one of the textual level
        identifiers.

        default: notset

      from

        The address from which email log notifications will originate.

        This must be set.

      to

        The address to which email log notifications will be sent.

        At least one 'to' line must be included, but multiple lines
        can be included if email log notifications should be sent to
        multiple addresses.

      smtp-server 

        The SMTP server that should be used to send email
        notifications.

	default: localhost

      subject 

        This is a format string specifying what information will be
        included in the subject line of the email notification.

	Information on what can be included in a format string can be
	found at:

	http://docs.python.org/lib/node293.html

	In addition to the substitutions listed there, %(line)s may
	also be used. This is the first line of %(message)s

        default: [Zope] %(line)s

      format 

        This is a format string specifying what information will be
        included in the body of the email notification.

	Information on what can be included in a format string can be
	found at:

	http://docs.python.org/lib/node293.html

        default: %(message)s

  Licensing

     Copyright (c) 2004 Simplistix Ltd
     Copyright (c) 2001-2003 New Information Paradigms Ltd

     This Software is released under the MIT License:
     http://www.opensource.org/licenses/mit-license.html
     See license.txt for more details.

  Changes

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
