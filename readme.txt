Mailing Logger

  This adds a more flexible and powerful email log handler. It has
  both customisable log format and subject line.

  All emails sent will have a header set as follows:

  X-Mailer: MailingLogger <version>

  This is to allow easier filtering of these emails.

  Installation

    Extract the .tar.gz which contains this file in the 
    Products directory of your Zope instance.
    
  Setup Instructions

    You will need to import Mailing Logger into your zope.conf and add
    either a mailing-logger or summarising-logger section in one or 
    more of the zope.conf logger sections.

    For example:

    %import Products.MailingLogger

    <eventlog>
      level info
      <mailing-logger>
        level   critical
        from    logging@example.com
        to      receiver@example.com
        to      support@example.com
        subject [Zope] %(line)s
      </mailing-logger>    
    </eventlog>

    NB: For the %import to work, INSTANCE_HOME must be available in
    the environment!

    A full description of the possible keys and defaults for the
    mailing-logger and summarising-logger sections are given below:

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

	In addition to the substitutions listed there, the following
	are also available:

        %(line)s - the first line of %(message)s
        %(hostname)s - the hostname of the current machine

        default: [%(hostname)s] %(line)s

      format 

        This is a format string specifying what information will be
        included in each message that is logged.

        With mailing-logger, one log message will be included in each
        email. With summarising-logger, all log messages will be 
        included in one email.

	Information on what can be included in a format string can be
	found at:

	http://docs.python.org/lib/node293.html

        default: %(message)s

      send-empty-entries

        This is a boolean value which specifies whether empty log
        entries will be mailed or not.

        Empty log entries are likely to occur when, for example, 
        a summarising logger is used in a cron job that runs
        very frequently but only generates log entries 
        infrequently.

        default: no

      flood-level

        This is an integer value specifying the maximum number of
        emails that can be sent in an hour that will not be considered
        a "flood".

        When a "flood" is detected, one email is sent at the CRITICAL
        level indicating that a flood has been detected, and no more
        emails will be sent in the same hour.

        So, this option, in effect, specifies the maximum number of
        emails that will be sent in any particular hour of the day.

        default: 10

  mailing-logger or summarising-logger?

     mailing-logger will send one email for each message logged.

     summarising-logger will send one email containing all messages
     logged from the time the logger is initialised to the time it
     is closed.

     summarising-logger should not be used for long running processes.
     It is designed for generating reports from single-run scripts or
     cron jobs.

  Licensing

     Copyright (c) 2004-2005 Simplistix Ltd
     Copyright (c) 2001-2003 New Information Paradigms Ltd

     This Software is released under the MIT License:
     http://www.opensource.org/licenses/mit-license.html
     See license.txt for more details.

  Changes

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
