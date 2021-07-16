# -*- coding: utf-8 -*-
"""
Tests of the `masci_tools.vis.data` module
"""
import pytest


def test_normalize_list_or_array():
    """
    Test of the normalize_list_or_array function
    """
    from masci_tools.vis.data import normalize_list_or_array
    import numpy as np
    import pandas as pd

    #Single array
    x = np.linspace(-1, 1, 10)
    data = normalize_list_or_array(x, 'x', {})
    assert data == {'x': x}

    y = [np.linspace(-5, 1, 10), [1, 2, 3, 5]]
    data = normalize_list_or_array(y, 'y', data)
    assert data == [{'x': x, 'y': y[0]}, {'x': x, 'y': y[1]}]

    z = 5
    data = normalize_list_or_array(z, 'z', data)
    assert data == [{'x': x, 'y': y[0], 'z': z}, {'x': x, 'y': y[1], 'z': 5}]

    color = ['red', 'blue']
    data = normalize_list_or_array(color, 'color', data)
    assert data == [{'x': x, 'y': y[0], 'z': z, 'color': 'red'}, {'x': x, 'y': y[1], 'z': z, 'color': 'blue'}]

    color2 = [pd.Series([1, 2, 3]), pd.Series([4, 5, 6])]
    data = normalize_list_or_array(color2, 'color', data)
    assert data == [{'x': x, 'y': y[0], 'z': z, 'color': color2[0]}, {'x': x, 'y': y[1], 'z': z, 'color': color2[1]}]

    too_long_data = [np.linspace(0, 1, 2), np.linspace(3, 4, 5), np.linspace(6, 7, 8)]
    with pytest.raises(ValueError):
        data = normalize_list_or_array(too_long_data, 'dont_enter_this', data)


def test_normalize_list_or_array_flatten_np():
    """
    Test of the normalize_list_or_array function with flatten_np=True
    """
    from masci_tools.vis.data import normalize_list_or_array
    import numpy as np

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
    import numpy as np

    x = np.linspace(-1, 1, 10)
    data = normalize_list_or_array(x, 'x', {}, forbid_split_up=True)
    assert data == {'x': x}

    y = [np.linspace(-5, 1, 10), [1, 2, 3, 5]]
    data = normalize_list_or_array(y, 'y', data, forbid_split_up=True)
    assert data == {'x': x, 'y': y}


def test_plot_data():
    pass


def test_plot_data_list_of_sources():
    pass


def test_plot_data_min():
    pass


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
