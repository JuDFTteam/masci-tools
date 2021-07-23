# -*- coding: utf-8 -*-
"""
Tests of the `masci_tools.vis.data` module
"""
import pytest
from itertools import product
import numpy as np
import pandas as pd

USE_CDS = True
try:
    from bokeh.models import ColumnDataSource
except ImportError:
    USE_CDS = False


def test_normalize_list_or_array():
    """
    Test of the normalize_list_or_array function
    """
    from masci_tools.vis.data import normalize_list_or_array

    #Single array
    x = np.linspace(-1, 1, 10)
    data = normalize_list_or_array(x, 'x', {})
    assert data == {'x': x}

    y = [np.linspace(-5, 1, 10), [1, 2, 3, 5]]
    data = normalize_list_or_array(y, 'y', data)
    assert data == [{'x_0': x, 'y_0': y[0]}, {'x_1': x, 'y_1': y[1]}]

    z = 5
    data = normalize_list_or_array(z, 'z', data)
    assert data == [{'x_0': x, 'y_0': y[0], 'z_0': z}, {'x_1': x, 'y_1': y[1], 'z_1': 5}]

    color = ['red', 'blue']
    data = normalize_list_or_array(color, 'color', data)
    assert data == [{
        'x_0': x,
        'y_0': y[0],
        'z_0': z,
        'color_0': 'red'
    }, {
        'x_1': x,
        'y_1': y[1],
        'z_1': z,
        'color_1': 'blue'
    }]

    color2 = [pd.Series([1, 2, 3]), pd.Series([4, 5, 6])]
    data = normalize_list_or_array(color2, 'color', data)
    assert data == [{
        'x_0': x,
        'y_0': y[0],
        'z_0': z,
        'color_0': color2[0]
    }, {
        'x_1': x,
        'y_1': y[1],
        'z_1': z,
        'color_1': color2[1]
    }]

    too_long_data = [np.linspace(0, 1, 2), np.linspace(3, 4, 5), np.linspace(6, 7, 8)]
    with pytest.raises(ValueError):
        data = normalize_list_or_array(too_long_data, 'dont_enter_this', data)


def test_normalize_list_or_array_flatten_np():
    """
    Test of the normalize_list_or_array function with flatten_np=True
    """
    from masci_tools.vis.data import normalize_list_or_array

    x = np.linspace(-1, 1, 10)
    y = np.linspace(-1, 1, 10)
    xv, yv = np.meshgrid(x, y)

    data = normalize_list_or_array(xv, 'x', {}, flatten_np=True)
    data = normalize_list_or_array(yv, 'y', data, flatten_np=True)

    assert data['x'].shape == (100,)
    assert data['y'].shape == (100,)


def test_normalize_list_or_array_forbid_split_up():
    """
    Test of the normalize_list_or_array function with forbid_split_up=True
    """
    from masci_tools.vis.data import normalize_list_or_array

    x = np.linspace(-1, 1, 10)
    data = normalize_list_or_array(x, 'x', {}, forbid_split_up=True)
    assert data == {'x': x}

    y = [np.linspace(-5, 1, 10), [1, 2, 3, 5]]
    data = normalize_list_or_array(y, 'y', data, forbid_split_up=True)
    assert data == {'x': x, 'y': y}


SINGLE_ENTRIES = [{
    'x': 'x',
    'y': 'y'
}, {
    'x_values': 'test',
    'y': ['y1', 'y2', 'y3']
}, {
    'color': ['test', 'x'],
    'type': ['y1', 'y2']
}]

SINGLE_COLUMNS = [[{
    'x': 'x',
    'y': 'y'
}], [{
    'x_values': 'test',
    'y': 'y1'
}, {
    'x_values': 'test',
    'y': 'y2'
}, {
    'x_values': 'test',
    'y': 'y3'
}], [{
    'color': 'test',
    'type': 'y1'
}, {
    'color': 'x',
    'type': 'y2'
}]]

x_data = np.linspace(-10, 10, 101)

dict_data = {
    'x': x_data,
    'test': x_data * 4,
    'y': x_data**2,
    'y1': 5 * x_data - 10,
    'y2': np.cos(x_data),
    'y3': np.exp(x_data)
}

SINGLE_SOURCES = [dict_data, pd.DataFrame(data=dict_data)]

if USE_CDS:
    SINGLE_SOURCES.append(ColumnDataSource(dict_data))


@pytest.mark.parametrize('inputs, data', product(zip(SINGLE_ENTRIES, SINGLE_COLUMNS), SINGLE_SOURCES))
def test_plot_data(inputs, data):
    """
    Basic test of PlotData
    """
    from masci_tools.vis.data import PlotData

    entries, expected_columns = inputs

    p = PlotData(data, **entries, use_column_source=True)

    assert len(p) == len(expected_columns)
    assert len(list(p.keys())) == len(expected_columns)
    assert len(list(p.values())) == len(expected_columns)
    assert len(list(p.items())) == len(expected_columns)

    for entry, col in zip(p.keys(), expected_columns):
        assert entry._fields == tuple(entries.keys())
        assert entry._asdict() == col

    for entry, col in zip(p.values(), expected_columns):
        assert entry._fields == tuple(entries.keys())
        assert entry._asdict() == {
            key: data[val] if getattr(data, 'data', None) is None else data.data[val] for key, val in col.items()
        }

    for (entry, source), col in zip(p.items(), expected_columns):
        assert entry._fields == tuple(entries.keys())
        assert entry._asdict() == col
        if isinstance(data, pd.DataFrame):
            assert source.equals(data)
        else:
            assert source == data

    entry = p.keys(first=True)
    assert entry._fields == tuple(entries.keys())
    assert entry._asdict() == expected_columns[0]

    entry = p.values(first=True)
    assert entry._fields == tuple(entries.keys())
    assert entry._asdict() == {
        key: data[val] if getattr(data, 'data', None) is None else data.data[val]
        for key, val in expected_columns[0].items()
    }

    entry, source = p.items(first=True)
    assert entry._fields == tuple(entries.keys())
    assert entry._asdict() == expected_columns[0]
    if isinstance(data, pd.DataFrame):
        assert source.equals(data)
    else:
        assert source == data


def test_plot_data_list_of_sources():
    pass


EXPECTED_MIN = [{
    'x': [-10.0],
    'y': [0.0]
}, {
    'x_values': [-40.0, -40.0, -40.0],
    'y': [-60.0, -0.9996930, 4.53999e-05]
}, {
    'color': [-40.0, -10.0],
    'type': [-60.0, -0.9996930]
}]


@pytest.mark.parametrize('inputs, data', product(zip(SINGLE_ENTRIES, EXPECTED_MIN), SINGLE_SOURCES))
def test_plot_data_min(inputs, data):
    """
    Test of PlotData min function
    """
    from masci_tools.vis.data import PlotData

    entries, expected_min = inputs

    p = PlotData(data, **entries, use_column_source=True)

    for key, expected in expected_min.items():

        assert p.min(key) == pytest.approx(min(expected))


@pytest.mark.parametrize('inputs, data', product(zip(SINGLE_ENTRIES, EXPECTED_MIN), SINGLE_SOURCES))
def test_plot_data_min_separate(inputs, data):
    """
    Test of PlotData min function
    """
    from masci_tools.vis.data import PlotData

    entries, expected_min = inputs

    p = PlotData(data, **entries, use_column_source=True)

    for key, expected in expected_min.items():

        assert p.min(key, separate=True) == pytest.approx(expected)


@pytest.mark.parametrize('data', SINGLE_SOURCES)
def test_plot_data_min_mask(data):
    """
    Test of PlotData min function
    """
    from masci_tools.vis.data import PlotData

    entries = SINGLE_ENTRIES[0]
    p = PlotData(data, **entries, use_column_source=True)
    assert p.min('x', mask=x_data > 5) == pytest.approx(5.2)

    entries = SINGLE_ENTRIES[1]
    p = PlotData(data, **entries, use_column_source=True)
    assert p.min('y', mask=[x_data > 5, x_data < 5, x_data >= 9],
                 separate=True) == pytest.approx([16.0, -0.9996930, 8103.0839275])


def test_plot_data_max():
    pass


def test_plot_data_apply():
    pass


def test_plot_data_copy_data():
    pass


def test_process_data_arguments():
    pass


def test_process_data_arguments_data_given():
    pass


def test_process_data_arguments_single_plot():
    pass
