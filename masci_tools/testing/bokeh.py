"""
Fixtures for testing bokeh plots.

The actual rendering is not tested. Instead the produced json is put through
the pytest-regressions plugin to be notified when it changes
"""
import pytest
import re
from pathlib import Path
import os
import warnings

pytest_plugins = ('pytest_regressions',)

__all__ = ('pytest_addoption', 'check_bokeh_plot')


def pytest_addoption(parser):
    parser.addoption('--show-bokeh-plots', action='store_true', help='Show the produced bokeh plots')
    parser.addoption('--add-bokeh-version',
                     action='store_true',
                     help='Store the results for a new installed bokeh version')


@pytest.fixture(scope='function')
def check_bokeh_plot(data_regression, clean_bokeh_json, pytestconfig, bokeh_basename, previous_bokeh_results, datadir):

    def _regression_bokeh_plot(bokeh_fig):

        basename = bokeh_basename()  #This will skip the test if bokeh is not installed

        if pytestconfig.getoption('--show-bokeh-plots'):
            from bokeh.io import show
            show(bokeh_fig)
        else:
            if not (datadir / basename).parent.is_dir():
                filename = basename.name
                prev_version = previous_bokeh_results(basename.parent)

                if not pytestconfig.getoption('--add-bokeh-version'):
                    if prev_version is not None:
                        basename = Path(prev_version) / filename
                        warnings.warn(f'Results for bokeh version {basename.parent} not available.'
                                      f'Using the last available version {prev_version}'
                                      'Use the option --add-bokeh-version to add results for this version')

            from bokeh.io import curdoc

            curdoc().clear()
            curdoc().add_root(bokeh_fig)
            data_regression.check(clean_bokeh_json(curdoc().to_json()), basename=os.fspath(basename))

    return _regression_bokeh_plot


@pytest.fixture(scope='function', name='bokeh_basename')
def fixture_bokeh_basename(request):

    def _get_bokeh_basename():
        try:
            import bokeh
            current_bokeh_version = bokeh.__version__
        except ImportError:
            pytest.skip('Bokeh regression tests are skipped only executed if bokeh is installed')

        #Copied from pytest-regressions
        basename = re.sub(r'[\W]', '_', request.node.name)
        return Path(f'bokeh-{current_bokeh_version}') / basename

    return _get_bokeh_basename


@pytest.fixture(scope='function', name='previous_bokeh_results')
def fixture_previous_bokeh_results(datadir):

    def _get_previous_test_results(current_version):

        latest_version = (0, 0, 0)

        for f in os.scandir(datadir):
            if f.is_dir() and f.name.startswith('bokeh-'):
                _, _, version = f.name.partition('-')
                version = tuple(int(x) for x in version.split('.'))
                if latest_version < version <= current_version:
                    latest_version = version
        if latest_version > (0, 0, 0):
            return '.'.join(map(str, latest_version))
        return None

    return _get_previous_test_results


@pytest.fixture(scope='function', name='clean_bokeh_json')
def fixture_clean_bokeh_json():
    """
    Make the dict form the produced json data
    suitable for data_regression

    - remove any reference to ids
    - sort lists after types and given attributes for reproducible order

    :param data: dict with the json data produced for the bokeh figure
    """

    def _clean_bokeh_json(data, np_precision=5, data_entry=False):
        """
        Make the dict form the produced json data
        suitable for data_regression

        - remove any reference to ids
        - sort lists after types and given attributes for reproducible order

        :param data: dict with the json data produced for the bokeh figure
        """
        from bokeh.util.serialization import decode_base64_dict, encode_base64_dict
        import numpy as np

        def get_contained_keys(dict_val):

            keys = set(dict_val.keys())
            for key, val in dict_val.items():
                if isinstance(val, dict):
                    keys = keys.union(get_contained_keys(val))

            return keys

        def get_normalized_order(dict_val, key_order, normed=None):

            if normed is None:
                normed = [(key, []) for key in key_order]
            for key, val in dict_val.items():

                if isinstance(val, dict):
                    normed = get_normalized_order(val, key_order, normed=normed)
                else:
                    index = key_order.index(key)
                    if not isinstance(val, list):
                        val = [val]

                    for v in val:
                        if isinstance(v, dict):
                            normed[index][1].extend(sorted(v.items()))
                        elif isinstance(v, (float, int)):
                            normed[index][1].append(str(v))
                        else:
                            normed[index][1].append(v)

            return normed

        def normalize_list_of_dicts(list_of_dicts):

            list_of_dicts = [_clean_bokeh_json(entry) for entry in list_of_dicts]
            contained_keys = set()
            for data in list_of_dicts:
                contained_keys = contained_keys.union(get_contained_keys(data))
            contained_keys.discard('type')
            key_order = ['type'] + sorted(contained_keys)

            return sorted(list_of_dicts, key=lambda x: tuple(get_normalized_order(x, key_order)))

        if '__ndarray__' in data:
            array = decode_base64_dict(data)
            array = np.around(array, decimals=np_precision)
            data = encode_base64_dict(array)

        for key, val in list(data.items()):
            if key in ('id', 'root_ids'):
                data.pop(key)
            elif isinstance(val, dict):
                data[key] = _clean_bokeh_json(val, np_precision=np_precision, data_entry=key == 'data')
            elif isinstance(val, list):

                for index, entry in enumerate(val):
                    if isinstance(entry, dict):
                        val[index] = _clean_bokeh_json(entry)
                    elif isinstance(entry, list):
                        val[index] = [_clean_bokeh_json(x) if isinstance(x, dict) else x for x in entry]

                if all(isinstance(x, dict) for x in val):
                    data[key] = normalize_list_of_dicts(val)
                elif all(isinstance(x, int) for x in val) and data_entry:
                    data[key] = encode_base64_dict(np.array(val))
                else:
                    data[key] = val

        return data

    return _clean_bokeh_json
