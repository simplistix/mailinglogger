# Copyright (c) 2004 Simplistix Ltd
# Copyright (c) 2001-2003 New Information Paradigms Ltd
#
# This Software is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.html
# See license.txt for more details.

from ZLogger import ZLogger
from MailingLogger import MailingLogger

loggers = list(ZLogger.loggers)
loggers.append(MailingLogger())
ZLogger.loggers = tuple(loggers)

