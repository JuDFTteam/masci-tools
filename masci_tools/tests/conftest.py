# -*- coding: utf-8 -*-
"""
Configurations for masci_tools tests
"""
import pytest


@pytest.fixture
def load_inpxml():
    """Returns the etree and schema_dict generator"""

    def _load_inpxml(path):
        import masci_tools.io.io_fleurxml as fleur_io
        with open(path, 'r') as inpxmlfile:
            return fleur_io.load_inpxml(inpxmlfile)

    return _load_inpxml


@pytest.fixture
def load_outxml():
    """Returns the etree and schema_dict generator"""

    def _load_outxml(path):
        import masci_tools.io.io_fleurxml as fleur_io
        with open(path, 'r') as outxmlfile:
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


@pytest.fixture(scope='function', name='clean_bokeh_json')
def fixture_clean_bokeh_json():
    """
    Make the dict form the produced json data
    suitable for data_regression

    - remove any reference to ids
    - sort lists after types and given attributes for reproducible order

    :param data: dict with the json data produced for the bokeh figure
    """

    def _clean_bokeh_json(data):
        """
        Make the dict form the produced json data
        suitable for data_regression

        - remove any reference to ids
        - sort lists after types and given attributes for reproducible order

        :param data: dict with the json data produced for the bokeh figure
        """

        for key, val in list(data.items()):
            if key in ('id', 'root_ids'):
                del data[key]
            elif isinstance(val, dict):
                data[key] = _clean_bokeh_json(val)
            elif isinstance(val, list):
                for index, entry in enumerate(val):
                    if isinstance(entry, dict):
                        val[index] = _clean_bokeh_json(entry)
                if all(isinstance(x, dict) for x in val):
                    data[key] = sorted(val, key=lambda x: (x['type'], *x.get('attributes', {}).items()))
                else:
                    data[key] = val

        return data

    return _clean_bokeh_json


@pytest.fixture(scope='function')
def check_bokeh_plot(data_regression, clean_bokeh_json):
    current_bokeh_version = '1.4.0'  #For now we only test bokeh plots if the right version is available

    try:
        import bokeh
        test_bokeh = current_bokeh_version == bokeh.__version__
    except ImportError:
        test_bokeh = False

    def _regression_bokeh_plot(bokeh_fig):
        if not test_bokeh:
            pytest.skip(
                f'Bokeh regression tests are skipped (Only executed if bokeh {current_bokeh_version} is installed')
        from bokeh.io import curdoc

        curdoc().clear()
        curdoc().add_root(bokeh_fig)
        data_regression.check(clean_bokeh_json(curdoc().to_json()))

    return _regression_bokeh_plot
