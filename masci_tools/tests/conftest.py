# -*- coding: utf-8 -*-
"""
Configurations for masci_tools tests
"""
import pytest


@pytest.fixture
def load_inpxml():
    """Returns the etree and schema_dict generator"""

    def _load_inpxml(path):
        from lxml import etree
        from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict
        with open(path, 'r') as inpxmlfile:
            tree = etree.parse(inpxmlfile)
            version = str(tree.xpath('//@fleurInputVersion')[0])
            schema_dict = InputSchemaDict.fromVersion(version)
        return tree, schema_dict

    return _load_inpxml


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
