# compatibility module for different python versions
import sys

if sys.version_info[:2] > (3, 0):

    PY2 = False
    PY3 = True

    Unicode = str
    
    from email.utils import formatdate, make_msgid
    from email.mime.text import MIMEText
    
    # Bytes = bytes
    # basestring = str

    # class_type_name = 'class'
    # ClassType = type
    # exception_module = 'builtins'
    # new_class = type
    # self_name = '__self__'
    # from io import StringIO
    # xrange = range
    
else:
    
    PY2 = True
    PY3 = False
    
    Unicode = unicode
    
    from email.Utils import formatdate, make_msgid
    from email.MIMEText import MIMEText
    
    # Bytes = str
    # basestring = basestring
    
    # class_type_name = 'type'
    # from types import ClassType
    # exception_module = 'exceptions'
    # from new import classobj as new_class
    # self_name = 'im_self'
    # from cStringIO import StringIO
    # xrange = xrange

    
