# -*- coding: utf-8 -*-
"""
Configurations for masci_tools tests
"""
import pytest
from pprint import pprint
from pathlib import Path
import os

pytest_plugins = ('masci_tools.testing.bokeh',)

CONFTEST_LOCATION = Path(__file__).parent.resolve()


@pytest.fixture
def test_file(relative_path):
    """
    Return path to file in the tests/files folder
    Returns filesystem path
    """
    return os.fspath(CONFTEST_LOCATION / Path(relative_path))


@pytest.mark.usefixtures('test_file')
@pytest.fixture
def load_inpxml():
    """Returns the etree and schema_dict generator"""

    def _load_inpxml(path, absolute=True):
        import masci_tools.io.io_fleurxml as fleur_io
        if not absolute:
            path = test_file(path)
        with open(path, 'r', encoding='utf-8') as inpxmlfile:
            return fleur_io.load_inpxml(inpxmlfile)

    return _load_inpxml


@pytest.mark.usefixtures('test_file')
@pytest.fixture
def load_outxml():
    """Returns the etree and schema_dict generator"""

    def _load_outxml(path, absolute=True):
        import masci_tools.io.io_fleurxml as fleur_io
        if not absolute:
            path = test_file(path)
        with open(path, 'r', encoding='utf-8') as outxmlfile:
            return fleur_io.load_outxml(outxmlfile)

    return _load_outxml


@pytest.fixture
def clean_parser_log():
    """Clean parser logs for consistent testing"""

    def _clean_parser_log(info_dict):

        clean_dict = {}
        clean_dict['parser_info'] = info_dict.pop('parser_info', [])
        clean_dict['parser_warnings'] = info_dict.pop('parser_warnings', [])
        clean_dict['parser_errors'] = info_dict.pop('parser_errors', [])

        return clean_dict

    return _clean_parser_log


@pytest.fixture(scope='session', autouse=True)
def disable_parser_tracebacks():
    """Disable logging of tracebacks in parser logs Thanks to
       https://stackoverflow.com/questions/54605699/python-logging-disable-stack-trace"""
    import logging

    class TracebackInfoFilter(logging.Filter):
        """Clear or restore the exception on log records"""

        def filter(self, record):
            record._exc_info_hidden, record.exc_info = record.exc_info, None
            # clear the exception traceback text cache, if created.
            record.exc_text = None
            return True

    inp_logger = logging.getLogger('masci_tools.io.parsers.fleur.fleur_inpxml_parser')
    out_logger = logging.getLogger('masci_tools.io.parsers.fleur.fleur_outxml_parser')

    traceback_filter = TracebackInfoFilter()
    inp_logger.addFilter(traceback_filter)
    out_logger.addFilter(traceback_filter)

    yield  #Now all tests run

    inp_logger.removeFilter(traceback_filter)
    out_logger.removeFilter(traceback_filter)
