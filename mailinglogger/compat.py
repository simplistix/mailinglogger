# compatibility module for different python versions
import sys

if sys.version_info[:2] > (3, 0):

    PY2 = False
    PY3 = True

    Unicode = str

    from email.utils import formatdate, make_msgid
    from email.mime.text import MIMEText

    from html import escape

else:

    PY2 = True
    PY3 = False

    Unicode = unicode

    from email.Utils import formatdate, make_msgid
    from email.MIMEText import MIMEText

    from cgi import escape
