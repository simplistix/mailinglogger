from doctest import REPORT_NDIFF, ELLIPSIS

from sybil import Sybil
from sybil.parsers.doctest import DocTestParser, FIX_BYTE_UNICODE_REPR
from sybil.parsers.codeblock import CodeBlockParser

from mailinglogger.tests.shared import _setUp, _tearDown

pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=REPORT_NDIFF|ELLIPSIS|FIX_BYTE_UNICODE_REPR),
        CodeBlockParser(),
    ],
    pattern='*.txt',
    setup=_setUp,
    teardown=_tearDown,
).pytest()
