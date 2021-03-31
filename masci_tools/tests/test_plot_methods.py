#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#from masci_tools.io.kkr_read_shapefun_info import read_shapefun
#from masci_tools.vis.kkr_plot_shapefun import plot_shapefun
#from masci_tools.vis.kkr_plot_dos import dosplot
#from masci_tools.vis.kkr_plot_bandstruc_qdos import dispersionplot
#from masci_tools.vis.kkr_plot_FS_qdos import FSqdos2D


def test_plot_methods_imports():
    """
    Test that all expected functions are still there
    """
    from masci_tools.vis.plot_methods import set_mpl_plot_defaults
    from masci_tools.vis.plot_methods import reset_mpl_plot_defaults
    from masci_tools.vis.plot_methods import show_mpl_plot_defaults
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


class TestSingleScatterPlot(object):
    """
    Test of the single_scatterplot function
    """

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='defaults.png')
    def test_default(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='param_change.png')
    def test_params_changed(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='scale.png')
    def test_scale(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()

        single_scatterplot(x, y, xlabel='X', ylabel='Y', title='Plot Test', scale={'y': 'log'}, show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='limits.png')
    def test_limits(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='area.png')
    def test_area(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='lines.png')
    def test_lines(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='lines_param_change.png')
    def test_lines_param_change(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='limits.png')
    def test_limits_deprecated(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='scale.png')
    def test_scale_deprecated(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='defaults.png')
    def test_deprecated_label(self):
        """
        Scatterplot with default parameters
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


class TestMultipleScatterPlot(object):
    """
    Test of the multiple_scatterplots function
    """

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='defaults.png')
    def test_default(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='param_change.png')
    def test_param_change(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='legend.png')
    def test_legend(self):
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
                              legend_options={'fontsize': 17},
                              show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='scale_limits.png')
    def test_scale_limits(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='xticks.png')
    def test_xticks(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='dict_selection.png')
    def test_dict_selection(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='area.png')
    def test_area(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='scale_limits.png')
    def test_scale_limits_deprecated(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='xticks.png')
    def test_xticks_deprecated(self):
        """
        Scatterplot with setting custom xticks
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='legend.png')
    def test_plot_labels_deprecated(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='legend.png')
    def test_legend_option_deprecated(self):
        """
        Scatterplot with default parameters
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='colors.png')
    def test_colors_deprecated(self):
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


class TestMultiScatterPlot(object):
    """
    Test of the multi_scatter_plot function
    """

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multi_scatter_plot/',
                                   filename='defaults.png')
    def test_default(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multi_scatter_plot/',
                                   filename='param_change.png')
    def test_param_change(self):
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


class TestMultiPlotMoved(object):
    """Test of the multiplot_moved function"""

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiplot_moved/',
                                   filename='defaults.png')
    def test_default(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiplot_moved/',
                                   filename='param_change.png')
    def test_param_change(self):
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
                        plot_label=['Line', None, 'cosine'],
                        legend=True,
                        min_add=20,
                        color=['darkred', 'darkblue', 'darkorange'],
                        scale_move=2.0,
                        show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiplot_moved/', filename='area.png')
    def test_area(self):
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


class TestWaterFallPlot(object):  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/waterfall_plot/',
                                   filename='defaults.png')
    def test_default(self):
        """
        Mulitplot_moved with default parameters
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


class TestSurfacePlot(object):  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/surface_plot/', filename='defaults.png')
    def test_default(self):
        """
        Mulitplot_moved with default parameters
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


class TestMultiAxisScatterPlot(object):  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiaxis/', filename='defaults.png')
    def test_defaults(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiaxis/',
                                   filename='non_standard_layout.png')
    def test_non_standard_layout(self):
        """
        Test of multiaxis_scatterplot with default values
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiaxis/',
                                   filename='overall_param_change.png')
    def test_overall_param_change(self):
        """
        Test of multiaxis_scatterplot with a variety of parameters changed
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiaxis/',
                                   filename='single_subplot_param_change.png')
    def test_single_subplot_param_change(self):
        """
        Test of multiaxis_scatterplot with a variety of parameters changed
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


class TestColormeshPlot(object):  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/colormesh/', filename='defaults.png')
    def test_defaults(self):
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


class TestHistogramPlot(object):  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/histogram/', filename='defaults.png')
    def test_defaults(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/histogram/', filename='param_change.png')
    def test_param_change(self):
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


class TestBarchartPlot(object):  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/barchart/', filename='defaults.png')
    def test_defaults(self):
        """
        Test of barchart plot with default values
        """
        import numpy as np
        from masci_tools.vis.plot_methods import barchart

        x = [np.linspace(0, 10, 11)] * 2
        y = [x[0]**2, [50] * 11]
        gcf().clear()

        barchart(x, y, show=False)

        # need to return the figure in order for mpl checks to work
        return gcf()


class TestResiduenPlot(object):  #pylint: disable=missing-class-docstring

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/residuen/', filename='defaults.png')
    def test_defaults(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/residuen/', filename='no_hist.png')
    def test_no_hist(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/residuen/',
                                   filename='param_change_residue.png')
    def test_param_change_residue_plot(self):
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

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/residuen/',
                                   filename='param_change_hist.png')
    def test_param_change_hist_plot(self):
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


class TestPlotConvergenceResults(object):  #pylint: disable=missing-class-docstring

    energies = [
        -69269.46134019217, -69269.42108466873, -69269.35509388152, -69269.62486438647, -69269.51102655893,
        -69269.48862754989, -69269.48874847183, -69269.48459145911, -69269.47327003669, -69269.47248623992,
        -69269.47244891679, -69269.47645687914, -69269.47922946361, -69269.4793222245, -69269.47901836311,
        -69269.47895198638, -69269.47886053707, -69269.47875692157, -69269.47890881824, -69269.47887586526
    ]

    distances = [
        11.6508412231, 10.5637525546, 7.1938351319, 2.6117836621, 2.4735288205, 2.9455389405, 1.8364080301,
        1.4740568937, 1.8542068593, 0.9186745766, 0.900191025, 0.5290019787, 0.0979035892, 0.1098240811, 0.0717916768,
        0.0258508395, 0.0300810883, 0.0067904499, 0.0085097364, 0.0073435947
    ]

    iteration = range(len(distances))

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/convergence/', filename='defaults.png')
    def test_defaults(self):
        """
        Test of convergence plot with default values
        """
        from masci_tools.vis.plot_methods import plot_convergence_results

        gcf().clear()

        #plot_convergence produces two figures, for testing we merge them into one
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        plot_convergence_results(self.iteration, self.distances, self.energies, show=False, axis1=ax1, axis2=ax2)

        # need to return the figure in order for mpl checks to work
        return fig

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/convergence/',
                                   filename='param_change.png')
    def test_param_change(self):
        """
        Test of convergence plot with changed parameters
        """
        from masci_tools.vis.plot_methods import plot_convergence_results

        gcf().clear()

        #plot_convergence produces two figures, for testing we merge them into one
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        plot_convergence_results(self.iteration,
                                 self.distances,
                                 self.energies,
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


class TestPlotConvergenceMulti(object):  #pylint: disable=missing-class-docstring

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

        plot_convergence_results_m(iteration, distances, energies, show=False, axis1=ax1, axis2=ax2, modes=[])

        # need to return the figure in order for mpl checks to work
        return fig
