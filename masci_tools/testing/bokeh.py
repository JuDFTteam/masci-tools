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
def check_bokeh_plot(data_regression, clean_bokeh_json_v2, clean_bokeh_json_v3, pytestconfig, bokeh_basename,
                     previous_bokeh_results, datadir):

    try:
        import bokeh
    except ImportError:
        pytest.skip('Bokeh regression tests are skipped only executed if bokeh is installed')

    def _regression_bokeh_plot(bokeh_fig):

        basename = bokeh_basename()  #This will skip the test if bokeh is not installed

        if pytestconfig.getoption('--show-bokeh-plots'):
            from bokeh.io import show
            show(bokeh_fig)
        else:
            if not (datadir / basename).parent.is_dir():
                filename = basename.name
                _, _, current_version = basename.parent.name.partition('-')
                current_version = tuple(int(x) for x in current_version.split('.'))
                prev_version = previous_bokeh_results(current_version)

                if not pytestconfig.getoption('--add-bokeh-version'):
                    if prev_version is not None:
                        basename = Path(f'bokeh-{prev_version}') / filename
                        warnings.warn(f'Results for bokeh version {current_version} not available.\n'
                                      f'Using the last available version {prev_version}\n'
                                      '    Use the option --add-bokeh-version to add results for this version')

            from packaging.version import Version
            if Version(bokeh.__version__).major >= 3:
                from bokeh.core.serialization import Serializer
                result = Serializer().serialize(bokeh_fig)
                result = clean_bokeh_json_v3(result.content)
            else:
                from bokeh.io import curdoc
                curdoc().clear()
                curdoc().add_root(bokeh_fig)
                result = clean_bokeh_json_v2(curdoc().to_json())
            result.pop('version', None)
            data_regression.check(result, basename=os.fspath(basename))

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


@pytest.fixture(scope='function', name='clean_bokeh_json_v2')
def fixture_clean_bokeh_json_v2():
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
        from bokeh.util.serialization import decode_base64_dict, encode_base64_dict  #pylint: disable=no-name-in-module
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

                index = key_order.index(key)
                if isinstance(val, dict):
                    normed = get_normalized_order(val, key_order, normed=normed)
                    normed[index][1].extend(sorted(val.keys()))
                else:
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

        data = {key: val for key, val in data.items() if key not in ('id', 'root_ids')}

        for key, val in data.items():
            if isinstance(val, dict):
                data[key] = _clean_bokeh_json(val, np_precision=np_precision, data_entry=key == 'data')
            elif isinstance(val, list):

                for index, entry in enumerate(val):
                    if isinstance(entry, dict):
                        val[index] = _clean_bokeh_json(entry)
                    elif isinstance(entry, list):
                        val[index] = [_clean_bokeh_json(x) if isinstance(x, dict) else x for x in entry]

                #Filter out empty dictionaries
                while {} in val:
                    val.remove({})

                if all(isinstance(x, dict) for x in val):
                    data[key] = normalize_list_of_dicts(val)
                elif all(isinstance(x, int) for x in val) and data_entry:
                    data[key] = encode_base64_dict(np.array(val))
                elif all(isinstance(x, float) for x in val) and data_entry:
                    data[key] = encode_base64_dict(np.around(np.array(val), decimals=np_precision))
                else:
                    data[key] = val
            elif isinstance(val, float):
                data[key] = round(val, np_precision)
        data = {key: val for key, val in data.items() if val not in (None, [], {})}

        return data

    return _clean_bokeh_json


@pytest.fixture(scope='function', name='clean_bokeh_json_v3')
def fixture_clean_bokeh_json_v3():
    """
    Make the dict form the produced json data
    suitable for data_regression

    - remove any reference to ids
    - sort lists after types and given attributes for reproducible order

    :param data: dict with the json data produced for the bokeh figure
    """

    def _clean_bokeh_json(data, np_precision=5):
        """
        Make the dict form the produced json data
        suitable for data_regression

        - remove any reference to ids
        - sort lists after types and given attributes for reproducible order

        :param data: dict with the json data produced for the bokeh figure
        """
        from bokeh.core.serialization import Buffer, Deserializer, Serializer
        import numpy as np
        import numbers

        def _serialize_base(val, decimals=5):

            if isinstance(val, (list, tuple)):
                return [_serialize_base(x, decimals=decimals) for x in val]
            if isinstance(val, dict):
                return _clean_bokeh_json(val, np_precision=decimals)
            if isinstance(val, Buffer):
                return val.to_base64()
            if isinstance(val, str):
                return str(val)
            if isinstance(val, numbers.Real) and not isinstance(val, numbers.Integral):
                return round(float(val), decimals)
            return val

        if data.get('type') == 'ndarray':
            array = Deserializer().deserialize(data)
            if array.dtype.char in np.typecodes['AllFloat']:
                array = np.around(array, decimals=np_precision)
                data = Serializer().serialize(array).content
        if data.get('type') == 'typed_array' and data.get('dtype') in ('float32', 'float64'):
            array = Deserializer().deserialize(data)
            array = np.around(array, decimals=np_precision)
            data = Serializer().serialize(array).content

        data = {key: val for key, val in data.items() if key not in ('id', 'root_ids')}

        for key, val in data.items():
            if isinstance(val, dict):
                data[key] = _clean_bokeh_json(val, np_precision=np_precision)
            elif isinstance(val, (list, tuple)):

                for index, entry in enumerate(val):
                    if isinstance(entry, dict):
                        val[index] = _clean_bokeh_json(entry)
                    elif isinstance(entry, (list, tuple)):
                        val[index] = [
                            _clean_bokeh_json(x) if isinstance(x, dict) else _serialize_base(x, decimals=np_precision)
                            for x in entry
                        ]
                    else:
                        val[index] = _serialize_base(entry, decimals=np_precision)

                #Filter out empty dictionaries
                while {} in val:
                    val.remove({})

                data[key] = val
            else:
                data[key] = _serialize_base(val, decimals=np_precision)
        data = {key: val for key, val in data.items() if val not in (None, [], {})}

        return data

    return _clean_bokeh_json
