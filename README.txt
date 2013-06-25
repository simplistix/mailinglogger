=============
MailingLogger
=============

For full documentation please see:
http://www.simplistix.co.uk/software/python/mailinglogger

If working offline, please consult the documentation source in the
`docs` directory.

Example usage
=============

Put in your buildout.cfg this configuration

    event-log-custom = 
      %import mailinglogger
      <mailing-logger>
        to EMAIL
        to EMAIL1
        from EMAIL_FROM
        level ERROR
        subject [My domain error] [%(hostname)s] %(line)s
        smtp-server SMTP_SERVER
        username USERNAME
        password PASSWORD
      </mailing-logger>


If you get the following exception:

    SMTPException: SMTP AUTH extension not supported by server.

you should add the optional `secure` configuration to the mailing-logger:

    secure [keyfile[, certfile]
 

Licensing
=========

Copyright (c) 2004-2011 Simplistix Ltd

Copyright (c) 2001-2003 New Information Paradigms Ltd

See docs/license.txt for details.
