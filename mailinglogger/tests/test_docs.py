import unittest
from doctest import REPORT_NDIFF, ELLIPSIS
from manuel import doctest, codeblock
from manuel.testing import TestSuite
from os.path import dirname, pardir, join
from mailinglogger.tests.shared import _setUp, _tearDown

docs_dir = join(dirname(__file__), pardir, pardir, 'docs')

options = REPORT_NDIFF | ELLIPSIS


def test_suite():
    m = doctest.Manuel(optionflags=options)
    m += codeblock.Manuel()
    return TestSuite(
        m,
        join(docs_dir, 'mailinglogger.txt'),
        join(docs_dir, 'summarisinglogger.txt'),
        join(docs_dir, 'subjectformatter.txt'),
        join(docs_dir, 'html.txt'),
        setUp=_setUp,
        tearDown=_tearDown,
    )

if __name__ == '__main__':
    unittest.main(default='test_suite')
