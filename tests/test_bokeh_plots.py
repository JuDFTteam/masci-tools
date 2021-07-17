# -*- coding: utf-8 -*-
"""
Tests of the bokeh visualization. Since the concrete visualization is difficult
to test we check the content of the underlying json for correctness
"""
import numpy as np
import pandas as pd


class TestBokehScatter:  #pylint: disable=missing-class-docstring

    def test_default(self, check_bokeh_plot):
        """
        Test with default values
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False)

        check_bokeh_plot(p)

    def test_param_change(self, check_bokeh_plot):
        """
        Test with parameters changed
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x',
                          'y',
                          data=source,
                          show=False,
                          color='darkred',
                          label_fontsize='24pt',
                          marker='square',
                          marker_size=12,
                          alpha=0.8)

        check_bokeh_plot(p)

    def test_limits(self, check_bokeh_plot):
        """
        Test with setting limits
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False, limits={'x': (0, 10), 'y': (-50, 50)})

        check_bokeh_plot(p)

    def test_straight_lines(self, check_bokeh_plot):
        """
        Test with straight lines
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False, straight_lines={'vertical': 0, 'horizontal': [10, 20, 30]})

        check_bokeh_plot(p)

    def test_legend(self, check_bokeh_plot):
        """
        Test with straight lines
        """
        from masci_tools.vis.bokeh_plots import bokeh_scatter
        x = np.linspace(-10, 10, 100)
        y = x**2

        source = pd.DataFrame(data={'x': x, 'y': y})

        p = bokeh_scatter('x', 'y', data=source, show=False, legend_label='Test Data')

        check_bokeh_plot(p)
