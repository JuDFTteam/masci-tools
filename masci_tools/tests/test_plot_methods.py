#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

# prevent issue with not having a display on travis-ci
# this needs to go *before* pyplot imports
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import gcf, title
#from masci_tools.io.kkr_read_shapefun_info import read_shapefun
#from masci_tools.vis.kkr_plot_shapefun import plot_shapefun
#from masci_tools.vis.kkr_plot_dos import dosplot
#from masci_tools.vis.kkr_plot_bandstruc_qdos import dispersionplot
#from masci_tools.vis.kkr_plot_FS_qdos import FSqdos2D

# TODO: test if interfaces stay the same...
# I do not write extensive testing, since plot_methods should be redesigned anyway....


class Test_plot_methods_imports(object):
    """
    Test plotting functions
    """

    #from masci_tools.vis.plot_methods import *
    from masci_tools.vis.plot_methods import set_plot_defaults
    from masci_tools.vis.plot_methods import single_scatterplot
    from masci_tools.vis.plot_methods import multiple_scatterplots
    from masci_tools.vis.plot_methods import multi_scatter_plot
    from masci_tools.vis.plot_methods import waterfall_plot
    from masci_tools.vis.plot_methods import multiplot_moved
    from masci_tools.vis.plot_methods import histogram
    from masci_tools.vis.plot_methods import default_histogram
    from masci_tools.vis.plot_methods import plot_convex_hull2d
    from masci_tools.vis.plot_methods import plot_residuen
    from masci_tools.vis.plot_methods import plot_convergence_results
    from masci_tools.vis.plot_methods import plot_convergence_results_m
    from masci_tools.vis.plot_methods import plot_lattice_constant
    from masci_tools.vis.plot_methods import plot_relaxation_results
    from masci_tools.vis.plot_methods import plot_dos
    from masci_tools.vis.plot_methods import plot_bands
    from masci_tools.vis.plot_methods import plot_one_element_corelv
    from masci_tools.vis.plot_methods import construct_corelevel_spectrum
    from masci_tools.vis.plot_methods import plot_corelevel_spectra
    from masci_tools.vis.plot_methods import plot_fleur_bands

    def test_set_defaults(self):
        from masci_tools.vis.plot_methods import linewidth_g
        from masci_tools.vis.plot_methods import set_plot_defaults
        set_plot_defaults(linewidth=3.0)
        assert linewidth_g == 2.0  # if worked should be 3.0


class TestSingleScatterPlot(object):
    """
    Test of the single_scatterplot function
    """

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='defaults.png')
    def test_single_scatterplot_default(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()

        single_scatterplot(y, x, 'X', 'Y', 'Plot Test', show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='param_change.png')
    def test_single_scatterplot_params_changed(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()

        single_scatterplot(y,
                           x,
                           'X',
                           'Y',
                           'Plot Test',
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
    def test_single_scatterplot_scale(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()

        single_scatterplot(y, x, 'X', 'Y', 'Plot Test', scale={'y': 'log'}, show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='limits.png')
    def test_single_scatterplot_limits(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()

        single_scatterplot(y, x, 'X', 'Y', 'Plot Test', limits={'y': (-100, 100), 'x': (0, 10)}, show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='area.png')
    def test_single_scatterplot_area(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()

        single_scatterplot(y, x, 'X', 'Y', 'Plot Test', show=False, area_plot=True, plot_alpha=0.3,marker=None,color='darkblue')
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='limits.png')
    def test_single_scatterplot_limits_deprecated(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()
        with pytest.deprecated_call():
            single_scatterplot(y, x, 'X', 'Y', 'Plot Test', limits=[(0, 10), (-100, 100)], show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='scale.png')
    def test_single_scatterplot_scale_deprecated(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()
        with pytest.deprecated_call():
            single_scatterplot(y, x, 'X', 'Y', 'Plot Test', scale=[None, 'log'], show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/single_scatterplot/',
                                   filename='defaults.png')
    def test_single_scatterplot_deprecated_label(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import single_scatterplot

        x = np.linspace(-10, 10, 100)
        y = x**2

        gcf().clear()
        with pytest.deprecated_call():
            single_scatterplot(y, x, 'X', 'Y', 'Plot Test', plotlabel='Test', show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()


class TestMultipleScatterPlot(object):
    """
    Test of the multiple_scatterplots function
    """

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='defaults.png')
    def test_multiple_scatterplots_default(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()

        multiple_scatterplots(y, x, 'X', 'Y', 'Plot Test', show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='param_change.png')
    def test_multiple_scatterplots_param_change(self):
        """
        Scatterplot with a variety of changed parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()

        multiple_scatterplots(y,
                              x,
                              'X',
                              'Y',
                              'Plot Test',
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
    def test_multiple_scatterplots_legend(self):
        """
        Scatterplot with setting the legend
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()

        multiple_scatterplots(y,
                              x,
                              'X',
                              'Y',
                              'Plot Test',
                              plot_label=['Parabola', 'Line', None, 'cosine'],
                              legend=True,
                              legend_options={'fontsize': 17},
                              show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='scale_limits.png')
    def test_multiple_scatterplots_scale_limits(self):
        """
        Scatterplot with setting scales and limits
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()

        multiple_scatterplots(y,
                              x,
                              'X',
                              'Y',
                              'Plot Test',
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
    def test_multiple_scatterplots_xticks(self):
        """
        Scatterplot with setting custom xticks
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()

        multiple_scatterplots(y,
                              x,
                              'X',
                              'Y',
                              'Plot Test',
                              xticks=[-10, 3, 3, 10, 20],
                              xticklabels=[r'$\pi$', '4', 'TEST', r'$\Omega$', r'$\frac{{1}}{{4}}$'],
                              show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='dict_selection.png')
    def test_multiple_scatterplots_dict_selection(self):
        """
        Test the partial setting of values via integer indexed dict
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()

        multiple_scatterplots(y,
                              x,
                              'X',
                              'Y',
                              'Plot Test',
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
    def test_multiple_scatterplots_area(self):
        """
        Test the partial setting of values via integer indexed dict
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()

        multiple_scatterplots(y,
                              x,
                              'X',
                              'Y',
                              'Plot Test',
                              marker='^',
                              color={4: 'k', 3: 'darkorange'},
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
    def test_multiple_scatterplots_scale_limits_deprecated(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()
        with pytest.deprecated_call():
            multiple_scatterplots(y,
                                  x,
                                  'X',
                                  'Y',
                                  'Plot Test',
                                  scale=[None, 'log'],
                                  limits=[(0, 10), (0.01, 100)],
                                  show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='xticks.png')
    def test_multiple_scatterplots_xticks_deprecated(self):
        """
        Scatterplot with setting custom xticks
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()
        with pytest.deprecated_call():
            multiple_scatterplots(y,
                                  x,
                                  'X',
                                  'Y',
                                  'Plot Test',
                                  xticks=[[r'$\pi$', '4', 'TEST', r'$\Omega$', r'$\frac{{1}}{{4}}$'],
                                          [-10, 3, 3, 10, 20]],
                                  show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='legend.png')
    def test_multiple_scatterplots_plot_labels_deprecated(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()
        with pytest.deprecated_call():
            multiple_scatterplots(y,
                                  x,
                                  'X',
                                  'Y',
                                  'Plot Test',
                                  plot_labels=['Parabola', 'Line', None, 'cosine'],
                                  legend=True,
                                  legend_options={'fontsize': 20},
                                  show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='legend.png')
    def test_multiple_scatterplots_legend_option_deprecated(self):
        """
        Scatterplot with default parameters
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()
        with pytest.deprecated_call():
            multiple_scatterplots(y,
                                  x,
                                  'X',
                                  'Y',
                                  'Plot Test',
                                  plot_label=['Parabola', 'Line', None, 'cosine'],
                                  legend=True,
                                  legend_option={'fontsize': 20},
                                  show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()

    @pytest.mark.mpl_image_compare(baseline_dir='files/plot_methods/matplotlib/multiple_scatterplots/',
                                   filename='colors.png')
    def test_multiple_scatterplots_colors_deprecated(self):
        """
        Scatterplot with setting colors via deprecated option
        """
        import numpy as np
        from masci_tools.vis.plot_methods import multiple_scatterplots

        x = [np.linspace(-10, 10, 100)] * 4 + [np.linspace(-10, 20, 100)]
        y = [x[0]**2, x[1] * 5 + 30, 50 * np.sin(x[2]), 50 * np.cos(x[3]), -5 * x[4] + 30]

        gcf().clear()
        with pytest.deprecated_call():
            multiple_scatterplots(y, x, 'X', 'Y', 'Plot Test', colors=['darkred', 'darkblue', 'limegreen'], show=False)
        # need to return the figure in order for mpl checks to work
        return gcf()
