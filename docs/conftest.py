from doctest import REPORT_NDIFF, ELLIPSIS

from sybil import Sybil
from sybil.parsers.doctest import DocTestParser
from sybil.parsers.codeblock import PythonCodeBlockParser

from mailinglogger.tests.shared import _setUp, _tearDown

pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=REPORT_NDIFF|ELLIPSIS),
        PythonCodeBlockParser(),
    ],
    pattern='*.txt',
    setup=_setUp,
    teardown=_tearDown,
).pytest()
