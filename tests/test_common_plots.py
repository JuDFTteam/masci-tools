# -*- coding: utf-8 -*-
"""
Tests of the vis.common module Only the general routines are tested here (e.g. dos and bands routines are tested via the higher level fleur tests)
"""
import pytest
import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib.pyplot import gcf
import matplotlib.pyplot as plt


def test_get_plotter():
    """
    Test of the get_plotter method
    """
    from masci_tools.vis.common import get_plotter, set_default_backend
    import masci_tools.vis.plot_methods as mpl
    import masci_tools.vis.bokeh_plots as bok

    assert get_plotter('mpl') is mpl.plot_params
    assert get_plotter('matplotlib') is mpl.plot_params
    assert get_plotter('bokeh') is bok.plot_params

    assert get_plotter() is mpl.plot_params
    set_default_backend('bokeh')
    assert get_plotter() is bok.plot_params
    set_default_backend('mpl')
    assert get_plotter() is mpl.plot_params


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='scatter_mpl.png')
def test_scatter_mpl():
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import scatter

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    scatter(x, y, legend=True, color='red', markersize=6, backend='mpl', plot_label='test', show=False)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='scatter_mpl.png')
def test_scatter_defaults():
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import scatter

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    scatter(x, y, legend=True, color='red', markersize=6, plot_label='test', show=False)

    return gcf()


def test_scatter_bokeh(check_bokeh_plot):
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import scatter

    x = np.linspace(-10, 10, 100)
    y = x**2

    p = scatter(x, y, color='red', marker_size=6, backend='bokeh', show=False)

    check_bokeh_plot(p)


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='line_mpl.png')
def test_line_mpl():
    """
    Test of the scatter function with mpl backend
    """
    from masci_tools.vis.common import line

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    line(x, y, legend=True, color='red', markersize=6, backend='mpl', plot_label='test', show=False)

    return gcf()


@pytest.mark.mpl_image_compare(baseline_dir='test_common_plots/', filename='line_mpl.png')
def test_line_defaults():
    """
    Test of the line function with mpl backend
    """
    from masci_tools.vis.common import line

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    line(x, y, legend=True, color='red', markersize=6, plot_label='test', show=False)

    return gcf()


def test_line_bokeh(check_bokeh_plot):
    """
    Test of the line function with mpl backend
    """
    from masci_tools.vis.common import line

    x = np.linspace(-10, 10, 100)
    y = x**2

    p = line(x, y, color='red', marker_size=6, backend='bokeh', show=False)

    check_bokeh_plot(p)
