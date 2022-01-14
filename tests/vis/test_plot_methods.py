#!/usr/bin/env python
"""
Tests of the matplotib plotting functions
"""

import pytest

# prevent issue with not having a display on travis-ci
# this needs to go *before* pyplot imports
import matplotlib

matplotlib.use('Agg')
from matplotlib.pyplot import gcf
import matplotlib.pyplot as plt


def test_plot_methods_imports():
    """
    Test that all expected functions are still there
    """
    from masci_tools.vis.plot_methods import set_mpl_plot_defaults
    from masci_tools.vis.plot_methods import reset_mpl_plot_defaults
    from masci_tools.vis.plot_methods import show_mpl_plot_defaults
    from masci_tools.vis.plot_methods import save_mpl_defaults
    from masci_tools.vis.plot_methods import load_mpl_defaults
    from masci_tools.vis.plot_methods import single_scatterplot
    from masci_tools.vis.plot_methods import multiple_scatterplots
    from masci_tools.vis.plot_methods import multi_scatter_plot
    from masci_tools.vis.plot_methods import colormesh_plot
    from masci_tools.vis.plot_methods import waterfall_plot
    from masci_tools.vis.plot_methods import surface_plot
    from masci_tools.vis.plot_methods import multiplot_moved
    from masci_tools.vis.plot_methods import multiaxis_scatterplot
    from masci_tools.vis.plot_methods import histogram
    from masci_tools.vis.plot_methods import barchart
    from masci_tools.vis.plot_methods import plot_convex_hull2d
    from masci_tools.vis.plot_methods import plot_residuen
    from masci_tools.vis.plot_methods import plot_convergence_results
    from masci_tools.vis.plot_methods import plot_convergence_results_m
    from masci_tools.vis.plot_methods import plot_lattice_constant
    from masci_tools.vis.plot_methods import plot_relaxation_results
    from masci_tools.vis.plot_methods import plot_dos
    from masci_tools.vis.plot_methods import plot_spinpol_dos
    from masci_tools.vis.plot_methods import plot_bands
    from masci_tools.vis.plot_methods import plot_spinpol_bands
    from masci_tools.vis.plot_methods import plot_one_element_corelv
    from masci_tools.vis.plot_methods import construct_corelevel_spectrum
    from masci_tools.vis.plot_methods import plot_corelevel_spectra
    #from masci_tools.vis.plot_methods import plot_fleur_bands


TEST_CHANGES = [{'markersize': 50}, {'show': False}, {'tick_paramsx': {'labelsize': 100}}]

EXPECTED_RESULT = [{
    'markersize': 50
}, {
    'show': False
}, {
    'tick_paramsx': {
        'size': 4.0,
        'width': 1.0,
        'labelsize': 100,
        'length': 5,
        'labelrotation': 0
    }
}]


@pytest.mark.parametrize('change_dict, result', zip(TEST_CHANGES, EXPECTED_RESULT))
def test_set_defaults(change_dict, result):
    """
    Test the setting of default values
    """
    from masci_tools.vis.plot_methods import plot_params
    from masci_tools.vis.plot_methods import set_mpl_plot_defaults
    from masci_tools.vis.plot_methods import reset_mpl_plot_defaults

    value_before = {}
    for key in change_dict:
        value_before[key] = plot_params[key]

    set_mpl_plot_defaults(**change_dict)

    for key, val in result.items():
        assert plot_params[key] == val

    reset_mpl_plot_defaults()

    for key, val in value_before.items():
        assert plot_params[key] == val


def test_mpl_save_defaults(file_regression):
    """
    Test saving of custom parameters
    """
    import tempfile
    from masci_tools.vis.plot_methods import set_mpl_plot_defaults
    from masci_tools.vis.plot_methods import save_mpl_defaults
    from masci_tools.vis.plot_methods import reset_mpl_plot_defaults

    set_mpl_plot_defaults(markersize=50,
                          show=False,
                          tick_paramsx={
                              'size': 4.0,
                              'width': 1.0,
                              'labelsize': 100,
                              'length': 5,
                              'labelrotation': 0
                          })

    with tempfile.NamedTemporaryFile('r') as file:
        save_mpl_defaults(file.name)

        txt = file.read().strip()
        file_regression.check(txt)
    reset_mpl_plot_defaults()


def test_mpl_load_defaults(file_regression):
    """
    Test loading of custom parameters
    """
    import tempfile
    from masci_tools.vis.plot_methods import set_mpl_plot_defaults
    from masci_tools.vis.plot_methods import reset_mpl_plot_defaults
    from masci_tools.vis.plot_methods import save_mpl_defaults
    from masci_tools.vis.plot_methods import load_mpl_defaults

    set_mpl_plot_defaults(markersize=50,
                          show=False,
                          tick_paramsx={
                              'size': 4.0,
                              'width': 1.0,
                              'labelsize': 100,
                              'length': 5,
                              'labelrotation': 0
                          })

    with tempfile.NamedTemporaryFile('r') as file:
        save_mpl_defaults(file.name)
        reset_mpl_plot_defaults()
        load_mpl_defaults(file.name)

    with tempfile.NamedTemporaryFile('r') as file:
        save_mpl_defaults(file.name)

        txt = file.read().strip()
        file_regression.check(txt)

    reset_mpl_plot_defaults()


class TestSingleScatterPlot:
    """
    Test of the single_scatterplot function
    """

@pytest.mark.mpl_image_compare
def test_single_scatter_defaults():
    """
    Scatterplot with default parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    single_scatterplot(x, y, xlabel='X', ylabel='Y', title='Plot Test', show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_single_scatter_param_change():
    """
    Scatterplot with changed parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    single_scatterplot(x,
                        y,
                        xlabel='X',
                        ylabel='Y',
                        title='Plot Test',
                        title_fontsize=30,
                        plot_label='Test',
                        color='darkred',
                        marker='^',
                        markersize=10,
                        linestyle='',
                        show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_single_scatter_scale():
    """
    Scatterplot with different axis scales
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    single_scatterplot(x, y, xlabel='X', ylabel='Y', title='Plot Test', scale={'y': 'log'}, show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_single_scatter_limits():
    """
    Scatterplot with modified plot limits
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    single_scatterplot(x,
                        y,
                        xlabel='X',
                        ylabel='Y',
                        title='Plot Test',
                        limits={
                            'y': (-100, 100),
                            'x': (0, 10)
                        },
                        show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_single_scatter_area():
    """
    Scatterplot with an area plot
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    single_scatterplot(x,
                        y,
                        xlabel='X',
                        ylabel='Y',
                        title='Plot Test',
                        show=False,
                        area_plot=True,
                        area_alpha=0.3,
                        marker=None,
                        color='darkblue')
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_single_scatter_lines():
    """
    Scatterplot with added straight lines
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    single_scatterplot(x,
                        y,
                        xlabel='X',
                        ylabel='Y',
                        title='Plot Test',
                        lines={
                            'horizontal': 50,
                            'vertical': [-5, 5]
                        },
                        show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_single_scatter_lines_param_change():
    """
    Scatterplot with added straight lines and changed parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()

    single_scatterplot(x,
                        y,
                        xlabel='X',
                        ylabel='Y',
                        title='Plot Test',
                        lines={
                            'horizontal': 50,
                            'vertical': [-5, {
                                'pos': 5,
                                'color': 'darkred',
                                'linestyle': ':',
                                'linewidth': 10
                            }]
                        },
                        show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare(filename='test_single_scatter_limits.png') #Same as the normal limits test
def test_single_scatter_limits_deprecated():
    """
    Scatterplot with deprecated parameter for modifying plot limits
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()
    with pytest.deprecated_call():
        single_scatterplot(x,
                            y,
                            xlabel='X',
                            ylabel='Y',
                            title='Plot Test',
                            limits=[(0, 10), (-100, 100)],
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare(filename='test_single_scatter_scale.png') #same as the normal scale test
def test_single_scatter_scale_deprecated():
    """
    Scatterplot with deprectated option for modifying axis scales
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()
    with pytest.deprecated_call():
        single_scatterplot(x, y, xlabel='X', ylabel='Y', title='Plot Test', scale=[None, 'log'], show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare(filename='test_single_scatter_defaults.png')
def test_single_scatter_deprecated_label():
    """
    Scatterplot with deprectated option for changing plot label
    """
    import numpy as np
    from masci_tools.vis.plot_methods import single_scatterplot

    x = np.linspace(-10, 10, 100)
    y = x**2

    gcf().clear()
    with pytest.deprecated_call():
        single_scatterplot(x, y, xlabel='X', ylabel='Y', title='Plot Test', plotlabel='Test', show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()


class TestMultipleScatterPlot:
    """
    Test of the multiple_scatterplots function
    """

@pytest.mark.mpl_image_compare
def test_multiple_scatter_defaults():
    """
    Scatterplot with default parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()

    multiple_scatterplots(x, y, xlabel='X', ylabel='Y', title='Plot Test', show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multiple_scatter_param_change():
    """
    Scatterplot with a variety of changed parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()

    multiple_scatterplots(x,
                            y,
                            xlabel='X',
                            ylabel='Y',
                            title='Plot Test',
                            title_fontsize=30,
                            plot_label=['Parabola', 'Line', None, 'cosine'],
                            marker='^',
                            linewidth=[1, 3],
                            color=['darkred', 'darkblue', 'limegreen'],
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multiple_scatter_legend():
    """
    Scatterplot with setting the legend
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()

    multiple_scatterplots(x,
                            y,
                            xlabel='X',
                            ylabel='Y',
                            title='Plot Test',
                            plot_label=['Parabola', 'Line', None, 'cosine'],
                            legend=True,
                            legend_options={'fontsize': 20},
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multiple_scatter_scale_limits():
    """
    Scatterplot with setting scales and limits
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()

    multiple_scatterplots(x,
                            y,
                            xlabel='X',
                            ylabel='Y',
                            title='Plot Test',
                            scale={'y': 'log'},
                            limits={
                                'y': (0.01, 100),
                                'x': (0, 10)
                            },
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multiple_scatter_xticks():
    """
    Scatterplot with setting custom xticks
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()

    multiple_scatterplots(x,
                            y,
                            xlabel='X',
                            ylabel='Y',
                            title='Plot Test',
                            xticks=[-10, 3, 3, 10, 20],
                            xticklabels=[r'$\pi$', '4', 'TEST', r'$\Omega$', r'$\frac{{1}}{{4}}$'],
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multiple_scatter_dict_selection():
    """
    Test the partial setting of values via integer indexed dict
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()

    multiple_scatterplots(x,
                            y,
                            xlabel='X',
                            ylabel='Y',
                            title='Plot Test',
                            marker='^',
                            color={4: 'k'},
                            plot_label={
                                0: 'Parabola',
                                1: 'Line',
                                3: 'cosine'
                            },
                            linewidth={2: 5},
                            legend=True,
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multiple_scatter_area():
    """
    Test multiple scatter plot with one plot as an area plot
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()

    multiple_scatterplots(x,
                            y,
                            xlabel='X',
                            ylabel='Y',
                            title='Plot Test',
                            marker='^',
                            color={
                                4: 'k',
                                3: 'darkorange'
                            },
                            area_plot={3: True},
                            plot_label={
                                0: 'Parabola',
                                1: 'Line',
                                3: 'cosine'
                            },
                            linewidth={2: 5},
                            legend=True,
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare(filename='test_multiple_scatter_scale_limits.png') #Same as non-deprecated test
def test_multiple_scatter_scale_limits_deprecated():
    """
    Scatterplot with deprecated options for setting scales and limits
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()
    with pytest.deprecated_call():
        multiple_scatterplots(x,
                                y,
                                xlabel='X',
                                ylabel='Y',
                                title='Plot Test',
                                scale=[None, 'log'],
                                limits=[(0, 10), (0.01, 100)],
                                show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare(filename='test_multiple_scatter_xticks.png')
def test_multiple_scatter_xticks_deprecated():
    """
    Scatterplot with deprecated option for setting custom xticks
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()
    with pytest.deprecated_call():
        multiple_scatterplots(x,
                                y,
                                xlabel='X',
                                ylabel='Y',
                                title='Plot Test',
                                xticks=[[r'$\pi$', '4', 'TEST', r'$\Omega$', r'$\frac{{1}}{{4}}$'],
                                        [-10, 3, 3, 10, 20]],
                                show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare(filename='test_multiple_scatter_legend.png')
def test_multiple_scatter_plot_labels_deprecated():
    """
    Scatterplot with deprecated option for setting custom plot labels
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()
    with pytest.deprecated_call():
        multiple_scatterplots(x,
                                y,
                                xlabel='X',
                                ylabel='Y',
                                title='Plot Test',
                                plot_labels=['Parabola', 'Line', None, 'cosine'],
                                legend=True,
                                legend_options={'fontsize': 20},
                                show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare(filename='test_multiple_scatter_legend.png')
def test_multiple_scatter_legend_option_deprecated():
    """
    Scatterplot with deprecated option for setting legend parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()
    with pytest.deprecated_call():
        multiple_scatterplots(x,
                                y,
                                xlabel='X',
                                ylabel='Y',
                                title='Plot Test',
                                plot_label=['Parabola', 'Line', None, 'cosine'],
                                legend=True,
                                legend_option={'fontsize': 20},
                                show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multiple_scatter_colors_deprecated():
    """
    Scatterplot with setting colors via deprecated option
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiple_scatterplots

    x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

    gcf().clear()
    with pytest.deprecated_call():
        multiple_scatterplots(x,
                                y,
                                xlabel='X',
                                ylabel='Y',
                                title='Plot Test',
                                colors=['darkred', 'darkblue', 'limegreen'],
                                show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()


@pytest.mark.mpl_image_compare
def test_multi_scatter_defaults():
    """
    Scatterplot with default parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multi_scatter_plot

    x = [np.linspace(-10, 10, 50)] * 2
    y = [x[0]**2, x[1] * 5 + 30]
    s = [100 * np.exp(-0.1 * x[0]**2), abs(x[1])]

    gcf().clear()

    multi_scatter_plot(x, y, size_data=s, xlabel='X', ylabel='Y', title='Plot Test', show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multi_scatter_param_change():
    """
    Scatterplot with changed parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multi_scatter_plot

    x = [np.linspace(-10, 10, 50)] * 2
    y = [x[0]**2, x[1] * 5 + 30]
    s = [100 * np.exp(-0.1 * x[0]**2), abs(x[1])]

    gcf().clear()

    multi_scatter_plot(x,
                        y,
                        size_data=s,
                        xlabel='X',
                        ylabel='Y',
                        title='Plot Test',
                        color=['darkred', 'darkorange'],
                        marker='^',
                        plot_alpha=0.6,
                        plot_label=['Parabola', 'Line'],
                        legend=True,
                        show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multi_plot_moved_defaults():
    """
    Mulitplot_moved with default parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiplot_moved

    x = [np.linspace(-10, 10, 100)] * 3
    y = [x[0] * 5 + 30, 50 * np.sin(x[1]), 50 * np.cos(x[2])]

    gcf().clear()

    multiplot_moved(x, y, xlabel='X', ylabel='Y', title='Plot Test', scale_move=2.0, show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multi_plot_moved_param_change():
    """
    Multiplot moved with changed parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiplot_moved

    x = [np.linspace(-10, 10, 100)] * 3
    y = [x[0] * 5 + 30, 50 * np.sin(x[1]), 50 * np.cos(x[2])]

    gcf().clear()

    multiplot_moved(x,
                    y,
                    xlabel='X',
                    ylabel='Y',
                    title='Plot Test',
                    plot_label=['Line', None, 'cosine'],
                    legend=True,
                    min_add=20,
                    color=['darkred', 'darkblue', 'darkorange'],
                    scale_move=2.0,
                    show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_multi_plot_moved_area():
    """
    Mulitplot_moved with changed parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiplot_moved

    x = [np.linspace(-10, 10, 100)] * 3
    y = [x[0] * 5 + 30, 50 * np.sin(x[1]), 50 * np.cos(x[2])]

    gcf().clear()

    multiplot_moved(x,
                    y,
                    xlabel='X',
                    ylabel='Y',
                    title='Plot Test',
                    area_plot={2: True},
                    area_linecolor='k',
                    show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_waterfall_plot_defaults():
    """
    Waterfall plot with default parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import waterfall_plot

    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)

    xv, yv = np.meshgrid(x, y)
    z = 10 * np.exp(-xv**2 - yv**2)
    xv, yv, z = xv.flatten(), yv.flatten(), z.flatten()

    gcf().clear()

    waterfall_plot(xv, yv, z, xlabel='X', ylabel='Y', zlabel='Z', title='Plot Test', show=False)
    # need to return the figure in order for mpl checks to work

    return gcf()

@pytest.mark.mpl_image_compare
def test_surface_plot_defaults():
    """
    Surface plot with default parameters
    """
    import numpy as np
    from masci_tools.vis.plot_methods import surface_plot

    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)

    xv, yv = np.meshgrid(x, y)
    z = 10 * np.exp(-xv**2 - yv**2)

    gcf().clear()

    surface_plot(xv, yv, z, xlabel='X', ylabel='Y', zlabel='Z', title='Plot Test', show=False)
    # need to return the figure in order for mpl checks to work

    return gcf()


@pytest.mark.mpl_image_compare
def test_multiaxis_defaults():
    """
    Test of multiaxis_scatterplot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiaxis_scatterplot
    x = [np.linspace(-10, 10, 100)] * 2 + [[np.linspace(-10, 10, 100)] * 2] + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, [50 * np.sin(x[2][0]), 50 * np.cos(x[2][1])], -5 * x[3] + 30]

    gcf().clear()

    multiaxis_scatterplot(x,
                            y,
                            axes_loc=[(0, 0), (0, 1), (1, 0), (1, 1)],
                            xlabel='X',
                            ylabel='Y',
                            title=['Parabola', 'Line1', 'sin/cos', 'Line2'],
                            num_rows=2,
                            num_cols=2,
                            show=False)
    # need to return the figure in order for mpl checks to work

    return gcf()

@pytest.mark.mpl_image_compare
def test_multiaxis_non_standard_layout():
    """
    Test of multiaxis_scatterplot with non standard layout
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiaxis_scatterplot
    x = [np.linspace(-10, 10, 100)] + [[np.linspace(-10, 10, 100)] * 2] * 2
    y = [x[0]**2, [-5 * x[1][0] + 30, x[1][1] * 5 + 30], [50 * np.sin(x[2][0]), 50 * np.cos(x[2][1])]]

    gcf().clear()

    multiaxis_scatterplot(x,
                            y,
                            axes_loc=[(0, 0), (0, 1), (1, 0)],
                            axes_kwargs={1: {
                                'rowspan': 2
                            }},
                            xlabel='X',
                            ylabel='Y',
                            title=['Parabola', 'Lines', 'sin/cos'],
                            num_rows=2,
                            num_cols=2,
                            show=False)
    # need to return the figure in order for mpl checks to work

    return gcf()

@pytest.mark.mpl_image_compare
def test_multiaxis_overall_param_change():
    """
    Test of multiaxis_scatterplot with a variety of parameters changed for all subplots
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiaxis_scatterplot
    x = [np.linspace(-10, 10, 100)] * 2 + [[np.linspace(-10, 10, 100)] * 2] + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, [50 * np.sin(x[2][0]), 50 * np.cos(x[2][1])], -5 * x[3] + 30]

    gcf().clear()

    multiaxis_scatterplot(x,
                            y,
                            axes_loc=[(0, 0), (0, 1), (1, 0), (1, 1)],
                            xlabel='X',
                            ylabel='Y',
                            title=['Parabola', 'Line1', 'sin/cos', 'Line2'],
                            marker='^',
                            color={0: 'darkred'},
                            linewidth=10,
                            title_fontsize=30,
                            markersize=15,
                            num_rows=2,
                            num_cols=2,
                            show=False)
    # need to return the figure in order for mpl checks to work

    return gcf()

@pytest.mark.mpl_image_compare
def test_multiaxis_single_subplot_param_change():
    """
    Test of multiaxis_scatterplot with a variety of parameters changed for a specific subplot
    """
    import numpy as np
    from masci_tools.vis.plot_methods import multiaxis_scatterplot
    x = [np.linspace(-10, 10, 100)] * 2 + [[np.linspace(-10, 10, 100)] * 2] + [np.linspace(-10, 20, 100)]
    y = [x[0]**2, x[1] * 5 + 30, [50 * np.sin(x[2][0]), 50 * np.cos(x[2][1])], -5 * x[3] + 30]

    gcf().clear()

    multiaxis_scatterplot(x,
                            y,
                            axes_loc=[(0, 0), (0, 1), (1, 0), (1, 1)],
                            xlabel='X',
                            ylabel='Y',
                            title=['Parabola', 'Line1', 'sin/cos', 'Line2'],
                            subplot_params={
                                0: {
                                    'color': 'limegreen',
                                    'scale': {
                                        'y': 'log'
                                    }
                                },
                                2: {
                                    'limits': {
                                        'x': (0, 10)
                                    },
                                    'color': {
                                        0: 'darkorange'
                                    },
                                    'plot_label': ['sin', 'cos'],
                                    'legend': True
                                }
                            },
                            num_rows=2,
                            num_cols=2,
                            show=False)
    # need to return the figure in order for mpl checks to work
    return gcf()


@pytest.mark.mpl_image_compare
def test_colormesh_defaults():
    """
    Test of colormesh plot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import colormesh_plot

    x = np.linspace(0, np.pi, 100)
    y = np.linspace(0, np.pi, 100)
    x, y = np.meshgrid(x, y)
    data = np.sin(x + y)

    gcf().clear()

    colormesh_plot(x, y, data, xlabel='X', ylabel='Y', title='sin', show=False)

    # need to return the figure in order for mpl checks to work
    return gcf()


@pytest.mark.mpl_image_compare
def test_histogram_defaults():
    """
    Test of histogram plot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import histogram

    np.random.seed(19680801)
    N_points = 10000

    # Generate a normal distribution, center at x=0 and y=5
    x = np.random.randn(N_points)

    gcf().clear()

    histogram(x, show=False)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_histogram_param_change():
    """
    Test of histogram plot with various parameters changed
    """
    import numpy as np
    from masci_tools.vis.plot_methods import histogram

    np.random.seed(19680801)
    N_points = 10000

    # Generate a normal distribution, center at x=0 and y=5
    x = np.random.randn(N_points)

    gcf().clear()

    histogram(x,
                color='darkred',
                linewidth=2,
                plot_alpha=0.3,
                plot_label='Normal',
                density=True,
                legend=True,
                orientation='horizontal',
                log=True,
                show=False)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_histogram_stacked_defaults():
    """
    Test of stacked histogram plot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import histogram

    np.random.seed(19680801)
    N_points = 10000

    # Generate a normal distribution, center at x=0 and y=5
    x = np.random.randn(N_points)
    x2 = np.random.randn(N_points)

    gcf().clear()

    histogram([x, x2], show=False, histtype='barstacked')

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_histogram_stacked_param_change():
    """
    Test of stacked histogram plot with various parameters changed
    """
    import numpy as np
    from masci_tools.vis.plot_methods import histogram

    np.random.seed(19680801)
    N_points = 10000

    # Generate a normal distribution, center at x=0 and y=5
    x = np.random.randn(N_points)
    x2 = np.random.randn(N_points)

    gcf().clear()

    histogram([x, x2],
                color=['darkblue', 'darkred'],
                histtype='barstacked',
                linewidth=2,
                legend=True,
                plot_label={1: 'This is on top'},
                show=False)

    # need to return the figure in order for mpl checks to work
    return gcf()


@pytest.mark.mpl_image_compare
def test_barchart_stacked_defaults():
    """
    Test of stacked barchart plot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = [np.linspace(0, 10, 11)] * 2
    y = [x[0]**2, [50] * 11]
    gcf().clear()

    barchart(x, y, show=False)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_stacked_param_change():
    """
    Test of stacked barchart plot with various parameters changed
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = [np.linspace(0, 10, 11)] * 2
    y = [x[0]**2, [50] * 11]
    gcf().clear()

    barchart(x,
                y,
                show=False,
                width=0.7,
                align='edge',
                limits={'x': (-2, 15)},
                color={1: 'darkred'},
                plot_label=['Bottom', 'Top'],
                legend=True)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_stacked_horizontal_param_change():
    """
    Test of stacked horizontal barchart plot with various parameters changed
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = [np.linspace(0, 10, 11)] * 2
    y = [x[0]**2, [50] * 11]
    gcf().clear()

    barchart(x,
                y,
                show=False,
                alignment='horizontal',
                width=0.7,
                align='edge',
                limits={'y': (-2, 15)},
                color={1: 'darkred'},
                plot_label=['Bottom', 'Top'],
                legend=True)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_grouped_even_defaults():
    """
    Test of grouped barchart plot with default values (even number)
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = [np.linspace(0, 10, 11)] * 2
    y = [x[0]**2, [50] * 11]
    gcf().clear()

    barchart(x, y, show=False, bar_type='grouped')

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_grouped_odd_defaults():
    """
    Test of grouped barchart plot with default values (odd number)
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = np.linspace(0, 20, 11)
    y = [x**2, [50] * 11, 20 * np.abs(np.sin(x))]
    gcf().clear()

    barchart(x, y, show=False, bar_type='grouped')

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_grouped_param_change():
    """
    Test of grouped barchart plot with various parameters changed
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = np.linspace(0, 20, 11)
    y = [x**2, [50] * 11, 20 * np.abs(np.sin(x))]
    gcf().clear()

    barchart(x,
                y,
                show=False,
                bar_type='grouped',
                width=0.5,
                align='edge',
                color={2: 'darkred'},
                plot_label=['One Set', 'Another Set', 'And another one'],
                legend=True)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_grouped_horizontal_param_change():
    """
    Test of grouped horizontal barchart plot with various parameters changed
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = np.linspace(0, 20, 11)
    y = [x**2, [50] * 11, 20 * np.abs(np.sin(x))]
    gcf().clear()

    barchart(x,
                y,
                show=False,
                alignment='horizontal',
                bar_type='grouped',
                width=0.5,
                align='edge',
                color={2: 'darkred'},
                plot_label=['One Set', 'Another Set', 'And another one'],
                legend=True)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_independent_defaults():
    """
    Test of independent barchart plot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = [np.linspace(0, 10, 11), np.linspace(0, 10, 11) + 15]
    y = [x[0]**2, 20 * np.abs(np.sin(x[1]))]
    gcf().clear()

    barchart(x, y, show=False, bar_type='independent')

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_independent_param_change():
    """
    Test of independent barchart plot with various parameters changed
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = [np.linspace(0, 10, 11), np.linspace(0, 10, 11) + 15]
    y = [x[0]**2, 20 * np.abs(np.sin(x[1]))]
    gcf().clear()

    barchart(x,
                y,
                show=False,
                bar_type='independent',
                width=0.5,
                color={1: 'darkred'},
                plot_label=['Left', 'Right'],
                legend=True)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_barchart_independent_horizontal_defaults():
    """
    Test of independent horizontal barchart plot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import barchart

    x = [np.linspace(0, 10, 11), np.linspace(0, 10, 11) + 15]
    y = [x[0]**2, 20 * np.abs(np.sin(x[1]))]
    gcf().clear()

    barchart(x, y, show=False, bar_type='independent', alignment='horizontal')

    # need to return the figure in order for mpl checks to work
    return gcf()


@pytest.mark.mpl_image_compare
def test_residuen_defaults():
    """
    Test of residuen plot with default values
    """
    import numpy as np
    from masci_tools.vis.plot_methods import plot_residuen

    np.random.seed(19680801)
    N_points = 100

    # Generate a normal distribution, center at x=0 and y=5
    rand = np.random.randn(N_points)

    x = np.linspace(-10, 10, N_points)
    fit = x**2
    real = fit + rand

    gcf().clear()

    plot_residuen(x, fit, real, show=False)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_residuen_no_hist():
    """
    Test of residuen plot without histogram
    """
    import numpy as np
    from masci_tools.vis.plot_methods import plot_residuen

    np.random.seed(19680801)
    N_points = 100

    # Generate a normal distribution, center at x=0 and y=5
    rand = np.random.randn(N_points)

    x = np.linspace(-10, 10, N_points)
    fit = x**2
    real = fit + rand

    gcf().clear()

    plot_residuen(x, fit, real, hist=False, show=False)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_residuen_param_change_residue_plot():
    """
    Test of residuen plot with changed parameters on residue plot
    """
    import numpy as np
    from masci_tools.vis.plot_methods import plot_residuen

    np.random.seed(19680801)
    N_points = 100

    # Generate a normal distribution, center at x=0 and y=5
    rand = np.random.randn(N_points)

    x = np.linspace(-10, 10, N_points)
    fit = x**2
    real = fit + rand

    gcf().clear()

    plot_residuen(x,
                    fit,
                    real,
                    show=False,
                    marker='^',
                    color='darkblue',
                    xlabel='X',
                    ylabel='Test Label',
                    labelfontsize=30)

    # need to return the figure in order for mpl checks to work
    return gcf()

@pytest.mark.mpl_image_compare
def test_residuen_param_change_hist_plot():
    """
    Test of residuen plot with changed parameters on histogram
    """
    import numpy as np
    from masci_tools.vis.plot_methods import plot_residuen

    np.random.seed(19680801)
    N_points = 100

    # Generate a normal distribution, center at x=0 and y=5
    rand = np.random.randn(N_points)

    x = np.linspace(-10, 10, N_points)
    fit = x**2
    real = fit + rand

    gcf().clear()

    plot_residuen(x,
                    fit,
                    real,
                    show=False,
                    hist_kwargs={
                        'color': 'darkblue',
                        'xlabel': 'X',
                        'ylabel': 'Test Label',
                        'labelfontsize': 30,
                        'plot_label': 'Residue',
                        'legend': True
                    })

    # need to return the figure in order for mpl checks to work
    return gcf()


@pytest.mark.mpl_image_compare
def test_convergence_defaults(convergence_plot_data):
    """
    Test of convergence plot with default values
    """
    from masci_tools.vis.plot_methods import plot_convergence_results

    gcf().clear()

    #plot_convergence produces two figures, for testing we merge them into one
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    iteration, distance, energy = convergence_plot_data(1)

    with pytest.deprecated_call():
        plot_convergence_results(iteration, distance, energy, show=False, axis1=ax1, axis2=ax2)

    # need to return the figure in order for mpl checks to work
    return fig

@pytest.mark.mpl_image_compare
def test_convergence_param_change(convergence_plot_data):
    """
    Test of convergence plot with changed parameters
    """
    from masci_tools.vis.plot_methods import plot_convergence_results

    gcf().clear()

    #plot_convergence produces two figures, for testing we merge them into one
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    iteration, distance, energy = convergence_plot_data(1)

    with pytest.deprecated_call():
        plot_convergence_results(iteration,
                                 distance,
                                 energy,
                                    show=False,
                                    axis1=ax1,
                                    axis2=ax2,
                                    linestyle='--',
                                    color='darkred',
                                    marker='s',
                                    linewidth=10,
                                    title_fontsize=20)

    # need to return the figure in order for mpl checks to work
    return fig


class TestPlotConvergenceMulti:  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/convergence_multi/',
                                   filename='defaults.png')
    def test_defaults(self):
        """
        Test of multiple convergence plot with default values
        """
        from masci_tools.vis.plot_methods import plot_convergence_results_m
        import numpy as np

        np.random.seed(19680801)
        number_iterations = np.random.randint(15, high=50, size=15)
        iteration = [np.array(range(iters)) for iters in number_iterations]

        noise_arr = [0.1 * np.random.randn(iters) + 1.0 for iters in number_iterations]

        distance_decay = np.random.rand(15)
        distance_offset = 100 * np.random.rand(15)

        energy_decay = np.random.rand(15)
        energy_offset = 20000 + 500 * np.random.rand(15)
        energy_offset2 = 1000 * np.random.rand(15)

        distances = [
            noise * offset * np.exp(-decay * iters)
            for iters, noise, decay, offset in zip(iteration, noise_arr, distance_decay, distance_offset)
        ]
        energies = [
            noise * offset2 * np.exp(-decay * iters) + offset for iters, noise, decay, offset, offset2 in zip(
                iteration, noise_arr, energy_decay, energy_offset, energy_offset2)
        ]

        gcf().clear()

        #plot_convergence produces two figures, for testing we merge them into one
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        with pytest.deprecated_call():
            plot_convergence_results_m(iteration, distances, energies, show=False, axis1=ax1, axis2=ax2, modes=[])

        # need to return the figure in order for mpl checks to work
        return fig


class TestPlotConvexHull2d:  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/convex_hull/', filename='defaults.png')
    def test_defaults_scipy(self):
        """
        Test with default parameters
        """
        from scipy.spatial import ConvexHull  #pylint: disable=no-name-in-module
        from masci_tools.vis.plot_methods import plot_convex_hull2d

        pts = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0, 0]]
        hull = ConvexHull(pts)

        gcf().clear()

        plot_convex_hull2d(hull, show=False)

        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/convex_hull/', filename='defaults.png')
    def test_defaults_pyhull(self):
        """
        Test with default parameters
        """
        pytest.importorskip('pyhull')
        from pyhull.convex_hull import ConvexHull  #pylint: disable=import-error
        from masci_tools.vis.plot_methods import plot_convex_hull2d

        pts = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0, 0]]
        hull = ConvexHull(pts)

        gcf().clear()

        plot_convex_hull2d(hull, show=False)

        return gcf()


class TestPlotLatticeConstant:  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/lattice_constant/',
                                   filename='defaults_single.png')
    def test_defaults_single(self):
        """
        Test with default parameters
        """
        from masci_tools.vis.plot_methods import plot_lattice_constant
        import numpy as np

        scaling = np.linspace(0.95, 1.04, 10)
        energy = -500.0 + 500.0 * (0.99 - scaling)**2

        gcf().clear()

        plot_lattice_constant(scaling, energy, show=False)

        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/lattice_constant/',
                                   filename='fit_single.png')
    def test_defaults_single_fity(self):
        """
        Test with default parameters
        """
        from masci_tools.vis.plot_methods import plot_lattice_constant
        import numpy as np

        np.random.seed(19680801)
        scaling = np.linspace(0.95, 1.04, 10)
        energy = -500.0 + 500 * (0.99 - scaling)**2

        noise = 0.5 * (np.random.rand(10) - 0.5)

        gcf().clear()

        plot_lattice_constant(scaling, energy + noise, fit_data=energy, show=False)

        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/lattice_constant/',
                                   filename='defaults_multi.png')
    def test_defaults_multi(self):
        """
        Test with default parameters
        """
        from masci_tools.vis.plot_methods import plot_lattice_constant
        import numpy as np

        np.random.seed(19680801)

        energy_offset = np.random.rand(5)
        energy_offset = -500.0 + energy_offset

        energy_scaling = np.random.rand(5) * 50
        energy_groundstate = np.random.rand(5)
        energy_groundstate = 1.0 + (energy_groundstate - 0.5) * 0.05

        scaling = np.linspace(0.95, 1.04, 10)
        energy = [
            offset + const * (ground - scaling)**2
            for offset, const, ground in zip(energy_offset, energy_scaling, energy_groundstate)
        ]
        scaling = [scaling] * 5

        gcf().clear()

        plot_lattice_constant(scaling, energy, show=False)

        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/lattice_constant/',
                                   filename='fit_multi.png')
    def test_defaults_multi_fity(self):
        """
        Test with default parameters
        """
        from masci_tools.vis.plot_methods import plot_lattice_constant
        import numpy as np

        np.random.seed(19680801)

        energy_offset = np.random.rand(5)
        energy_offset = -500.0 + energy_offset

        energy_scaling = np.random.rand(5) * 50
        energy_groundstate = np.random.rand(5)
        energy_groundstate = 1.0 + (energy_groundstate - 0.5) * 0.05

        scaling = np.linspace(0.95, 1.04, 10)
        energy_fit = [
            offset + const * (ground - scaling)**2
            for offset, const, ground in zip(energy_offset, energy_scaling, energy_groundstate)
        ]
        energy_noise = [energy + (np.random.rand(10) - 0.5) * 0.05 for energy in energy_fit]
        scaling = [scaling] * 5

        gcf().clear()

        plot_lattice_constant(scaling, energy_noise, fit_data=energy_fit, show=False)

        return gcf()
