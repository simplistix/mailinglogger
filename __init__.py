# Copyright (c) 2001 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.
#
# $Id: __init__.py,v 1.2.2.1 2003/03/05 22:59:54 chrisw Exp $

from ZLogger import ZLogger
from MailingLogger import MailingLogger

loggers = list(ZLogger.loggers)
loggers.append(MailingLogger())
ZLogger.loggers = tuple(loggers)

