# Copyright (c) 2001 New Information Paradigms Ltd
#
# This Software is realease under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: mailer.py,v 1.2.2.1 2003/03/05 22:59:54 chrisw Exp $

from smtplib import SMTP
from rfc822 import Message
from StringIO import StringIO
from string import join

template = """From: %(from)s
To: %(to)s
Subject: %(subject)s

%(body)s
"""

# mail a message
def send(address,subject='',body='',template=template,smtp_server='localhost'):
    message = template % {'from':address,
                          'to':address,
                          'subject':subject,
                          'body':body}
    mfile=StringIO(message)
    mo=Message(mfile)

    to_a=[]
    for header in (mo.getaddrlist('to'),
                   mo.getaddrlist('cc'),
                   mo.getaddrlist('bcc')):
        if not header: continue
        for name, addr in header:
            to_a.append(addr)

    from_a=mo.getaddr('from')[1]

    server = SMTP(smtp_server)
    server.sendmail(from_a,to_a,message)
